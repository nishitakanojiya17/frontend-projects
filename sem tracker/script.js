/* =============================================
   RGPV 6th Sem Tracker — script.js
   ============================================= */

/* ========== SYLLABUS DATA ==========
   Edit this object to customize subjects, units, and topics.
   Structure: subjects[] → units[] → topics[]
   ======================================== */
const SYLLABUS = [
  {
    id: "toc",
    code: "AL-601",
    name: "Theory of Computation",
    shortName: "TOC",
    priority: "high",
    color: "#6c63ff",
    units: [
      {
        id: "toc_u1",
        name: "Unit 1 – Introduction to Automata",
        topics: [
          "Examples of Automata Machines",
          "Finite Automata as Language Acceptor",
          "Finite Automata as Language Translator",
          "Moore Machines",
          "Mealy Machines",
          "Composite Machine",
          "Conversion: Mealy to Moore",
          "Conversion: Moore to Mealy"
        ]
      },
      {
        id: "toc_u2",
        name: "Unit 2 – Types of Finite Automata",
        topics: [
          "Non-Deterministic Finite Automata (NDFA)",
          "Deterministic Finite Automata (DFA)",
          "Conversion of NDFA to DFA",
          "Minimization of Automata",
          "Regular Expression",
          "Arden's Theorem",
          "Union, Intersection, Concatenation, Closure",
          "2-Way DFA"
        ]
      },
      {
        id: "toc_u3",
        name: "Unit 3 – Grammars",
        topics: [
          "Types of Grammar",
          "Context Sensitive Grammar",
          "Context Free Grammar",
          "Regular Grammar",
          "Derivation Trees",
          "Ambiguity in Grammar",
          "Simplification of CFG",
          "Grammar to Automata Conversion",
          "Chomsky Hierarchy",
          "Killing Null and Unit Productions",
          "Chomsky Normal Form (CNF)",
          "Greibach Normal Form (GNF)"
        ]
      },
      {
        id: "toc_u4",
        name: "Unit 4 – Pushdown Automata",
        topics: [
          "Introduction to PDA",
          "Deterministic PDA",
          "Non-Deterministic PDA",
          "PDA to CFG Conversion",
          "CFG to PDA Conversion",
          "CFG Equivalent to PDA",
          "Petri Net Model"
        ]
      },
      {
        id: "toc_u5",
        name: "Unit 5 – Turing Machine",
        topics: [
          "Techniques for TM Construction",
          "Universal Turing Machine",
          "Multitape Turing Machine",
          "Multihead Turing Machine",
          "Multidimensional Turing Machine",
          "NP-Complete Problems",
          "Decidability",
          "Decidable Languages",
          "Undecidable Languages",
          "Halting Problem",
          "Post Correspondence Problem"
        ]
      }
    ]
  },
  {
    id: "cn",
    code: "AL-602",
    name: "Computer Networks",
    shortName: "CN",
    priority: "high",
    color: "#4dabf7",
    units: [
      {
        id: "cn_u1",
        name: "Unit 1 – Network Fundamentals & Physical Layer",
        topics: [
          "Computer Network Definitions, Goals, Components",
          "Network Architecture and Classifications",
          "Protocol Hierarchy and Design Issues",
          "ISO-OSI Reference Model",
          "OSI vs TCP/IP Comparison",
          "Connection Oriented vs Connectionless Services",
          "Physical Layer: Media, Bandwidth, Data Rate",
          "Modulation Techniques"
        ]
      },
      {
        id: "cn_u2",
        name: "Unit 2 – Data Link Layer",
        topics: [
          "Data Link Layer Services",
          "Framing",
          "Flow Control",
          "Error Control",
          "Elementary Data Link Protocols",
          "Sliding Window Protocols",
          "Go-Back-N Protocol",
          "Selective Repeat Protocol",
          "Hybrid ARQ",
          "Finite State Machine Models",
          "Petri Net Models",
          "ARP / RARP / GARP"
        ]
      },
      {
        id: "cn_u3",
        name: "Unit 3 – MAC Sub Layer",
        topics: [
          "MAC Addressing",
          "Binary Exponential Back-off (BEB)",
          "ALOHA",
          "Slotted ALOHA",
          "CSMA",
          "CSMA/CD",
          "CSMA/CA",
          "Basic Bit Map Protocol",
          "Limited Contention Protocols",
          "IEEE 802 Standards"
        ]
      },
      {
        id: "cn_u4",
        name: "Unit 4 – Network Layer",
        topics: [
          "Network Layer Services and Design Issues",
          "Least Cost Routing Algorithm",
          "Dijkstra's Algorithm",
          "Bellman-Ford Algorithm",
          "Hierarchical Routing",
          "Broadcast and Multicast Routing",
          "IP Addressing",
          "IP Header Format",
          "Packet Forwarding",
          "Fragmentation and Reassembly",
          "ICMP",
          "IPv4 vs IPv6 Comparison"
        ]
      },
      {
        id: "cn_u5",
        name: "Unit 5 – Transport & Application Layer",
        topics: [
          "Transport Layer Design Issues",
          "UDP Header Format",
          "Per-Segment Checksum",
          "TCP Connection Management",
          "TCP Reliability",
          "TCP Flow Control",
          "TCP Congestion Control",
          "TCP Timer Management",
          "WWW and HTTP",
          "FTP and SSH",
          "Email: SMTP, MIME, IMAP",
          "DNS",
          "SNMP"
        ]
      }
    ]
  },
  {
    id: "ivp",
    code: "AL-603",
    name: "Image and Video Processing",
    shortName: "IVP",
    priority: "medium",
    color: "#00c9a7",
    units: [
      {
        id: "ivp_u1",
        name: "Module 1 – Image Representation & Analysis",
        topics: [
          "Introduction to Computer Vision",
          "Numerical Representation of Images",
          "Image Augmentation",
          "Image Enhancement",
          "Image Processing Basics",
          "Color Transforms",
          "Geometric Transforms",
          "Feature Recognition",
          "Feature Extraction"
        ]
      },
      {
        id: "ivp_u2",
        name: "Module 2 – Image Segmentation",
        topics: [
          "Object Detection",
          "Breaking Image into Parts",
          "Finding Contours",
          "Edge Detection",
          "Background Subtraction for Video"
        ]
      },
      {
        id: "ivp_u3",
        name: "Module 3 – Object Motion & Tracking",
        topics: [
          "Tracking a Single Point Over Time",
          "Motion Models",
          "Analyzing Video as Image Sequences",
          "Feature Tracking Methods",
          "Feature Matching Across Frames",
          "Optical Flow"
        ]
      },
      {
        id: "ivp_u4",
        name: "Module 4 – Robotic Localization",
        topics: [
          "Bayesian Statistics for Localization",
          "Sensor Measurements for Navigation",
          "Gaussian Uncertainty",
          "Histogram Filter in Python"
        ]
      },
      {
        id: "ivp_u5",
        name: "Module 5 – Image Restoration",
        topics: [
          "Degradation Model",
          "Noise Models",
          "Estimation of Degradation Function",
          "Wiener Filter Restoration",
          "Inverse Filter Restoration"
        ]
      }
    ]
  },
  {
    id: "cc",
    code: "AL-604",
    name: "Cloud Computing",
    shortName: "CC",
    priority: "medium",
    color: "#ff8c42",
    units: [
      {
        id: "cc_u1",
        name: "Unit 1 – Introduction to Cloud",
        topics: [
          "Grid vs Cloud Computing",
          "Cloud Characteristics and Components",
          "Business and IT Perspective",
          "Cloud Models (Public, Private, Hybrid)",
          "Amazon EC2",
          "Google App Engine",
          "Microsoft Azure",
          "Utility and Elastic Computing"
        ]
      },
      {
        id: "cc_u2",
        name: "Unit 2 – Cloud Services",
        topics: [
          "SaaS (Software as a Service)",
          "PaaS (Platform as a Service)",
          "IaaS (Infrastructure as a Service)",
          "Cloud Design using SOA",
          "Conceptual Cloud Model and Stack",
          "Computing on Demand",
          "Information Life Cycle Management",
          "Cloud Analytics",
          "Virtual Desktop Infrastructure",
          "Storage Cloud"
        ]
      },
      {
        id: "cc_u3",
        name: "Unit 3 – Virtualization",
        topics: [
          "Virtualization Definition and Benefits",
          "Hardware Virtualization (HVM)",
          "Hypervisor Study",
          "Logical Partitioning (LPAR)",
          "Storage Virtualization",
          "SAN and NAS",
          "Cloud Server Virtualization",
          "Virtualized Data Center"
        ]
      },
      {
        id: "cc_u4",
        name: "Unit 4 – Cloud Security",
        topics: [
          "Cloud Security Fundamentals",
          "Vulnerability Assessment",
          "Privacy and Security in Cloud",
          "Cloud Security Architecture",
          "Trusted Cloud Computing",
          "Identity Management",
          "Access Control",
          "Autonomic Security",
          "Virtualization Security Management",
          "VM Security Techniques"
        ]
      },
      {
        id: "cc_u5",
        name: "Unit 5 – SOA & Cloud Platforms",
        topics: [
          "SOA and Cloud",
          "SOA and IaaS",
          "Cloud Infrastructure Benchmarks",
          "Business Intelligence and OLAP",
          "QoS Issues in Cloud",
          "Mobile Cloud Computing",
          "Inter-Cloud and Sky Computing",
          "Xen Cloud Platform",
          "Eucalyptus",
          "OpenNebula",
          "Nimbus"
        ]
      }
    ]
  }
];

/* ========== QUOTES ========== */
const QUOTES = [
  { text: "The expert in anything was once a beginner.", author: "Helen Hayes" },
  { text: "Consistency is the key to achieving and maintaining momentum.", author: "Darren Hardy" },
  { text: "Study hard what interests you the most in the most undisciplined, irreverent and original manner possible.", author: "Richard Feynman" },
  { text: "Don't watch the clock; do what it does. Keep going.", author: "Sam Levenson" },
  { text: "The future belongs to those who learn more skills and combine them in creative ways.", author: "Robert Greene" },
  { text: "Success is the sum of small efforts repeated day in and day out.", author: "Robert Collier" },
  { text: "Push yourself because no one else is going to do it for you.", author: "Unknown" },
  { text: "Great things are done by a series of small things brought together.", author: "Vincent Van Gogh" }
];

/* ========== STATE ========== */
let progress = {};   // { topicId: true/false }
let notes = {};      // { subjectId: "text" }
let tasks = [];      // [{ text, done }]
let weekPlan = {};   // { "Mon_0": "text", ... }
let revisions = {};  // { topicId: true }
let pomodoroSessions = 0;
let pomodoroInterval = null;
let pomodoroSeconds = 25 * 60;
let pomodoroRunning = false;
let accentColor = "#6c63ff";

/* ========== LOCAL STORAGE ========== */
const LS = {
  load() {
    progress = JSON.parse(localStorage.getItem("rgpv_progress") || "{}");
    notes = JSON.parse(localStorage.getItem("rgpv_notes") || "{}");
    tasks = JSON.parse(localStorage.getItem("rgpv_tasks") || "[]");
    weekPlan = JSON.parse(localStorage.getItem("rgpv_weekplan") || "{}");
    revisions = JSON.parse(localStorage.getItem("rgpv_revisions") || "{}");
    pomodoroSessions = parseInt(localStorage.getItem("rgpv_pomo") || "0");
    accentColor = localStorage.getItem("rgpv_accent") || "#6c63ff";
    const theme = localStorage.getItem("rgpv_theme") || "dark";
    document.documentElement.setAttribute("data-theme", theme);
  },
  save() {
    localStorage.setItem("rgpv_progress", JSON.stringify(progress));
    localStorage.setItem("rgpv_notes", JSON.stringify(notes));
    localStorage.setItem("rgpv_tasks", JSON.stringify(tasks));
    localStorage.setItem("rgpv_weekplan", JSON.stringify(weekPlan));
    localStorage.setItem("rgpv_revisions", JSON.stringify(revisions));
    localStorage.setItem("rgpv_pomo", pomodoroSessions.toString());
    localStorage.setItem("rgpv_accent", accentColor);
  }
};

/* ========== HELPERS ========== */
function getSubjectProgress(subj) {
  let total = 0, done = 0;
  subj.units.forEach(u => {
    u.topics.forEach(t => {
      total++;
      const key = `${subj.id}_${u.id}_${t}`;
      if (progress[key]) done++;
    });
  });
  return { total, done, pct: total ? Math.round((done / total) * 100) : 0 };
}

function getOverallStats() {
  let total = 0, done = 0;
  SYLLABUS.forEach(s => {
    const p = getSubjectProgress(s);
    total += p.total;
    done += p.done;
  });
  return { total, done, pct: total ? Math.round((done / total) * 100) : 0 };
}

function hex2rgba(hex, a) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return `rgba(${r},${g},${b},${a})`;
}

function setAccent(color) {
  accentColor = color;
  document.documentElement.style.setProperty("--accent", color);
  document.documentElement.style.setProperty("--accent-glow", hex2rgba(color, 0.3));
  LS.save();
}

/* ========== PAGE ROUTING ========== */
function showPage(pageId) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
  document.getElementById(`page-${pageId}`).classList.add("active");
  document.querySelector(`.nav-item[data-page="${pageId}"]`).classList.add("active");
  if (pageId === "dashboard") renderDashboard();
  if (pageId === "subjects") renderSubjects();
  if (pageId === "analytics") renderAnalytics();
  if (pageId === "planner") renderPlanner();
  closeSidebar();
}

/* ========== SIDEBAR MOBILE ========== */
function openSidebar() {
  document.getElementById("sidebar").classList.add("open");
  document.getElementById("sidebarOverlay").classList.add("open");
}
function closeSidebar() {
  document.getElementById("sidebar").classList.remove("open");
  document.getElementById("sidebarOverlay").classList.remove("open");
}

/* ========== DASHBOARD ========== */
function renderDashboard() {
  // Greeting
  const hour = new Date().getHours();
  const greet = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  document.getElementById("greetingText").textContent = `${greet}, Engineer! 👋`;

  // Stats
  const stats = getOverallStats();
  document.getElementById("statOverall").textContent = `${stats.pct}%`;
  document.getElementById("statOverallBar").style.width = `${stats.pct}%`;
  document.getElementById("statCompleted").textContent = stats.done;
  document.getElementById("statPending").textContent = stats.total - stats.done;

  // Streak
  const streak = parseInt(localStorage.getItem("rgpv_streak") || "0");
  document.getElementById("statStreak").textContent = streak;

  // Quote
  const q = QUOTES[Math.floor(Math.random() * QUOTES.length)];
  document.getElementById("quoteText").textContent = q.text;
  document.getElementById("quoteAuthor").textContent = `— ${q.author}`;

  // Goal
  const goal = localStorage.getItem("rgpv_goal") || "";
  document.getElementById("goalDisplay").textContent = goal || "No goal set yet. Add one above!";

  // Exam countdown
  const examDate = localStorage.getItem("rgpv_examdate");
  if (examDate) {
    document.getElementById("examDate").value = examDate;
    const days = Math.ceil((new Date(examDate) - new Date()) / (1000 * 60 * 60 * 24));
    document.getElementById("countdownVal").textContent = days > 0 ? `${days} days` : "Today!";
  }

  // Subject overview
  const grid = document.getElementById("subjectOverviewGrid");
  grid.innerHTML = "";
  SYLLABUS.forEach(subj => {
    const p = getSubjectProgress(subj);
    const card = document.createElement("div");
    card.className = "overview-card";
    card.innerHTML = `
      <div class="overview-card-top">
        <div>
          <div class="overview-subject-name">${subj.name}</div>
          <span class="overview-code">${subj.code}</span>
        </div>
        <span class="priority-badge priority-${subj.priority === 'high' ? 'high' : subj.priority === 'medium' ? 'med' : 'low'}">
          ${subj.priority}
        </span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:0.8rem;color:var(--text-muted)">${p.done}/${p.total} topics</span>
        <span class="overview-pct" style="color:${subj.color}">${p.pct}%</span>
      </div>
      <div class="progress-bar-wrap">
        <div class="progress-bar-fill" style="width:${p.pct}%;background:${subj.color}"></div>
      </div>
    `;
    card.onclick = () => { showPage("subjects"); setTimeout(() => openSubjectModal(subj.id), 100); };
    grid.appendChild(card);
  });
}

/* ========== SUBJECTS PAGE ========== */
function renderSubjects(filter = "all", search = "") {
  const grid = document.getElementById("subjectsGrid");
  grid.innerHTML = "";

  SYLLABUS.forEach(subj => {
    const p = getSubjectProgress(subj);
    if (filter === "completed" && p.pct < 100) return;
    if (filter === "pending" && p.pct === 100) return;
    if (search && !subj.name.toLowerCase().includes(search.toLowerCase()) &&
        !subj.code.toLowerCase().includes(search.toLowerCase())) return;

    const card = document.createElement("div");
    card.className = "subject-card";
    card.innerHTML = `
      <div class="subject-card-header">
        <div>
          <div class="subject-card-name">${subj.name}</div>
          <span class="overview-code">${subj.code}</span>
        </div>
        <span class="priority-badge priority-${subj.priority === 'high' ? 'high' : subj.priority === 'medium' ? 'med' : 'low'}">
          ${subj.priority}
        </span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span class="subject-units-preview">${subj.units.length} units · ${p.total} topics</span>
        <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.2rem;color:${subj.color}">${p.pct}%</span>
      </div>
      <div class="progress-bar-wrap" style="height:8px">
        <div class="progress-bar-fill" style="width:${p.pct}%;background:linear-gradient(90deg,${subj.color},${subj.color}cc)"></div>
      </div>
      <button class="btn-open" style="background:linear-gradient(135deg,${subj.color},${subj.color}bb)" onclick="openSubjectModal('${subj.id}')">
        Open Subject →
      </button>
    `;
    grid.appendChild(card);
  });
}

/* ========== SUBJECT MODAL ========== */
function openSubjectModal(subjId) {
  const subj = SYLLABUS.find(s => s.id === subjId);
  if (!subj) return;

  document.getElementById("modalSubjectName").textContent = subj.name;
  document.getElementById("modalSubjectCode").textContent = subj.code;

  const body = document.getElementById("modalBody");
  body.innerHTML = "";

  subj.units.forEach(unit => {
    let doneCount = 0;
    const topicItems = unit.topics.map(topic => {
      const key = `${subj.id}_${unit.id}_${topic}`;
      const checked = !!progress[key];
      if (checked) doneCount++;
      return `
        <div class="topic-item">
          <input type="checkbox" class="topic-cb" id="${key}" ${checked ? "checked" : ""}
            onchange="toggleTopic('${key}','${unit.id}','${subj.id}')" />
          <label class="topic-label ${checked ? 'done' : ''}" for="${key}">${topic}</label>
        </div>
      `;
    }).join("");

    const pct = unit.topics.length ? Math.round((doneCount / unit.topics.length) * 100) : 0;

    const block = document.createElement("div");
    block.className = "unit-block";
    block.innerHTML = `
      <div class="unit-header" onclick="toggleUnit('${unit.id}')">
        <span class="unit-name">${unit.name}</span>
        <div style="display:flex;align-items:center;gap:12px">
          <div class="unit-progress-mini">
            <div class="mini-bar"><div class="mini-bar-fill" id="minibar_${unit.id}" style="width:${pct}%"></div></div>
            <span>${doneCount}/${unit.topics.length}</span>
          </div>
          <span class="unit-toggle" id="utoggle_${unit.id}">▼</span>
        </div>
      </div>
      <div class="unit-topics" id="unit_${unit.id}">${topicItems}</div>
    `;
    body.appendChild(block);
  });

  // Notes
  const notesSection = document.createElement("div");
  notesSection.className = "modal-notes";
  notesSection.innerHTML = `
    <div class="card-title">📝 Notes</div>
    <textarea class="notes-textarea" id="notesArea_${subj.id}" placeholder="Add your notes here...">${notes[subj.id] || ""}</textarea>
    <button class="btn-sm" style="margin-top:8px" onclick="saveNotes('${subj.id}')">Save Notes</button>
  `;
  body.appendChild(notesSection);

  document.getElementById("subjectModal").classList.add("open");
}

function toggleUnit(unitId) {
  const el = document.getElementById(`unit_${unitId}`);
  const toggle = document.getElementById(`utoggle_${unitId}`);
  el.classList.toggle("open");
  toggle.textContent = el.classList.contains("open") ? "▲" : "▼";
}

function toggleTopic(key, unitId, subjId) {
  progress[key] = !progress[key];
  const label = document.querySelector(`label[for="${key}"]`);
  if (label) label.classList.toggle("done", progress[key]);

  // Update mini bar
  const subj = SYLLABUS.find(s => s.id === subjId);
  const unit = subj?.units.find(u => u.id === unitId);
  if (unit) {
    let done = 0;
    unit.topics.forEach(t => {
      if (progress[`${subjId}_${unitId}_${t}`]) done++;
    });
    const pct = Math.round((done / unit.topics.length) * 100);
    const bar = document.getElementById(`minibar_${unitId}`);
    if (bar) bar.style.width = `${pct}%`;
  }

  LS.save();
  updateStreak();
}

function saveNotes(subjId) {
  notes[subjId] = document.getElementById(`notesArea_${subjId}`).value;
  LS.save();
}

/* ========== STREAK ========== */
function updateStreak() {
  const today = new Date().toDateString();
  const last = localStorage.getItem("rgpv_lastStudy");
  let streak = parseInt(localStorage.getItem("rgpv_streak") || "0");

  if (last === today) return;
  const yesterday = new Date(Date.now() - 86400000).toDateString();
  if (last === yesterday) streak++;
  else streak = 1;

  localStorage.setItem("rgpv_lastStudy", today);
  localStorage.setItem("rgpv_streak", streak.toString());
}

/* ========== PLANNER ========== */
const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function renderPlanner() {
  document.getElementById("pomodoroCount").textContent = pomodoroSessions;

  // Tasks
  renderTasks();

  // Week grid
  const grid = document.getElementById("weekGrid");
  grid.innerHTML = "";
  DAYS.forEach(day => {
    const col = document.createElement("div");
    col.className = "day-col";
    col.innerHTML = `<div class="day-label">${day}</div>`;
    [0, 1, 2].forEach(slot => {
      const key = `${day}_${slot}`;
      const textarea = document.createElement("textarea");
      textarea.className = "day-slot";
      textarea.placeholder = slot === 0 ? "Morning" : slot === 1 ? "Afternoon" : "Evening";
      textarea.value = weekPlan[key] || "";
      textarea.oninput = () => { weekPlan[key] = textarea.value; LS.save(); };
      col.appendChild(textarea);
    });
    grid.appendChild(col);
  });
}

function renderTasks() {
  const list = document.getElementById("taskList");
  list.innerHTML = "";
  tasks.forEach((task, i) => {
    const li = document.createElement("li");
    li.className = "task-item";
    li.innerHTML = `
      <input type="checkbox" class="task-cb" ${task.done ? "checked" : ""} onchange="toggleTask(${i})" />
      <span class="task-text ${task.done ? 'done' : ''}">${task.text}</span>
      <button class="task-del" onclick="deleteTask(${i})">✕</button>
    `;
    list.appendChild(li);
  });
}

function addTask() {
  const input = document.getElementById("taskInput");
  if (!input.value.trim()) return;
  tasks.push({ text: input.value.trim(), done: false });
  input.value = "";
  LS.save();
  renderTasks();
}

function toggleTask(i) {
  tasks[i].done = !tasks[i].done;
  LS.save();
  renderTasks();
}

function deleteTask(i) {
  tasks.splice(i, 1);
  LS.save();
  renderTasks();
}

function clearCompletedTasks() {
  tasks = tasks.filter(t => !t.done);
  LS.save();
  renderTasks();
}

/* ========== POMODORO ========== */
function formatTime(secs) {
  const m = Math.floor(secs / 60).toString().padStart(2, "0");
  const s = (secs % 60).toString().padStart(2, "0");
  return `${m}:${s}`;
}

function startTimer() {
  if (pomodoroRunning) return;
  pomodoroRunning = true;
  pomodoroInterval = setInterval(() => {
    if (pomodoroSeconds <= 0) {
      clearInterval(pomodoroInterval);
      pomodoroRunning = false;
      pomodoroSessions++;
      LS.save();
      document.getElementById("pomodoroCount").textContent = pomodoroSessions;
      document.getElementById("timerLabel").textContent = "✅ Session complete!";
      return;
    }
    pomodoroSeconds--;
    document.getElementById("timerDisplay").textContent = formatTime(pomodoroSeconds);
  }, 1000);
}

function pauseTimer() {
  clearInterval(pomodoroInterval);
  pomodoroRunning = false;
}

function resetTimer(mins) {
  clearInterval(pomodoroInterval);
  pomodoroRunning = false;
  pomodoroSeconds = (mins || 25) * 60;
  document.getElementById("timerDisplay").textContent = formatTime(pomodoroSeconds);
  document.getElementById("timerLabel").textContent = mins === 5 ? "Break Time" : mins === 15 ? "Long Break" : "Focus Session";
}

/* ========== ANALYTICS ========== */
function renderAnalytics() {
  // Chart bars
  const chartBars = document.getElementById("chartBars");
  chartBars.innerHTML = "";
  const colors = SYLLABUS.map(s => s.color);

  SYLLABUS.forEach((subj, i) => {
    const p = getSubjectProgress(subj);
    const group = document.createElement("div");
    group.className = "bar-group";
    group.innerHTML = `
      <span class="bar-pct">${p.pct}%</span>
      <div class="bar-fill" style="height:${Math.max(4, p.pct * 1.5)}px;background:linear-gradient(180deg,${colors[i]},${colors[i]}88);width:100%" title="${subj.name}: ${p.pct}%"></div>
      <span class="bar-name">${subj.shortName}</span>
    `;
    chartBars.appendChild(group);
  });

  // Top subjects
  const sorted = [...SYLLABUS].sort((a, b) => getSubjectProgress(b).pct - getSubjectProgress(a).pct);
  const topEl = document.getElementById("topSubjects");
  topEl.innerHTML = "";
  sorted.forEach((subj, i) => {
    const p = getSubjectProgress(subj);
    topEl.innerHTML += `
      <div class="top-subject-item">
        <span class="top-rank">${i + 1}</span>
        <div class="top-subject-info">
          <div class="top-subject-name">${subj.name}</div>
          <div class="top-subject-pct">${p.done}/${p.total} topics done</div>
          <div class="top-subject-bar"><div class="top-subject-bar-fill" style="width:${p.pct}%;background:${subj.color}"></div></div>
        </div>
        <span style="font-family:'Syne',sans-serif;font-weight:800;color:${subj.color}">${p.pct}%</span>
      </div>
    `;
  });

  // Stats overview
  const overall = getOverallStats();
  const statsEl = document.getElementById("statsOverview");
  statsEl.innerHTML = `
    <div class="stats-row"><span class="stats-row-label">Total Topics</span><span class="stats-row-value">${overall.total}</span></div>
    <div class="stats-row"><span class="stats-row-label">Completed</span><span class="stats-row-value" style="color:var(--green)">${overall.done}</span></div>
    <div class="stats-row"><span class="stats-row-label">Pending</span><span class="stats-row-value" style="color:var(--orange)">${overall.total - overall.done}</span></div>
    <div class="stats-row"><span class="stats-row-label">Overall Progress</span><span class="stats-row-value">${overall.pct}%</span></div>
    <div class="stats-row"><span class="stats-row-label">Study Streak</span><span class="stats-row-value" style="color:var(--red)">🔥 ${localStorage.getItem("rgpv_streak") || 0} days</span></div>
    <div class="stats-row"><span class="stats-row-label">Pomodoros Done</span><span class="stats-row-value">🍅 ${pomodoroSessions}</span></div>
  `;

  // Revision tracker (all subjects, all units as revision items)
  const revEl = document.getElementById("revisionGrid");
  revEl.innerHTML = "";
  SYLLABUS.forEach(subj => {
    subj.units.forEach(unit => {
      const key = `rev_${unit.id}`;
      const done = !!revisions[key];
      revEl.innerHTML += `
        <div class="revision-item">
          <input type="checkbox" class="revision-cb" id="${key}" ${done ? "checked" : ""}
            onchange="toggleRevision('${key}')" />
          <label class="revision-label" for="${key}"><strong>${subj.shortName}</strong> — ${unit.name}</label>
          ${done ? '<span class="revision-status">✅ Revised</span>' : ''}
        </div>
      `;
    });
  });
}

function toggleRevision(key) {
  revisions[key] = !revisions[key];
  LS.save();
  renderAnalytics();
}

/* ========== EXPORT REPORT ========== */
function exportReport() {
  const overall = getOverallStats();
  let report = `RGPV 6th Semester Progress Report\n`;
  report += `Generated: ${new Date().toLocaleString()}\n`;
  report += `=====================================\n\n`;
  report += `Overall Progress: ${overall.pct}% (${overall.done}/${overall.total} topics)\n`;
  report += `Study Streak: ${localStorage.getItem("rgpv_streak") || 0} days\n\n`;

  SYLLABUS.forEach(subj => {
    const p = getSubjectProgress(subj);
    report += `\n${subj.name} (${subj.code})\n`;
    report += `---------------------------------\n`;
    report += `Progress: ${p.pct}% — ${p.done}/${p.total} topics done\n`;
    subj.units.forEach(unit => {
      let done = 0;
      unit.topics.forEach(t => { if (progress[`${subj.id}_${unit.id}_${t}`]) done++; });
      report += `  ${unit.name}: ${done}/${unit.topics.length}\n`;
    });
    if (notes[subj.id]) report += `  Notes: ${notes[subj.id]}\n`;
  });

  const blob = new Blob([report], { type: "text/plain" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "RGPV_Progress_Report.txt";
  a.click();
}

/* ========== BACKUP / RESTORE ========== */
function backupData() {
  const data = {
    progress, notes, tasks, weekPlan, revisions,
    pomodoroSessions, accentColor,
    goal: localStorage.getItem("rgpv_goal"),
    streak: localStorage.getItem("rgpv_streak"),
    examdate: localStorage.getItem("rgpv_examdate")
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "RGPV_Backup.json";
  a.click();
}

function restoreData(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result);
      progress = data.progress || {};
      notes = data.notes || {};
      tasks = data.tasks || [];
      weekPlan = data.weekPlan || {};
      revisions = data.revisions || {};
      pomodoroSessions = data.pomodoroSessions || 0;
      accentColor = data.accentColor || "#6c63ff";
      if (data.goal) localStorage.setItem("rgpv_goal", data.goal);
      if (data.streak) localStorage.setItem("rgpv_streak", data.streak);
      if (data.examdate) localStorage.setItem("rgpv_examdate", data.examdate);
      LS.save();
      setAccent(accentColor);
      renderDashboard();
      alert("✅ Data restored successfully!");
    } catch {
      alert("❌ Invalid backup file.");
    }
  };
  reader.readAsText(file);
}

/* ========== SETTINGS ========== */
function renderSettings() {
  const theme = document.documentElement.getAttribute("data-theme");
  document.getElementById("themeCheckbox").checked = theme === "light";
}

/* ========== THEME ========== */
function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("rgpv_theme", next);
  updateThemeUI(next);
}

function updateThemeUI(theme) {
  const isLight = theme === "light";
  document.getElementById("themeIcon").textContent = isLight ? "🌙" : "☀️";
  document.getElementById("themeLabel").textContent = isLight ? "Dark Mode" : "Light Mode";
  document.getElementById("themeToggleSm").textContent = isLight ? "🌙" : "☀️";
  document.getElementById("themeCheckbox").checked = isLight;
}

/* ========== INIT ========== */
function init() {
  LS.load();
  setAccent(accentColor);
  updateThemeUI(document.documentElement.getAttribute("data-theme") || "dark");

  // Nav
  document.querySelectorAll(".nav-item").forEach(el => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      showPage(el.dataset.page);
    });
  });

  // Sidebar mobile
  document.getElementById("hamburger").onclick = openSidebar;
  document.getElementById("sidebarOverlay").onclick = closeSidebar;

  // Theme
  document.getElementById("themeToggle").onclick = toggleTheme;
  document.getElementById("themeToggleSm").onclick = toggleTheme;
  document.getElementById("themeCheckbox").onchange = toggleTheme;

  // Dashboard goal
  document.getElementById("saveGoalBtn").onclick = () => {
    const v = document.getElementById("todayGoalInput").value.trim();
    if (v) {
      localStorage.setItem("rgpv_goal", v);
      document.getElementById("goalDisplay").textContent = v;
    }
  };

  // Exam date
  document.getElementById("examDate").onchange = (e) => {
    localStorage.setItem("rgpv_examdate", e.target.value);
    const days = Math.ceil((new Date(e.target.value) - new Date()) / (1000 * 60 * 60 * 24));
    document.getElementById("countdownVal").textContent = days > 0 ? `${days} days` : "Today!";
  };

  // Export
  document.getElementById("exportBtn").onclick = exportReport;

  // Modal close
  document.getElementById("modalClose").onclick = () => {
    document.getElementById("subjectModal").classList.remove("open");
    renderSubjects(document.getElementById("filterSelect").value, document.getElementById("searchInput").value);
    renderDashboard();
  };
  document.getElementById("subjectModal").onclick = (e) => {
    if (e.target === document.getElementById("subjectModal")) {
      document.getElementById("subjectModal").classList.remove("open");
      renderSubjects();
      renderDashboard();
    }
  };

  // Search / Filter
  document.getElementById("searchInput").oninput = (e) => {
    renderSubjects(document.getElementById("filterSelect").value, e.target.value);
  };
  document.getElementById("filterSelect").onchange = (e) => {
    renderSubjects(e.target.value, document.getElementById("searchInput").value);
  };

  // Pomodoro
  document.getElementById("timerStart").onclick = startTimer;
  document.getElementById("timerPause").onclick = pauseTimer;
  document.getElementById("timerReset").onclick = () => resetTimer(25);

  document.querySelectorAll(".timer-opt").forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll(".timer-opt").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const mins = parseInt(btn.dataset.mins);
      resetTimer(mins);
    };
  });

  // Tasks
  document.getElementById("addTaskBtn").onclick = addTask;
  document.getElementById("taskInput").onkeydown = (e) => { if (e.key === "Enter") addTask(); };
  document.getElementById("clearTasksBtn").onclick = clearCompletedTasks;

  // Settings
  document.getElementById("resetAllBtn").onclick = () => {
    if (confirm("⚠️ Reset ALL progress? This cannot be undone.")) {
      progress = {}; notes = {}; tasks = []; weekPlan = {}; revisions = {};
      pomodoroSessions = 0;
      localStorage.removeItem("rgpv_streak");
      localStorage.removeItem("rgpv_goal");
      localStorage.removeItem("rgpv_examdate");
      LS.save();
      renderDashboard();
      alert("✅ Progress reset.");
    }
  };

  document.getElementById("backupBtn").onclick = backupData;
  document.getElementById("restoreBtn").onclick = () => document.getElementById("restoreFile").click();
  document.getElementById("restoreFile").onchange = (e) => { if (e.target.files[0]) restoreData(e.target.files[0]); };

  // Color swatches
  document.querySelectorAll(".swatch").forEach(s => {
    if (s.dataset.color === accentColor) s.classList.add("active");
    else s.classList.remove("active");
    s.onclick = () => {
      document.querySelectorAll(".swatch").forEach(sw => sw.classList.remove("active"));
      s.classList.add("active");
      setAccent(s.dataset.color);
    };
  });

  // Render initial page
  renderDashboard();
}

document.addEventListener("DOMContentLoaded", init);
