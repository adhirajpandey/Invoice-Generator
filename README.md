# Invoice-Generator

## Overview

The Invoice-Generator is a tool designed to facilitate the generation of multiple PDF invoices simultaneously, utilizing CSV data as its source. 

## Features

- **Bulk Invoice Generation:** Create multiple invoices in one go from a single CSV data source.
- **PDF Format:** The invoices are generated in a widely accepted and professional PDF format.
- **Data Source:** Utilizes CSV data, enabling users to manage and modify invoice data effortlessly.

## Installation and Usage

1. Clone the project to your local system using: `git clone https://github.com/adhirajpandey/Invoice-Generator`
2. Install the required dependency: `pip install -r requirements.txt`
3. Checkout sample data and your custom data in `invoice_data.csv` and also add output directory.
4. Make modifications in `generate.py` (if any).
5. Run `python3 generate.py` to start generating PDF invoices for data in csv file.