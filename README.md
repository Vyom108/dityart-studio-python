# DityArt Studio — Python Edition

A Python-only Streamlit storefront for **DityArt Studio**, featuring the original product catalog and artwork, product discovery, WhatsApp enquiries, and a custom order form backed by SQLite.

> **Where Creativity Meets Craftsmanship.**

This is a separate Python rebuild. The original TypeScript project is kept unchanged. The app reuses its catalog of 21 products and matching artwork.

## What you can do

- Explore featured products, search the catalog, and filter by **Personalized Gifts**, **Kids Stationery**, or **Corporate Branding**.
- Open product details with images, descriptions, features, and related products.
- Start a WhatsApp enquiry with the selected product and a prefilled message.
- Submit a custom order with customer and project details, then save it locally in SQLite.
- Browse Home, Products, Categories, About, Contact, Custom Order, FAQ, Privacy Policy, and Terms and Conditions.

Custom order records begin with the **New** status. The database supports **New**, **Contacted**, **In Design**, and **Completed**. Customer submissions are not shown on public pages, and there is no unauthenticated admin dashboard.

## Project structure

```text
.
├── app.py                 # Streamlit entry point and navigation
├── database.py            # SQLite setup and order persistence
├── storefront.py          # Catalog and shared storefront logic
├── data/                  # Product catalog and local order database
├── assets/                # Reused brand and product artwork
├── tests/                 # Basic database and form logic tests
├── .streamlit/             # Streamlit configuration
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- Internet access to install the packages listed in `requirements.txt`

## Run locally

### Linux or macOS

```bash
git clone https://github.com/Vyom108/dityart-studio-python.git
cd dityart-studio-python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Windows PowerShell

```powershell
git clone https://github.com/Vyom108/dityart-studio-python.git
cd dityart-studio-python
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit opens the site in your browser. If it does not open automatically, visit [http://localhost:8501](http://localhost:8501). Stop the server with **Ctrl+C** in the terminal.

## Run the tests

With the virtual environment activated, run:

```bash
python -m unittest discover -s tests -v
```

## Brand and contact

- **Location:** Rajkot, Gujarat, India
- **Email:** [dityartstudio@gmail.com](mailto:dityartstudio@gmail.com)
- **WhatsApp:** [+91 90819 13600](https://wa.me/919081913600)
- **Instagram:** [@dityart_studio](https://instagram.com/dityart_studio)

## Customer data and deployment

Order enquiries are stored in `data/orders.sqlite3` on the machine running the app. Keep this database private and back it up securely if you need to retain submissions. It is excluded from source control. A hosted deployment should provide persistent private storage; temporary hosting disks may be erased when an instance restarts or is replaced.

## Implementation notes

The interface uses Streamlit's native pages, widgets, and layout features. It contains no custom HTML, CSS, or JavaScript. Streamlit controls some navigation and layout behavior, so the result follows its built-in component capabilities.
