/* ============================================================
   NISHITA KANOJIYA – PORTFOLIO SCRIPTS
   ============================================================ */

/* ============================================================
   CONFIG — paste your Google Apps Script Web App URL here
   ============================================================ */
const GOOGLE_SHEET_URL = 'https://script.google.com/a/macros/indoreinstitute.com/s/AKfycbw3LeUxZd17UQCse6brIkPVMEF-rgmNv2YL2bBTJcvmSpoe4O57HijNHlf8xDVEhQ6t/exec';

/* ============================================================
   1. TYPED TEXT EFFECT
   ============================================================ */
const roles = [
  'AI/ML Engineer',
  'Research Intern @ IIT Indore',
  'Deep Learning Developer',
  'NLP Enthusiast',
  'Data Analytics Explorer',
  'Problem Solver',
];

let roleIndex   = 0;
let charIndex   = 0;
let isDeleting  = false;
const typedEl   = document.getElementById('typedText');

function typeEffect() {
  if (!typedEl) return;

  const current = roles[roleIndex];

  if (isDeleting) {
    typedEl.textContent = current.slice(0, charIndex - 1);
    charIndex--;
  } else {
    typedEl.textContent = current.slice(0, charIndex + 1);
    charIndex++;
  }

  let delay = isDeleting ? 60 : 100;

  if (!isDeleting && charIndex === current.length) {
    delay = 1800;          // pause at end
    isDeleting = true;
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false;
    roleIndex  = (roleIndex + 1) % roles.length;
    delay = 400;           // pause before next word
  }

  setTimeout(typeEffect, delay);
}

document.addEventListener('DOMContentLoaded', () => {
  setTimeout(typeEffect, 800);
});


/* ============================================================
   2. NAVBAR — scroll behaviour + active link highlighting
   ============================================================ */
const navbar    = document.getElementById('navbar');
const navLinks  = document.querySelectorAll('.nav-links a');
const sections  = document.querySelectorAll('section[id]');

function onScroll() {
  // Sticky style
  if (window.scrollY > 60) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }

  // Active nav link
  let current = '';
  sections.forEach(sec => {
    const top    = sec.offsetTop - 100;
    const height = sec.offsetHeight;
    if (window.scrollY >= top && window.scrollY < top + height) {
      current = sec.getAttribute('id');
    }
  });

  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === `#${current}`) {
      link.classList.add('active');
    }
  });

  // Back-to-top button
  const btn = document.getElementById('backToTop');
  if (btn) {
    if (window.scrollY > 400) {
      btn.classList.add('show');
    } else {
      btn.classList.remove('show');
    }
  }
}

window.addEventListener('scroll', onScroll, { passive: true });
onScroll(); // run once on load


/* ============================================================
   3. MOBILE HAMBURGER MENU
   ============================================================ */
const hamburger  = document.getElementById('hamburger');
const navLinkUl  = document.getElementById('navLinks');

if (hamburger && navLinkUl) {
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    navLinkUl.classList.toggle('open');
  });

  // Close menu when a link is clicked
  navLinkUl.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('open');
      navLinkUl.classList.remove('open');
    });
  });

  // Close menu on outside click
  document.addEventListener('click', (e) => {
    if (!navbar.contains(e.target)) {
      hamburger.classList.remove('open');
      navLinkUl.classList.remove('open');
    }
  });
}


/* ============================================================
   4. SMOOTH SCROLL for anchor links
   ============================================================ */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});


/* ============================================================
   5. SCROLL-REVEAL (IntersectionObserver)
   ============================================================ */
const fadeEls = document.querySelectorAll('.fade-in');

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        // Stagger siblings in the same parent
        const siblings = entry.target.parentElement
          ? [...entry.target.parentElement.querySelectorAll('.fade-in')]
          : [];
        const idx = siblings.indexOf(entry.target);
        const delay = idx * 80;

        setTimeout(() => {
          entry.target.classList.add('visible');
        }, delay);

        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
);

fadeEls.forEach(el => observer.observe(el));


/* ============================================================
   6. BACK TO TOP BUTTON
   ============================================================ */
const backBtn = document.getElementById('backToTop');
if (backBtn) {
  backBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}


/* ============================================================
   7. CONTACT FORM — submits to Google Sheets via Apps Script
   ============================================================ */
const contactForm = document.getElementById('contactForm');
const formNote    = document.getElementById('formNote');

if (contactForm) {
  contactForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    const name    = document.getElementById('name').value.trim();
    const email   = document.getElementById('email').value.trim();
    const subject = document.getElementById('subject').value.trim();
    const message = document.getElementById('message').value.trim();

    // Basic validation
    if (!name || !email || !subject || !message) {
      showNote('⚠️ Please fill in all fields.', 'error');
      return;
    }
    if (!isValidEmail(email)) {
      showNote('⚠️ Please enter a valid email address.', 'error');
      return;
    }

    // Check URL is configured
    if (!GOOGLE_SHEET_URL || GOOGLE_SHEET_URL === 'YOUR_APPS_SCRIPT_WEB_APP_URL_HERE') {
      showNote('⚠️ Form not configured yet. Please add the Google Apps Script URL.', 'error');
      return;
    }

    const submitBtn = contactForm.querySelector('button[type="submit"]');
    submitBtn.disabled  = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending…';

    try {
      // Send as URL-encoded form data via a hidden iframe trick
      // This avoids CORS issues with institutional Google accounts entirely
      submitToSheet({ name, email, subject, message });

      // Give Apps Script 2s to process then confirm
      await new Promise(resolve => setTimeout(resolve, 2000));
      contactForm.reset();
      showNote('✅ Message sent! I\'ll get back to you soon.', 'success');

    } catch (err) {
      showNote('❌ Something went wrong. Please try emailing me directly.', 'error');
      console.error('Form submission error:', err);

    } finally {
      submitBtn.disabled  = false;
      submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
    }
  });
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showNote(msg, type) {
  if (!formNote) return;
  formNote.textContent = msg;
  formNote.className   = `form-note ${type}`;
  setTimeout(() => {
    formNote.textContent = '';
    formNote.className   = 'form-note';
  }, 6000);
}

/* Hidden iframe form submission — bypasses CORS entirely.
   Apps Script receives a standard HTML form POST.              */
function submitToSheet(data) {
  // Remove any old iframe
  const old = document.getElementById('_gs_iframe');
  if (old) old.remove();

  // Create silent hidden iframe as target
  const iframe = document.createElement('iframe');
  iframe.id    = '_gs_iframe';
  iframe.name  = '_gs_iframe';
  iframe.style.cssText = 'display:none;width:0;height:0;border:none;position:absolute;';
  document.body.appendChild(iframe);

  // Build a hidden form that posts into the iframe
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = GOOGLE_SHEET_URL;
  form.target = '_gs_iframe';
  form.style.display = 'none';

  const fields = { ...data };
  Object.entries(fields).forEach(([key, val]) => {
    const input = document.createElement('input');
    input.type  = 'hidden';
    input.name  = key;
    input.value = val;
    form.appendChild(input);
  });

  document.body.appendChild(form);
  form.submit();

  // Cleanup after 5s
  setTimeout(() => {
    form.remove();
    iframe.remove();
  }, 5000);
}


/* ============================================================
   8. SKILL TAG HOVER RIPPLE (lightweight touch)
   ============================================================ */
document.querySelectorAll('.skill-tag').forEach(tag => {
  tag.addEventListener('mouseenter', function () {
    this.style.transform = 'scale(1.06)';
  });
  tag.addEventListener('mouseleave', function () {
    this.style.transform = 'scale(1)';
  });
});


/* ============================================================
   9. STATS COUNTER ANIMATION
   ============================================================ */
const stats = document.querySelectorAll('.stat h3');

const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.6 }
);

stats.forEach(stat => counterObserver.observe(stat));

function animateCounter(el) {
  const raw    = el.textContent.trim();           // e.g. "8.21", "5+", "2×", "7+"
  const suffix = raw.replace(/[\d.]/g, '');       // "+", "×", ""
  const target = parseFloat(raw);
  if (isNaN(target)) return;

  const isDecimal = raw.includes('.');
  const duration  = 1200;
  const steps     = 40;
  const stepTime  = duration / steps;
  let   current   = 0;

  const timer = setInterval(() => {
    current += target / steps;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = (isDecimal ? current.toFixed(2) : Math.floor(current)) + suffix;
  }, stepTime);
}


/* ============================================================
   10. CURSOR GLOW (optional subtle effect)
   ============================================================ */
const glow = document.createElement('div');
glow.style.cssText = `
  position: fixed;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(124,58,237,0.07) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
  transition: transform 0.18s ease;
  transform: translate(-50%, -50%);
`;
document.body.appendChild(glow);

let mouseX = 0, mouseY = 0;
let glowX  = 0, glowY  = 0;

document.addEventListener('mousemove', e => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});

function animateGlow() {
  glowX += (mouseX - glowX) * 0.08;
  glowY += (mouseY - glowY) * 0.08;
  glow.style.left = glowX + 'px';
  glow.style.top  = glowY + 'px';
  requestAnimationFrame(animateGlow);
}
animateGlow();


/* ============================================================
   11. PROJECT CARD — tilt effect on hover (desktop only)
   ============================================================ */
if (window.matchMedia('(hover: hover)').matches) {
  document.querySelectorAll('.project-card, .research-card').forEach(card => {
    card.addEventListener('mousemove', function (e) {
      const rect   = this.getBoundingClientRect();
      const cx     = rect.left + rect.width  / 2;
      const cy     = rect.top  + rect.height / 2;
      const dx     = (e.clientX - cx) / (rect.width  / 2);
      const dy     = (e.clientY - cy) / (rect.height / 2);
      const tiltX  = dy * -5;
      const tiltY  = dx *  5;
      this.style.transform = `translateY(-6px) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
      this.style.transition = 'transform 0.1s ease';
    });

    card.addEventListener('mouseleave', function () {
      this.style.transform = '';
      this.style.transition = 'transform 0.35s ease';
    });
  });
}


/* ============================================================
   12. PRELOADER fade-out on window load
   ============================================================ */
window.addEventListener('load', () => {
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.5s ease';
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.body.style.opacity = '1';
    });
  });
});
