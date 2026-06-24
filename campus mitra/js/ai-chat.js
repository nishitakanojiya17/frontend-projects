/**
 * Campus Mitra — AI Chat Widget
 * Context-aware assistant for students and faculty.
 * Calls /api/ai/query/ with the user's JWT token to get real-data answers.
 */

(function () {
  // ── Inject styles ──────────────────────────────────────────────────────────
  const style = document.createElement('style');
  style.textContent = `
    #cm-chat-btn {
      position: fixed; bottom: 28px; right: 28px; z-index: 9999;
      width: 62px; height: 62px; border-radius: 50%;
      background: linear-gradient(135deg, #7c5cfc, #4f8ef7);
      border: none; cursor: pointer; box-shadow: 0 6px 24px rgba(124,92,252,0.45);
      display: flex; align-items: center; justify-content: center;
      font-size: 28px; transition: transform 0.2s, box-shadow 0.2s;
    }
    #cm-chat-btn:hover { transform: scale(1.08); box-shadow: 0 8px 32px rgba(124,92,252,0.55); }

    #cm-chat-panel {
      position: fixed; bottom: 104px; right: 28px; z-index: 9998;
      width: 520px; height: 680px;
      background: white; border-radius: 20px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.18);
      display: flex; flex-direction: column;
      border: 1px solid #e2e8f0;
      transform: translateY(20px) scale(0.95);
      opacity: 0; pointer-events: none;
      transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    #cm-chat-panel.open {
      transform: translateY(0) scale(1);
      opacity: 1; pointer-events: all;
    }

    #cm-chat-header {
      padding: 18px 20px; border-radius: 20px 20px 0 0;
      background: linear-gradient(135deg, #7c5cfc, #4f8ef7);
      display: flex; align-items: center; gap: 12px;
    }
    #cm-chat-header .avatar {
      width: 42px; height: 42px; border-radius: 50%;
      background: rgba(255,255,255,0.2);
      display: flex; align-items: center; justify-content: center;
      font-size: 20px; flex-shrink: 0;
    }
    #cm-chat-header .info .name { font-size: 15px; font-weight: 700; color: white; }
    #cm-chat-header .info .sub  { font-size: 12px; color: rgba(255,255,255,0.75); margin-top: 2px; }
    #cm-chat-close {
      margin-left: auto; background: none; border: none; cursor: pointer;
      color: rgba(255,255,255,0.8); font-size: 18px; line-height: 1;
    }

    #cm-chat-messages {
      flex: 1; overflow-y: auto; padding: 18px; display: flex;
      flex-direction: column; gap: 12px;
      background: #f8faff;
    }
    #cm-chat-messages::-webkit-scrollbar { width: 4px; }
    #cm-chat-messages::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 4px; }

    .cm-msg { max-width: 88%; display: flex; flex-direction: column; }
    .cm-msg.user { align-self: flex-end; align-items: flex-end; }
    .cm-msg.bot  { align-self: flex-start; align-items: flex-start; }

    .cm-bubble {
      padding: 12px 16px; border-radius: 16px; font-size: 14px;
      line-height: 1.6; word-break: break-word; white-space: pre-wrap;
    }
    .cm-msg.user .cm-bubble {
      background: linear-gradient(135deg, #7c5cfc, #4f8ef7);
      color: white; border-bottom-right-radius: 4px;
    }
    .cm-msg.bot .cm-bubble {
      background: white; color: #1e293b;
      border: 1px solid #e2e8f0; border-bottom-left-radius: 4px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .cm-bubble strong { font-weight: 700; }
    .cm-time { font-size: 10px; color: #94a3b8; margin-top: 3px; padding: 0 4px; }

    .cm-typing { display: flex; align-items: center; gap: 5px; padding: 8px 14px; }
    .cm-typing span { width: 7px; height: 7px; border-radius: 50%; background: #7c5cfc; animation: bounce 1.2s infinite; }
    .cm-typing span:nth-child(2) { animation-delay: 0.2s; }
    .cm-typing span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce { 0%,60%,100% { transform: translateY(0); } 30% { transform: translateY(-6px); } }

    .cm-suggestions {
      display: flex; flex-wrap: wrap; gap: 6px; padding: 8px 16px 4px;
    }
    .cm-sug {
      padding: 5px 12px; border-radius: 20px; font-size: 11px; font-weight: 600;
      border: 1px solid #e2e8f0; background: white; cursor: pointer; color: #7c5cfc;
      transition: all 0.15s;
    }
    .cm-sug:hover { background: #7c5cfc; color: white; border-color: #7c5cfc; }

    #cm-chat-input-row {
      display: flex; gap: 8px; padding: 12px 16px;
      border-top: 1px solid #e2e8f0; background: white;
      border-radius: 0 0 20px 20px;
    }
    #cm-chat-input {
      flex: 1; padding: 9px 14px; border: 1.5px solid #e2e8f0;
      border-radius: 12px; font-family: 'DM Sans', sans-serif;
      font-size: 13px; outline: none; transition: border-color 0.2s;
    }
    #cm-chat-input:focus { border-color: #7c5cfc; }
    #cm-chat-send {
      width: 38px; height: 38px; border-radius: 12px;
      background: linear-gradient(135deg, #7c5cfc, #4f8ef7);
      border: none; cursor: pointer; display: flex;
      align-items: center; justify-content: center; font-size: 16px;
      flex-shrink: 0; transition: opacity 0.2s;
    }
    #cm-chat-send:hover { opacity: 0.85; }
  `;
  document.head.appendChild(style);

  // ── HTML ───────────────────────────────────────────────────────────────────
  const html = `
    <button id="cm-chat-btn" title="Ask AI Assistant">🤖</button>
    <div id="cm-chat-panel">
      <div id="cm-chat-header">
        <div class="avatar">🤖</div>
        <div class="info">
          <div class="name">Campus Mitra AI</div>
          <div class="sub">Ask about attendance, notes, assignments & more</div>
        </div>
        <button id="cm-chat-close">✕</button>
      </div>
      <div id="cm-chat-messages"></div>
      <div class="cm-suggestions">
        <button class="cm-sug" onclick="cmAsk('What is my attendance?')">📊 My Attendance</button>
        <button class="cm-sug" onclick="cmAsk('Show study materials')">📚 Notes</button>
        <button class="cm-sug" onclick="cmAsk('Any pending assignments?')">📝 Assignments</button>
        <button class="cm-sug" onclick="cmAsk('Any new announcements?')">🔔 Notices</button>
        <button class="cm-sug" onclick="cmAsk('Explain the main concepts from my notes')">✨ Explain Notes</button>
      </div>
      <div id="cm-chat-input-row">
        <input id="cm-chat-input" type="text" placeholder="Ask me anything..." autocomplete="off"
          onkeydown="if(event.key==='Enter')cmSend()">
        <button id="cm-chat-send" onclick="cmSend()">➤</button>
      </div>
    </div>
  `;
  const wrapper = document.createElement('div');
  wrapper.innerHTML = html;
  document.body.appendChild(wrapper);

  // ── State ──────────────────────────────────────────────────────────────────
  let isOpen = false;
  const panel    = document.getElementById('cm-chat-panel');
  const messages = document.getElementById('cm-chat-messages');
  const input    = document.getElementById('cm-chat-input');

  // ── Toggle ─────────────────────────────────────────────────────────────────
  document.getElementById('cm-chat-btn').onclick = () => {
    isOpen = !isOpen;
    panel.classList.toggle('open', isOpen);
    if (isOpen && messages.children.length === 0) {
      showWelcome();
    }
    if (isOpen) setTimeout(() => input.focus(), 300);
  };
  document.getElementById('cm-chat-close').onclick = () => {
    isOpen = false;
    panel.classList.remove('open');
  };

  // ── Welcome message ────────────────────────────────────────────────────────
  function showWelcome() {
    const name = (localStorage.getItem('name') || 'there').split(' ')[0];
    addMessage('bot', `👋 Hi ${name}! I'm your Campus Mitra AI assistant.\n\nAsk me about your attendance, notes, assignments, announcements, or timetable!`);
  }

  // ── Add message bubble ─────────────────────────────────────────────────────
  function addMessage(type, text) {
    const div = document.createElement('div');
    div.className = `cm-msg ${type}`;
    const time = new Date().toLocaleTimeString('en-IN', {hour:'2-digit', minute:'2-digit'});
    // Convert **bold** markdown to <strong>
    const formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    div.innerHTML = `<div class="cm-bubble">${formatted}</div><span class="cm-time">${time}</span>`;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }

  // ── Typing indicator ───────────────────────────────────────────────────────
  function showTyping() {
    const div = document.createElement('div');
    div.className = 'cm-msg bot';
    div.id = 'cm-typing';
    div.innerHTML = `<div class="cm-bubble cm-typing"><span></span><span></span><span></span></div>`;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }
  function hideTyping() {
    const t = document.getElementById('cm-typing');
    if (t) t.remove();
  }

  // ── Send message ───────────────────────────────────────────────────────────
  async function cmSend() {
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    addMessage('user', text);
    showTyping();

    try {
      const token = localStorage.getItem('access_token');
      if (!token) { hideTyping(); addMessage('bot', '🔒 Please log in to use the AI assistant.'); return; }

      // Always use absolute backend URL
      const backendUrl = (window.BACKEND_URL && window.BACKEND_URL !== '') ? window.BACKEND_URL : 'http://127.0.0.1:8000';
      const res = await fetch(`${backendUrl}/api/ai/query/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ message: text })
      });
      hideTyping();
      if (res.ok) {
        const data = await res.json();
        const reply = data.reply || "I couldn't find an answer. Try asking differently!";
        const isRag = data.rag === true;
        const prefix = isRag ? '✨ *From your notes:*\n\n' : '';
        addMessage('bot', prefix + reply);
      } else if (res.status === 401) {
        addMessage('bot', '🔒 Session expired. Please log in again.');
      } else if (res.status === 403) {
        addMessage('bot', '⚠️ Access denied. Make sure you are logged in as a student or faculty.');
      } else {
        let errMsg = `⚠️ Error ${res.status}`;
        try { const e = await res.json(); errMsg += `: ${e.detail || e.error || JSON.stringify(e)}`; } catch(x) {}
        addMessage('bot', errMsg + '\n\nMake sure the backend server is running at http://127.0.0.1:8000');
      }
    } catch (e) {
      hideTyping();
      addMessage('bot', '⚠️ Cannot reach the server. Make sure the backend is running.');
    }
  }

  // ── Quick ask ──────────────────────────────────────────────────────────────
  window.cmAsk = function (text) {
    if (!isOpen) { isOpen = true; panel.classList.add('open'); }
    input.value = text;
    cmSend();
  };

  window.cmSend = cmSend;
})();
