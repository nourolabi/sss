# Glanzwerk Rheinland - Professional Invoice System

🚗 **Grün gedacht, sauber gemacht**

A professional invoice generation system for Glanzwerk Rheinland car wash services, built with Streamlit.

## Features

### 🎯 Core Functionality
- **Professional Invoice Generation**: Create detailed invoices with company branding
- **15 Service Types**: Complete range of car wash and detailing services
- **Multi-language Support**: German interface with Arabic subtitle support
- **PDF Export**: Generate professional PDF invoices for download

### 💰 Advanced Pricing & Discounts
- **Regular Customer Discount**: 10% automatic discount for loyal customers
- **Discount Codes**: Pre-configured codes (NEUKUNDE, STAMMKUNDE, WINTER2025, SOMMER2025)
- **Manual Discount**: Flexible percentage-based discounts
- **Additional Services**: Custom services with flexible pricing

### 📋 Service Catalog
1. **Außenreinigung per Hand** - 50€
2. **Felgenreinigung & Flugrostentfernung** - 30€
3. **Innenraumreinigung** - 70€
4. **Lederreinigung & -pflege** - 60€
5. **Lederreparatur** - 100€
6. **Polster- & Teppichreinigung** - 80€
7. **Scheibenreinigung innen & außen** - 20€
8. **Lackpolitur & Glanzversiegelung** - 150€
9. **Nano-Keramik-Versiegelung** - 300€
10. **Motorraumreinigung** - 40€
11. **Geruchsneutralisierung & Ozonbehandlung** - 50€
12. **Tierhaarentfernung** - 40€
13. **Hagelschaden- und Dellenentfernung** - 200€
14. **Auto Folierung** - 500€
15. **Abhol- und Bringservice** - 25€

## 🚀 Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/glanzwerk-invoice-system.git
cd glanzwerk-invoice-system

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Streamlit Cloud Deployment
1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Deploy from your forked repository
5. Set the main file path to `app.py`

## 📱 Usage

### Creating an Invoice
1. **Enter Customer Information**
   - Customer name
   - Vehicle registration number

2. **Select Main Service**
   - Choose from 15 available services
   - View service description and pricing

3. **Add Additional Services** (Optional)
   - Format: "Description: Price"
   - Example: "Special Cleaning: 25€"

4. **Apply Discounts** (Optional)
   - Check "Regular Customer" for 10% discount
   - Enter discount code for additional savings
   - Add manual discount percentage

5. **Generate Invoice**
   - Click "Calculate Invoice" to preview
   - Download PDF for professional presentation

### Discount Codes
- **NEUKUNDE**: 15% discount for new customers
- **STAMMKUNDE**: 10% discount for regular customers
- **WINTER2025**: 20% seasonal discount
- **SOMMER2025**: 12% seasonal discount

## 🏢 Company Information

**Glanzwerk Rheinland**
- **Address**: Krasnaer Str. 1, 56566 Neuwied, Deutschland
- **Phone**: +49 171 1858241
- **Email**: Glanzwerk.Rheinland@gmail.com
- **Instagram**: @glanzwerk_rheinland
- **Motto**: "Grün gedacht, sauber gemacht"

### Banking Details
- **Bank**: Sparkasse Neuwied
- **IBAN**: DE89 5745 0120 0000 1234 56
- **BIC**: MALADE51NWD

## 🛠 Technical Details

### Built With
- **Streamlit**: Web application framework
- **FPDF2**: PDF generation library
- **Pandas**: Data manipulation and analysis
- **Pillow**: Image processing

### File Structure
```
glanzwerk-invoice-system/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── assets/               # Static assets (logos, images)
```

### Key Features Implementation
- **Responsive Design**: Mobile-friendly interface
- **Real-time Calculation**: Instant price updates
- **Professional PDF**: Company-branded invoices
- **Error Handling**: Input validation and user feedback
- **Multi-discount Support**: Stackable discount system

## 📄 Invoice Features

### PDF Invoice Includes
- Company logo and branding
- Invoice number and dates
- Customer and vehicle information
- Detailed service breakdown
- Tax calculations (19% MwSt.)
- Applied discounts
- Payment terms and banking details
- Professional footer with contact information

### Automatic Calculations
- Net prices for all services
- 19% VAT (MwSt.) calculation
- Multiple discount application
- Final total with all adjustments

## 🔧 Customization

### Adding New Services
Edit the `services` dictionary in `app.py`:
```python
services = {
    'new_service': {
        'name': 'New Service Name',
        'price': 100,
        'description': 'Service description'
    }
}
```

### Adding Discount Codes
Edit the `discount_codes` dictionary:
```python
discount_codes = {
    'NEWCODE': 25,  # 25% discount
}
```

## 📞 Support

For technical support or business inquiries:
- **Email**: Glanzwerk.Rheinland@gmail.com
- **Phone**: +49 171 1858241

## 📜 License

This project is proprietary software developed for Glanzwerk Rheinland.

---

**© 2025 Glanzwerk Rheinland - Professional Car Wash Services**

*Grün gedacht, sauber gemacht* 🌱✨

