# Real Estate Consultancy – Stackly PropTech Intelligence Platform

> Premier strategic real estate consultancy & PropTech intelligence platform empowering investors, home buyers, and developers with actionable telemetry and sustainable scale.

---

### 🌐 Live Deployment
- **Live Website**: [https://lingalamanasa.github.io/Real-Estate-Consultany/](https://lingalamanasa.github.io/Real-Estate-Consultany/)
- **Repository**: [https://github.com/lingalamanasa/Real-Estate-Consultany](https://github.com/lingalamanasa/Real-Estate-Consultany)

---

### 📱 Responsive Design & UI/UX Features
- **Mobile First & Multi-Device Testing**: Fully responsive across Mobile (320px, 360px, 375px, 390px, 414px, 430px), Tablet (768px, 1024px), Laptop (1280px, 1366px, 1440px), and Desktop (1600px, 1920px+).
- **Springboard Mobile Menu Navigation**:
  - Clean hamburger menu with 180° animated morph into close 'X' icon.
  - Backdrop blur overlay with background scroll lock.
  - Sequential spring entrance animations (`cubic-bezier(0.175, 0.885, 0.32, 1.275)`) with staggered delay for menu items.
  - Automatic close upon link navigation, backdrop click, or Escape key.
- **Wobble Card Entrance Animations**:
  - Intersection Observer scroll-triggered physics entrance across all property cards, service cards, why choose us pillars, consultant headshots, and testimonial grids.
  - Smooth spring easing without layout shifts.
  - Accessibility compliant with `prefers-reduced-motion: reduce`.
- **Horizontal Scroll Protection & Responsive Tables**:
  - Viewport-locked overflow shield (`overflow-x: hidden !important;`) preventing horizontal window shifting.
  - All 27 dashboard tables wrapped in dedicated `.dash-table-wrap` containers with custom touch momentum scrolling.
- **Interactive Financial Tools**:
  - Real estate mortgage & ROI visual calculators with live sliders and dynamic repayment breakdowns.

---

### 📂 Website Structure
- `index.html` - Homepage with hero telemetry slider, instant property search filters, category cards, featured property listings, mortgage & ROI calculators, and 1-on-1 consultation onboarding.
- `about.html` - Brand vision, RICS-accredited leadership team, benchmark comparisons, and corporate governance.
- `services.html` - High-yield commercial acquisitions, title forensic audits, NRI cross-border desk, and VIP advisory chambers.
- `blog.html` - RERA legal updates, 2026 Tamil Nadu master plan corridors, and market intelligence whitepapers.
- `contact.html` - Salem headquarters contact desk, priority callback form, and interactive FAQ accordions.
- `admin-dashboard.html` & sub-dashboards - Executive Cockpit with live telemetry, token queues, and forensic risk grades.
- `user-dashboard.html` & sub-dashboards - Investor property portfolio dashboard, active consultations, milestone tracking, and vault access.
- `login.html` & `signup.html` - Role-based investor/admin authentication with dynamic session synchronization.
- `404.html` - Interactive error page with animated canvas and preserved return routes.
