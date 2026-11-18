// Cloudflare Pages Function: POST /api/contact
// Emails form submissions to the firm through Resend (https://resend.com).
// Set these in Cloudflare Pages → Settings → Variables and Secrets:
//   RESEND_API_KEY  (secret)  — API key from Resend
//   CONTACT_TO                — where submissions go, e.g. meredith@navigalaw.com
//   CONTACT_FROM              — verified sender, e.g. "Naviga Law website <web@navigalaw.com>"

const MAX = { name: 120, first: 80, last: 80, email: 200, phone: 40, topic: 80, message: 5000 };

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function reply(request, status, body) {
  const wantsJson = (request.headers.get('Accept') || '').includes('application/json');
  if (wantsJson) return Response.json(body, { status });
  // Plain HTML form post (no JS): go to the thank-you page, or back with an error flag.
  const loc = status === 200 ? '/thanks/' : '/form-error/';
  return Response.redirect(new URL(loc, request.url).toString(), 303);
}

export async function onRequestPost({ request, env }) {
  let data;
  try { data = await request.formData(); } catch { return reply(request, 400, { error: 'Could not read the form.' }); }

  // Honeypot: real people never fill this in.
  if ((data.get('company') || '').trim()) return reply(request, 200, { ok: true });

  const f = {};
  for (const k of Object.keys(MAX)) f[k] = String(data.get(k) || '').trim().slice(0, MAX[k]);
  const kind = data.get('form') === 'consultation' ? 'consultation' : 'contact';
  const name = f.name || [f.first, f.last].filter(Boolean).join(' ');

  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email)) {
    return reply(request, 422, { error: 'Please add your name and a valid email address.' });
  }
  if (kind === 'contact' && !f.message) return reply(request, 422, { error: 'Please tell us a little about how we can help.' });

  if (!env.RESEND_API_KEY || !env.CONTACT_TO || !env.CONTACT_FROM) {
    return reply(request, 500, { error: 'The form isn’t connected yet. Please email info@navigalaw.com or call (207) 805-2182.' });
  }

  const subject = kind === 'consultation'
    ? `Consultation request: ${name}${f.topic ? ' — ' + f.topic : ''}`
    : `Website message: ${name}`;
  const rows = [['Name', name], ['Email', f.email], ['Phone', f.phone], ['Topic', f.topic], ['Message', f.message]]
    .filter(([, v]) => v)
    .map(([k, v]) => `<tr><td style="padding:6px 12px 6px 0;color:#4F5F6A;vertical-align:top">${k}</td><td style="padding:6px 0;white-space:pre-wrap">${esc(v)}</td></tr>`)
    .join('');
  const html = `<div style="font-family:Georgia,serif;color:#22303A"><p style="font-size:18px">${kind === 'consultation' ? 'New consultation request' : 'New message'} from navigalaw.com</p><table style="border-collapse:collapse;font-size:15px">${rows}</table></div>`;

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: env.CONTACT_FROM, to: env.CONTACT_TO.split(',').map((s) => s.trim()), reply_to: f.email, subject, html }),
  });
  if (!r.ok) {
    console.log('Resend error', r.status, await r.text());
    return reply(request, 502, { error: 'We couldn’t send that just now. Please email info@navigalaw.com or call (207) 805-2182.' });
  }
  return reply(request, 200, { ok: true });
}

export function onRequest() {
  return new Response('Method not allowed', { status: 405, headers: { Allow: 'POST' } });
}
