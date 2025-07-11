# -*- coding: utf-8 -*-
"""
Created on Wed May 14 of 2025

Author: Paulo Barbosa

Description:
This script provides a graphical user interface (GUI) to select a PDF file, 
extract structured tabular data from all pages using `pdfplumber`, and convert it into a DataFrame.

The extracted data includes program number, program name, program director, 
email address, and preliminary position.

It also includes logging functionalities to capture issues found during parsing. 
The final structured data is exported to both Excel and CSV formats.

The Excel and Csv files are saved in the sub-folder 'Output'
The Log file are saved in the sub-folder 'Log'
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pdfplumber
import pandas as pd
import logging
from datetime import datetime
import re

# Suppress verbose pdfminer logs
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# === GUI File Selector ===
def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        initialdir="C:/Users",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
    )

    if not file_path:
        print("No file selected.")
        return None

    if not file_path.lower().endswith(".pdf"):
        messagebox.showerror("Invalid file", "❌ The selected file is not a PDF. Please choose a PDF file.")
        return None

    print(f"✅ PDF file selected: {file_path}")
    return file_path

# === Logging Setup ===
def setup_logging(pdf_name):
    log_dir = "Log"
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, f"log_{pdf_name}.txt")

    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write("DATE_TIME\t\tFILE_NAME\tPAGE_NUMBER\tDESCRIPTION\n")

    return log_file_path

def log_issue(description, filename, page_number):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp}\t{filename}\t{page_number}\t\t{description}\n"
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(entry)

# === Email Finder ===
def find_email(items):
    joined_after_ph = ''
    email_pattern = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
    
    # Find the index of the line starting with 'Ph:'
    for i, item in enumerate(items):
        if item.strip().startswith('Ph:'):
            # Join all lines after this one
            joined_after_ph = ''.join(items[i+1:]).replace(' ', '')

    match = email_pattern.search(joined_after_ph)
    
    return match.group() if match else ''

# === Table Extractor ===
def extract_tables_from_pdf(pdf, total_pages):
    tables = []
    for i in range(total_pages):
        print(f"Extract table from page {i + 1}")
        table = pdf.pages[i].extract_tables()

        if not table:
            log_issue("No table found", pdffile, i + 1)
            continue

        for row in table[0]:
            row.append(i + 1)  # Append page number to each row
            tables.append(row)

    return tables

# === Row Parser ===
def process_table_rows(tables):
    parsed_data = []

    for row in tables:
        page_number = row[-1]

        if not row[0].startswith('['):
            continue

        parts = row[0].split(']')
        if not parts[0][1:].isnumeric():
            continue

        prog_number = parts[0][1:].strip()
        if len(prog_number) != 10:
            log_issue(f"Program number '{prog_number}' is not 10 digits", pdffile, page_number)

        prog_name = parts[1].strip().replace('\n', ' ')
        prog_director = row[2].replace('\n', ' ')
        email = find_email(row[1].split('\n'))
        position = '' if len(row) == 6 else row[5].strip()


        # Log missing fields
        missing = []
        if not prog_name: missing.append('Program Name')
        if not prog_director: missing.append('Program Director')
        if not email: missing.append('Email')
        if not position and len(row) >= 7: missing.append('Preliminary Position')

        if missing:
            log_issue(f"Missing fields in Program Number '{prog_number}': {', '.join(missing)}", pdffile, page_number)

        parsed_data.append([prog_number, prog_name, prog_director, email, position])

    return parsed_data

# === Output Writer ===
def export_to_files(df, base_filename):
    output_folder = os.path.join(os.getcwd(), 'Output')
    os.makedirs(output_folder, exist_ok=True)

    excel_path = os.path.join(output_folder, f"{base_filename}.xlsx")
    csv_path = os.path.join(output_folder, f"{base_filename}.csv")

    try:
        df.to_excel(excel_path, sheet_name='Sheet1', index=False)
        df.to_csv(csv_path, index=False, quoting=1)
        print(f"✅ Excel and CSV files created in {output_folder}")
        log_issue(f"Files '{base_filename}.xlsx' and '{base_filename}.csv' created successfully", pdffile, '--')
    except Exception as e:
        print(f"❌ Error writing files: {e}")
        log_issue(f"Error writing files: {e}", pdffile, '--')

# === Main Execution ===
filepath = select_pdf_file()
if not filepath:
    exit()

pdffile = os.path.basename(filepath)

pdf = pdfplumber.open(filepath)
number_of_pages = len(pdf.pages)
print(f"Number of pages: {number_of_pages}")
print("Metadata:", pdf.metadata)

log_file_path = setup_logging(pdffile.split('.')[0])
log_issue("Start processing file", pdffile, '--')

tables = extract_tables_from_pdf(pdf, number_of_pages)
if tables and len(tables[0]) == 6:
    log_issue("PDF table structure lacks 'Preliminary Positions' column", pdffile, '--')

data = process_table_rows(tables)
df = pd.DataFrame(data, columns=['Program Number', 'Program Name', 'Program Director', 'Email Address', 'Preliminary Position'])

log_issue("End processing file", pdffile, '--')
export_to_files(df, pdffile.split('.')[0])


