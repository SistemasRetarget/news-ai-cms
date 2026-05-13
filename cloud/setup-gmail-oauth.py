#!/usr/bin/env python3
"""
Setup OAuth2 para Gmail API — Una sola vez por Luis

Uso:
  python3 setup-gmail-oauth.py

Pasos:
1. Script abre navegador para que autorices
2. Copias el código que aparece
3. Script obtiene refresh token
4. Script guarda en Google Cloud Secret Manager

El refresh token se usa en compass-email-responder.py
"""

import os
import json
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from google.cloud import secretmanager

# Scopes necesarios
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]

PROJECT_ID = "retarget-mcp"
SECRET_NAME = "gmail-refresh-token"


def create_oauth_credentials():
    """Crea OAuth client_secrets.json interactivo."""

    print("""
╔═══════════════════════════════════════════════════════════╗
║      SETUP: Autorizar Gmail API para Compass             ║
╚═══════════════════════════════════════════════════════════╝

Necesitamos crear una aplicación OAuth en Google Cloud Console.

Pasos:
1. Abre: https://console.cloud.google.com/apis/credentials
2. Crea "OAuth 2.0 Client ID" → Aplicación de escritorio
3. Descarga el JSON
4. Cópialo aquí

Esperando cliente_secret.json...
    """)

    client_secret_path = "client_secret.json"

    if not os.path.exists(client_secret_path):
        client_secret_path = input("Ruta a client_secret.json: ").strip()

    if not os.path.exists(client_secret_path):
        print(f"❌ Archivo no encontrado: {client_secret_path}")
        return None

    return client_secret_path


def get_refresh_token(client_secret_path):
    """Obtiene refresh token via flujo OAuth."""

    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secret_path,
            scopes=SCOPES,
            redirect_uri='http://localhost:8080/'
        )

        # Abre navegador
        credentials = flow.run_local_server(port=8080)

        print(f"""
✅ Autorización exitosa
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Token:       {credentials.token[:20]}...
Refresh:     {credentials.refresh_token[:20]}...
Expira:      {credentials.expiry}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)

        return credentials.refresh_token

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def save_to_secret_manager(project_id, secret_name, refresh_token):
    """Guarda refresh token en Google Cloud Secret Manager."""

    try:
        client = secretmanager.SecretManagerServiceClient()
        parent = f"projects/{project_id}"

        # Crear secret (si no existe)
        try:
            client.create_secret(
                request={
                    "parent": parent,
                    "secret_id": secret_name,
                    "secret": {"replication": {"automatic": {}}},
                }
            )
            print(f"✅ Secret creado: {secret_name}")
        except Exception as e:
            if "already exists" in str(e):
                print(f"ℹ️  Secret ya existe: {secret_name}")
            else:
                raise

        # Agregar version
        response = client.add_secret_version(
            request={
                "parent": f"{parent}/secrets/{secret_name}",
                "payload": {"data": refresh_token.encode("UTF-8")},
            }
        )

        print(f"✅ Token guardado en Secret Manager")
        print(f"   Ruta: {response.name}")
        return True

    except Exception as e:
        print(f"❌ Error guardando en Secret Manager: {e}")
        print(f"   Alternativa: Guarda manualmente en .env")
        return False


def save_to_env():
    """Guarda refresh token en .env local (alternativa)."""

    print("""
Alternativa: Guardando en .env local
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

    refresh_token = input("Pega el refresh token: ").strip()

    with open(".env.local", "w") as f:
        f.write(f"GMAIL_REFRESH_TOKEN={refresh_token}\n")

    print("✅ Guardado en .env.local")
    print("   (No commits este archivo a git)")


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║      COMPASS: Configuración de Gmail API                 ║
║      Esta es una operación única, requiere autorización ║
╚═══════════════════════════════════════════════════════════╝
    """)

    # Obtener credenciales
    client_secret_path = create_oauth_credentials()
    if not client_secret_path:
        return

    # Obtener refresh token
    refresh_token = get_refresh_token(client_secret_path)
    if not refresh_token:
        print("❌ No se pudo obtener refresh token")
        return

    # Guardar en Secret Manager
    print("\n📍 Opción 1: Google Cloud Secret Manager (recomendado)")
    save_choice = input("¿Guardar en Secret Manager? (s/n): ").strip().lower()

    if save_choice == 's':
        save_to_secret_manager(PROJECT_ID, SECRET_NAME, refresh_token)
    else:
        print("\n📍 Opción 2: .env local (desarrollo)")
        save_to_env()

    print("""
✅ Setup completado
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Próximos pasos:

1. Deploy de Cloud Function:
   gcloud functions deploy compass-email-responder \\
     --runtime python311 \\
     --trigger-http \\
     --entry-point main

2. Cloud Scheduler (cada 5 min):
   gcloud scheduler jobs create http compass-responder \\
     --schedule="*/5 * * * *" \\
     --http-method=GET \\
     --uri=[CLOUD_FUNCTION_URL]

3. Monitoreo:
   gcloud functions logs read compass-email-responder --limit 50

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)


if __name__ == "__main__":
    main()
