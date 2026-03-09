(function () {
  // Create floating button
  const btn = document.createElement("div");
  btn.innerText = "Chat";
  btn.style.position = "fixed";
  btn.style.bottom = "20px";
  btn.style.right = "20px";
  btn.style.background = "#0d6efd";
  btn.style.color = "white";
  btn.style.padding = "12px 16px";
  btn.style.borderRadius = "50px";
  btn.style.cursor = "pointer";
  btn.style.fontFamily = "Arial, sans-serif";
  btn.style.zIndex = "9999";
  btn.style.boxShadow = "0 4px 10px rgba(0,0,0,0.2)";
  document.body.appendChild(btn);

  // Create chat box
  const box = document.createElement("div");
  box.style.position = "fixed";
  box.style.bottom = "80px";
  box.style.right = "20px";
  box.style.width = "320px";
  box.style.height = "420px";
  box.style.background = "#fff";
  box.style.border = "1px solid #ddd";
  box.style.borderRadius = "12px";
  box.style.display = "none";
  box.style.flexDirection = "column";
  box.style.fontFamily = "Arial, sans-serif";
  box.style.zIndex = "9999";
  box.style.boxShadow = "0 10px 25px rgba(0,0,0,0.25)";
  document.body.appendChild(box);

  box.innerHTML = `
    <div style="background:#0d6efd;color:white;padding:12px;border-radius:12px 12px 0 0;">
      <b>NINA — Hospital Assistant</b>
    </div>
    <div id="nina-messages" style="flex:1;padding:10px;overflow-y:auto;font-size:14px;">
      <div><b>NINA:</b> Assalam-o-Alaikum! Type <i>menu</i> to begin.</div>
    </div>
    <div style="padding:8px;border-top:1px solid #eee;">
      <input id="nina-input" placeholder="Type your message..."
        style="width:100%;padding:8px;border-radius:6px;border:1px solid #ccc;" />
    </div>
  `;

  btn.onclick = () => {
    box.style.display = box.style.display === "none" ? "flex" : "none";
  };

  const input = box.querySelector("#nina-input");
  const messages = box.querySelector("#nina-messages");

  input.addEventListener("keydown", async (e) => {
    if (e.key !== "Enter" || !input.value.trim()) return;

    const text = input.value;
    input.value = "";

    messages.innerHTML += `<div><b>You:</b> ${text}</div>`;
    messages.scrollTop = messages.scrollHeight;

    const API_BASE = window.NINA_API_BASE || window.location.origin;

const res = await fetch(`${API_BASE}/chat`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: text, session_id: "web" })
});

    const data = await res.json();
    messages.innerHTML += `<div><b>NINA:</b> ${data.reply}</div>`;
    messages.scrollTop = messages.scrollHeight;
  });
})();
