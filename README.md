# 🚀 Lead Automation Tool

A production-style Python project that cleans, enriches, and scores leads using APIs and AI.

---

## 🔥 Features

- ✅ CSV Lead Cleaning (email, phone, duplicates)
- ✅ API-based enrichment (company, location)
- ✅ AI lead scoring (Hot / Warm / Cold)
- ✅ Async processing for high performance
- ✅ CLI-based usage
- ✅ Input validation and error handling
- ✅ Unit tests with pytest

---

## 📁 Project Structure

```
src/lead_automation/
├── services/
├── utils/
├── main.py
├── config.py

tests/
data/
output/
```

---

## ⚙️ Setup

### 1. Clone repo

```bash
git clone <your-repo-url>
cd lead_cleaner
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Setup environment variables

Create `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
API_BASE_URL=https://openrouter.ai/api/v1
MAX_CONCURRENT_REQUESTS=5
```

---

## 🚀 Usage

---

### 🔹 Clean Leads

```bash
python -m lead_automation.main clean-leads data/leads.csv
```

---

### 🔹 Enrich Leads

```bash
python -m lead_automation.main enrich-leads data/leads.csv
```

---

## 📊 Example Input

```csv
name,email,phone
John, TEST@EMAIL.COM ,123-456
```

---

## 📊 Example Output

```csv
name,email,phone,company,city,lead_score,reason
John,test@email.com,123456,Google,NY,Hot,High intent
```

---

## 🧪 Run Tests

```bash
pytest
```

---

## 🧠 Tech Stack

- Python
- Typer (CLI)
- httpx (async API calls)
- pytest (testing)
- Pydantic (config management)

---

## 🔥 Future Improvements

- Add FastAPI backend
- Add database (PostgreSQL)
- Add dashboard UI
- Deploy as SaaS tool

---

## 👨‍💻 Author

Built by Bhupendra (Jon Singh)