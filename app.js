/**
 * STACKLY REAL ESTATE CONSULTANCY
 * Core Application Logic, View Routing, Role Switcher, and Interactive Calculators
 */

// Initialize preloader immediately
initPreloader();

document.addEventListener('DOMContentLoaded', () => {
  initRouting();
  initAuthModals();
  initCalculators();
  initSquareYardsSearch();
  initMobileNav();
  initWobbleCardAnimations();
  initDashboardFeatures();
  initHeroSlider();
  initDynamicCardUIUX();
  initPageScrollAnimations();
});

// ==========================================
// 0. BRANDED PAGE PRELOADER LOGIC
// ==========================================
function initPreloader() {
  const preloader = document.getElementById('pagePreloader');
  if (!preloader) return;

  const hidePreloader = () => {
    if (preloader.classList.contains('fade-out')) return;
    preloader.classList.add('fade-out');
    setTimeout(() => {
      preloader.style.display = 'none';
    }, 550);
  };

  // Allow preloader to show for a snappy, elegant minimum duration (700ms), then hide smoothly on page load
  const minTimer = new Promise(res => setTimeout(res, 700));
  const loadEvt = new Promise(res => {
    if (document.readyState === 'complete') {
      res();
    } else {
      window.addEventListener('load', res, { once: true });
    }
  });

  Promise.all([minTimer, loadEvt]).then(hidePreloader);

  // Maximum fallback timeout: guarantee dismissal within 1.2s
  setTimeout(hidePreloader, 1200);
}

// ==========================================
// DASHBOARD UTILITIES & LOGOUT
// ==========================================
function initDashboardFeatures() {
  const sidebarToggle = document.getElementById('dashSidebarToggle');
  const sidebar = document.querySelector('.dashboard-sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      sidebar.classList.toggle('mobile-open');
    });
  }

  // Unified Bulletproof Logout Handler
  document.querySelectorAll('.btn-logout-action, .btn-logout-sidebar').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      localStorage.removeItem('stackly_auth_user');
      localStorage.removeItem('stackly_user_role');
      if (typeof showToast === 'function') {
        showToast('Logged out successfully. Redirecting to home...');
      }
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 450);
    });
  });

  // Action buttons
  document.querySelectorAll('.btn-book-consult').forEach(btn => {
    btn.addEventListener('click', () => {
      if (typeof showToast === 'function') {
        showToast('<i class="fa-solid fa-calendar-check"></i> Advisory Slot Booked: Consultant Adv. Shilpi Singh assigned.');
      }
    });
  });

  document.querySelectorAll('.btn-export-census').forEach(btn => {
    btn.addEventListener('click', () => {
      if (typeof showToast === 'function') {
        showToast('<i class="fa-solid fa-download"></i> Downloading Stackly Executive Real Estate Census PDF...');
      }
    });
  });
}

// 1. ROUTING & VIEW NAVIGATION
// ==========================================
function initRouting() {
  const navLinks = document.querySelectorAll('.nav-link, .route-trigger');
  
  function handleHash() {
    const hash = window.location.hash.replace('#', '') || 'home';
    activateView(hash);
  }

  window.addEventListener('hashchange', handleHash);
  
  // If no hash in URL, check if there are standalone pages or active view
  if (window.location.hash) {
    handleHash();
  }
}

function activateView(viewId) {
  const views = document.querySelectorAll('.page-view');
  if (!views.length) return; // If standalone separate HTML page

  let targetView = document.getElementById(`view-${viewId}`);
  if (!targetView) {
    targetView = document.getElementById('view-home');
  }

  views.forEach(v => v.style.display = 'none');
  if (targetView) {
    targetView.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Update active nav links
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('data-target') === viewId) {
      link.classList.add('active');
    }
  });

  // Hide main nav/footer if viewing full dashboards
  const mainHeader = document.querySelector('.top-header');
  const mainFooter = document.querySelector('.footer-dark');
  const emergencyBanner = document.querySelector('.emergency-banner');

  if (viewId === 'user-dashboard' || viewId === 'admin-dashboard') {
    if (mainHeader) mainHeader.style.display = 'none';
    if (mainFooter) mainFooter.style.display = 'none';
    if (emergencyBanner) emergencyBanner.style.display = 'none';
  } else {
    if (mainHeader) mainHeader.style.display = 'block';
    if (mainFooter) mainFooter.style.display = 'block';
    if (emergencyBanner) emergencyBanner.style.display = 'flex';
  }
}

// ==========================================
// 2. AUTH MODALS & ROLE SWITCHING (Screenshots 2 & 3)
// ==========================================
let currentAuthRole = 'user'; // 'user' or 'admin'

function initAuthModals() {
  const loginModal = document.getElementById('loginModal');
  const signupModal = document.getElementById('signupModal');

  // Open triggers
  document.querySelectorAll('.open-login-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (loginModal) {
        e.preventDefault();
        closeModal(signupModal);
        openModal(loginModal);
      }
    });
  });

  document.querySelectorAll('.open-signup-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (signupModal) {
        e.preventDefault();
        closeModal(loginModal);
        openModal(signupModal);
      }
    });
  });

  // Close triggers
  document.querySelectorAll('.modal-close-trigger, .btn-back-home').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (loginModal || signupModal) {
        e.preventDefault();
        closeModal(loginModal);
        closeModal(signupModal);
      }
    });
  });

  // Close on outside click
  window.addEventListener('click', (e) => {
    if (e.target === loginModal) closeModal(loginModal);
    if (e.target === signupModal) closeModal(signupModal);
  });

  // Close on Escape key
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal(loginModal);
      closeModal(signupModal);
      // quickview removed
    }
  });

  // Role Switcher Buttons in Login & Signup
  document.querySelectorAll('.role-tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const parent = this.closest('.role-tabs');
      parent.querySelectorAll('.role-tab-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      currentAuthRole = this.getAttribute('data-role');
      
      // Update label/placeholder hints
      const modal = this.closest('.auth-modal-card');
      const emailInput = modal.querySelector('.auth-email-input');
      if (emailInput) {
        emailInput.placeholder = currentAuthRole === 'admin' 
          ? 'admin@stacklyrealty.com or Staff ID' 
          : 'name@example.com or Client ID';
      }
    });
  });

  // Login Form Submission
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      closeModal(loginModal);
      showToast(`Signing in as ${currentAuthRole.toUpperCase()}...`);
      
      setTimeout(() => {
        if (currentAuthRole === 'admin') {
          if (document.getElementById('view-admin-dashboard')) {
            window.location.hash = 'admin-dashboard';
          } else {
            window.location.href = 'admin-dashboard.html';
          }
        } else {
          if (document.getElementById('view-user-dashboard')) {
            window.location.hash = 'user-dashboard';
          } else {
            window.location.href = 'user-dashboard.html';
          }
        }
      }, 500);
    });
  }

  // Signup Form Submission
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
      e.preventDefault();
      closeModal(signupModal);
      showToast(`Account created! Welcome to Stackly Realty Cloud.`);
      setTimeout(() => {
        if (currentAuthRole === 'admin') {
          window.location.hash = 'admin-dashboard';
        } else {
          window.location.hash = 'user-dashboard';
        }
      }, 500);
    });
  }
}

function lockBodyScroll() {
  document.body.classList.add('modal-open');
}

function unlockBodyScroll() {
  const anyActive = document.querySelector('.modal-overlay.active');
  if (!anyActive) {
    document.body.classList.remove('modal-open');
  }
}

function openModal(modal) {
  if (modal) {
    modal.classList.add('active');
    lockBodyScroll();
  }
}

function closeModal(modal) {
  if (modal) {
    modal.classList.remove('active');
    unlockBodyScroll();
  }
}

// ==========================================
// 3. INTERACTIVE CALCULATORS & TOOLS
// ==========================================
function initCalculators() {
  const loanRange = document.getElementById('loanAmountRange');
  const loanText = document.getElementById('loanAmountDisplay');
  const rateRange = document.getElementById('loanRateRange');
  const rateText = document.getElementById('loanRateDisplay');
  const tenureRange = document.getElementById('loanTenureRange');
  const tenureText = document.getElementById('loanTenureDisplay');
  const emiOutput = document.getElementById('calculatedEmiOutput');
  const totalInterestOutput = document.getElementById('totalInterestOutput');

  function calculateEMI() {
    if (!loanRange || !rateRange || !tenureRange) return;

    const P = parseFloat(loanRange.value);
    const annualRate = parseFloat(rateRange.value);
    const years = parseFloat(tenureRange.value);

    loanText.textContent = `₹ ${(P / 100000).toFixed(1)} Lakhs (${(P / 10000000).toFixed(2)} Cr)`;
    rateText.textContent = `${annualRate.toFixed(2)} % p.a.`;
    tenureText.textContent = `${years} Years`;

    const r = (annualRate / 12) / 100;
    const n = years * 12;

    const emi = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
    const totalPayment = emi * n;
    const totalInterest = totalPayment - P;

    if (emiOutput) emiOutput.textContent = `₹ ${Math.round(emi).toLocaleString('en-IN')} / mo`;
    if (totalInterestOutput) totalInterestOutput.textContent = `₹ ${Math.round(totalInterest).toLocaleString('en-IN')}`;
  }

  if (loanRange && rateRange && tenureRange) {
    loanRange.addEventListener('input', calculateEMI);
    rateRange.addEventListener('input', calculateEMI);
    tenureRange.addEventListener('input', calculateEMI);
    calculateEMI();
  }
}

// ==========================================
// 4. SQUAREYARDS SEARCH HUB
// ==========================================
function initSquareYardsSearch() {
  const searchTabs = document.querySelectorAll('.sy-tab-btn');
  searchTabs.forEach(tab => {
    tab.addEventListener('click', function() {
      searchTabs.forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      showToast(`Showing verified inventory for: ${this.textContent}`);
    });
  });

  const searchBtn = document.getElementById('sySearchBtn');
  if (searchBtn) {
    searchBtn.addEventListener('click', () => {
      const city = document.getElementById('syCitySelect')?.value || 'Salem';
      const query = document.getElementById('syQueryInput')?.value || 'Prime';
      const budget = document.getElementById('syBudgetSelect')?.value || 'All';
      showToast(`Found 48 RERA verified properties in ${city} matching "${query}" (${budget})`);
      
      const projectSec = document.getElementById('sec-projects');
      if (projectSec) projectSec.scrollIntoView({ behavior: 'smooth' });
    });
  }

  // VIP Lead Form
  const vipForm = document.getElementById('vipLeadForm');
  if (vipForm) {
    vipForm.addEventListener('submit', (e) => {
      e.preventDefault();
      window.location.href = '404.html';
    });
  }

  // Admin Leads: Manual Token Issuance Form Validation
  const tokenForm = document.getElementById('tokenIssuanceForm');
  if (tokenForm) {
    tokenForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const nameInput = document.getElementById('clientFullName');
      if (nameInput && !nameInput.value.trim()) {
        nameInput.focus();
        showToast('Please enter client full name.');
        return;
      }
      window.location.href = '404.html';
    });
  }

  // User Dashboard: Inquiry Ticket Form Validation
  const inquiryForm = document.getElementById('inquiryTicketForm');
  if (inquiryForm) {
    inquiryForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const subjInput = document.getElementById('inquirySubject');
      if (subjInput && !subjInput.value.trim()) {
        subjInput.focus();
        showToast('Please enter inquiry subject.');
        return;
      }
      window.location.href = '404.html';
    });
  }
}

// ==========================================
// 5. MOBILE NAVIGATION & DRAWER
// ==========================================
function initMobileNav() {
  const navToggle = document.getElementById('mobileNavToggle');
  const navMenu = document.getElementById('navMenu');

  // Create or get mobile nav backdrop overlay
  let backdrop = document.getElementById('mobileNavBackdrop');
  if (!backdrop && navMenu) {
    backdrop = document.createElement('div');
    backdrop.id = 'mobileNavBackdrop';
    backdrop.className = 'mobile-nav-backdrop';
    document.body.appendChild(backdrop);
  }

  function openMobileNav() {
    if (!navMenu) return;
    navMenu.classList.add('mobile-open');
    if (navToggle) {
      navToggle.classList.add('toggle-active');
      navToggle.setAttribute('aria-expanded', 'true');
      const icon = navToggle.querySelector('i');
      if (icon) {
        icon.className = 'fa-solid fa-xmark';
      }
    }
    if (backdrop) backdrop.classList.add('active');
    document.body.classList.add('menu-open');
  }

  function closeMobileNav() {
    if (!navMenu) return;
    navMenu.classList.remove('mobile-open');
    if (navToggle) {
      navToggle.classList.remove('toggle-active');
      navToggle.setAttribute('aria-expanded', 'false');
      const icon = navToggle.querySelector('i');
      if (icon) {
        icon.className = 'fa-solid fa-bars';
      }
    }
    if (backdrop) backdrop.classList.remove('active');
    document.body.classList.remove('menu-open');
  }

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = navMenu.classList.contains('mobile-open');
      if (isOpen) {
        closeMobileNav();
      } else {
        openMobileNav();
      }
    });

    if (backdrop) {
      backdrop.addEventListener('click', closeMobileNav);
    }

    const drawerCloseBtn = document.getElementById('mobileDrawerClose');
    if (drawerCloseBtn) {
      drawerCloseBtn.addEventListener('click', closeMobileNav);
    }

    // Close when clicking nav links
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', closeMobileNav);
    });

    // Close with Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navMenu.classList.contains('mobile-open')) {
        closeMobileNav();
      }
    });
  }

  // Dashboard Mobile Sidebar Toggle
  const dashSidebarToggle = document.getElementById('dashSidebarToggle');
  const dashSidebar = document.querySelector('.dashboard-sidebar');
  let dashBackdrop = document.getElementById('dashSidebarBackdrop');

  if (dashSidebar && !dashBackdrop) {
    dashBackdrop = document.createElement('div');
    dashBackdrop.id = 'dashSidebarBackdrop';
    dashBackdrop.className = 'mobile-nav-backdrop';
    document.body.appendChild(dashBackdrop);
  }

  function openDashSidebar() {
    if (!dashSidebar) return;
    dashSidebar.classList.add('mobile-open');
    if (dashBackdrop) dashBackdrop.classList.add('active');
    document.body.classList.add('menu-open');
  }

  function closeDashSidebar() {
    if (!dashSidebar) return;
    dashSidebar.classList.remove('mobile-open');
    if (dashBackdrop) dashBackdrop.classList.remove('active');
    document.body.classList.remove('menu-open');
  }

  if (dashSidebarToggle && dashSidebar) {
    dashSidebarToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      if (dashSidebar.classList.contains('mobile-open')) {
        closeDashSidebar();
      } else {
        openDashSidebar();
      }
    });

    if (dashBackdrop) {
      dashBackdrop.addEventListener('click', closeDashSidebar);
    }

    dashSidebar.querySelectorAll('a, button').forEach(el => {
      el.addEventListener('click', () => {
        if (window.innerWidth <= 1024) {
          closeDashSidebar();
        }
      });
    });
  }
}

// ==========================================
// 5B. WOBBLE CARD ENTRANCE ANIMATION (INTERSECTION OBSERVER)
// ==========================================
function initWobbleCardAnimations() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  const cardSelectors = [
    '.project-card',
    '.featured-prop-card',
    '.service-card',
    '.service-detail-card',
    '.why-card',
    '.why-us-card',
    '.advisor-card',
    '.team-card',
    '.testi-card',
    '.testimonial-card',
    '.category-card',
    '.metric-card',
    '.stat-card',
    '.audit-feature-card',
    '.article-card',
    '.blog-card',
    '.portal-card',
    '.faq-item',
    '.calculator-card',
    '.dash-section-block'
  ];

  const cards = document.querySelectorAll(cardSelectors.join(', '));
  if (!cards.length) return;

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const card = entry.target;
        const parent = card.parentElement;
        let index = 0;
        if (parent) {
          const siblings = Array.from(parent.children).filter(el => el.classList.contains('wobble-card'));
          index = siblings.indexOf(card);
          if (index < 0) index = 0;
        }
        const delay = Math.min(index * 0.08, 0.48);
        card.style.animationDelay = `${delay}s`;
        card.classList.add('wobble-active');
        obs.unobserve(card);
      }
    });
  }, {
    rootMargin: '0px 0px -40px 0px',
    threshold: 0.12
  });

  cards.forEach(card => {
    card.classList.add('wobble-card');
    observer.observe(card);
  });
}

// ==========================================
// 6. DASHBOARD ACTIONS (Unified in initDashboardFeatures)
// ==========================================

// ==========================================
// TOAST NOTIFICATIONS
// ==========================================
function showToast(message) {
  let toast = document.getElementById('appToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'appToast';
    toast.className = 'toast-msg';
    document.body.appendChild(toast);
  }

  toast.innerHTML = `<span><i class="fa-solid fa-bolt"></i></span> <span>${message}</span>`;
  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
  }, 4000);
}

// ==========================================
// 7. HERO ANIMATING IMAGE SLIDER
// ==========================================
function initHeroSlider() {
  const sliders = document.querySelectorAll('.hero-animating-slider');
  sliders.forEach(slider => {
    const slides = slider.querySelectorAll('.hero-slide');
    const dots = slider.querySelectorAll('.hero-slide-dot');
    const prevBtn = slider.querySelector('.hero-prev-btn');
    const nextBtn = slider.querySelector('.hero-next-btn');

    if (!slides.length) return;

    let currentIndex = 0;
    let timer = null;

    function goToSlide(index) {
      slides[currentIndex].classList.remove('active');
      if (dots[currentIndex]) dots[currentIndex].classList.remove('active');

      currentIndex = (index + slides.length) % slides.length;

      slides[currentIndex].classList.add('active');
      if (dots[currentIndex]) dots[currentIndex].classList.add('active');
    }

    function nextSlide() {
      goToSlide(currentIndex + 1);
    }

    function prevSlide() {
      goToSlide(currentIndex - 1);
    }

    function startAutoplay() {
      stopAutoplay();
      timer = setInterval(nextSlide, 4500);
    }

    function stopAutoplay() {
      if (timer) clearInterval(timer);
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        nextSlide();
        startAutoplay();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        prevSlide();
        startAutoplay();
      });
    }

    dots.forEach((dot, idx) => {
      dot.addEventListener('click', () => {
        goToSlide(idx);
        startAutoplay();
      });
    });

    slider.addEventListener('mouseenter', stopAutoplay);
    slider.addEventListener('mouseleave', startAutoplay);

    startAutoplay();
  });
}

// ==========================================
// 8. DYNAMIC UI/UX CARD DESIGN SYSTEM
// ==========================================
function initDynamicCardUIUX() {
  // A. Ultra-Fluid 3D Tilt & Magnetic Physics + Cursor Spotlight for all cards
  const interactiveCards = document.querySelectorAll(
    '.project-card, .category-card, .locality-card, .localities-card, .dev-marquee-card, .process-card, .testi-card, .metric-card-box, .pricing-card, .faq-card, .calc-box-card, .service-card, .blog-card'
  );

  interactiveCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transition = 'transform 0.1s ease-out, box-shadow 0.25s ease, border-color 0.25s ease';
    });

    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);

      // Snappy 3D perspective rotation
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = ((y - centerY) / centerY) * -5.5;
      const rotateY = ((x - centerX) / centerX) * 5.5;
      card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-8px) scale3d(1.018, 1.018, 1.018)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease, border-color 0.3s ease';
      card.style.transform = '';
    });
  });

  // B. Interactive Bookmark Hearts
  document.querySelectorAll('.btn-bookmark-action').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      this.classList.toggle('bookmarked');
      const isSaved = this.classList.contains('bookmarked');
      this.innerHTML = isSaved ? '<i class="fa-solid fa-heart"></i>' : '<i class="fa-regular fa-heart"></i>';
      const title = this.closest('.project-card')?.querySelector('.project-title')?.textContent || 'Property';
      showToast(isSaved ? `<i class="fa-solid fa-star"></i> Saved "${title}" to your favorites!` : `Removed "${title}" from favorites.`);
    });
  });

  // C. Interactive Specs Accordion Toggle on Cards
  document.querySelectorAll('.card-expand-toggle').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      const card = this.closest('.project-card');
      const drawer = card ? card.querySelector('.card-expand-drawer') : null;
      if (drawer) {
        drawer.classList.toggle('open');
        this.innerHTML = drawer.classList.contains('open') 
          ? `<span><i class="fa-solid fa-chevron-up"></i> Hide Detailed Specs</span>` 
          : `<span><i class="fa-solid fa-chevron-down"></i> Quick Specs & Legal Breakdown</span>`;
      }
    });
  });

  // D. Interactive Comparison System & Floating Dock
  let comparedItems = [];
  const compareDock = document.getElementById('compareDock');
  const compareCount = document.getElementById('compareCount');
  const compareThumbs = document.getElementById('compareThumbs');
  const clearCompareBtn = document.getElementById('clearCompareBtn');

  document.querySelectorAll('.btn-compare-action').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      const card = this.closest('.project-card');
      if (!card) return;
      const title = card.querySelector('.project-title')?.textContent || 'Property';
      const img = card.querySelector('.project-img-box img')?.src || '';
      const price = card.querySelector('.project-price')?.textContent || '';

      const idx = comparedItems.findIndex(i => i.title === title);
      if (idx > -1) {
        comparedItems.splice(idx, 1);
        this.style.background = '';
        this.style.color = '#ffffff';
        showToast(`Removed "${title}" from comparison.`);
      } else {
        if (comparedItems.length >= 3) {
          showToast('<i class="fa-solid fa-triangle-exclamation"></i> You can compare up to 3 properties simultaneously.');
          return;
        }
        comparedItems.push({ title, img, price });
        this.style.background = '#06b6d4';
        this.style.color = '#16042b';
        showToast(`Added "${title}" to live comparison dock.`);
      }
      renderCompareDock();
    });
  });

  function renderCompareDock() {
    if (!compareDock) return;
    if (comparedItems.length > 0) {
      compareDock.classList.add('visible');
      if (compareCount) compareCount.textContent = `(${comparedItems.length}/3)`;
      if (compareThumbs) {
        compareThumbs.innerHTML = comparedItems.map(item => `
          <div class="compare-thumb-item" title="${item.title}">
            <img src="${item.img}" alt="${item.title}">
          </div>
        `).join('');
      }
    } else {
      compareDock.classList.remove('visible');
    }
  }

  if (clearCompareBtn) {
    clearCompareBtn.addEventListener('click', () => {
      comparedItems = [];
      document.querySelectorAll('.btn-compare-action').forEach(b => {
        b.style.background = '';
        b.style.color = '#ffffff';
      });
      renderCompareDock();
      showToast('Cleared all compared properties.');
    });
  }

  // F. Interactive Inventory Filter Pills
  const filterPills = document.querySelectorAll('.uiux-pill-btn');
  const projectCards = document.querySelectorAll('.projects-grid .project-card');
  filterPills.forEach(pill => {
    pill.addEventListener('click', function() {
      filterPills.forEach(p => p.classList.remove('active'));
      this.classList.add('active');
      const cat = this.getAttribute('data-cat') || 'all';

      projectCards.forEach(card => {
        const cardCat = card.getAttribute('data-category') || 'all';
        if (cat === 'all' || cardCat === cat) {
          card.style.display = 'flex';
          card.style.animation = 'fadeInUp 0.35s ease';
        } else {
          card.style.display = 'none';
        }
      });
      showToast(`Filter applied: Showing ${this.textContent.trim()}`);
    });
  });

  // G. Dynamic Layout Mode Switcher (Grid, Bento, List)
  const modeBtns = document.querySelectorAll('.uiux-mode-btn');
  const projectsGrid = document.querySelector('.projects-grid');
  modeBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      modeBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const mode = this.getAttribute('data-mode');
      if (projectsGrid) {
        projectsGrid.classList.remove('layout-bento', 'layout-list');
        if (mode === 'bento') projectsGrid.classList.add('layout-bento');
        if (mode === 'list') projectsGrid.classList.add('layout-list');
      }
      showToast(`Layout switched to: ${this.textContent.trim()} UI`);
    });
  });

  // H. Category Cards Click & Category CTA Pill Handlers
  document.querySelectorAll('.category-cta-pill').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      window.location.href = '404.html';
    });
  });

  document.querySelectorAll('.category-card').forEach(card => {
    card.addEventListener('click', function(e) {
      if (e.target.closest('.category-cta-pill')) {
        e.preventDefault();
        e.stopPropagation();
        window.location.href = '404.html';
        return;
      }
      const catTitle = this.querySelector('.category-title')?.textContent.toLowerCase() || '';
      const projectSec = document.getElementById('sec-projects');
      if (projectSec) projectSec.scrollIntoView({ behavior: 'smooth' });

      // Match corresponding filter pill if exists
      filterPills.forEach(pill => {
        const pillCat = pill.getAttribute('data-cat');
        if (catTitle.includes('villa') && pillCat === 'villas') pill.click();
        else if (catTitle.includes('apartment') && pillCat === 'apartments') pill.click();
        else if (catTitle.includes('commercial') && pillCat === 'commercial') pill.click();
        else if (catTitle.includes('plot') && pillCat === 'plots') pill.click();
      });
    });
  });
}

// ==========================================
// 10. SCROLLING ANIMATIONS & PROGRESS TRACKER
// ==========================================
function initPageScrollAnimations() {
  // A. Top Scroll Progress Bar
  let progressBar = document.getElementById('scrollProgressBar');
  if (!progressBar) {
    progressBar = document.createElement('div');
    progressBar.id = 'scrollProgressBar';
    document.body.appendChild(progressBar);
  }

  // B. Floating Back-to-Top Button
  let bttBtn = document.getElementById('backToTopBtn');
  if (!bttBtn) {
    bttBtn = document.createElement('button');
    bttBtn.id = 'backToTopBtn';
    bttBtn.setAttribute('aria-label', 'Back to top');
    bttBtn.setAttribute('title', 'Back to top');
    bttBtn.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';
    document.body.appendChild(bttBtn);
  }

  bttBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // C. Scroll Event Listener (Throttled via requestAnimationFrame)
  const mainHeader = document.querySelector('.top-header');
  let ticking = false;

  function onScroll() {
    const scrollY = window.scrollY || document.documentElement.scrollTop;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const progress = maxScroll > 0 ? (scrollY / maxScroll) * 100 : 0;

    if (progressBar) {
      progressBar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
    }

    if (bttBtn) {
      if (scrollY > 350) {
        bttBtn.classList.add('visible');
      } else {
        bttBtn.classList.remove('visible');
      }
    }

    if (mainHeader) {
      if (scrollY > 40) {
        mainHeader.classList.add('header-scrolled');
      } else {
        mainHeader.classList.remove('header-scrolled');
      }
    }

    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(onScroll);
      ticking = true;
    }
  }, { passive: true });

  // Run on mount
  onScroll();

  // D. Comprehensive IntersectionObserver for Scroll Reveal across EVERY Section
  const revealTargets = document.querySelectorAll(
    'section, .section-header-block, .featured-card, .category-card, .localities-card, .stat-card, .price-card, .testi-card, .dev-pill, .faq-card, .pricing-card, .salem-map-wrapper, .vip-lead-box, .service-hero, .lead-capture-card, .project-card, .developer-card, .process-card, .market-intel-container, .calc-box-card, .dev-marquee-card, .dash-section-block, .dash-sec-head, .metric-card-box, .dash-table tbody tr, .hero-slider-wrap, .hero-content-wrap'
  );

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          
          // Animate numbers inside if present (stats, metrics, roi, counters)
          entry.target.querySelectorAll('.stat-number, .count-target, .metric-number').forEach(numEl => {
            if (!numEl.dataset.animated) {
              numEl.dataset.animated = 'true';
              animateCounter(numEl);
            }
          });

          obs.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.08,
      rootMargin: '0px 0px -30px 0px'
    });

    revealTargets.forEach(el => {
      // Add base reveal class if not already present
      if (!el.classList.contains('reveal') && !el.classList.contains('reveal-left') && !el.classList.contains('reveal-right') && !el.classList.contains('reveal-scale')) {
        el.classList.add('reveal');
      }

      // Add staggered delay to grid items and table rows
      const parentGrid = el.closest('.projects-grid, .categories-grid, .localities-grid, .stats-row, .testimonials-grid, .pricing-grid, .process-grid, .dash-metrics-grid, tbody');
      if (parentGrid) {
        const siblings = Array.from(parentGrid.children);
        const indexInParent = siblings.indexOf(el);
        if (indexInParent >= 0) {
          const delayClass = `delay-${(indexInParent % 6) + 1}`;
          el.classList.add(delayClass);
        }
      }

      observer.observe(el);
    });
  } else {
    // Fallback for older browsers
    revealTargets.forEach(el => el.classList.add('revealed'));
  }

  // E. Counter Animation Helper
  function animateCounter(el) {
    const text = el.textContent.trim();
    const match = text.match(/([\d,\.]+)/);
    if (!match) return;

    const rawNum = parseFloat(match[1].replace(/,/g, ''));
    if (isNaN(rawNum)) return;

    const prefix = text.slice(0, match.index);
    const suffix = text.slice(match.index + match[0].length);
    const duration = 1400;
    const startTime = performance.now();

    function updateCounter(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      const currentVal = rawNum * easeProgress;

      let formatted = currentVal >= 1000 ? Math.round(currentVal).toLocaleString() : currentVal.toFixed(rawNum % 1 !== 0 ? 1 : 0);
      el.textContent = `${prefix}${formatted}${suffix}`;

      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      } else {
        el.textContent = text;
      }
    }

    requestAnimationFrame(updateCounter);
  }
}




// ========================================================
// STACKLY USER SESSION & DASHBOARD USER SYNC
// ========================================================
(function syncStacklyUser() {
  function applyUser() {
    const raw = localStorage.getItem('stackly_user_email') || 'manu@gmail.com';
    let username = raw;
    if (raw.includes('@')) {
      const part = raw.split('@')[0];
      username = part.charAt(0).toUpperCase() + part.slice(1);
    }
    const initials = (username.length >= 2 ? username.slice(0, 2) : username).toUpperCase();

    document.querySelectorAll('.current-user-email, .user-email-line').forEach(el => {
      el.textContent = raw;
    });
    document.querySelectorAll('.current-user-name, .user-name-line').forEach(el => {
      el.textContent = username;
    });
    document.querySelectorAll('.current-user-initials, .avatar-initials').forEach(el => {
      el.textContent = initials;
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyUser);
  } else {
    applyUser();
  }
})();

// Dynamic Table Responsive Mobile Label Fallback
(function initTableMobileLabels() {
  function applyLabels() {
    document.querySelectorAll('.dash-table').forEach(table => {
      const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
      table.querySelectorAll('tbody tr').forEach(row => {
        Array.from(row.children).forEach((cell, idx) => {
          if (headers[idx] && !cell.getAttribute('data-label')) {
            cell.setAttribute('data-label', headers[idx]);
          }
        });
      });
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyLabels);
  } else {
    applyLabels();
  }
})();
