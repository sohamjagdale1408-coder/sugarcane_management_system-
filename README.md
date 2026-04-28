# 🌿 SugarSense — Sugar Management System

A production-like web application for managing sugarcane farm data.
Built with **Flask**, **SQLite**, and a clean responsive UI.

---

## 📁 Folder Structure

```
sugar_management/
├── app.py                  ← Flask application (routes, DB helpers)
├── logic.py                ← Business logic (calculations)
├── requirements.txt        ← Python dependencies
├── database.db             ← SQLite database (auto-created on first run)
├── templates/
│   ├── base.html           ← Shared layout + navbar
│   ├── index.html          ← Home page (form)
│   ├── result.html         ← Results page
│   └── records.html        ← All records table
└── static/
    ├── css/
    │   └── style.css       ← Complete stylesheet
    └── js/
        └── main.js         ← Frontend interactions
```

---

## 🚀 Setup & Run

### 1. Prerequisites
- Python 3.8 or higher
- pip

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python app.py
```

### 4. Open in browser
```
http://127.0.0.1:5000
```

The SQLite database (`database.db`) is created automatically on the first run.

---

## 📊 Features

| Feature | Description |
|---|---|
| Farm Entry Form | Input farmer, crop, soil, area, irrigation, fertilizer & planting date |
| Water Calculation | Total water usage (litres) over a full season |
| Yield Estimate | Tons of sugarcane based on soil type & crop variety |
| Sugar Output | Kilograms of sugar extracted from yield |
| Harvest Date | Projected from planting date + crop growth period |
| Records Table | Searchable table of all entries with summary stats |
| Delete Records | Remove individual entries with confirmation |

---

## 🌿 Supported Crop Varieties

| Variety | Growth (months) | Sugar Rate |
|---|---|---|
| Co 86032 | 12 | 10.5% |
| CoM 0265 | 14 | 11.5% |
| CoC 671  | 12 | 10.0% |
| CoS 767  | 10 | 9.5%  |
| Co 419   | 13 | 10.8% |
| CoJ 64   | 12 | 11.2% |

---

## 🛡️ Security
- All database queries use parameterized statements (no SQL injection)
- Input validated on both client and server side
- Flask secret key used for session security
