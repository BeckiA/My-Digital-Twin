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


def build_top_html() -> str:
    """Renders the top branding header pinned at the top of the viewport."""
    return """
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500;1,9..144,600&family=Sora:wght@400;500;600&display=swap" rel="stylesheet" />

<header class="twin-top">
  <div class="twin-brand">
    <span class="twin-brand-name">Avatar</span>
    <span class="twin-brand-sub">Bereket Abera · Digital Twin</span>
  </div>
  <div class="twin-status" title="Active and ready to chat">
    <span class="twin-status-dot"></span>
    <span class="twin-status-text">Online</span>
  </div>
</header>
""".strip()


def build_hero_html(photo_uri: str = PHOTO_DATA_URI) -> str:
    """Renders the landing hero section with avatar, headline, lede, and suggestion pills."""
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
<div class="twin-hero-container">
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
</div>
""".strip()


TOP_HTML = build_top_html()
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
        <path fill="currentColor" d="M12 .3a12 12 0 0 0-3.79 23.4c.6.11.82-.26.82-.58v-2.02c-3.34.73-4.04-1.61-4.04-1.61-.55-1.38-1.33-1.75-1.33-1.75-1.09-.74.08-.73 1.2.09 1.84 1.24 1.84 1.24 1.07 1.84 2.8 1.31 3.49 1 .11-.78.42-1.31.76-1.61-2.66-.3-5.46-1.33-5.46-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.17 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.65.24 2.87.12 3.17.77.84 1.24 1.91 1.24 3.22 0 4.61-2.8 5.62-5.48 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.22.7.82.58A12 12 0 0 0 12 .3z"/>
      </svg>
      <span>GitHub</span>
    </a>
  </nav>
</footer>
""".strip()

CSS = """
:root, gradio-app, .gradio-container {
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
  --text-white: #FFFFFF;
  --muted: #8E8BBF;
  --send: #6454f0;
  --send-hover: #7b6cf5;
  --user-bubble: #6454f0;
  --halo: rgba(110, 226, 245, 0.38);
  --radius-pill: 999px;
  --radius-bar: 28px;
  --font-display: "Fraunces", "Iowan Old Style", "Palatino Linotype", Georgia, serif;
  --font-ui: "Sora", "Avenir Next", "Segoe UI", sans-serif;
  --max: 980px;

  /* Gradio internal token resets to eliminate any default gray background */
  --block-background-fill: transparent !important;
  --block-border-width: 0px !important;
  --block-border-color: transparent !important;
  --block-shadow: none !important;
  --background-fill-primary: transparent !important;
  --background-fill-secondary: transparent !important;
  --border-color-primary: transparent !important;
  --input-background-fill: transparent !important;
  --panel-background-fill: transparent !important;
}

/* =========================================================================
   ERADICATE ALL VERTICAL & HORIZONTAL SCROLLBARS EVERYWHERE
   ========================================================================= */
html, body, gradio-app, .gradio-container, .column, .chatbot, .twin-chat,
.bubble-wrap, .wrapper, [scrollable="true"], [class*="bubble"], [class*="scroll"],
.gradio-container *, * {
  scrollbar-width: none !important;
  -ms-overflow-style: none !important;
}

*::-webkit-scrollbar,
html::-webkit-scrollbar,
body::-webkit-scrollbar,
gradio-app::-webkit-scrollbar,
.gradio-container::-webkit-scrollbar,
.twin-chat::-webkit-scrollbar,
.chatbot::-webkit-scrollbar,
.bubble-wrap::-webkit-scrollbar,
.wrapper::-webkit-scrollbar,
[scrollable="true"]::-webkit-scrollbar {
  display: none !important;
  width: 0 !important;
  height: 0 !important;
  background: transparent !important;
}

.built-with, .show-api, .api-docs,
gradio-app > .footer,
.gradio-container > footer,
footer:not(.twin-foot),
.footer:not(.twin-foot) {
  display: none !important;
}

/* =========================================================================
   FULL PAGE VIEWPORT LOCK (App fills 100vh; smooth mousewheel/touch scroll)
   ========================================================================= */
html, body {
  height: 100% !important;
  height: 100vh !important;
  height: 100dvh !important;
  max-height: 100vh !important;
  max-height: 100dvh !important;
  overflow: hidden !important;
  margin: 0 !important;
  padding: 0 !important;
  box-sizing: border-box !important;
}

html, body, gradio-app {
  background: var(--void) !important;
  color: var(--text) !important;
}

body {
  background-color: var(--void) !important;
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(110, 226, 245, 0.12), transparent 55%),
    radial-gradient(ellipse 70% 40% at 50% 100%, rgba(100, 84, 240, 0.10), transparent 55%),
    linear-gradient(rgba(195, 192, 255, 0.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(195, 192, 255, 0.035) 1px, transparent 1px) !important;
  background-size: auto, auto, 48px 48px, 48px 48px !important;
  background-attachment: fixed !important;
  display: flex !important;
  flex-direction: column !important;
}

gradio-app {
  height: 100% !important;
  height: 100vh !important;
  height: 100dvh !important;
  max-height: 100vh !important;
  max-height: 100dvh !important;
  overflow: hidden !important;
  display: flex !important;
  flex-direction: column !important;
  flex: 1 1 auto !important;
}

/* App container: Full page height, centered spacious column */
.gradio-container {
  background: transparent !important;
  color: var(--text) !important;
  font-family: var(--font-ui) !important;
  width: 100% !important;
  max-width: var(--max) !important;
  min-width: 0 !important;
  margin: 0 auto !important;
  padding: 0 24px 12px !important;
  display: flex !important;
  flex-direction: column !important;
  flex: 1 1 0 !important;
  height: 100% !important;
  height: 100vh !important;
  height: 100dvh !important;
  max-height: 100vh !important;
  max-height: 100dvh !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
  position: relative !important;
}

.gradio-container > div,
.gradio-container .main,
.gradio-container .contain,
.gradio-container .wrap {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
  background: transparent !important;
  display: flex !important;
  flex-direction: column !important;
  flex: 1 1 0 !important;
  min-height: 0 !important;
  height: 100% !important;
  max-height: 100% !important;
  overflow: hidden !important;
  gap: 0 !important;
  row-gap: 0 !important;
  box-sizing: border-box !important;
}

.gradio-container .column,
.gradio-container .row,
.gradio-container .gap,
.gradio-container .form {
  gap: 0 !important;
  row-gap: 0 !important;
}

.gradio-container * { min-width: 0; }

/* ---------- Top brand strip (Always pinned at top) ---------- */
.twin-top {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding: 12px 0 8px !important;
  border-bottom: 1px solid rgba(100, 84, 240, 0.35) !important;
  margin-bottom: 0 !important;
  flex: 0 0 auto !important;
  width: 100% !important;
  box-sizing: border-box !important;
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
  color: var(--text-white);
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

.twin-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(110, 226, 245, 0.08);
  border: 1px solid rgba(110, 226, 245, 0.22);
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  font-family: var(--font-ui);
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--ice);
}
.twin-status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #34d399;
  box-shadow: 0 0 8px #34d399;
  animation: twin-pulse 2s infinite ease-in-out;
}
@keyframes twin-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

/* =========================================================================
   HERO SECTION (Centered on landing, hides when chat starts)
   ========================================================================= */
.twin-hero-container {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  flex: 1 1 0 !important;
  min-height: 0 !important;
  margin: auto 0 !important;
  width: 100% !important;
  box-sizing: border-box !important;
  overflow-y: auto !important;
  scrollbar-width: none !important;
}

.twin-hero {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
  padding: 8px 0 16px !important;
  margin: auto 0 !important;
  animation: twin-rise 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
  flex-shrink: 0 !important;
  width: 100% !important;
}
@keyframes twin-rise {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .twin-hero { animation: none !important; }
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
  font-size: clamp(1.6rem, 4.2vw, 2.2rem) !important;
  font-weight: 560 !important;
  font-optical-sizing: auto;
  line-height: 1.25 !important;
  letter-spacing: -0.01em !important;
  color: var(--text-white) !important;
  margin: 0 0 8px !important;
  max-width: 18em;
  border: 0 !important;
  padding: 0 !important;
}
.twin-headline em {
  font-style: italic;
  font-weight: 500;
  color: var(--ice);
}

.twin-tagline {
  font-family: var(--font-display);
  font-size: clamp(1rem, 2.3vw, 1.18rem);
  font-weight: 500;
  color: var(--text);
  margin: 0 0 8px;
  max-width: 28em;
  line-height: 1.35;
}
.twin-lede {
  font-family: var(--font-ui);
  font-size: 0.86rem;
  font-weight: 400;
  color: var(--muted);
  margin: 0 0 16px;
  max-width: 36em;
  line-height: 1.45;
}

.twin-pills {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  width: 100%;
  max-width: 680px;
  margin: 0 0 12px !important;
}
.twin-pill {
  font-family: var(--font-ui) !important;
  font-size: 0.82rem !important;
  font-weight: 500 !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  color: var(--text) !important;
  background: rgba(11, 6, 89, 0.85) !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
  border: 1px solid rgba(110, 226, 245, 0.24) !important;
  border-radius: var(--radius-pill) !important;
  padding: 10px 18px !important;
  min-height: 0 !important;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(4, 0, 70, 0.4) !important;
  transition: border-color 0.15s ease, background 0.15s ease, color 0.15s ease, transform 0.15s ease-out, box-shadow 0.15s ease !important;
}
@media (hover: hover) {
  .twin-pill:hover {
    border-color: var(--ice) !important;
    color: #FFFFFF !important;
    background: rgba(19, 13, 108, 0.95) !important;
    box-shadow: 0 4px 16px rgba(110, 226, 245, 0.25) !important;
    transform: translateY(-1.5px) !important;
  }
}
.twin-pill:not(:disabled):active {
  transform: scale(0.96) !important;
  transition: transform 150ms ease-out !important;
}
.twin-pill:focus-visible {
  outline: 2px solid var(--ice);
  outline-offset: 2px;
}

/* =========================================================================
   HERO AUTO-HIDE ONCE CHAT STARTS
   ========================================================================= */
body.twin-has-chat .twin-hero-container,
body.twin-has-chat .twin-hero,
body.twin-has-chat div:has(> .twin-hero-container),
body.twin-has-chat div:has(> .twin-hero),
.gradio-container.twin-has-chat .twin-hero-container,
.gradio-container.twin-has-chat .twin-hero,
.gradio-container.twin-has-chat div:has(> .twin-hero-container),
.gradio-container:has(.twin-chat .message-row) .twin-hero-container,
.gradio-container:has(.twin-chat .message-row) .twin-hero,
.gradio-container:has(.twin-chat .message-row) div:has(> .twin-hero-container),
.gradio-container:has(.twin-chat [data-testid="bot"]) .twin-hero-container,
.gradio-container:has(.twin-chat [data-testid="bot"]) .twin-hero,
.gradio-container:has(.twin-chat [data-testid="user"]) .twin-hero-container,
.gradio-container:has(.twin-chat [data-testid="user"]) .twin-hero,
.gradio-container:has(.chatbot .message-row) .twin-hero-container,
.gradio-container:has(.chatbot .message-row) .twin-hero {
  display: none !important;
  height: 0 !important;
  max-height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  border: 0 !important;
  opacity: 0 !important;
  pointer-events: none !important;
  overflow: hidden !important;
}

/* =========================================================================
   CHAT STREAM (NEVER HIDDEN, takes full central body, scrolls seamlessly)
   ========================================================================= */
.gradio-container .column:has(.twin-chat),
.gradio-container .column:has(.chatbot),
.gradio-container .column.fill-height {
  display: flex !important;
  flex-direction: column !important;
  flex: 1 1 0 !important;
  min-height: 0 !important;
  height: auto !important;
  max-height: 100% !important;
  width: 100% !important;
  gap: 0 !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
}

/* Chat container is ALWAYS available, visible, and full-page width */
.twin-chat,
.chatbot,
.gradio-container .twin-chat,
.gradio-container .chatbot {
  display: flex !important;
  flex-direction: column !important;
  flex: 1 1 0 !important;
  min-height: 0 !important;
  height: auto !important;
  max-height: none !important;
  opacity: 1 !important;
  pointer-events: auto !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 !important;
  padding: 8px 4px 6px !important;
  overflow-y: auto !important;
  overscroll-behavior: contain !important;
  scroll-behavior: smooth !important;
  scrollbar-width: none !important;
  -ms-overflow-style: none !important;
  box-sizing: border-box !important;
}

.chatbot > .block-label,
.chatbot > label,
.chatbot .label-wrap,
.chatbot .block-label,
.chatbot > .label-container,
.chatbot .placeholder,
.chatbot .placeholder * {
  display: none !important;
}

.chatbot > .wrapper,
.chatbot .bubble-wrap,
.chatbot .message-wrap,
.chatbot .scroll-hide,
[scrollable="true"] {
  min-height: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  width: 100% !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  overflow-y: auto !important;
  scrollbar-width: none !important;
  -ms-overflow-style: none !important;
}

/* Message rows */
.message-row,
.message-row > div,
.message-row .role,
.bubble-wrap {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

.message-row {
  margin-bottom: 16px !important;
  width: 100% !important;
}

.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  border: 0 !important;
  box-shadow: none !important;
  border-radius: 18px !important;
  padding: 14px 22px !important;
  font-family: var(--font-ui) !important;
  font-size: 0.96rem !important;
  line-height: 1.65 !important;
}

.message-row.user-row .message,
.message-row.user-row .message-bubble,
.message-row.user-row .bubble,
.message-row[data-role="user"] .message,
.message-row[data-role="user"] .message-bubble {
  background: var(--user-bubble) !important;
  color: #ffffff !important;
  box-shadow: 0 4px 18px rgba(100, 84, 240, 0.35) !important;
}

.message-row.bot-row .message,
.message-row.bot-row .message-bubble,
.message-row.bot-row .bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .message-bubble {
  background: var(--surface-2) !important;
  color: var(--text) !important;
  border: 1px solid var(--line) !important;
  box-shadow: 0 4px 16px rgba(4, 0, 70, 0.6) !important;
}

.message-row .message p,
.message-row .message-bubble p,
.message-row .bubble p,
.message-row .prose p {
  font-size: 0.96rem !important;
  line-height: 1.65 !important;
  margin: 0 0 10px !important;
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

/* =========================================================================
   COMPOSER / INPUT SECTION (Docked to bottom, comfortably sized, NEVER HIDDEN)
   ========================================================================= */
.gradio-container div:has(> #twin-message),
.gradio-container div:has(> .form:has(#twin-message)),
.gradio-container .group:has(#twin-message),
.gradio-container .wrap:has(#twin-message),
.twin-composer-host {
  flex: 0 0 auto !important;
  width: 100% !important;
  max-width: 740px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  position: relative !important;
  z-index: 30 !important;
  margin-top: 8px !important;
  margin-bottom: 2px !important;
  padding: 2px !important;
  box-sizing: border-box !important;
}

/* Eradicate ANY gray backgrounds, borders, or boxes around the input */
.gradio-container label,
.gradio-container label[class*="svelte"],
.gradio-container .block,
.gradio-container .block.padded,
.gradio-container .padded,
.gradio-container .unpadded_box,
.gradio-container .panel-full,
.gradio-container .fixed-panel,
.gradio-container .form,
.gradio-container .group,
.gradio-container .gr-group,
.gradio-container .gr-form,
.gradio-container fieldset,
.gradio-container [data-testid="group"],
.gradio-container [data-testid="textbox"],
.gradio-container [data-testid="textbox"] > div,
.gradio-container .input-container,
.gradio-container .scroll-hide,
.gradio-container .wrap:has(textarea),
.gradio-container div:has(> textarea),
.gradio-container div:has(textarea.twin-input),
#twin-message,
#twin-message.block,
#twin-message label {
  background: transparent !important;
  background-color: transparent !important;
  border: 0 !important;
  border-width: 0 !important;
  border-color: transparent !important;
  outline: none !important;
  box-shadow: none !important;
  -webkit-box-shadow: none !important;
  --block-background-fill: transparent !important;
  --block-border-width: 0px !important;
  --block-border-color: transparent !important;
  --block-shadow: none !important;
  --background-fill-primary: transparent !important;
  --background-fill-secondary: transparent !important;
  --border-color-primary: transparent !important;
  --input-background-fill: transparent !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* Inner input flex row */
.input-row,
.gr-input-row,
.chat-input-row,
form[class*="input"],
form:has(textarea),
div:has(> textarea):has(button) {
  display: flex !important;
  align-items: center !important;
  position: relative !important;
  width: 100% !important;
  gap: 0 !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  outline: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* Comfortable width with prominent, continuous border on all 4 sides */
.twin-input,
.twin-input textarea,
textarea.twin-input,
#twin-message textarea,
textarea,
.form textarea {
  width: 100% !important;
  background: rgba(12, 7, 92, 0.88) !important;
  backdrop-filter: blur(14px) !important;
  -webkit-backdrop-filter: blur(14px) !important;
  border: 1.5px solid rgba(110, 226, 245, 0.65) !important;
  border-top: 1.5px solid rgba(110, 226, 245, 0.65) !important;
  border-bottom: 1.5px solid rgba(110, 226, 245, 0.65) !important;
  border-left: 1.5px solid rgba(110, 226, 245, 0.65) !important;
  border-right: 1.5px solid rgba(110, 226, 245, 0.65) !important;
  color: #FFFFFF !important;
  font-family: var(--font-ui) !important;
  font-size: 1rem !important;
  font-weight: 400 !important;
  letter-spacing: -0.01em !important;
  padding: 16px 72px 16px 24px !important;
  line-height: 1.5 !important;
  min-height: 58px !important;
  height: 58px !important;
  border-radius: var(--radius-bar) !important;
  box-shadow:
    0 0 0 1px rgba(110, 226, 245, 0.22),
    0 10px 32px -6px rgba(4, 0, 70, 0.85),
    0 0 16px rgba(100, 84, 240, 0.15) !important;
  resize: none !important;
  box-sizing: border-box !important;
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
  transition: border-color 0.15s ease, box-shadow 0.15s ease, background 0.15s ease !important;
}

.twin-input:hover,
.twin-input textarea:hover,
#twin-message textarea:hover,
textarea:hover,
.form textarea:hover {
  border-color: rgba(110, 226, 245, 0.88) !important;
  background: rgba(19, 13, 108, 0.94) !important;
  box-shadow:
    0 0 0 1px rgba(110, 226, 245, 0.38),
    0 12px 36px -6px rgba(4, 0, 70, 0.9),
    0 0 20px rgba(110, 226, 245, 0.25) !important;
}

.twin-input:focus,
.twin-input textarea:focus,
#twin-message textarea:focus,
textarea:focus,
.form textarea:focus {
  border-color: var(--ice) !important;
  outline: none !important;
  background: rgba(19, 13, 108, 0.98) !important;
  box-shadow:
    0 0 0 2.5px rgba(110, 226, 245, 0.42),
    0 14px 40px -6px rgba(100, 84, 240, 0.45) !important;
}

textarea::placeholder,
input::placeholder {
  color: var(--muted) !important;
  opacity: 0.9 !important;
  font-size: 0.98rem !important;
}

/* Submit send button */
button.primary,
button[variant="primary"],
button.submit,
button.submit-button,
.submit-button,
button.lg.primary,
.twin-send {
  background: linear-gradient(135deg, #7b6cf5 0%, #6454f0 100%) !important;
  border: 1px solid rgba(110, 226, 245, 0.3) !important;
  color: #ffffff !important;
  min-height: 44px !important;
  min-width: 44px !important;
  width: 44px !important;
  height: 44px !important;
  padding: 0 !important;
  border-radius: 15px !important;
  align-self: center !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin-left: -56px !important;
  margin-right: 8px !important;
  position: relative;
  z-index: 5;
  flex-shrink: 0 !important;
  box-shadow: 0 4px 18px rgba(100, 84, 240, 0.5) !important;
  cursor: pointer !important;
  transition: transform 0.15s ease-out, background 0.15s ease, box-shadow 0.15s ease !important;
}

@media (hover: hover) {
  button.primary:hover,
  button.submit:hover,
  .submit-button:hover,
  button.lg.primary:hover,
  .twin-send:hover {
    background: linear-gradient(135deg, #8d7ff7 0%, #7060f5 100%) !important;
    border-color: var(--ice) !important;
    box-shadow: 0 6px 22px rgba(110, 226, 245, 0.4) !important;
    transform: scale(1.04);
  }
}

button.primary:not(:disabled):active,
button.submit:not(:disabled):active,
.submit-button:not(:disabled):active,
button.lg.primary:not(:disabled):active,
.twin-send:not(:disabled):active {
  transform: scale(0.96) !important;
  transition: transform 150ms ease-out !important;
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

/* Hint under input */
.twin-hints {
  display: flex !important;
  flex-wrap: wrap !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 8px 18px !important;
  text-align: center !important;
  font-family: var(--font-ui) !important;
  font-size: 0.74rem !important;
  color: var(--muted) !important;
  max-width: 740px !important;
  margin: 4px auto 2px !important;
  line-height: 1.3 !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  flex: 0 0 auto !important;
}
.twin-hints .twin-hint-item {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  background: transparent !important;
}
.twin-hints kbd {
  font-family: var(--font-ui) !important;
  font-size: 0.70rem !important;
  font-weight: 600 !important;
  color: var(--ice) !important;
  background: rgba(110, 226, 245, 0.09) !important;
  border: 1px solid rgba(110, 226, 245, 0.25) !important;
  border-radius: 5px !important;
  padding: 1px 6px !important;
  box-shadow: 0 1px 3px rgba(4, 0, 70, 0.4) !important;
}

/* Footer & social links (Always visible, pinned at bottom) */
.twin-foot {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  padding: 4px 0 2px !important;
  font-family: var(--font-ui) !important;
  flex: 0 0 auto !important;
  background: transparent !important;
}
.twin-social {
  display: flex !important;
  flex-wrap: wrap !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 16px 28px !important;
}
.twin-social-link {
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
  font-size: 0.82rem !important;
  font-weight: 500 !important;
  color: var(--muted) !important;
  text-decoration: none !important;
  padding: 3px 8px !important;
  border-radius: 8px !important;
  transition: color 0.15s ease, background 0.15s ease, transform 0.15s ease !important;
}
.twin-social-link svg {
  flex-shrink: 0;
  opacity: 0.9;
}
@media (hover: hover) {
  .twin-social-link:hover {
    color: var(--ice) !important;
    background: rgba(110, 226, 245, 0.08) !important;
    transform: translateY(-1px);
  }
}
.twin-social-link:active {
  transform: scale(0.96) !important;
}
.twin-social-link:focus-visible {
  outline: 2px solid var(--ice);
  outline-offset: 2px;
}

/* Gradio built-in examples (if shown) — hero pills replace these */
.examples, .examples-holder, [data-testid="examples"] {
  display: none !important;
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

::selection { background: var(--ice); color: var(--void); }

@media (max-width: 640px) {
  .gradio-container { padding: 0 12px 6px !important; }
  .twin-top { padding: 10px 0 6px !important; }
  .twin-avatar { width: 80px !important; height: 80px !important; }
  .twin-headline { font-size: 1.5rem !important; }
  .twin-pill { font-size: 0.76rem !important; padding: 8px 14px !important; }
  .twin-lede { font-size: 0.82rem; }
  .twin-input,
  .twin-input textarea,
  textarea.twin-input,
  #twin-message textarea {
    padding: 14px 60px 14px 18px !important;
    min-height: 52px !important;
    font-size: 0.95rem !important;
  }
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

  let chatActive = false;

  const killAllScrollbars = () => {
    let s = document.getElementById('twin-kill-scrollbars');
    if (!s) {
      s = document.createElement('style');
      s.id = 'twin-kill-scrollbars';
      s.textContent = `
        html, body, gradio-app, .gradio-container, .column, .chatbot, .twin-chat,
        .bubble-wrap, .wrapper, [scrollable="true"], * {
          scrollbar-width: none !important;
          -ms-overflow-style: none !important;
        }
        *::-webkit-scrollbar {
          display: none !important;
          width: 0 !important;
          height: 0 !important;
          background: transparent !important;
        }
      `;
      document.head.appendChild(s);
    }
  };

  const lockAppViewport = () => {
    document.documentElement.style.setProperty('overflow', 'hidden', 'important');
    document.documentElement.style.setProperty('height', '100%', 'important');
    document.body.style.setProperty('overflow', 'hidden', 'important');
    document.body.style.setProperty('height', '100%', 'important');
    const app = document.querySelector('gradio-app');
    if (app) {
      app.style.setProperty('overflow', 'hidden', 'important');
      app.style.setProperty('height', '100%', 'important');
    }
  };

  const activateChat = () => {
    chatActive = true;
    document.body.classList.add('twin-has-chat');
    const container = document.querySelector('.gradio-container');
    if (container) container.classList.add('twin-has-chat');
  };

  const checkChatState = () => {
    const chat = document.querySelector('.twin-chat, .chatbot');
    const hasMessages = Boolean(
      chat && chat.querySelector('.message-row, [data-testid="bot"], [data-testid="user"], [class*="message-bubble"], .bubble')
    );
    if (hasMessages) {
      activateChat();
    }
  };

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
    if (!btn.dataset.twinSubmitWired) {
      btn.dataset.twinSubmitWired = '1';
      btn.addEventListener('click', () => {
        const area = findMessageArea();
        if (area && area.value.trim().length > 0) {
          activateChat();
        }
      });
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

        activateChat();
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

    area.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        if (area.value.trim().length > 0) {
          activateChat();
        }
      }
    });

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
    for (let i = 0; i < 8 && node; i += 1) {
      if (node.classList && node.classList.contains('gradio-container')) break;
      node.style.setProperty('border', '0', 'important');
      node.style.setProperty('outline', 'none', 'important');
      node.style.setProperty('box-shadow', 'none', 'important');
      node.style.setProperty('background', 'transparent', 'important');
      node.style.setProperty('background-color', 'transparent', 'important');
      node = node.parentElement;
    }

    const host = area.closest('.block') || area.closest('label') || area.closest('.group');
    if (host) {
      host.style.setProperty('background', 'transparent', 'important');
      host.style.setProperty('background-color', 'transparent', 'important');
      host.style.setProperty('border', '0', 'important');
      host.style.setProperty('box-shadow', 'none', 'important');
      host.classList.add('twin-composer-host');
    }
  };

  const autoScrollChat = () => {
    const chat = document.querySelector('.twin-chat, .chatbot, .bubble-wrap, [scrollable="true"]');
    if (!chat) return;
    const isNearBottom = chat.scrollHeight - chat.scrollTop - chat.clientHeight < 160;
    if (isNearBottom) {
      chat.scrollTop = chat.scrollHeight;
    }
  };

  const scan = () => {
    killAllScrollbars();
    lockAppViewport();
    checkChatState();
    wirePills();
    document.querySelectorAll('textarea').forEach(watchTextarea);
    styleSendButton();
    ensureHints();
    hideGradioFooter();
    clearComposerChrome();
    autoScrollChat();
  };

  setTimeout(focusInput, 300);
  setTimeout(scan, 100);
  setTimeout(scan, 500);
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""
