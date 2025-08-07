import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF
import io
import base64
import re
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Glanzwerk Rheinland - Invoice System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .service-card {
        background: #f0fdf4;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin: 0.5rem 0;
    }
    .invoice-preview {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }
    .total-amount {
        background: #10b981;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .discount-badge {
        background: #dcfce7;
        color: #166534;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

class GlanzwerkInvoicePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        # Company header
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'GLANZWERK RHEINLAND', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Grün gedacht, sauber gemacht', 0, 1, 'C')
        self.cell(0, 5, 'Krasnaer Str. 1, 56566 Neuwied, Deutschland', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-40)
        self.set_font('Arial', '', 9)
        
        # Contact information
        self.cell(60, 4, 'Glanzwerk Rheinland', 0, 0, 'L')
        self.cell(70, 4, 'Glanzwerk.Rheinland@gmail.com', 0, 0, 'L')
        self.cell(60, 4, 'Bankverbindung:', 0, 1, 'L')
        
        self.cell(60, 4, 'Krasnaer Str. 1', 0, 0, 'L')
        self.cell(70, 4, '+49 171 1858241', 0, 0, 'L')
        self.cell(60, 4, 'Bank: Sparkasse Neuwied', 0, 1, 'L')
        
        self.cell(60, 4, '56566 Neuwied', 0, 0, 'L')
        self.cell(70, 4, 'Instagram: @glanzwerk_rheinland', 0, 0, 'L')
        self.cell(60, 4, 'IBAN: DE89 5745 0120 0000 1234 56', 0, 1, 'L')

def parse_additional_services(text):
    """Parse additional services from text format"""
    if not text or not text.strip():
        return []
    
    services = []
    for line in text.strip().split('\n'):
        match = re.match(r'^(.+?):\s*(\d+(?:\.\d{1,2})?)€?$', line.strip(), re.IGNORECASE)
        if match:
            services.append({
                'description': match.group(1).strip(),
                'price': float(match.group(2))
            })
    
    return services

def generate_pdf(invoice_data):
    """Generate PDF invoice"""
    pdf = GlanzwerkInvoicePDF()
    pdf.add_page()
    
    # Invoice header
    current_date = datetime.now()
    due_date = current_date + timedelta(days=14)
    invoice_number = f"2025-{current_date.strftime('%m%d%H%M')}"
    
    pdf.set_xy(120, 35)
    pdf.set_font('Arial', '', 11)
    pdf.cell(70, 6, f'Rechnungsnummer: {invoice_number}', 0, 1, 'L')
    pdf.set_x(120)
    pdf.cell(70, 6, f'Rechnungsdatum: {current_date.strftime("%d.%m.%Y")}', 0, 1, 'L')
    pdf.set_x(120)
    pdf.cell(70, 6, f'Fälligkeitsdatum: {due_date.strftime("%d.%m.%Y")}', 0, 1, 'L')
    
    # Customer information
    pdf.set_xy(10, 70)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'RECHNUNG', 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 6, 'Sehr geehrte Damen und Herren,', 0, 1, 'L')
    pdf.ln(3)
    pdf.cell(0, 6, 'vielen Dank für Ihre Inanspruchnahme unserer Dienstleistungen.', 0, 1, 'L')
    pdf.ln(8)
    
    pdf.cell(0, 6, f'Kunde: {invoice_data["customer_name"]}', 0, 1, 'L')
    pdf.cell(0, 6, f'Fahrzeug: {invoice_data["vehicle_number"]}', 0, 1, 'L')
    pdf.ln(8)
    
    # Service table
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(80, 8, 'Beschreibung', 1, 0, 'L')
    pdf.cell(25, 8, 'Anzahl', 1, 0, 'C')
    pdf.cell(25, 8, 'Einzelpreis', 1, 0, 'R')
    pdf.cell(25, 8, 'MwSt.', 1, 0, 'R')
    pdf.cell(25, 8, 'Gesamt', 1, 1, 'R')
    
    # Main service
    pdf.set_font('Arial', '', 10)
    service_net = invoice_data['service_price']
    service_tax = service_net * 0.19
    service_gross = service_net + service_tax
    
    pdf.cell(80, 8, invoice_data['service_name'], 1, 0, 'L')
    pdf.cell(25, 8, '1', 1, 0, 'C')
    pdf.cell(25, 8, f"{service_net:.2f}EUR", 1, 0, 'R')
    pdf.cell(25, 8, f"{service_tax:.2f}EUR", 1, 0, 'R')
    pdf.cell(25, 8, f"{service_gross:.2f}EUR", 1, 1, 'R')
    
    # Additional services
    for additional in invoice_data['additional_services']:
        add_net = additional['price']
        add_tax = add_net * 0.19
        add_gross = add_net + add_tax
        
        pdf.cell(80, 8, additional['description'], 1, 0, 'L')
        pdf.cell(25, 8, '1', 1, 0, 'C')
        pdf.cell(25, 8, f"{add_net:.2f}EUR", 1, 0, 'R')
        pdf.cell(25, 8, f"{add_tax:.2f}EUR", 1, 0, 'R')
        pdf.cell(25, 8, f"{add_gross:.2f}EUR", 1, 1, 'R')
    
    # Totals
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(155, 8, 'Zwischensumme inkl. MwSt.', 1, 0, 'R')
    pdf.cell(25, 8, f"{invoice_data['gross_price']:.2f}EUR", 1, 1, 'R')
    
    if invoice_data['total_discount_percent'] > 0:
        pdf.set_font('Arial', '', 10)
        pdf.cell(155, 8, f"Gesamtrabatt ({invoice_data['total_discount_percent']}%)", 1, 0, 'L')
        pdf.cell(25, 8, f"-{invoice_data['discount_amount']:.2f}EUR", 1, 1, 'R')
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(155, 10, 'Gesamt inkl. MwSt.', 1, 0, 'R')
    pdf.cell(25, 10, f"{invoice_data['total_price']:.2f}EUR", 1, 1, 'R')
    
    pdf.ln(8)
    
    # Payment information
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f'Bitte überweisen Sie den Betrag bis spätestens {due_date.strftime("%d.%m.%Y")}', 0, 1, 'L')
    pdf.ln(5)
    pdf.cell(0, 6, 'Mit freundlichen Grüßen,', 0, 1, 'L')
    pdf.cell(0, 6, 'Glanzwerk Rheinland', 0, 1, 'L')
    
    return pdf.output(dest='S').encode('latin1')

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚗 Glanzwerk Rheinland</h1>
        <h3>Professional Invoice System - نظام الفواتير الاحترافي</h3>
        <p>Krasnaer Str. 1, 56566 Neuwied, Deutschland</p>
        <p><em>Grün gedacht, sauber gemacht</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Services data
    services = {
        'aussenreinigung': {'name': 'Außenreinigung per Hand', 'price': 50, 'description': 'Professionelle Handwäsche außen'},
        'felgenreinigung': {'name': 'Felgenreinigung & Flugrostentfernung', 'price': 30, 'description': 'Intensive Felgenpflege'},
        'innenraumreinigung': {'name': 'Innenraumreinigung', 'price': 70, 'description': 'Komplette Innenraumreinigung'},
        'lederreinigung': {'name': 'Lederreinigung & -pflege', 'price': 60, 'description': 'Professionelle Lederpflege'},
        'lederreparatur': {'name': 'Lederreparatur', 'price': 100, 'description': 'Reparatur von Lederschäden'},
        'polsterreinigung': {'name': 'Polster- & Teppichreinigung', 'price': 80, 'description': 'Tiefenreinigung der Polster'},
        'scheibenreinigung': {'name': 'Scheibenreinigung innen & außen', 'price': 20, 'description': 'Kristallklare Scheiben'},
        'lackpolitur': {'name': 'Lackpolitur & Glanzversiegelung', 'price': 150, 'description': 'Hochglanzpolitur mit Versiegelung'},
        'nanokeramik': {'name': 'Nano-Keramik-Versiegelung', 'price': 300, 'description': 'Premium Keramikversiegelung'},
        'motorraumreinigung': {'name': 'Motorraumreinigung', 'price': 40, 'description': 'Professionelle Motorraumreinigung'},
        'geruchsneutralisierung': {'name': 'Geruchsneutralisierung & Ozonbehandlung', 'price': 50, 'description': 'Ozonbehandlung gegen Gerüche'},
        'tierhaarentfernung': {'name': 'Tierhaarentfernung', 'price': 40, 'description': 'Spezielle Tierhaarentfernung'},
        'hagelschaden': {'name': 'Hagelschaden- und Dellenentfernung', 'price': 200, 'description': 'Professionelle Dellenreparatur'},
        'folierung': {'name': 'Auto Folierung', 'price': 500, 'description': 'Komplette Fahrzeugfolierung'},
        'abholservice': {'name': 'Abhol- und Bringservice', 'price': 25, 'description': 'Bequemer Hol- und Bringservice'}
    }
    
    discount_codes = {
        'NEUKUNDE': 15,
        'STAMMKUNDE': 10,
        'WINTER2025': 20,
        'SOMMER2025': 12
    }
    
    # Layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Neue Rechnung erstellen")
        
        # Customer Information
        st.subheader("👤 Kundendaten")
        customer_name = st.text_input("Kundenname", placeholder="Kundenname eingeben")
        vehicle_number = st.text_input("Fahrzeugkennzeichen", placeholder="Kennzeichen eingeben")
        
        # Service Selection
        st.subheader("🚗 Hauptdienstleistung")
        service_options = [f"{service['name']} - {service['price']}€" for service in services.values()]
        service_names = list(services.keys())
        
        selected_service_index = st.selectbox(
            "Dienstleistung auswählen",
            range(len(service_options)),
            format_func=lambda x: service_options[x],
            index=None,
            placeholder="Dienstleistung wählen"
        )
        
        if selected_service_index is not None:
            selected_service_key = service_names[selected_service_index]
            selected_service = services[selected_service_key]
            st.info(f"📝 {selected_service['description']}")
        
        # Additional Services
        st.subheader("📄 Zusätzliche Dienstleistungen")
        additional_services_text = st.text_area(
            "Zusatzleistungen (Format: 'Beschreibung: Preis')",
            placeholder="Beispiel:\nSpezialreinigung: 25€\nWachsbehandlung: 40€",
            height=100
        )
        
        # Discounts
        st.subheader("💰 Rabatte")
        is_regular_customer = st.checkbox("Stammkunde (10% Rabatt)")
        discount_code = st.text_input("Rabattcode", placeholder="z.B. NEUKUNDE, STAMMKUNDE")
        manual_discount = st.number_input("Manueller Rabatt (%)", min_value=0.0, max_value=100.0, step=0.1)
        
        # Calculate button
        if st.button("🧮 Rechnung berechnen", type="primary", use_container_width=True):
            if customer_name and vehicle_number and selected_service_index is not None:
                # Store calculation in session state
                st.session_state.invoice_calculated = True
                st.session_state.customer_name = customer_name
                st.session_state.vehicle_number = vehicle_number
                st.session_state.selected_service = selected_service
                st.session_state.additional_services_text = additional_services_text
                st.session_state.is_regular_customer = is_regular_customer
                st.session_state.discount_code = discount_code
                st.session_state.manual_discount = manual_discount
            else:
                st.error("Bitte füllen Sie alle Pflichtfelder aus!")
    
    with col2:
        st.header("📄 Rechnungsvorschau")
        
        if hasattr(st.session_state, 'invoice_calculated') and st.session_state.invoice_calculated:
            # Calculate invoice
            service = st.session_state.selected_service
            additional_services = parse_additional_services(st.session_state.additional_services_text)
            
            # Calculate prices
            service_price = service['price']
            additional_total = sum(item['price'] for item in additional_services)
            net_price = service_price + additional_total
            
            tax_rate = 0.19
            tax_amount = net_price * tax_rate
            gross_price = net_price + tax_amount
            
            # Calculate discounts
            total_discount_percent = 0
            discount_sources = []
            
            if st.session_state.is_regular_customer:
                total_discount_percent += 10
                discount_sources.append('Stammkundenrabatt (10%)')
            
            if st.session_state.discount_code.upper() in discount_codes:
                code_discount = discount_codes[st.session_state.discount_code.upper()]
                total_discount_percent += code_discount
                discount_sources.append(f'Code {st.session_state.discount_code.upper()} ({code_discount}%)')
            
            if st.session_state.manual_discount > 0:
                total_discount_percent += st.session_state.manual_discount
                discount_sources.append(f'Manueller Rabatt ({st.session_state.manual_discount}%)')
            
            discount_amount = gross_price * (total_discount_percent / 100)
            total_price = gross_price - discount_amount
            
            # Invoice preview
            st.markdown('<div class="invoice-preview">', unsafe_allow_html=True)
            
            # Header
            st.markdown("### 📋 RECHNUNG")
            current_date = datetime.now()
            due_date = current_date + timedelta(days=14)
            invoice_number = f"2025-{current_date.strftime('%m%d%H%M')}"
            
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.write(f"**Rechnungsnummer:** {invoice_number}")
                st.write(f"**Kunde:** {st.session_state.customer_name}")
            with col_info2:
                st.write(f"**Datum:** {current_date.strftime('%d.%m.%Y')}")
                st.write(f"**Fahrzeug:** {st.session_state.vehicle_number}")
            
            st.divider()
            
            # Service table
            invoice_data = []
            invoice_data.append({
                'Beschreibung': service['name'],
                'Preis': f"{service_price:.2f}€"
            })
            
            for additional in additional_services:
                invoice_data.append({
                    'Beschreibung': additional['description'],
                    'Preis': f"{additional['price']:.2f}€"
                })
            
            invoice_data.append({
                'Beschreibung': 'MwSt. (19%)',
                'Preis': f"{tax_amount:.2f}€"
            })
            
            invoice_data.append({
                'Beschreibung': '**Zwischensumme**',
                'Preis': f"**{gross_price:.2f}€**"
            })
            
            if total_discount_percent > 0:
                invoice_data.append({
                    'Beschreibung': f'🎯 Gesamtrabatt ({total_discount_percent}%)',
                    'Preis': f"-{discount_amount:.2f}€"
                })
            
            df = pd.DataFrame(invoice_data)
            st.table(df)
            
            # Total
            st.markdown(f'<div class="total-amount">Gesamt inkl. MwSt.: {total_price:.2f}€</div>', unsafe_allow_html=True)
            
            # Discount badges
            if discount_sources:
                st.markdown("**Angewandte Rabatte:**")
                for source in discount_sources:
                    st.markdown(f'<span class="discount-badge">{source}</span>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # PDF Generation
            if st.button("📥 PDF-Rechnung herunterladen", type="secondary", use_container_width=True):
                invoice_data_pdf = {
                    'customer_name': st.session_state.customer_name,
                    'vehicle_number': st.session_state.vehicle_number,
                    'service_name': service['name'],
                    'service_price': service_price,
                    'additional_services': additional_services,
                    'net_price': net_price,
                    'tax_amount': tax_amount,
                    'gross_price': gross_price,
                    'total_discount_percent': total_discount_percent,
                    'discount_sources': discount_sources,
                    'discount_amount': discount_amount,
                    'total_price': total_price
                }
                
                pdf_bytes = generate_pdf(invoice_data_pdf)
                
                st.download_button(
                    label="📄 PDF herunterladen",
                    data=pdf_bytes,
                    file_name=f"Rechnung_{st.session_state.customer_name.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.info("📝 Füllen Sie das Formular aus, um eine Rechnungsvorschau zu sehen")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.875rem;">
        <p>© 2025 Glanzwerk Rheinland - Professional Car Wash Services</p>
        <p>📞 +49 171 1858241 | 📧 Glanzwerk.Rheinland@gmail.com | 📍 Krasnaer Str. 1, 56566 Neuwied</p>
        <p style="color: #10b981; font-weight: 500;">Grün gedacht, sauber gemacht</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

