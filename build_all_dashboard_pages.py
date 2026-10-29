import os

workspace = r'c:\Users\manu1\OneDrive\Desktop\Real Estate Consultancy'

# Common SVG logo mark
logo_svg_user = '''<svg class="stackly-logo-mark" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M58 8L20 54H48L42 92L80 46H52L58 8Z" fill="url(#goldGradDashU)" stroke="#d97706" stroke-width="2"/>
            <defs>
              <linearGradient id="goldGradDashU" x1="20" y1="8" x2="80" y2="92" gradientUnits="userSpaceOnUse">
                <stop stop-color="#FBBF24"/>
                <stop offset="1" stop-color="#F59E0B"/>
              </linearGradient>
            </defs>
          </svg>'''

logo_svg_admin = '''<svg class="stackly-logo-mark" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M58 8L20 54H48L42 92L80 46H52L58 8Z" fill="url(#goldGradDashA)" stroke="#d97706" stroke-width="2"/>
            <defs>
              <linearGradient id="goldGradDashA" x1="20" y1="8" x2="80" y2="92" gradientUnits="userSpaceOnUse">
                <stop stop-color="#FBBF24"/>
                <stop offset="1" stop-color="#F59E0B"/>
              </linearGradient>
            </defs>
          </svg>'''

# 7 User Pages Config
user_pages = [
    {
        'file': 'user-dashboard.html',
        'id': 'overview',
        'title': 'My Property Dashboard',
        'icon': 'fa-house',
        'sub': 'Your personal real estate portfolio summary, active advisory consultations, and acquisition deals at a glance.'
    },
    {
        'file': 'user-telemetry.html',
        'id': 'telemetry',
        'title': 'Portfolio & Yield Telemetry',
        'icon': 'fa-arrow-trend-up',
        'sub': 'Live equity benchmarks, rental yield performance, and macro micro-market price appreciation telemetry.'
    },
    {
        'file': 'user-consultations.html',
        'id': 'consultations',
        'title': 'Advisory Consultations',
        'icon': 'fa-calendar-days',
        'sub': 'Scheduled senior partner strategy sessions, legal consultations with Dr. Shilpi Singh, and meeting minutes.'
    },
    {
        'file': 'user-reports.html',
        'id': 'reports',
        'title': 'Title Audits & RERA Reports',
        'icon': 'fa-file-contract',
        'sub': 'Government RERA registration certificates, 40-year parent deed legal searches, and drone structural audits.'
    },
    {
        'file': 'user-pipeline.html',
        'id': 'pipeline',
        'title': 'Acquisition Pipeline',
        'icon': 'fa-map-location-dot',
        'sub': 'Exclusive off-market builder mandates, letter of intent negotiations, and comparative IRR exit projections.'
    },
    {
        'file': 'user-escrow.html',
        'id': 'escrow',
        'title': 'Escrow & Payment Schedules',
        'icon': 'fa-briefcase',
        'sub': 'Tri-party RERA escrow account ledger, construction-linked milestone tranches, and bank disbursals.'
    },
    {
        'file': 'user-vault.html',
        'id': 'vault',
        'title': 'Mortgage & Document Vault',
        'icon': 'fa-credit-card',
        'sub': '256-Bit SSL encrypted digital repository for sale deeds, patta/chitta records, and home loan facilities.'
    }
]

# 7 Admin Pages Config
admin_pages = [
    {
        'file': 'admin-dashboard.html',
        'id': 'overview',
        'title': 'Executive Overview',
        'icon': 'fa-chart-column',
        'sub': 'Macro real estate advisory KPIs, active client deal flow, and High Court title approval velocity.'
    },
    {
        'file': 'admin-leads.html',
        'id': 'leads',
        'title': 'Lead & Token Queue',
        'icon': 'fa-ticket',
        'sub': 'Real-time investor consultation queue, VIP site visit requests, and advisor SLA response tracking.'
    },
    {
        'file': 'admin-inventory.html',
        'id': 'inventory',
        'title': 'Inventory & Roster',
        'icon': 'fa-building',
        'sub': '1,420+ RERA-vetted institutional units across Godrej, Prestige, Casagrand, Sobha, and Puravankara.'
    },
    {
        'file': 'admin-occupancy.html',
        'id': 'occupancy',
        'title': 'Occupancy & Wards',
        'icon': 'fa-arrow-trend-up',
        'sub': 'Commercial IT park tenant leases, residential tenancy agreements, and rental yield performance.'
    },
    {
        'file': 'admin-telemetry.html',
        'id': 'telemetry',
        'title': 'Risk Telemetry',
        'icon': 'fa-brain',
        'sub': 'Predictive developer default risk models, infrastructure corridor valuation forecasts, and RERA compliance.'
    },
    {
        'file': 'admin-legal.html',
        'id': 'legal',
        'title': 'Diagnostic & Title Lab',
        'icon': 'fa-file-contract',
        'sub': 'High Court 120-point legal audit processing, encumbrance certificate verification, and advocate attestation.'
    },
    {
        'file': 'admin-revenue.html',
        'id': 'revenue',
        'title': 'Revenue & TPA Claims',
        'icon': 'fa-credit-card',
        'sub': 'Quarterly gross advisory revenue, direct developer mandate payouts, and client escrow ledger analytics.'
    }
]

print("Script base ready.")
