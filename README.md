# ⚡ Volt-Trace Backend

> **Autonomous Digital Carbon Footprint Analyzer**

This is the backend engine of the Volt-Trace project, built with FastAPI and LangChain.

---

## 🚀 Key Features

- **Real-time Carbon Analysis**: Dissects website assets to calculate precise CO2 emissions.
- **Agentic AI Audit**: Uses **Google Gemini** and **LangChain** to provide performance optimization advice.
- **Environmental Formulas**: Implements the Sustainable Web Design Model for accurate reporting.

---

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python)
- **Scraping**: BeautifulSoup4, LXML
- **AI/LLM**: LangChain, Google Generative AI (Gemini 2.5 Flash)
- **Environment**: Python 3.10+

---

## 📦 Getting Started

### **Prerequisites**
- Python (v3.10+)
- Google Gemini API Key

### **Installation**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### **Run Server**
```bash
export GOOGLE_API_KEY="your_api_key_here"
uvicorn main:app --reload
```

---

## 🧠 How It Works

1. **Scraping**: The Python engine fetches the target URL and calculates the total payload size.
2. **Math**: It calculates CO2 grams based on page weight and grid intensity.
3. **Reasoning**: A LangChain agent audits the assets and provides optimization solutions.

---

## 📄 License

This project is licensed under the MIT License.
