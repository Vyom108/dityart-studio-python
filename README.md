# DityArt Studio — Python edition

Python-only Streamlit rebuild of DityArt Studio, featuring the original product catalog and artwork, searchable categories, product details, WhatsApp inquiries, and a custom order form with private SQLite storage.

A beginner-friendly Streamlit storefront for DityArt Studio. It reuses the original catalog of 21 products and matching product artwork. The original TypeScript website remains untouched.

## Requirements

- Python 3.10 or newer
- Internet access to install Streamlit the first time

## Run locally on Linux or macOS

```bash
cd dityart-studio-python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Run locally on Windows PowerShell

```powershell
cd dityart-studio-python
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit opens the local website in your browser. If it does not open automatically, visit **http://localhost:8501**. Stop the server with `Ctrl+C` in the terminal.

## Pages and features

- Home page with the original brand artwork, product search and category filters, studio story, reasons to choose DityArt, customization steps, original customer testimonials, FAQ, and inquiry banner.
- Searchable product catalog with category filters and individual product detail views.
- Category browser, About, Contact, Custom Order, FAQ, Privacy Policy, and Terms and Conditions pages.
- WhatsApp inquiry links include the selected product name and a useful prefilled message.
- Five-step custom order form captures category, product, customer name, phone, email, city, recipient name, occasion, custom text, budget, preferred colours, required date, and notes, then saves the enquiry and offers a prefilled WhatsApp handoff.
- Submissions are stored in `data/orders.sqlite3` using Python's built-in `sqlite3`. The database is local to this installation; customer records are not displayed on any public page.
- Order status is initialized as **New**. The database supports **New**, **Contacted**, **In Design**, and **Completed** values. There is intentionally no public admin dashboard.

## Run basic checks

```bash
python -m unittest discover -s tests -v
```

## Data and privacy

Back up `data/orders.sqlite3` securely if you need to retain order enquiries. Do not commit that database to source control. A public deployment needs a persistent private disk or managed database; ephemeral hosting can lose local SQLite data when an instance is replaced. Streamlit reruns the Python script as users interact with widgets, and its navigation and layout are constrained to Streamlit's built-in components. This app uses no custom HTML, CSS, or JavaScript.
