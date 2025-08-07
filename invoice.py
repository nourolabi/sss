from flask import Blueprint, request, jsonify, send_file
from fpdf import FPDF
import os
import tempfile
from datetime import datetime, timedelta
import io
import re

invoice_bp = Blueprint('invoice', __name__)

class GlanzwerkInvoicePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        # Add logo
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'glanzwerk_logo.png')
        if os.path.exists(logo_path):
            self.image(logo_path, x=10, y=8, w=25)
        
        # Company header line
        self.set_font('Arial', '', 10)
        self.set_xy(45, 15)
        self.cell(0, 5, 'Glanzwerk Rheinland, Krasnaer Str. 1, 56566 Neuwied, Deutschland', 0, 1, 'L')
        self.ln(10)
        
    def footer(self):
        self.set_y(-40)
        
        # Footer with company details
        self.set_font('Arial', '', 9)
        
        # Left column
        self.cell(60, 4, 'Glanzwerk Rheinland', 0, 0, 'L')
        self.cell(70, 4, 'Glanzwerk.Rheinland@gmail.com', 0, 0, 'L')
        self.cell(60, 4, 'Bankverbindung:', 0, 1, 'L')
        
        self.cell(60, 4, 'Krasnaer Str. 1', 0, 0, 'L')
        self.cell(70, 4, '+49 171 1858241', 0, 0, 'L')
        self.cell(60, 4, 'Bank: Sparkasse Neuwied', 0, 1, 'L')
        
        self.cell(60, 4, '56566 Neuwied', 0, 0, 'L')
        self.cell(70, 4, 'Instagram: @glanzwerk_rheinland', 0, 0, 'L')
        self.cell(60, 4, 'IBAN: DE89 5745 0120 0000 1234 56', 0, 1, 'L')
        
        self.cell(60, 4, 'Deutschland', 0, 0, 'L')
        self.cell(70, 4, 'Grün gedacht, sauber gemacht', 0, 0, 'L')
        self.cell(60, 4, 'BIC: MALADE51NWD', 0, 1, 'L')
        
    def customer_address(self, customer_name, vehicle_number):
        # Customer address section
        self.set_font('Arial', '', 11)
        self.cell(0, 6, customer_name, 0, 1, 'L')
        self.cell(0, 6, f'Fahrzeug: {vehicle_number}', 0, 1, 'L')
        self.ln(5)
        
    def invoice_header(self, invoice_number):
        # Invoice details in right column
        current_date = datetime.now()
        due_date = current_date + timedelta(days=14)
        
        # Position for right-aligned content
        self.set_xy(120, 35)
        self.set_font('Arial', '', 11)
        
        self.cell(70, 6, f'Rechnungsnummer: {invoice_number}', 0, 1, 'L')
        self.set_x(120)
        self.cell(70, 6, f'Rechnungsdatum: {current_date.strftime("%d.%m.%Y")}', 0, 1, 'L')
        self.set_x(120)
        self.cell(70, 6, f'Fälligkeitsdatum: {due_date.strftime("%d.%m.%Y")}', 0, 1, 'L')
        
        # Reset position for main content
        self.set_xy(10, 70)
        
    def invoice_title(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'RECHNUNG', 0, 1, 'L')
        self.ln(5)
        
    def greeting_text(self):
        self.set_font('Arial', '', 11)
        self.cell(0, 6, 'Sehr geehrte Damen und Herren,', 0, 1, 'L')
        self.ln(3)
        self.cell(0, 6, 'vielen Dank für Ihre Inanspruchnahme unserer Dienstleistungen bei Glanzwerk Rheinland.', 0, 1, 'L')
        self.cell(0, 6, 'Nachfolgend finden Sie die Details Ihrer Rechnung:', 0, 1, 'L')
        self.ln(8)
        
    def service_table(self, invoice_data):
        # Table header
        self.set_font('Arial', 'B', 11)
        self.cell(80, 8, 'Beschreibung', 1, 0, 'L')
        self.cell(25, 8, 'Anzahl', 1, 0, 'C')
        self.cell(25, 8, 'Einzelpreis', 1, 0, 'R')
        self.cell(25, 8, 'MwSt.', 1, 0, 'R')
        self.cell(25, 8, 'Gesamt', 1, 1, 'R')
        
        # Main service row
        self.set_font('Arial', '', 10)
        service_description = invoice_data['service_name']
        service_net = invoice_data['service_price']
        service_tax = service_net * 0.19
        service_gross = service_net + service_tax
        
        self.cell(80, 8, service_description, 1, 0, 'L')
        self.cell(25, 8, '1', 1, 0, 'C')
        self.cell(25, 8, f"{service_net:.2f}EUR", 1, 0, 'R')
        self.cell(25, 8, f"{service_tax:.2f}EUR", 1, 0, 'R')
        self.cell(25, 8, f"{service_gross:.2f}EUR", 1, 1, 'R')
        
        # Additional services
        for additional in invoice_data['additional_services']:
            add_net = additional['price']
            add_tax = add_net * 0.19
            add_gross = add_net + add_tax
            
            self.cell(80, 8, additional['description'], 1, 0, 'L')
            self.cell(25, 8, '1', 1, 0, 'C')
            self.cell(25, 8, f"{add_net:.2f}EUR", 1, 0, 'R')
            self.cell(25, 8, f"{add_tax:.2f}EUR", 1, 0, 'R')
            self.cell(25, 8, f"{add_gross:.2f}EUR", 1, 1, 'R')
        
        # Subtotal
        self.set_font('Arial', 'B', 10)
        self.cell(155, 8, 'Zwischensumme inkl. MwSt.', 1, 0, 'R')
        self.cell(25, 8, f"{invoice_data['gross_price']:.2f}EUR", 1, 1, 'R')
        
        # Discount rows if applicable
        if invoice_data['total_discount_percent'] > 0:
            for discount_source in invoice_data['discount_sources']:
                self.set_font('Arial', '', 10)
                self.cell(155, 8, discount_source, 1, 0, 'L')
                self.cell(25, 8, f"-{invoice_data['discount_amount']:.2f}EUR", 1, 1, 'R')
        
        # Total row
        self.set_font('Arial', 'B', 11)
        self.cell(155, 10, 'Gesamt inkl. MwSt.', 1, 0, 'R')
        self.cell(25, 10, f"{invoice_data['total_price']:.2f}EUR", 1, 1, 'R')
        
        self.ln(8)
        
    def payment_info(self):
        self.set_font('Arial', '', 10)
        
        # Payment method
        self.cell(0, 6, 'Bezahlung durch: [Bar / Überweisung / PayPal]', 0, 1, 'L')
        self.ln(3)
        
        # Payment terms
        self.cell(0, 6, 'Sofern nichts anderes angegeben ist, entspricht der Monat des', 0, 1, 'L')
        self.cell(0, 6, 'Rechnungsdatums dem Leistungszeitpunkt.', 0, 1, 'L')
        self.ln(3)
        
        due_date = (datetime.now() + timedelta(days=14)).strftime("%d.%m.%Y")
        self.cell(0, 6, f'Bitte überweisen Sie den Betrag bis spätestens {due_date}', 0, 1, 'L')
        self.ln(5)
        
        # Closing text
        self.cell(0, 6, 'Bei Fragen stehen wir Ihnen gerne zur Verfügung.', 0, 1, 'L')
        self.cell(0, 6, 'Wir danken Ihnen für Ihr Vertrauen und freuen uns auf eine weitere Zusammenarbeit.', 0, 1, 'L')
        self.ln(8)
        
        # Signature
        self.cell(0, 6, 'Mit freundlichen Grüßen,', 0, 1, 'L')
        self.cell(0, 6, 'Glanzwerk Rheinland', 0, 1, 'L')

def parse_additional_services(text):
    """Parse additional services from text format"""
    if not text or not text.strip():
        return []
    
    services = []
    for line in text.strip().split('\n'):
        # Match pattern: "Description: Price" or "Description: Price€"
        match = re.match(r'^(.+?):\s*(\d+(?:\.\d{1,2})?)€?$', line.strip(), re.IGNORECASE)
        if match:
            services.append({
                'description': match.group(1).strip(),
                'price': float(match.group(2))
            })
    
    return services

@invoice_bp.route('/generate', methods=['POST'])
def generate_invoice():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customerName', 'vehicleNumber', 'selectedService']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # All 15 services
        services = {
            'aussenreinigung': {'name': 'Außenreinigung per Hand', 'price': 50},
            'felgenreinigung': {'name': 'Felgenreinigung & Flugrostentfernung', 'price': 30},
            'innenraumreinigung': {'name': 'Innenraumreinigung', 'price': 70},
            'lederreinigung': {'name': 'Lederreinigung & -pflege', 'price': 60},
            'lederreparatur': {'name': 'Lederreparatur', 'price': 100},
            'polsterreinigung': {'name': 'Polster- & Teppichreinigung', 'price': 80},
            'scheibenreinigung': {'name': 'Scheibenreinigung innen & außen', 'price': 20},
            'lackpolitur': {'name': 'Lackpolitur & Glanzversiegelung', 'price': 150},
            'nanokeramik': {'name': 'Nano-Keramik-Versiegelung', 'price': 300},
            'motorraumreinigung': {'name': 'Motorraumreinigung', 'price': 40},
            'geruchsneutralisierung': {'name': 'Geruchsneutralisierung & Ozonbehandlung', 'price': 50},
            'tierhaarentfernung': {'name': 'Tierhaarentfernung', 'price': 40},
            'hagelschaden': {'name': 'Hagelschaden- und Dellenentfernung', 'price': 200},
            'folierung': {'name': 'Auto Folierung', 'price': 500},
            'abholservice': {'name': 'Abhol- und Bringservice', 'price': 25}
        }
        
        # Discount codes
        discount_codes = {
            'NEUKUNDE': 15,
            'STAMMKUNDE': 10,
            'WINTER2025': 20,
            'SOMMER2025': 12
        }
        
        service = services.get(data['selectedService'])
        if not service:
            return jsonify({'error': 'Invalid service selected'}), 400
        
        # Parse additional services
        additional_services = parse_additional_services(data.get('additionalServices', ''))
        
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
        
        # Regular customer discount
        if data.get('isRegularCustomer', False):
            total_discount_percent += 10
            discount_sources.append('Stammkundenrabatt (10%)')
        
        # Discount code
        discount_code = data.get('discountCode', '').upper()
        if discount_code and discount_code in discount_codes:
            code_discount = discount_codes[discount_code]
            total_discount_percent += code_discount
            discount_sources.append(f'Code {discount_code} ({code_discount}%)')
        
        # Manual discount
        manual_discount = data.get('manualDiscountPercent')
        if manual_discount and str(manual_discount).replace('.', '').isdigit():
            manual_discount = float(manual_discount)
            total_discount_percent += manual_discount
            discount_sources.append(f'Manueller Rabatt ({manual_discount}%)')
        
        discount_amount = gross_price * (total_discount_percent / 100)
        total_price = gross_price - discount_amount
        
        # Generate invoice number
        invoice_number = f"2025-{datetime.now().strftime('%m%d%H%M')}"
        
        # Prepare invoice data
        invoice_data = {
            'customer_name': data['customerName'],
            'vehicle_number': data['vehicleNumber'],
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
        
        # Generate PDF
        pdf = GlanzwerkInvoicePDF()
        pdf.add_page()
        
        # Customer address
        pdf.customer_address(invoice_data['customer_name'], invoice_data['vehicle_number'])
        
        # Invoice header with numbers and dates
        pdf.invoice_header(invoice_number)
        
        # Invoice title
        pdf.invoice_title()
        
        # Greeting text
        pdf.greeting_text()
        
        # Service table
        pdf.service_table(invoice_data)
        
        # Payment information
        pdf.payment_info()
        
        # Create a BytesIO object to store the PDF
        pdf_buffer = io.BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin1')
        pdf_buffer.write(pdf_output)
        pdf_buffer.seek(0)
        
        # Return the PDF file
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'Rechnung_{invoice_number}_{data["customerName"].replace(" ", "_")}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

