# 💰 FinanceBuddy Mini
### Explainable Budget & Fraud-Alert Agent System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![AWS Bedrock](https://img.shields.io/badge/AWS_Bedrock-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)

**FinanceBuddy Mini** is an intelligent financial assistant that transforms raw transaction data into actionable insights. By leveraging a multi-agent AI architecture, it categorizes expenses, detects fraud patterns, and generates personalized financial plans.

---

## ✨ Key Features

### 🤖 Multi-Agent Architecture
- **File Parser Agent**: Normalizes messy CSV data into structured formats.
- **Categorizer Agent**: Intelligently assigns categories (Food, Travel, Bills, etc.) to transactions.
- **Anomaly Detection Agent**: Scans for suspicious activities like sudden spikes, unknown merchants, or duplicate charges.
- **Forecasting Agent**: Predicts future spending and suggests actionable savings targets.

### 📊 Interactive Dashboard
- **Real-time Analysis**: Upload a file and get insights in seconds.
- **Visual Reports**: Interactive charts showing spending breakdowns.
- **Fraud Alerts**: Clear, red-flag warnings for potential anomalies.
- **Personalized Plan**: AI-generated advice on where to cut costs and how much to save.

### 🛡️ Robust & Secure
- **Privacy First**: Processes data securely.
- **Dual AI Engine**: Powered by **Claude 3.7 Sonnet** with automatic **Gemini 2.0 Flash** fallback for uninterrupted service.

---

## 🚀 Getting Started

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Magudeshhmw/FinanceBuddy.git
   cd FinanceBuddy
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the App**
   ```bash
   streamlit run finance_app.py
   ```

### Usage

1. **Launch**: Open `http://localhost:8501` in your browser.
2. **Upload**: Drag & drop your bank statement (CSV).
3. **Demo Mode**: Don't have data? Click **"Normal"** or **"Fraud"** demo buttons to see the AI in action.
4. **Analyze**: Click the **"🔍 Analyze Finances"** button.
5. **Explore**:
   - Check the **Summary** for net balance.
   - Review **Alerts** for any red flags.
   - Read your **Personalized Plan** for financial advice.

---

## 🔮 Future Roadmap

- [ ] **Bank API Integration**: Direct connection to major banks via Plaid/Yodlee.
- [ ] **Receipt Scanning**: OCR support for physical receipts.
- [ ] **Subscription Manager**: Dedicated agent to track and cancel unused subscriptions.
- [ ] **Investment Advisor**: AI suggestions for investing surplus funds.
- [ ] **Multi-Currency Support**: Automatic conversion for international travel.

---

## 📂 Project Structure

```
FinanceBuddy/
├── finance_app.py      # Main Streamlit application
├── finance_lib.py      # AI Agent logic and LLM orchestration
├── demo_data.py        # Sample datasets for testing
└── README.md           # Project documentation
```

---

## 🛡️ License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  <sub>Empowering your financial freedom with AI.</sub>
</div>
