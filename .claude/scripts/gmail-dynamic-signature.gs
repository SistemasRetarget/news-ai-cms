/**
 * Gmail Dynamic Signature — COMPASS
 * Agrega firma automáticamente según tipo de correo
 * - Respuesta a cliente: abajo centrado
 * - Interno (@retarget.cl): arriba centrado
 * - SIEMPRE
 */

const SIGNATURE_HTML = `
<div style="text-align: center; margin: 20px 0; font-family: Arial, sans-serif; color: #666;">
  <div style="font-size: 14px; font-weight: bold; color: #FF6B35; margin-bottom: 8px;">COMPASS</div>
  <div style="font-size: 12px;">SISTEMAS - RETARGET</div>
  <div style="font-size: 11px;">sistemas@retarget.cl</div>
  <div style="font-size: 11px;">retarget.cl</div>
</div>
`;

function isClientDomain(email) {
  // Agregar dominios de clientes aquí si es necesario
  const clientDomains = [
    'parquefutangue.com',
    'termasaguascalientes.cl',
    'puyehue.cl',
    'puebloladehesa.cl'
  ];
  return clientDomains.some(domain => email.includes(domain));
}

function isInternalDomain(email) {
  return email.includes('@retarget.cl');
}

function isReplyToClient(draft) {
  const subject = draft.subject || '';
  return subject.toLowerCase().startsWith('re:');
}

function addSignature(draft) {
  const to = draft.to || '';
  const cc = draft.cc || '';
  const bcc = draft.bcc || '';
  const body = draft.body || '';

  const isInternal = isInternalDomain(to) && isInternalDomain(cc) && isInternalDomain(bcc);
  const isClient = isClientDomain(to) || isReplyToClient(draft);

  let newBody = body;

  if (isInternal) {
    // Interno: firma ARRIBA centrado
    newBody = SIGNATURE_HTML + '<br>' + body;
  } else if (isClient) {
    // Cliente: firma ABAJO centrado
    newBody = body + '<br>' + SIGNATURE_HTML;
  }

  return newBody;
}

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('COMPASS')
    .addItem('Activar Firmas Dinámicas', 'enableDynamicSignatures')
    .addToUi();
}

function enableDynamicSignatures() {
  // Obtener todos los borradores
  const drafts = GmailApp.getDraftMessages();

  drafts.forEach(draft => {
    const to = draft.getTo();
    const cc = draft.getCc() || '';
    const bcc = draft.getBcc() || '';
    const subject = draft.getSubject();
    const body = draft.getPlainBody();

    const isInternal = to.includes('@retarget.cl');
    const isClient = !isInternal || subject.toLowerCase().startsWith('re:');

    let newBody = body;

    if (isInternal && !subject.toLowerCase().startsWith('re:')) {
      // Interno: firma ARRIBA
      newBody = 'COMPASS\nSISTEMAS - RETARGET\nsistemas@retarget.cl\nretarget.cl\n\n' + body;
    } else {
      // Cliente o respuesta: firma ABAJO
      newBody = body + '\n\nCOMPASS\nSISTEMAS - RETARGET\nsistemas@retarget.cl\nretarget.cl';
    }

    draft.getGmailDraft().refresh();
  });

  SpreadsheetApp.getUi().alert('✅ Firmas dinámicas aplicadas a ' + drafts.length + ' borradores');
}

function onMailOpen() {
  // Ejecutar automáticamente cuando abres Gmail
  // Requiere permisos especiales
  const drafts = GmailApp.getDraftMessages();

  if (drafts.length > 0) {
    drafts.forEach(draft => {
      const to = draft.getTo();
      const subject = draft.getSubject();
      const body = draft.getPlainBody();

      const isInternal = to.includes('@retarget.cl') && !subject.toLowerCase().startsWith('re:');

      let newBody = body;

      if (isInternal) {
        newBody = 'COMPASS\nSISTEMAS - RETARGET\nsistemas@retarget.cl\nretarget.cl\n\n' + body;
      } else {
        newBody = body + '\n\nCOMPASS\nSISTEMAS - RETARGET\nsistemas@retarget.cl\nretarget.cl';
      }

      // Actualizar borrador
      draft.getGmailDraft().setBody(newBody);
    });
  }
}
