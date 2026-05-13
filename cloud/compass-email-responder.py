"""
Cloud Function: Compass Auto-Responder
Escucha correos de Mauricio/Leig, responde con template + stats Sheets.
Registra ticket pendiente en Sheets para que Luis complete después.

Trigger: Cloud Scheduler cada 5 minutos
Deploy: gcloud functions deploy compass-email-responder \
  --runtime python311 --trigger-topic compass-scheduler \
  --entry-point main
"""

import functions_framework
import json
import os
from datetime import datetime
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuración
SHEETS_ID = "1murmG-pdc5GkJ1CYc4_1UISRTcipMxPYv2jiH_-7ZIY"
SHEET_NAME = "Retarget-Mayo-2026"
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]

# Contactos que disparan auto-respuesta
ALLOWED_FROM = ['mauricio@', 'leig@']  # Búsqueda parcial


def get_secret_manager_client():
    """Obtiene cliente de Secret Manager."""
    from google.cloud import secretmanager
    return secretmanager.SecretManagerServiceClient()


def read_secret(secret_name, project_id):
    """Lee secret desde Google Cloud Secret Manager."""
    try:
        client = get_secret_manager_client()
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error reading secret {secret_name}: {e}")
        return None


def get_credentials():
    """Obtiene credenciales de Google Cloud (Sheets + Gmail API)."""
    cred_path = '/workspace/retarget-mcp-2d37bb49c600.json'

    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Credenciales no encontradas en {cred_path}")

    credentials = Credentials.from_service_account_file(
        cred_path,
        scopes=SCOPES
    )
    return credentials


def get_gmail_credentials_oauth():
    """Obtiene credenciales OAuth para Gmail desde Secret Manager."""
    from google.oauth2.credentials import Credentials

    project_id = os.getenv('GCP_PROJECT_ID', 'retarget-mcp')
    secret_name = os.getenv('GMAIL_REFRESH_TOKEN_SECRET', 'gmail-refresh-token')

    refresh_token = read_secret(secret_name, project_id)

    if not refresh_token:
        raise ValueError("No refresh token found in Secret Manager")

    # Crear credenciales con refresh token
    credentials = Credentials(
        token=None,  # Será obtenido al hacer request
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id='YOUR_CLIENT_ID.apps.googleusercontent.com',  # Será reemplazado
        client_secret='YOUR_CLIENT_SECRET'  # Será reemplazado
    )

    return credentials


def get_gmail_service(credentials):
    """Construye cliente Gmail API."""
    return build('gmail', 'v1', credentials=credentials)


def get_sheets_service(credentials):
    """Construye cliente Sheets API."""
    return build('sheets', 'v4', credentials=credentials)


def search_unreplied_emails(gmail_service, from_filter):
    """Busca threads sin responder de un contacto específico."""
    try:
        query = f'from:{from_filter} is:unread -label:compass-processed'
        results = gmail_service.users().messages().list(
            userId='me',
            q=query,
            maxResults=5
        ).execute()
        return results.get('messages', [])
    except HttpError as error:
        print(f'Gmail API error: {error}')
        return []


def get_message_details(gmail_service, message_id):
    """Obtiene contenido completo de un mensaje."""
    try:
        message = gmail_service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
        return message
    except HttpError as error:
        print(f'Error fetching message: {error}')
        return None


def classify_request(subject, body):
    """Clasifica tipo de request: 'correction', 'status', 'clarification'."""
    subject_lower = subject.lower()
    body_lower = body.lower()

    # Patrones de corrección/problema
    if any(w in subject_lower for w in ['error', 'problema', 'broken', 'falla', 'no funciona', 'incorrect']):
        return 'correction'

    # Patrones de reporte/status
    if any(w in subject_lower for w in ['estado', 'status', 'avance', 'progress', 'how is', 'qué hay']):
        return 'status'

    # Default: aclaración
    return 'clarification'


def get_sheet_stats(sheets_service):
    """Lee Sheets vivo y retorna stats de tickets."""
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=SHEETS_ID,
            range=f'{SHEET_NAME}!A:N'
        ).execute()

        rows = result.get('values', [])[1:]  # Skip header

        completed = sum(1 for row in rows if len(row) > 7 and 'Completado' in row[7])
        pending = sum(1 for row in rows if len(row) > 7 and 'Pendiente' in row[7])
        in_progress = sum(1 for row in rows if len(row) > 7 and 'En progreso' in row[7])

        return {
            'completed_today': completed,
            'pending': pending,
            'in_progress': in_progress,
            'total': len(rows)
        }
    except Exception as e:
        print(f'Sheet stats error: {e}')
        return None


def build_response(request_type, stats):
    """Construye respuesta según template + stats."""

    # Firma fija para todos los emails
    signature = """⚡ Zorrito — RETARGET
sistemas@retarget.cl · retarget.cl"""

    if request_type == 'correction':
        # Template 2: Corrección Recibida
        response = f"""Hola,

Anotado. Revisamos el punto reportado.

Corrección tomada. Lo resolvemos y confirmamos cuando esté live.

{signature}"""

    elif request_type == 'status':
        # Template 4: Reporte Avance
        response = f"""Hola,

Aquí el estado de las iniciativas:

📊 Resumen:
✅ {stats['completed_today']} completadas hoy
⏳ {stats['in_progress']} en progreso
⏲️ {stats['pending']} pendientes
📈 Total: {stats['total']} tickets

Estamos ejecutando en orden de prioridad. Reportamos cambios cuando hay movimiento.

{signature}"""

    else:
        # Template 5: Pedido de Aclaración (default)
        response = f"""Hola,

Revisamos tu mensaje. Antes de ejecutar necesitamos confirmar un punto:

¿Puedes dar más detalle sobre lo que necesitas?

En cuanto confirmes, lo tomamos de inmediato.

{signature}"""

    return response


def register_in_sheets(sheets_service, from_addr, subject, request_type):
    """Registra nuevo ticket en Sheets como 'Pendiente Luis - Detalles'."""
    try:
        # Obtener número de fila siguiente
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=SHEETS_ID,
            range=f'{SHEET_NAME}!A:A'
        ).execute()
        rows = result.get('values', [])
        next_row = len(rows) + 1

        # Generar ticket ID
        last_ticket = rows[-1][0] if rows else 'T-00'
        ticket_num = int(last_ticket.split('-')[1]) + 1 if len(rows) > 1 else 1
        ticket_id = f'T-{ticket_num:02d}'

        # Datos nuevos
        new_row = [
            ticket_id,                          # A: Ticket
            'Correo Externo',                  # B: Negocio
            'Múltiple',                        # C: Sitio
            from_addr,                         # D: Origen
            subject,                           # E: Problema
            '[Pendiente Luis - Detalles]',     # F: Solución
            'Pendiente Luis',                  # G: Estado
            datetime.now().strftime('%Y-%m-%d'), # H: Fecha creación
            '',                                # I: Fecha estimada
            'COMPASS',                         # J: Responsable
            '',                                # K: % Completo
            '',                                # L: Aprendizaje
            request_type,                      # M: Tipo request
            f'Registrado por auto-responder'   # N: Notas
        ]

        # Append a Sheets
        body = {
            'values': [new_row]
        }
        sheets_service.spreadsheets().values().append(
            spreadsheetId=SHEETS_ID,
            range=f'{SHEET_NAME}!A{next_row}',
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()

        return ticket_id
    except Exception as e:
        print(f'Sheet registration error: {e}')
        return None


def send_reply(gmail_service, message_id, subject, body):
    """Envía reply al thread del mensaje."""
    try:
        # Obtener thread ID
        message = gmail_service.users().messages().get(
            userId='me',
            id=message_id
        ).execute()

        thread_id = message.get('threadId')

        # Preparar reply
        reply_headers = f"To: {message['payload']['headers'][0].get('value', '')}\n"
        reply_headers += f"Subject: {subject}\n"
        reply_headers += "Content-Type: text/plain; charset=\"UTF-8\"\n"

        message_body = f"{reply_headers}\n{body}"

        # Enviar
        raw_message = message_body.encode('utf-8')
        import base64
        raw = base64.urlsafe_b64encode(raw_message).decode()

        message = {'raw': raw}

        sent = gmail_service.users().messages().send(
            userId='me',
            body=message,
            threadId=thread_id
        ).execute()

        print(f'Reply sent: {sent["id"]}')
        return True
    except Exception as e:
        print(f'Send reply error: {e}')
        return False


def mark_as_processed(gmail_service, message_id):
    """Marca mensaje como procesado (label compass-processed)."""
    try:
        gmail_service.users().messages().modify(
            userId='me',
            id=message_id,
            body={
                'addLabelIds': ['compass-processed'],
                'removeLabelIds': ['UNREAD']
            }
        ).execute()
    except Exception as e:
        print(f'Error marking processed: {e}')


@functions_framework.http
def main(request):
    """HTTP trigger para Cloud Function."""
    try:
        credentials = get_credentials()
        gmail = get_gmail_service(credentials)
        sheets = get_sheets_service(credentials)

        # Get Sheets stats
        stats = get_sheet_stats(sheets)
        if not stats:
            return {'status': 'error', 'message': 'Could not fetch sheet stats'}

        processed_count = 0

        # Procesar correos de cada contacto permitido
        for contact in ALLOWED_FROM:
            messages = search_unreplied_emails(gmail, contact)

            for msg in messages:
                msg_details = get_message_details(gmail, msg['id'])
                if not msg_details:
                    continue

                # Extraer info
                headers = {h['name']: h['value'] for h in msg_details['payload']['headers']}
                from_addr = headers.get('From', 'unknown')
                subject = headers.get('Subject', '(sin asunto)')

                # Clasificar y responder
                request_type = classify_request(subject, '')
                response_body = build_response(request_type, stats)

                # Registrar en Sheets
                ticket_id = register_in_sheets(sheets, from_addr, subject, request_type)
                if ticket_id:
                    print(f'Registered: {ticket_id}')

                # Enviar reply
                if send_reply(gmail, msg['id'], f'Re: {subject}', response_body):
                    mark_as_processed(gmail, msg['id'])
                    processed_count += 1

        return {
            'status': 'success',
            'messages_processed': processed_count,
            'stats': stats
        }

    except Exception as e:
        print(f'Cloud Function error: {e}')
        return {'status': 'error', 'message': str(e)}, 500
