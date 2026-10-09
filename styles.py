"""Visual system and chrome for Bereket Abera's digital twin Gradio UI.

Inspiration: edwarddonner.com/avatar — centered hero chat, deep indigo stage,
circular portrait, serif invitation, pill starters, rounded message bar.
Palette: primary #040046, accent #6ee2f5, secondary #6454f0, ink #C3C0FF.
"""

from __future__ import annotations

import base64
import html
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_PHOTO_PATH = _ROOT / "me" / "Bereket_Abera_25.jpg"

def _photo_data_uri() -> str:
    if not _PHOTO_PATH.exists():
        return ""
    encoded = base64.b64encode(_PHOTO_PATH.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


PHOTO_DATA_URI = _photo_data_uri()

EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on now?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

# Compact labels for hero pills (full prompts stay in data-prompt / EXAMPLES)
PILL_PROMPTS = [
    ("Background & experience", EXAMPLES[0]),
    ("Current projects", EXAMPLES[1]),
    ("Technical skills", EXAMPLES[2]),
    ("Get in touch", EXAMPLES[3]),
]


def build_hero_html(photo_uri: str = PHOTO_DATA_URI) -> str:
    pills = "\n".join(
        (
            f'<button type="button" class="twin-pill" '
            f'data-prompt="{html.escape(prompt, quote=True)}">'
            f"{html.escape(label)}</button>"
        )
        for label, prompt in PILL_PROMPTS
    )
    avatar = (
        f'<img class="twin-avatar" src="{photo_uri}" alt="Bereket Abera" width="120" height="120" />'
        if photo_uri
        else '<div class="twin-avatar twin-avatar--fallback" aria-hidden="true"></div>'
    )
    return f"""
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500;1,9..144,600&family=Sora:wght@400;500;600&display=swap" rel="stylesheet" />

<header class="twin-top">
  <div class="twin-brand">
    <span class="twin-brand-name">Avatar</span>
    <span class="twin-brand-sub">Bereket Abera · Digital Twin</span>
  </div>
</header>

<section class="twin-hero" aria-label="Introduction">
  <div class="twin-avatar-wrap">
    {avatar}
  </div>
  <h1 class="twin-headline">
    I'm Bereket Abera's <em>digital twin.</em>
  </h1>
  <p class="twin-tagline">Ask me anything about my career — work, skills, and projects.</p>
  <p class="twin-lede">
    I know Bereket's background as a Flutter developer and AI-focused engineer.
    Ask about experience, what he's building, or how to get in touch.
  </p>
  <div class="twin-pills" role="group" aria-label="Suggested questions">
    {pills}
  </div>
</section>
""".strip()


HERO_HTML = build_hero_html()

LINKEDIN_URL = "https://www.linkedin.com/in/bereket-abera"
GITHUB_URL = "https://github.com/BeckiA"

FOOTER_HTML = f"""
<footer class="twin-foot">
  <nav class="twin-social" aria-label="Social links">
    <a class="twin-social-link" href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">
      <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false">
        <path fill="currentColor" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.23 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.46c.98 0 1.77-.77 1.77-1.73V1.73C24 .77 23.21 0 22.23 0z"/>
      </svg>
      <span>LinkedIn</span>
    </a>
    <a class="twin-social-link" href="{GITHUB_URL}" target="_blank" rel="noopener noreferrer">
      <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false">
        <path fill="currentColor" d="M12 .3a12 12 0 0 0-3.79 23.4c.6.11.82-.26.82-.58v-2.02c-3.34.73-4.04-1.61-4.04-1.61-.55-1.38-1.33-1.75-1.33-1.75-1.09-.74.08-.73.08-.73 1.2.09 1.84 1.24 1.84 1.24 1.07 1.84 2.8 1.31 3.49 1 .11-.78.42-1.31.76-1.61-2.66-.3-5.46-1.33-5.46-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.17 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.65.24 2.87.12 3.17.77.84 1.24 1.91 1.24 3.22 0 4.61-2.8 5.62-5.48 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.22.7.82.58A12 12 0 0 0 12 .3z"/>
      </svg>
      <span>GitHub</span>
    </a>
  </nav>
</footer>
""".strip()

CSS = """
:root {
  /* Brand tokens */
  --b-primary: #040046;
  --b-accent: #6ee2f5;
  --b-secondary: #6454f0;
  --b-white: #C3C0FF;

  --void: #040046;
  --surface: #0B0659;
  --surface-2: #130D6C;
  --line: #2a2478;
  --line-soft: rgba(110, 226, 245, 0.28);
  --ice: #6ee2f5;
  --ice-dim: #8E8BBF;
  --text: #C3C0FF;
  --muted: #8E8BBF;
  --send: #6454f0;
  --send-hover: #7b6cf5;
  --user-bubble: #6454f0;
  --halo: rgba(110, 226, 245, 0.38);
  --radius-pill: 999px;
  --radius-bar: 22px;
  --font-display: "Fraunces", "Iowan Old Style", "Palatino Linotype", Georgia, serif;
  --font-ui: "Sora", "Avenir Next", "Segoe UI", sans-serif;
  --max: 720px;
}

.built-with, .show-api, .api-docs,
gradio-app > .footer,
.gradio-container > footer,
footer:not(.twin-foot),
.footer:not(.twin-foot) {
  display: none !important;
}

html, body, gradio-app {
  background: var(--void) !important;
  color: var(--text) !important;
}

body {
  background-color: var(--void) !important;
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(110, 226, 245, 0.10), transparent 55%),
    linear-gradient(rgba(195, 192, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(195, 192, 255, 0.04) 1px, transparent 1px) !important;
  background-size: auto, 48px 48px, 48px 48px !important;
  background-attachment: fixed !important;
  min-height: 100vh;
}

.gradio-container {
  background: transparent !important;
  color: var(--text) !important;
  font-family: var(--font-ui) !important;
  width: 100% !important;
  max-width: var(--max) !important;
  min-width: 0 !important;
  margin: 0 auto !important;
  padding: 0 20px 16px !important;
}
.gradio-container .main,
.gradio-container .contain,
.gradio-container .wrap {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
  background: transparent !important;
  gap: 0 !important;
  row-gap: 0 !important;
}
.gradio-container .column,
.gradio-container .row,
.gradio-container .gap,
.gradio-container .form {
  gap: 0.4rem !important;
  row-gap: 0.4rem !important;
}
.gradio-container * { min-width: 0; }

/* ---------- Top brand strip ---------- */
.twin-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0 6px;
  border-bottom: 1px solid rgba(100, 84, 240, 0.35);
  margin-bottom: 12px;
}
.twin-brand {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.twin-brand-name {
  font-family: var(--font-ui);
  font-weight: 600;
  font-size: 1.15rem;
  letter-spacing: -0.02em;
  color: var(--text);
  line-height: 1.2;
}
.twin-brand-sub {
  font-family: var(--font-ui);
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--ice-dim);
}

/* ---------- Hero ---------- */
.twin-hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 4px 0 0;
  animation: twin-rise 0.7s ease-out both;
}
@keyframes twin-rise {
  from { opacity: 0; transform: translateY(14px); }
  to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .twin-hero { animation: none; }
}

.twin-avatar-wrap {
  position: relative;
  margin-bottom: 12px;
}
.twin-avatar-wrap::before {
  content: "";
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  background: radial-gradient(circle, var(--halo), transparent 70%);
  z-index: 0;
  pointer-events: none;
}
.twin-avatar {
  position: relative;
  z-index: 1;
  width: 96px;
  height: 96px;
  border-radius: 50%;
  object-fit: cover;
  object-position: center top;
  border: 2px solid rgba(110, 226, 245, 0.45);
  box-shadow: 0 0 0 5px rgba(4, 0, 70, 0.85);
  display: block;
}
.twin-avatar--fallback {
  background: var(--surface-2);
}

.twin-headline {
  font-family: var(--font-display) !important;
  font-size: clamp(1.55rem, 4vw, 2.1rem) !important;
  font-weight: 560 !important;
  font-optical-sizing: auto;
  line-height: 1.25 !important;
  letter-spacing: -0.01em !important;
  color: var(--text) !important;
  margin: 0 0 8px !important;
  max-width: 18em;
  border: 0 !important;
  padding: 0 !important;
  position: static !important;
  width: auto !important;
  height: auto !important;
  clip: auto !important;
  overflow: visible !important;
  white-space: normal !important;
}
.twin-headline em {
  font-style: italic;
  font-weight: 500;
  color: var(--ice);
}

.twin-tagline {
  font-family: var(--font-display);
  font-size: clamp(0.98rem, 2.2vw, 1.15rem);
  font-weight: 500;
  color: var(--text);
  margin: 0 0 8px;
  max-width: 28em;
  line-height: 1.35;
}
.twin-lede {
  font-family: var(--font-ui);
  font-size: 0.85rem;
  font-weight: 400;
  color: var(--muted);
  margin: 0 0 12px;
  max-width: 36em;
  line-height: 1.45;
}

.twin-pills {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  width: 100%;
  max-width: 640px;
  margin: 0 0 4px;
}
.twin-pill {
  font-family: var(--font-ui) !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  color: var(--text) !important;
  background: rgba(11, 6, 89, 0.85) !important;
  border: 1px solid var(--line-soft) !important;
  border-radius: var(--radius-pill) !important;
  padding: 10px 16px !important;
  min-height: 0 !important;
  cursor: pointer;
  transition: border-color 0.15s ease, background 0.15s ease, color 0.15s ease;
}
.twin-pill:hover {
  border-color: var(--ice) !important;
  color: var(--ice) !important;
  background: rgba(19, 13, 108, 0.95) !important;
}
.twin-pill:focus-visible {
  outline: 2px solid var(--ice);
  outline-offset: 2px;
}

.twin-foot {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 14px 0 8px;
  font-family: var(--font-ui);
}
.twin-social {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 18px 28px;
}
.twin-social-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--muted);
  text-decoration: none;
  transition: color 0.15s ease;
}
.twin-social-link svg {
  flex-shrink: 0;
  opacity: 0.9;
}
.twin-social-link:hover {
  color: var(--ice);
}
.twin-social-link:focus-visible {
  outline: 2px solid var(--ice);
  outline-offset: 3px;
  border-radius: 4px;
}

/* ---------- Blocks / surfaces ---------- */
.block, .form,
.block.padded,
.padded,
.unpadded_box,
.panel-full,
.fixed-panel {
  background: transparent !important;
  box-shadow: none !important;
  border: 0 !important;
  outline: none !important;
}

/* Hide chatbot chrome label */
.chatbot > .block-label,
.chatbot > label,
.chatbot .label-wrap,
.chatbot .block-label,
.chatbot > .label-container {
  display: none !important;
}

/* Empty chat: collapse so hero sits near the composer */
.twin-chat,
.chatbot,
.chatbot.block {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  min-height: 0 !important;
  max-height: 0 !important;
  height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
  opacity: 0;
  pointer-events: none;
}
.twin-chat:has(.message-row),
.twin-chat:has([data-testid="bot"]),
.twin-chat:has([data-testid="user"]),
.chatbot:has(.message-row),
.chatbot:has([class*="message"]),
.chatbot:has([data-testid="bot"]),
.chatbot:has([data-testid="user"]) {
  min-height: 160px !important;
  max-height: min(42vh, 360px) !important;
  height: auto !important;
  opacity: 1;
  pointer-events: auto;
  margin: 4px 0 8px !important;
  padding: 0 !important;
  overflow: auto !important;
}

.chatbot .placeholder,
.chatbot .placeholder * {
  color: var(--muted) !important;
  display: none !important;
}

/* Message rows */
.message-row,
.message-row > div,
.message-row .role,
.message-wrap, .bubble-wrap {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  border: 0 !important;
  box-shadow: none !important;
  border-radius: 16px !important;
  padding: 10px 14px !important;
  font-family: var(--font-ui) !important;
  font-size: 0.9rem !important;
  line-height: 1.55 !important;
}

.message-row.user-row .message,
.message-row.user-row .message-bubble,
.message-row.user-row .bubble,
.message-row[data-role="user"] .message,
.message-row[data-role="user"] .message-bubble {
  background: var(--user-bubble) !important;
  color: #ffffff !important;
}

.message-row.bot-row .message,
.message-row.bot-row .message-bubble,
.message-row.bot-row .bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .message-bubble {
  background: var(--surface-2) !important;
  color: var(--text) !important;
  border: 1px solid var(--line) !important;
}

.message-row .message p,
.message-row .message-bubble p,
.message-row .bubble p,
.message-row .prose p {
  font-size: 0.9rem !important;
  line-height: 1.55 !important;
  margin: 0 0 8px !important;
  color: inherit !important;
}
.message-row .message p:last-child,
.message-row .message-bubble p:last-child,
.message-row .bubble p:last-child {
  margin-bottom: 0 !important;
}

.message-row .message a,
.message-row .message-bubble a {
  color: var(--ice) !important;
  text-decoration: underline;
}

/* ---------- Composer / input bar ---------- */
/* Strip Gradio's outer gray frame around textbox + send */
#twin-message,
#twin-message.block,
.block:has(#twin-message),
.block:has(textarea),
.form:has(textarea),
.wrap:has(> textarea),
.wrap:has(textarea),
div:has(> textarea):has(button),
[data-testid="textbox"],
[data-testid="textbox"] > div,
.input-container,
.scroll-hide {
  background: transparent !important;
  border: 0 !important;
  outline: none !important;
  box-shadow: none !important;
  --block-border-width: 0 !important;
  --block-border-color: transparent !important;
}

.input-row,
.gr-input-row,
.chat-input-row,
form[class*="input"],
form:has(textarea) {
  align-items: center !important;
  gap: 0 !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  outline: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

.twin-input,
.twin-input textarea,
textarea.twin-input,
#twin-message textarea,
textarea,
.form textarea {
  background: var(--surface) !important;
  border: 1px solid rgba(110, 226, 245, 0.35) !important;
  color: var(--text) !important;
  font-family: var(--font-ui) !important;
  font-size: 0.92rem !important;
  padding: 14px 60px 14px 18px !important;
  line-height: 1.4 !important;
  min-height: 52px !important;
  border-radius: var(--radius-bar) !important;
  box-shadow: none !important;
  resize: none !important;
  box-sizing: border-box !important;
}
.twin-input:focus,
.twin-input textarea:focus,
#twin-message textarea:focus,
textarea:focus,
.form textarea:focus {
  border-color: var(--ice) !important;
  outline: none !important;
  box-shadow: 0 0 0 1px rgba(110, 226, 245, 0.35) !important;
}
textarea::placeholder, input::placeholder {
  color: var(--muted) !important;
  opacity: 1 !important;
}

/* Hint under input */
.twin-hints {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px 14px;
  text-align: center;
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--muted);
  margin: 8px 0 0;
  line-height: 1.35;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}
.twin-hints .twin-hint-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: transparent !important;
}
.twin-hints kbd {
  font-family: var(--font-ui);
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--ice);
  background: rgba(110, 226, 245, 0.08);
  border: 1px solid rgba(110, 226, 245, 0.22);
  border-radius: 6px;
  padding: 2px 7px;
}

/* ---------- Buttons ---------- */
button {
  font-family: var(--font-ui) !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  font-size: 0.85rem !important;
  font-weight: 500 !important;
  border-radius: 12px !important;
  cursor: pointer;
}

button.primary,
button[variant="primary"],
button.submit,
button.submit-button,
.submit-button,
button.lg.primary,
.twin-send {
  background: var(--send) !important;
  border: 1px solid var(--send) !important;
  color: #ffffff !important;
  min-height: 46px !important;
  min-width: 46px !important;
  width: 46px !important;
  height: 46px !important;
  padding: 0 !important;
  border-radius: 14px !important;
  align-self: center !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin-left: -58px !important;
  position: relative;
  z-index: 3;
  flex-shrink: 0 !important;
  box-shadow: 0 4px 16px rgba(100, 84, 240, 0.45);
}
button.primary:hover,
button.submit:hover,
.submit-button:hover,
button.lg.primary:hover,
.twin-send:hover {
  background: var(--send-hover) !important;
  border-color: var(--send-hover) !important;
  color: #ffffff !important;
}

button.submit svg,
button.submit-button svg,
.submit-button svg,
button.primary svg,
button[variant="primary"] svg,
.twin-send svg {
  width: 20px !important;
  height: 20px !important;
  margin: 0 !important;
  display: block !important;
  color: #ffffff !important;
  fill: currentColor !important;
  stroke: currentColor !important;
}

/* Gradio built-in examples (if shown) — match pills */
.examples, .examples-holder, [data-testid="examples"] {
  background: transparent !important;
  padding: 0 !important;
  margin-top: 12px !important;
  display: none !important; /* hero pills replace these */
}

.icon-button, .chatbot .icon-button {
  color: var(--muted) !important;
  background: transparent !important;
  border: 0 !important;
  min-height: 0 !important;
  padding: 4px !important;
}
.icon-button:hover, .chatbot .icon-button:hover {
  color: var(--ice) !important;
}

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--void); }
::-webkit-scrollbar-thumb { background: var(--line); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--ice-dim); }

::selection { background: var(--ice); color: var(--void); }

@media (max-width: 640px) {
  .gradio-container { padding: 0 14px 12px !important; }
  .twin-avatar { width: 84px; height: 84px; }
  .twin-pill { font-size: 0.75rem !important; padding: 8px 12px !important; }
  .twin-lede { font-size: 0.8rem; }
}

/* Keep the empty landing view inside one viewport */
@media (max-height: 820px) {
  .twin-top { margin-bottom: 8px; padding-top: 6px; }
  .twin-avatar { width: 80px; height: 80px; }
  .twin-avatar-wrap { margin-bottom: 8px; }
  .twin-lede { display: none; }
  .twin-foot { padding: 10px 0 4px; }
}
"""

JS = """
() => {
  document.title = 'Bereket Abera · Digital Twin';

  const SEND_ICON = `
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">
      <path fill="currentColor" d="M3.4 20.6 21 12 3.4 3.4l-.1 6.8L15 12 3.3 13.8z"/>
    </svg>
  `;

  const setTextareaValue = (area, text) => {
    const proto = window.HTMLTextAreaElement.prototype;
    const descriptor = Object.getOwnPropertyDescriptor(proto, 'value');
    if (descriptor && descriptor.set) {
      descriptor.set.call(area, text);
    } else {
      area.value = text;
    }
    area.dispatchEvent(new Event('input', { bubbles: true }));
    area.dispatchEvent(new Event('change', { bubbles: true }));
  };

  const findMessageArea = () => {
    const areas = Array.from(document.querySelectorAll('textarea'));
    if (!areas.length) return null;
    return areas[areas.length - 1];
  };

  const isStopButton = (btn) => {
    const label = `${btn.getAttribute('aria-label') || ''} ${btn.textContent || ''}`.toLowerCase();
    return label.includes('stop') || label.includes('cancel') || btn.classList.contains('stop');
  };

  const findSubmit = () => {
    const area = findMessageArea();
    const scope = area
      ? (area.closest('form') || area.closest('.wrap') || area.parentElement?.parentElement || document)
      : document;
    const selectors = [
      'button.submit',
      'button.submit-button',
      '.submit-button',
      'button[aria-label*="Send" i]',
      'button[aria-label*="Submit" i]',
      'button.primary',
    ];
    const candidates = Array.from(scope.querySelectorAll(selectors.join(', ')));
    return candidates.find((btn) =>
      !btn.closest('.twin-pills') &&
      !btn.classList.contains('twin-pill') &&
      !isStopButton(btn)
    ) || null;
  };

  const styleSendButton = () => {
    const btn = findSubmit();
    if (!btn) return;
    btn.classList.add('twin-send');
    btn.setAttribute('aria-label', 'Send message');
    btn.setAttribute('title', 'Send');
    if (btn.dataset.twinIcon !== '1') {
      btn.innerHTML = SEND_ICON;
      btn.dataset.twinIcon = '1';
    }
  };

  const wirePills = () => {
    document.querySelectorAll('.twin-pill').forEach((btn) => {
      if (btn.dataset.twinWired) return;
      btn.dataset.twinWired = '1';
      btn.addEventListener('click', () => {
        const prompt = btn.getAttribute('data-prompt') || '';
        const area = findMessageArea();
        if (!area || !prompt) return;
        setTextareaValue(area, prompt);
        area.focus();
        const submit = findSubmit();
        if (submit && !submit.disabled) {
          setTimeout(() => submit.click(), 40);
        }
      });
    });
  };

  const focusInput = () => {
    const area = findMessageArea();
    if (area) area.focus();
  };

  const watchTextarea = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };

  const ensureHints = () => {
    if (document.querySelector('.twin-hints')) return;
    const area = findMessageArea();
    if (!area) return;
    const host = area.closest('.form') || area.closest('[class*="input"]') || area.parentElement;
    if (!host) return;
    const anchor = host.parentElement || host;
    const hints = document.createElement('div');
    hints.className = 'twin-hints';
    hints.innerHTML = `
      <span class="twin-hint-item"><kbd>Enter</kbd> to send</span>
      <span class="twin-hint-item"><kbd>Shift + Enter</kbd> for a new line</span>
    `;
    anchor.appendChild(hints);
  };

  const hideGradioFooter = () => {
    document.querySelectorAll('footer, .footer, .built-with').forEach((el) => {
      if (el.classList.contains('twin-foot') || el.closest('.twin-foot')) return;
      el.style.setProperty('display', 'none', 'important');
    });
  };

  const clearComposerChrome = () => {
    const area = findMessageArea();
    if (!area) return;
    let node = area.parentElement;
    for (let i = 0; i < 6 && node; i += 1) {
      if (node.classList && node.classList.contains('gradio-container')) break;
      node.style.setProperty('border', '0', 'important');
      node.style.setProperty('outline', 'none', 'important');
      node.style.setProperty('box-shadow', 'none', 'important');
      node.style.setProperty('background', 'transparent', 'important');
      node = node.parentElement;
    }
  };

  const scan = () => {
    wirePills();
    document.querySelectorAll('textarea').forEach(watchTextarea);
    styleSendButton();
    ensureHints();
    hideGradioFooter();
    clearComposerChrome();
  };

  setTimeout(focusInput, 300);
  setTimeout(scan, 200);
  setTimeout(scan, 800);
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""
