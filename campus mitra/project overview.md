# 🏛 Campus Mitra — Smart Academic Management Platform

> **Minor Project** | Indore Institute of Science and Technology (IIST), Indore, MP
> **Team:** VisionX | **Lead Developer:** Nishita



## 📖 Project Overview

**Campus Mitra** is a centralized, role-based academic management platform developed for Indore Institute of Science and Technology (IIST). It replaces fragmented tools like WhatsApp groups, Excel sheets, and outdated ERP systems with one seamless digital ecosystem.

Built using **Python/Django** on the backend and **HTML/CSS/JavaScript** on the frontend with **MySQL** as the database, Campus Mitra provides every stakeholder — students, teachers, parents, and administrators — with a personalized dashboard that simplifies academic responsibilities and enhances collaboration.

---

## ❗ Problem Statement

Most educational institutions still rely on scattered, disconnected tools:

- 📱 **WhatsApp groups** for announcements
- 📊 **Excel sheets** for attendance tracking
- 📋 **Physical notice boards** for timetables
- 🖥 **Outdated ERP systems** with limited functionality

This results in:
- Students missing important updates
- Teachers wasting time managing multiple platforms
- Parents unable to monitor their child's progress remotely
- Administrators struggling to maintain accurate, centralized records

Campus Mitra addresses all these issues by **combining all academic operations into one unified platform**.

---

## 🎯 Objectives

- ✅ Create a unified digital platform for all academic tasks
- ✅ Provide role-based access for Students, Teachers, Parents & Admins
- ✅ Enable real-time attendance tracking and reporting
- ✅ Centralize notes, study materials, and assignments
- ✅ Deliver instant campus-wide announcements
- ✅ Allow parents to remotely monitor student progress
- ✅ Reduce manual workload and human errors
- ✅ Build a scalable, cloud-ready, AI-extensible architecture

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.x, Django Framework |
| **Database** | MySQL 8.0 |
| **Frontend** | HTML5, CSS3, JavaScript |
| **UI Framework** | Bootstrap 5 |
| **Icons** | Font Awesome 5, Bootstrap Icons |
| **Animations** | WOW.js, Animate.css |
| **Carousel** | Owl Carousel |
| **AI Integration** | RAG (Retrieval-Augmented Generation) |
| **Version Control** | GitHub |
| **API Style** | RESTful APIs |
| **Dev Tools** | VS Code / PyCharm |

---

## 📁 Project Structure

```
campus-mitra/
│
├── 📄 index.html               # Home page (public landing)
├── 📄 about.html               # About Campus Mitra
├── 📄 team.html                # Our Team page
├── 📄 login.html               # Login portal (role-based)
│
├── 📄 student-dashboard.html   # Student dashboard
├── 📄 faculty-dashboard.html   # Faculty/Teacher dashboard
├── 📄 parent-dashboard.html    # Parent dashboard
├── 📄 admin-dashboard.html     # Administrator dashboard
│
├── 📄 404.html                 # 404 error page
├── 📄 README.md                # Project documentation
│
├── 📁 css/
│   ├── bootstrap.min.css
│   └── style.css
│
├── 📁 js/
│   └── main.js
│
├── 📁 img/
│   ├── about.jpg
│   ├── carousel-1.jpg
│   ├── carousel-2.jpg
│   ├── team-1.jpg ... team-4.jpg
│   └── course-1.jpg ... course-3.jpg
│
└── 📁 lib/
    ├── animate/
    ├── easing/
    ├── owlcarousel/
    ├── waypoints/
    └── wow/
```

---

## 🌐 Pages & Features

### Public Pages

| Page | File | Description |
|------|------|-------------|
| Home | `index.html` | Landing page with features, about section, team preview |
| About | `about.html` | Background, key stats, solution approach, tech stack |
| Our Team | `team.html` | Developer profiles and project information |
| Login | `login.html` | Role-based login portal with demo credentials |
| 404 | `404.html` | Custom error page |

### Navbar (all public pages)
```
Home  |  About  |  Features  |  Our Team  |  [ Login ]
```

---

## 🖥 Dashboards

### 🎓 Student Dashboard (`student-dashboard.html`)

| Section | Details |
|---------|---------|
| Hero Card | Name, Enroll No., Semester, Section, quick stats |
| Stat Cards | Attendance %, Assignments done, CGPA |
| Today's Timetable | Subject, Room, Faculty, status (Now/Theory/Lab) |
| Attendance Tracker | Subject-wise bars with shortage warnings |
| Recent Notes | Downloadable study materials |
| Notices | Urgent and general announcements |
| Quick Actions | Download Notes, View Results, Submit Assignment, Logout |

---

### 👩‍🏫 Faculty Dashboard (`faculty-dashboard.html`)

| Section | Details |
|---------|---------|
| Hero Card | Name, Faculty ID, department stats |
| Stat Cards | Attendance marked, assignments submitted, pending announcements |
| Attendance Marking | Live table with Present/Absent/Late buttons per student |
| Today's Classes | Schedule with student count per class |
| Upload Notes | Drag-and-drop file upload area with recent uploads list |
| Post Announcement | Audience selector, urgency tag, recent posts |

---

### 👨‍👩‍👧 Parent Dashboard (`parent-dashboard.html`)

| Section | Details |
|---------|---------|
| Hero Card | Guardian name, child overview |
| Child Profile Card | Full profile with CGPA, semester, section tags |
| Stat Cards | Attendance %, CGPA, shortage alerts count |
| Attendance Details | Subject-wise bars with shortage warnings |
| School Notices | Urgent/general notices |
| Contact Teachers | Direct message buttons per faculty |
| Results Table | Last semester marks with grade badges |

---

### 🛡 Admin Dashboard (`admin-dashboard.html`)

| Section | Details |
|---------|---------|
| Hero Card | Institution stats — students, faculty, departments, uptime |
| Stat Cards | Total students, faculty, attendance alerts, active notices |
| User Management | Table with Edit/Delete, role color tags, status |
| Department Stats | Bar chart for each department |
| Timetable Manager | Quick slot editor with class/section selector |
| Post Announcement | Full audience + urgency selector |
| Attendance Alerts | Shortage list with "Send Alert to Parents" action |

---

## 🔐 Login Credentials (Demo)

| Role | Email | Password | Redirects To |
|------|-------|----------|--------------|
| 🎓 Student | student@iist.ac.in | student123 | student-dashboard.html |
| 👩‍🏫 Faculty | faculty@iist.ac.in | faculty123 | faculty-dashboard.html |
| 👨‍👩‍👧 Parent | parent@iist.ac.in | parent123 | parent-dashboard.html |
| 🛡 Admin | admin@iist.ac.in | admin123 | admin-dashboard.html |

> **Demo Mode:** Leave fields empty and click Sign In — auto-redirects based on selected role.

---

## 🔀 Navigation Flow

```
index.html
  ├── about.html
  ├── index.html#features  (anchor scroll)
  ├── team.html
  └── login.html
        ├── student-dashboard.html
        ├── faculty-dashboard.html
        ├── parent-dashboard.html
        └── admin-dashboard.html
              └── (Logout → login.html)
              └── (Public Site → index.html)
```

### Logout paths on every dashboard (3 ways):
1. Sidebar nav → 🚪 **Logout**
2. User card bottom → ⏻ **Power button**
3. Topbar right → ⏻ **Logout button**

---

## 📦 Core Modules

### 1. 📋 Attendance Management
- Teachers mark attendance digitally (Present / Absent / Late)
- Real-time records visible to students and parents
- Automated shortage detection with alerts
- Reports exportable per subject/student

### 2. 📚 Notes & Study Material Distribution
- Faculty upload PDFs, PPTs, DOCX files
- Students download from a categorized single module
- Materials organized by subject and date
- Drag-and-drop upload interface

### 3. 🗓 Timetable Management
- Admin creates and updates class schedules
- Students and faculty view live timetables
- Room and faculty assigned per slot
- Supports class-section-wise filtering

### 4. 📢 Announcements & Notifications
- Admin and faculty post instant notices
- Target by role: All / Students / Faculty / Parents / Department
- Urgency levels: General / Urgent / Event
- Students and parents receive real-time updates

### 5. 🔐 Role-Based Authentication
- Secure login with 4 distinct user roles
- Each role sees only relevant features and data
- Password-protected with session management
- Prevents unauthorized access to sensitive records

### 6. 🤖 RAG-Based AI Integration *(Planned)*
- Retrieval-Augmented Generation for intelligent search
- Natural language queries for notes and schedules
- Chatbot for academic assistance
- Predictive attendance analytics

---

## 👥 User Roles

```
┌────────────────────────────────────────────────────┐
│                   CAMPUS MITRA                     │
├──────────┬──────────┬──────────┬───────────────────┤
│ STUDENT  │ FACULTY  │  PARENT  │      ADMIN        │
├──────────┼──────────┼──────────┼───────────────────┤
│ View     │ Mark     │ Monitor  │ Manage all        │
│ timetable│ attendance│attendance│ users            │
│          │          │          │                   │
│ Download │ Upload   │ View     │ Create            │
│ notes    │ materials│ results  │ schedules         │
│          │          │          │                   │
│ Check    │ Post     │ Contact  │ Post              │
│ attendance│ notices │ faculty  │ announcements     │
│          │          │          │                   │
│ Submit   │ Track    │ Track    │ Export            │
│ assignments│assignments│progress│ reports          │
└──────────┴──────────┴──────────┴───────────────────┘
```

---

## 🔄 Methodology

### Development Model: Agile
Campus Mitra follows the **Agile Model** with iterative sprints:

```
Sprint 1 (Week 1–2)  → Requirement Gathering
Sprint 2 (Week 3–4)  → Database & UI Design
Sprint 3 (Week 5–6)  → Module Development
                        (Attendance, Timetable, Notes, Announcements)
Sprint 4 (Week 7)    → Integration & Testing
Sprint 5 (Week 8)    → Documentation & Final Submission
```

### Feasibility
| Type | Status |
|------|--------|
| **Technical** | ✅ Open-source stack, runs on any OS/server |
| **Economic** | ✅ Zero licensing cost, minimal hosting cost |
| **Operational** | ✅ Intuitive UI, role-based dashboards, no training needed |

---

## 🚀 How to Run

### Option 1 — Open directly in browser (Frontend only)
```bash
# Clone or download the project
git clone https://github.com/your-username/campus-mitra.git
cd campus-mitra

# Open index.html in any browser
open index.html
# or double-click index.html
```

### Option 2 — Run with Django backend
```bash
# Install Python dependencies
pip install django mysqlclient

# Create Django project
django-admin startproject campusmitra
cd campusmitra

# Configure MySQL in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'campus_mitra_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
python manage.py runserver

# Visit
http://127.0.0.1:8000/
```

### Prerequisites
- Python 3.x
- MySQL 8.0
- Any modern browser (Chrome, Firefox, Edge)
- VS Code or PyCharm (recommended)

---

## 🔭 Future Scope

| Feature | Description |
|---------|-------------|
| 🤖 AI Chatbot | RAG-powered academic assistant using uploaded notes |
| 📱 Mobile App | Android/iOS app with push notifications |
| 📊 Predictive Analytics | Attendance trends and performance prediction |
| ☁ Cloud Deployment | AWS / Azure / DigitalOcean hosting |
| 🏫 Multi-Institution | Expand beyond IIST to other colleges |
| 📝 Exam Management | Scheduling, seating, and result management |
| 💰 Fee Tracking | Fee payment and receipt management |
| 🔔 Auto Alerts | Automated SMS/email for attendance shortage |
| 🗂 Assignment Evaluation | Digital submission and faculty grading |
| 🧑‍💼 Faculty Workload | Automated workload and scheduling system |

---

## 👨‍💻 Team

| Name | Role | Technologies |
|------|------|-------------|
| **Nishita** | Lead Developer | Python, Django, MySQL, RESTful APIs, RAG |
| Team Member | Frontend Developer | HTML, CSS, JavaScript, Bootstrap |
| Team Member | Database Engineer | MySQL, Django ORM, Schema Design |
| Team Member | System Analyst & Tester | UML Diagrams, Testing, Documentation |

> **Institution:** Indore Institute of Science and Technology (IIST), Rau–Pithampur Road, Indore, Madhya Pradesh
> **Project Guide:** Faculty Mentor, Department of Computer Science & Engineering

---

## 📚 References

1. Pressman, R. S., *Software Engineering: A Practitioner's Approach*, McGraw-Hill, 2015.
2. Sommerville, I., *Software Engineering*, Pearson Education, 2016.
3. Django Software Foundation, *Django Documentation* — https://docs.djangoproject.com/
4. Oracle Corporation, *MySQL 8.0 Documentation* — https://dev.mysql.com/doc/
5. IEEE Computer Society, *IEEE Standard for Software Requirements Specification (SRS)*, IEEE 830.
6. Beck, K. et al., *Agile Manifesto* — https://agilemanifesto.org/
7. Fowler, M., *UML Distilled*, Addison-Wesley, 2004.
8. Fielding, R. T., *REST Architectural Style*, University of California, 2000.
9. OpenAI, *Retrieval-Augmented Generation (RAG) Documentation* — https://platform.openai.com/docs
10. W3C, *HTML, CSS and JavaScript Standards* — https://www.w3.org/

---

## 📄 License

This project is developed as an academic minor project at IIST Indore. All rights reserved.

&copy; Campus Mitra — Nishita | VisionX | IIST Indore | 2024–25

---

*Built with ❤️ at Indore Institute of Science and Technology*