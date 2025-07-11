# pdfplumber_usage_example - PDF Data Extractor for Residency Program Listings

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![pdfplumber](https://img.shields.io/badge/pdfplumber-0.10.0-orange)
![pandas](https://img.shields.io/badge/pandas-2.0.0-red)

A Python tool to extract structured residency program data from unstructured PDFs, designed for the **Internal Medicine Residency Program Listings** use case. Parses inconsistent formatting, unpredictable line breaks, and fragmented text blocks into a clean tabular format.

---

## 🎯 Key Features
- **GUI-based PDF selection** (Tkinter)  
- **Extracts 5 critical fields** per program:
  - Program Number (10-digit ID)
  - Full Program Name
  - Program Director (Name + Degree)
  - Email Address
  - Preliminary Position (Yes/No)
- **Handles edge cases**:
  - Missing emails
  - Multi-line program names
  - Inconsistent spacing/wrapping
- **Logging system** to track parsing issues
- **Exports to Excel & CSV** (saved in `/Output`)

---

## 📦 Installation
1. Clone the repository:
   ```bash
    git clone https://github.com/your-username/pdf-residency-data-extractor.git

2. Install dependencies:
   pip install pdfplumber pandas tk

## 🛠️ Usage
    python pdf_extractor.py

1. **Select a PDF via the GUI file picker.**

2. **The script will:**
   - Parse all pages
   - Log issues in /Log/log_[filename].txt
   - Save outputs to /Output/[filename].xlsx and .csv

## 🔍 Parsing Logic (Critical Rules)
| Field               | Extraction Rule                                                                 |
|---------------------|---------------------------------------------------------------------------------|
| **Program Number**  | 10-digit ID in `[1234567890]` format (brackets removed)                         |
| **Program Name**    | Text after ID, stops before address/`Ph:` (handles 1–3 line splits)             |
| **Program Director**| Full name + degree (e.g., `John Doe MD`) after email, before accreditation      |
| **Email**           | Extracted from text after `Ph:` using regex (marked blank if missing)           |
| **Preliminary Pos** | Standardized to `Yes`/`No` from end of block                                   |

## 📂 Project Structure
<pre>
.
├── pdf_extractor.py        # Main script
├── Output/                 # Generated Excel/CSV files
├── Log/                    # Parsing issue logs
└── README.md               # This file
</pre>

## 🚨 Limitations
Not AI-based: Relies on deterministic parsing rules (unlike LLM-based tools).

PDF Format-Specific: Designed for the provided Internal Medicine Residency PDF structure.

Requires Cleanup: Some edge cases may need manual review (logged in detail).

## 📜 Logging Example
| DATE_TIME          | FILE_NAME  | PAGE_NUMBER | DESCRIPTION                              |
|--------------------|------------|-------------|------------------------------------------|
| 2025-05-14 14:30:12 | sample.pdf | 3           | Missing email in Program Number '1234567890' |
| 2025-05-14 14:30:13 | sample.pdf | 5           | Program number '123' is not 10 digits    |

## 📄 License
MIT License - Free for academic/commercial use with attribution.

