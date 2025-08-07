# 🚀 Deployment Instructions

## GitHub Setup

### 1. Create GitHub Repository
```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Glanzwerk Rheinland Invoice System"

# Add remote repository (replace with your GitHub repo URL)
git remote add origin https://github.com/yourusername/glanzwerk-invoice-system.git

# Push to GitHub
git push -u origin main
```

### 2. Repository Structure
Your repository should contain:
```
glanzwerk-invoice-system/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # Documentation
├── .gitignore               # Git ignore file
├── deploy_instructions.md   # This file
├── .streamlit/
│   └── config.toml         # Streamlit configuration
└── assets/
    └── glanzwerk_logo.png  # Company logo
```

## Streamlit Cloud Deployment

### 1. Access Streamlit Cloud
- Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
- Sign in with your GitHub account

### 2. Deploy Application
1. Click "New app"
2. Select your GitHub repository
3. Choose the branch (usually `main`)
4. Set the main file path: `app.py`
5. Click "Deploy!"

### 3. Configuration
- **App URL**: Will be automatically generated (e.g., `https://yourapp.streamlit.app`)
- **Python version**: 3.9+ (automatically detected)
- **Dependencies**: Installed from `requirements.txt`

### 4. Environment Variables (if needed)
If you need to add secrets or environment variables:
1. Go to your app settings in Streamlit Cloud
2. Click on "Secrets"
3. Add any required secrets in TOML format

## Alternative Deployment Options

### 1. Heroku Deployment
Create additional files for Heroku:

**Procfile:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt:**
```
python-3.9.18
```

### 2. Docker Deployment
Create a Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

### 3. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

## Post-Deployment Checklist

### ✅ Functionality Tests
- [ ] Customer information input works
- [ ] Service selection displays correctly
- [ ] Additional services parsing works
- [ ] Discount calculations are accurate
- [ ] PDF generation and download works
- [ ] All 15 services are available
- [ ] Discount codes function properly

### ✅ UI/UX Tests
- [ ] Responsive design on mobile
- [ ] Logo displays correctly
- [ ] Colors match brand guidelines
- [ ] German text displays properly
- [ ] Invoice preview is readable

### ✅ Business Logic Tests
- [ ] Tax calculation (19% MwSt.) is correct
- [ ] Multiple discounts stack properly
- [ ] Regular customer discount applies
- [ ] Manual discount percentage works
- [ ] Final totals are accurate

## Troubleshooting

### Common Issues

**1. Dependencies not installing:**
- Check `requirements.txt` format
- Ensure all package names are correct
- Try pinning specific versions

**2. Logo not displaying:**
- Verify logo file is in `assets/` directory
- Check file path in code
- Ensure image format is supported

**3. PDF generation fails:**
- Check fpdf2 installation
- Verify font availability
- Test with simple PDF first

**4. Streamlit app won't start:**
- Check Python version compatibility
- Verify main file path is correct
- Review error logs in deployment console

### Getting Help
- **Streamlit Documentation**: [https://docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [https://discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: Create issues in your repository

## Maintenance

### Regular Updates
1. **Update Dependencies**: Regularly update `requirements.txt`
2. **Security Patches**: Monitor for security updates
3. **Feature Additions**: Add new services or discount codes as needed
4. **Bug Fixes**: Address any reported issues promptly

### Monitoring
- Monitor app performance in Streamlit Cloud dashboard
- Check error logs regularly
- Gather user feedback for improvements

---

**🎉 Your Glanzwerk Rheinland Invoice System is ready for deployment!**

For support: Glanzwerk.Rheinland@gmail.com

