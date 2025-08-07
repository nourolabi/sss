import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { FileText, Download, Car, User, Calculator, CheckCircle, Percent } from 'lucide-react'
import glanzwerkLogo from './assets/glanzwerk_logo.png'
import './App.css'

function App() {
  const [customerName, setCustomerName] = useState('')
  const [vehicleNumber, setVehicleNumber] = useState('')
  const [selectedService, setSelectedService] = useState('')
  const [additionalServices, setAdditionalServices] = useState('')
  const [isRegularCustomer, setIsRegularCustomer] = useState(false)
  const [discountCode, setDiscountCode] = useState('')
  const [manualDiscountPercent, setManualDiscountPercent] = useState('')
  const [invoiceData, setInvoiceData] = useState(null)

  const services = [
    { id: 'aussenreinigung', name: 'Außenreinigung per Hand', price: 50, description: 'Professionelle Handwäsche außen' },
    { id: 'felgenreinigung', name: 'Felgenreinigung & Flugrostentfernung', price: 30, description: 'Intensive Felgenpflege' },
    { id: 'innenraumreinigung', name: 'Innenraumreinigung', price: 70, description: 'Komplette Innenraumreinigung' },
    { id: 'lederreinigung', name: 'Lederreinigung & -pflege', price: 60, description: 'Professionelle Lederpflege' },
    { id: 'lederreparatur', name: 'Lederreparatur', price: 100, description: 'Reparatur von Lederschäden' },
    { id: 'polsterreinigung', name: 'Polster- & Teppichreinigung', price: 80, description: 'Tiefenreinigung der Polster' },
    { id: 'scheibenreinigung', name: 'Scheibenreinigung innen & außen', price: 20, description: 'Kristallklare Scheiben' },
    { id: 'lackpolitur', name: 'Lackpolitur & Glanzversiegelung', price: 150, description: 'Hochglanzpolitur mit Versiegelung' },
    { id: 'nanokeramik', name: 'Nano-Keramik-Versiegelung', price: 300, description: 'Premium Keramikversiegelung' },
    { id: 'motorraumreinigung', name: 'Motorraumreinigung', price: 40, description: 'Professionelle Motorraumreinigung' },
    { id: 'geruchsneutralisierung', name: 'Geruchsneutralisierung & Ozonbehandlung', price: 50, description: 'Ozonbehandlung gegen Gerüche' },
    { id: 'tierhaarentfernung', name: 'Tierhaarentfernung', price: 40, description: 'Spezielle Tierhaarentfernung' },
    { id: 'hagelschaden', name: 'Hagelschaden- und Dellenentfernung', price: 200, description: 'Professionelle Dellenreparatur' },
    { id: 'folierung', name: 'Auto Folierung', price: 500, description: 'Komplette Fahrzeugfolierung' },
    { id: 'abholservice', name: 'Abhol- und Bringservice', price: 25, description: 'Bequemer Hol- und Bringservice' }
  ]

  const discountCodes = {
    'NEUKUNDE': 15,
    'STAMMKUNDE': 10,
    'WINTER2025': 20,
    'SOMMER2025': 12
  }

  const parseAdditionalServices = (text) => {
    if (!text.trim()) return []
    
    return text.split('\n').map(line => {
      const match = line.match(/^(.+?):\s*(\d+(?:\.\d{1,2})?)€?$/i)
      if (match) {
        return {
          description: match[1].trim(),
          price: parseFloat(match[2])
        }
      }
      return null
    }).filter(Boolean)
  }

  const calculateInvoice = () => {
    const service = services.find(s => s.id === selectedService)
    if (!service || !customerName || !vehicleNumber) return

    let netPrice = service.price
    
    // Add additional services
    const additionalServicesList = parseAdditionalServices(additionalServices)
    const additionalTotal = additionalServicesList.reduce((sum, item) => sum + item.price, 0)
    netPrice += additionalTotal

    const taxRate = 0.19
    const taxAmount = netPrice * taxRate
    const grossPrice = netPrice + taxAmount
    
    // Calculate discounts
    let totalDiscountPercent = 0
    let discountSources = []
    
    // Regular customer discount
    if (isRegularCustomer) {
      totalDiscountPercent += 10
      discountSources.push('Stammkundenrabatt (10%)')
    }
    
    // Discount code
    if (discountCode && discountCodes[discountCode.toUpperCase()]) {
      const codeDiscount = discountCodes[discountCode.toUpperCase()]
      totalDiscountPercent += codeDiscount
      discountSources.push(`Code ${discountCode.toUpperCase()} (${codeDiscount}%)`)
    }
    
    // Manual discount
    if (manualDiscountPercent && !isNaN(parseFloat(manualDiscountPercent))) {
      const manualDiscount = parseFloat(manualDiscountPercent)
      totalDiscountPercent += manualDiscount
      discountSources.push(`Manueller Rabatt (${manualDiscount}%)`)
    }
    
    const discountAmount = grossPrice * (totalDiscountPercent / 100)
    const finalPrice = grossPrice - discountAmount

    const invoice = {
      invoiceNumber: `2025-${Date.now().toString().slice(-8)}`,
      date: new Date().toLocaleDateString('de-DE'),
      dueDate: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toLocaleDateString('de-DE'),
      customerName,
      vehicleNumber,
      service: service.name,
      serviceDescription: service.description,
      netPrice: service.price,
      additionalServices: additionalServicesList,
      additionalTotal,
      totalNetPrice: netPrice,
      taxAmount,
      grossPrice,
      totalDiscountPercent,
      discountSources,
      discountAmount,
      finalPrice,
      isRegularCustomer,
      discountCode,
      manualDiscountPercent
    }

    setInvoiceData(invoice)
  }

  const generatePDF = async () => {
    try {
      const response = await fetch('/api/invoice/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          customerName,
          vehicleNumber,
          selectedService,
          additionalServices,
          isRegularCustomer,
          discountCode,
          manualDiscountPercent
        })
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.style.display = 'none'
        a.href = url
        a.download = `Rechnung_${customerName.replace(/\s+/g, '_')}.pdf`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      } else {
        const error = await response.json()
        alert(`خطأ في توليد PDF: ${error.error}`)
      }
    } catch (error) {
      console.error('Error generating PDF:', error)
      alert('حدث خطأ أثناء توليد ملف PDF')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-4 mb-4">
            <img src={glanzwerkLogo} alt="Glanzwerk Rheinland Logo" className="w-20 h-20" />
            <div>
              <h1 className="text-4xl font-bold text-gray-900">Glanzwerk Rheinland</h1>
              <p className="text-lg text-gray-600">Professional Invoice System - نظام الفواتير الاحترافي</p>
            </div>
          </div>
          <p className="text-sm text-gray-500 mt-2">Krasnaer Str. 1, 56566 Neuwied, Deutschland</p>
          <p className="text-sm text-green-600 font-medium">Grün gedacht, sauber gemacht</p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Invoice Form */}
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Neue Rechnung erstellen
              </CardTitle>
              <CardDescription>
                Kundendaten und Dienstleistungen für professionelle Rechnungserstellung
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Customer Information */}
              <div className="space-y-4">
                <h3 className="font-semibold flex items-center gap-2">
                  <User className="w-4 h-4" />
                  Kundendaten
                </h3>
                <div className="space-y-3">
                  <div>
                    <Label htmlFor="customerName">Kundenname</Label>
                    <Input
                      id="customerName"
                      placeholder="Kundenname eingeben"
                      value={customerName}
                      onChange={(e) => setCustomerName(e.target.value)}
                      className="mt-1"
                    />
                  </div>
                  <div>
                    <Label htmlFor="vehicleNumber">Fahrzeugkennzeichen</Label>
                    <Input
                      id="vehicleNumber"
                      placeholder="Kennzeichen eingeben"
                      value={vehicleNumber}
                      onChange={(e) => setVehicleNumber(e.target.value)}
                      className="mt-1"
                    />
                  </div>
                </div>
              </div>

              <Separator />

              {/* Service Selection */}
              <div className="space-y-4">
                <h3 className="font-semibold flex items-center gap-2">
                  <Car className="w-4 h-4" />
                  Hauptdienstleistung
                </h3>
                <div>
                  <Label htmlFor="service">Dienstleistung auswählen</Label>
                  <Select value={selectedService} onValueChange={setSelectedService}>
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Dienstleistung wählen" />
                    </SelectTrigger>
                    <SelectContent>
                      {services.map((service) => (
                        <SelectItem key={service.id} value={service.id}>
                          <div className="flex justify-between items-center w-full">
                            <span>{service.name}</span>
                            <span className="text-sm text-gray-500 ml-4">{service.price}€</span>
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                {selectedService && (
                  <div className="p-3 bg-green-50 rounded-lg">
                    <p className="text-sm text-green-800">
                      {services.find(s => s.id === selectedService)?.description}
                    </p>
                  </div>
                )}
              </div>

              <Separator />

              {/* Additional Services */}
              <div className="space-y-4">
                <h3 className="font-semibold flex items-center gap-2">
                  <FileText className="w-4 h-4" />
                  Zusätzliche Dienstleistungen
                </h3>
                <div>
                  <Label htmlFor="additionalServices">Zusatzleistungen (Format: "Beschreibung: Preis")</Label>
                  <Textarea
                    id="additionalServices"
                    placeholder="Beispiel:&#10;Spezialreinigung: 25€&#10;Wachsbehandlung: 40€"
                    value={additionalServices}
                    onChange={(e) => setAdditionalServices(e.target.value)}
                    className="mt-1 h-20"
                  />
                </div>
              </div>

              <Separator />

              {/* Discounts */}
              <div className="space-y-4">
                <h3 className="font-semibold flex items-center gap-2">
                  <Percent className="w-4 h-4" />
                  Rabatte
                </h3>
                <div className="grid grid-cols-1 gap-3">
                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="regularCustomer"
                      checked={isRegularCustomer}
                      onChange={(e) => setIsRegularCustomer(e.target.checked)}
                      className="rounded"
                    />
                    <Label htmlFor="regularCustomer" className="text-sm">
                      Stammkunde (10% Rabatt)
                    </Label>
                  </div>
                  <div>
                    <Label htmlFor="discountCode">Rabattcode</Label>
                    <Input
                      id="discountCode"
                      placeholder="z.B. NEUKUNDE, STAMMKUNDE"
                      value={discountCode}
                      onChange={(e) => setDiscountCode(e.target.value)}
                      className="mt-1"
                    />
                  </div>
                  <div>
                    <Label htmlFor="manualDiscount">Manueller Rabatt (%)</Label>
                    <Input
                      id="manualDiscount"
                      type="number"
                      placeholder="z.B. 5"
                      value={manualDiscountPercent}
                      onChange={(e) => setManualDiscountPercent(e.target.value)}
                      className="mt-1"
                    />
                  </div>
                </div>
              </div>

              <Button 
                onClick={calculateInvoice}
                className="w-full bg-green-600 hover:bg-green-700"
                disabled={!customerName || !vehicleNumber || !selectedService}
              >
                <Calculator className="w-4 h-4 mr-2" />
                Rechnung berechnen
              </Button>
            </CardContent>
          </Card>

          {/* Invoice Preview */}
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Rechnungsvorschau
              </CardTitle>
              <CardDescription>
                Überprüfung der Rechnungsdetails vor dem Download
              </CardDescription>
            </CardHeader>
            <CardContent>
              {invoiceData ? (
                <div className="space-y-6">
                  {/* Invoice Header */}
                  <div className="text-center border-b pb-4">
                    <h2 className="text-2xl font-bold text-gray-900">RECHNUNG</h2>
                    <div className="mt-2 text-sm text-gray-600">
                      <p>Rechnungsnummer: {invoiceData.invoiceNumber}</p>
                      <p>Rechnungsdatum: {invoiceData.date}</p>
                      <p>Fälligkeitsdatum: {invoiceData.dueDate}</p>
                    </div>
                  </div>

                  {/* Customer Info */}
                  <div>
                    <h3 className="font-semibold mb-2">Kunde:</h3>
                    <p className="text-gray-700">{invoiceData.customerName}</p>
                    <p className="text-gray-600 text-sm">Fahrzeug: {invoiceData.vehicleNumber}</p>
                  </div>

                  {/* Service Details */}
                  <div className="border rounded-lg overflow-hidden">
                    <table className="w-full text-sm">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="text-left p-3">Beschreibung</th>
                          <th className="text-right p-3">Betrag</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr className="border-t">
                          <td className="p-3">
                            <div>
                              <p className="font-medium">{invoiceData.service}</p>
                              <p className="text-gray-600 text-xs">{invoiceData.serviceDescription}</p>
                            </div>
                          </td>
                          <td className="text-right p-3">{invoiceData.netPrice.toFixed(2)}€</td>
                        </tr>
                        {invoiceData.additionalServices.map((service, index) => (
                          <tr key={index} className="border-t">
                            <td className="p-3">{service.description}</td>
                            <td className="text-right p-3">{service.price.toFixed(2)}€</td>
                          </tr>
                        ))}
                        <tr className="border-t">
                          <td className="p-3">MwSt. (19%)</td>
                          <td className="text-right p-3">{invoiceData.taxAmount.toFixed(2)}€</td>
                        </tr>
                        <tr className="border-t bg-gray-50">
                          <td className="p-3 font-medium">Zwischensumme</td>
                          <td className="text-right p-3 font-medium">{invoiceData.grossPrice.toFixed(2)}€</td>
                        </tr>
                        {invoiceData.totalDiscountPercent > 0 && (
                          <tr className="border-t">
                            <td className="p-3 text-green-600">
                              <div className="flex items-center gap-1">
                                <CheckCircle className="w-4 h-4" />
                                Gesamtrabatt ({invoiceData.totalDiscountPercent}%)
                              </div>
                            </td>
                            <td className="text-right p-3 text-green-600">-{invoiceData.discountAmount.toFixed(2)}€</td>
                          </tr>
                        )}
                        <tr className="border-t bg-green-50">
                          <td className="p-3 font-bold text-lg">Gesamt inkl. MwSt.</td>
                          <td className="text-right p-3 font-bold text-lg text-green-600">
                            {invoiceData.finalPrice.toFixed(2)}€
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  {invoiceData.discountSources.length > 0 && (
                    <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                      <div className="space-y-1">
                        <h4 className="font-medium text-green-800">Angewandte Rabatte:</h4>
                        {invoiceData.discountSources.map((source, index) => (
                          <div key={index} className="flex items-center gap-2">
                            <Badge variant="secondary" className="bg-green-100 text-green-800">
                              {source}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <Button 
                    onClick={generatePDF}
                    className="w-full bg-green-600 hover:bg-green-700"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    PDF-Rechnung herunterladen
                  </Button>
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <FileText className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>Füllen Sie das Formular aus, um eine Rechnungsvorschau zu sehen</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-sm text-gray-500">
          <p>© 2025 Glanzwerk Rheinland - Professional Car Wash Services</p>
          <p className="mt-1">
            📞 +49 171 1858241 | 📧 Glanzwerk.Rheinland@gmail.com | 📍 Krasnaer Str. 1, 56566 Neuwied
          </p>
          <p className="text-green-600 font-medium">Grün gedacht, sauber gemacht</p>
        </div>
      </div>
    </div>
  )
}

export default App

