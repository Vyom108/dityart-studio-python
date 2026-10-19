"""DityArt Studio: a small, Python-only Streamlit storefront."""

from __future__ import annotations

import json
import sqlite3
from datetime import date
from pathlib import Path

import streamlit as st

from database import save_order
from storefront import filter_products, whatsapp_link

ROOT = Path(__file__).parent
PRODUCTS = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))
CATEGORIES = {
    "personalized-gifts": "Personalized Gifts",
    "kids-stationery": "Kids Stationery",
    "corporate-branding": "Corporate Branding",
}
WHATSAPP = "919081913600"
EMAIL = "dityartstudio@gmail.com"
INSTAGRAM = "https://instagram.com/dityart_studio"
PAGES = ["Home", "Products", "Categories", "About", "Contact", "Custom Order", "FAQ", "Privacy Policy", "Terms and Conditions"]
TESTIMONIALS = [
    ("Yash Bhavsar", "Amazing experience! The work was excellent, creative, and done with great attention to detail. Very professional and talented. Highly recommended!"),
    ("Kothari Kajal", "I ordered fridge magnets. They are really great, and the service is excellent too. You can find a wide variety of wonderful customized products there, so you can confidently place an order."),
    ("Shivangi Madhak", "I got customized stickers for my laptop from them, and they turned out to be of great quality. You should definitely give them a try too! 😊"),
]

st.set_page_config(page_title="DityArt Studio", page_icon="🎨", layout="wide", initial_sidebar_state="collapsed")


def wa_link(message: str) -> str:
    return whatsapp_link(message, WHATSAPP)


def go_to(page: str) -> None:
    """Update the page selector from a widget callback, before rerun."""
    st.session_state.page = page
    st.session_state.navigation = page


def open_product(slug: str) -> None:
    st.session_state.selected_product = slug
    go_to("Product Details")


def open_category(label: str) -> None:
    st.session_state.category_filter = label
    st.session_state.category_select = label
    go_to("Products")


def order_next() -> None:
    st.session_state.custom_order_step = min(4, st.session_state.get("custom_order_step", 0) + 1)
    st.session_state.custom_order_error = ""


def order_back() -> None:
    st.session_state.custom_order_step = max(0, st.session_state.get("custom_order_step", 0) - 1)
    st.session_state.custom_order_error = ""


def heading(title: str, intro: str | None = None) -> None:
    st.title(title)
    if intro:
        st.write(intro)


def card(product: dict, index: int) -> None:
    with st.container(border=True):
        st.image(ROOT / "assets" / "products" / product["image"], use_container_width=True)
        st.subheader(product["name"])
        st.caption(CATEGORIES[product["category"]])
        st.write(product["short_description"])
        first, second = st.columns(2)
        first.button("View details", key=f"detail_{index}", use_container_width=True, on_click=open_product, args=(product["slug"],))
        second.link_button("Ask on WhatsApp", wa_link(f"Hi DityArt Studio! I would love to know more about {product['name']} — {product['short_description']}"), use_container_width=True)


def product_grid(products: list[dict], columns: int = 3) -> None:
    for start in range(0, len(products), columns):
        row = st.columns(columns)
        for column, product in zip(row, products[start:start + columns]):
            with column:
                source_index = next(i for i, source in enumerate(PRODUCTS) if source["slug"] == product["slug"])
                card(product, source_index)


def home_page() -> None:
    with st.container(border=True):
        left, right = st.columns([1, 1])
        with left:
            st.image(ROOT / "assets" / "girl-story-cutout.png", use_container_width=True)
        with right:
            st.image(ROOT / "assets" / "dityart-logo.png", width=360)
            st.caption("MADE WITH HEART IN RAJKOT")
            st.write("Personalized gifts, kids stationery, and business details made for your people and your story.")
            a, b = st.columns(2)
            a.button("Explore products", type="primary", use_container_width=True, on_click=go_to, args=("Products",))
            b.button("Share your idea", use_container_width=True, on_click=go_to, args=("Custom Order",))
            st.markdown("✦ ✦ ✦  **Tiny Details, Big Feelings.**")
    st.subheader("Find your product")
    st.header("What are you looking for?")
    st.write("Browse the collection or search for a product. Choose any item to see details and ask us about ordering on WhatsApp.")
    filter_col, search_col = st.columns([1, 2])
    home_category = filter_col.selectbox("Collection", ["All products", *CATEGORIES.values()], key="home_product_category")
    home_query = search_col.text_input("Search products", placeholder="Search wallet card, fridge magnet, sticker...", key="home_product_search")
    home_items = [{**p, "category_label": CATEGORIES[p["category"]]} for p in PRODUCTS]
    visible = filter_products(home_items, home_category if home_category != "All products" else "All categories", home_query)
    st.caption(f"{len(visible)} products")
    if visible:
        product_grid(visible, columns=4)
    else:
        st.info("No products found. Try another word or category.")
    st.button("View all products", on_click=go_to, args=("Products",))
    st.divider()
    st.subheader("Our story")
    st.header("Small studio. Big love for detail.")
    st.write("DityArt Studio began in 2019 as a tiny desk, a stack of paper, and the belief that ordinary gifts can feel extraordinary when they’re made for a specific person. Today, our small team of makers, illustrators, and stationery lovers still hand-finishes every order.")
    st.write("We work in small batches, check every colour by eye, and keep talking with you on WhatsApp until you have something you love. No mass production and no generic templates — every design is made for your story.")
    metric_a, metric_b, metric_c = st.columns(3)
    metric_a.metric("Years in the studio", f"{date.today().year - 2019}+")
    metric_b.metric("Creations handcrafted", "1.2k+")
    metric_c.metric("Average client joy", "5★")
    st.button("Read more about us", on_click=go_to, args=("About",))
    st.divider()
    st.caption("WHY DITYART")
    st.header("Made with more than a name on it.")
    reasons = [
        ("♡  Made around your story", "Names, photos, colours and little details are considered with care."),
        ("🎨  Designed with intention", "Every piece balances playful creativity with a polished finish."),
        ("✦  A lovely process", "We keep the conversation simple on WhatsApp, from idea to final detail."),
    ]
    reason_columns = st.columns(3)
    for column, (title, copy) in zip(reason_columns, reasons):
        with column, st.container(border=True):
            st.subheader(title)
            st.write(copy)
    st.divider()
    st.caption("CUSTOMIZATION PROCESS")
    st.header("Simple from hello to happy dance.")
    steps = [
        ("01 · Tell us your idea", "Send a WhatsApp message with your occasion, photos, and thoughts."),
        ("02 · We shape the details", "We help turn it into a design that feels like you."),
        ("03 · Made with care", "Your finished piece is prepared with the finishing touches it deserves."),
    ]
    step_columns = st.columns(3)
    for column, (title, copy) in zip(step_columns, steps):
        with column, st.container(border=True):
            st.subheader(title)
            st.write(copy)
    st.divider()
    st.caption("5.0 STARS · 45 GOOGLE REVIEWS")
    st.header("Made for people, remembered by people.")
    testimonial_columns = st.columns(3)
    for column, (name, review) in zip(testimonial_columns, TESTIMONIALS):
        with column, st.container(border=True):
            st.write(f"★★★★★  “{review}”")
            st.caption(name)
    st.link_button("Loved our work? Read or leave us a Google review", "https://www.google.com/maps/search/?api=1&query=DityArt+Studio+Rajkot")
    st.divider()
    st.caption("HELPFUL DETAILS")
    st.header("A few questions, answered.")
    for question, answer in FAQS:
        with st.expander(question):
            st.write(answer)
    st.divider()
    with st.container(border=True):
        st.caption("LET’S MAKE SOMETHING SPECIAL")
        st.header("Have an idea? We’d love to bring it to life.")
        st.write("Tell us what you’re dreaming up and we’ll help turn it into a personal creation.")
        left, right = st.columns(2)
        left.link_button("Start your custom order on WhatsApp", wa_link("Hi DityArt Studio! I'd like to customize something."), type="primary", use_container_width=True)
        right.button("Open the custom order form", on_click=go_to, args=("Custom Order",), use_container_width=True)


FAQS = [
    ("How do I place an order?", "Send us a WhatsApp message with your idea, occasion, and any reference photos. We will guide you from there."),
    ("Can I customise every product?", "Yes. Names, messages, colours, photos, and many design details can be tailored to your story."),
    ("How early should I enquire?", "The earlier the better, especially for gifting dates or larger brand orders. We will confirm the timeline on WhatsApp."),
]


def products_page() -> None:
    heading("The product shelf", "Search all of our personalised gifts, kids stationery, and business design services.")
    categories = ["All categories", *CATEGORIES.values()]
    selected_category = st.selectbox("Category", categories, index=categories.index(st.session_state.get("category_filter", "All categories")), key="category_select")
    st.session_state.category_filter = selected_category
    query = st.text_input("Search products", placeholder="Try photo albums or stickers")
    labeled_products = [{**p, "category_label": CATEGORIES[p["category"]]} for p in PRODUCTS]
    filtered = filter_products(labeled_products, selected_category, query)
    st.caption(f"{len(filtered)} product{'s' if len(filtered) != 1 else ''}")
    if filtered:
        product_grid(filtered)
    else:
        st.info("No products match that search. Try another name or category.")


def categories_page() -> None:
    heading("Browse by category", "Choose a collection to see the kinds of creations we make.")
    for key, label in CATEGORIES.items():
        collection = [p for p in PRODUCTS if p["category"] == key]
        with st.container(border=True):
            st.subheader(label)
            st.write(f"{len(collection)} thoughtful designs and services")
            st.write(", ".join(p["name"] for p in collection))
            st.button(f"Browse {label}", key=f"category_{key}", on_click=open_category, args=(label,))


def product_detail_page() -> None:
    slug = st.session_state.get("selected_product", "")
    product = next((item for item in PRODUCTS if item["slug"] == slug), None)
    if not product:
        st.info("Choose a product from the catalog to see its details.")
        st.button("Browse products", on_click=go_to, args=("Products",))
        return
    st.button("← Back to products", on_click=go_to, args=("Products",))
    image_col, info_col = st.columns([1, 1])
    with image_col:
        st.image(ROOT / "assets" / "products" / product["image"], use_container_width=True)
    with info_col:
        st.caption(CATEGORIES[product["category"]])
        st.title(product["name"])
        st.write(product["description"])
        st.subheader("Made with care")
        for feature in product["features"]:
            st.write(f"• {feature}")
        st.subheader("Perfect for")
        st.write(" · ".join(product["perfect_for"]))
        st.link_button("Ask about this product on WhatsApp", wa_link(f"Hi DityArt Studio! I'm interested in {product['name']}. Please share details and customisation options."), type="primary")
    related = [p for p in PRODUCTS if p["category"] == product["category"] and p["slug"] != slug][:3]
    if related:
        st.subheader("More from this collection")
        product_grid(related)


def about_page() -> None:
    heading("Our story", "Small studio. Big love for detail.")
    st.image(ROOT / "assets" / "girl-story.png", use_container_width=True)
    st.write("DityArt Studio began in 2019 as a tiny desk, a stack of paper, and the simple belief that ordinary gifts can feel extraordinary when they’re made for a specific person. Today we’re a small team of makers, illustrators, and stationery lovers in Rajkot, still hand-finishing every order.")
    st.write("We work in small batches, check every colour by eye, and keep talking with you on WhatsApp until you have something you love. No mass production and no generic templates. We make each design for your story.")
    a, b, c = st.columns(3)
    a.metric("Since", "2019")
    b.metric("Creations handcrafted", "1.2k+")
    c.metric("Client joy", "5★")


def contact_page() -> None:
    heading("Say hello", "Have an idea? We’d love to bring it to life.")
    st.write("Tell us what you’re dreaming up and we’ll help turn it into a personal creation.")
    a, b = st.columns(2)
    with a:
        st.subheader("DityArt Studio")
        st.write("📍 Rajkot, Gujarat, India")
        st.write("🕘 Studio hours: 9:00 am to 9:00 pm")
        st.write(f"✉️ [{EMAIL}](mailto:{EMAIL})")
        st.write("📱 +91 90819 13600")
        st.link_button("Open map", "https://www.google.com/maps/search/?api=1&query=DityArt+Studio+Rajkot")
    with b:
        st.link_button("Chat with us on WhatsApp", wa_link("Hi DityArt Studio! I'd like to customize something."), type="primary")
        st.link_button("Visit Instagram", INSTAGRAM)
        st.link_button("Visit Facebook", "https://facebook.com/DityArt%20Studio")
        st.link_button("Email the studio", f"mailto:{EMAIL}")
        st.link_button("Find DityArt Studio in Rajkot", "https://www.google.com/maps/search/?api=1&query=DityArt+Studio+Rajkot")


def custom_order_page() -> None:
    from database import validate_order

    steps = ["Category", "Product", "Your details", "Customisation", "Review"]
    data = st.session_state.setdefault("order_form_data", {})
    st.caption("CUSTOM MADE, SIMPLY")
    heading("Let’s make it yours.", "Answer a few thoughtful questions, then continue the conversation with us on WhatsApp.")
    step = st.session_state.setdefault("custom_order_step", 0)
    st.progress(step / (len(steps) - 1), text=f"Step {step + 1} of {len(steps)} · {steps[step]}")
    if st.session_state.get("custom_order_error"):
        st.error(st.session_state.custom_order_error)

    submitted = False
    with st.form(f"custom_order_step_{step}", border=True):
        if step == 0:
            st.subheader("Choose a category")
            category = st.selectbox("Product category", ["Choose a category", *CATEGORIES.values()], key="order_category_input")
        elif step == 1:
            st.subheader("Choose a product")
            chosen_category = data.get("category", "Choose a category")
            category_key = next((key for key, label in CATEGORIES.items() if label == chosen_category), None)
            available = [p for p in PRODUCTS if p["category"] == category_key]
            product_name = st.selectbox("Product", ["Choose a product", *[p["name"] for p in available]], key="order_product_input")
        elif step == 2:
            st.subheader("Tell us about you")
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Full Name *", key="order_name_input")
                phone = st.text_input("Mobile Number *", placeholder="+91 90819 13600", key="order_phone_input")
            with col_b:
                email = st.text_input("Email (Optional)", key="order_email_input")
                city = st.text_input("City *", key="order_city_input")
        elif step == 3:
            st.subheader("Make it personal")
            col_a, col_b = st.columns(2)
            with col_a:
                recipient = st.text_input("Recipient Name", key="order_recipient_input")
                occasion = st.text_input("Occasion", key="order_occasion_input")
                required_text = st.text_area("Custom Text / Quote", key="order_quote_input")
                colours = st.text_input("Preferred Colours", key="order_colours_input")
            with col_b:
                required_date = st.date_input("Required Delivery Date", value=None, key="order_date_input")
                budget = st.text_input("Budget (Optional)", key="order_budget_input")
                notes = st.text_area("Special Instructions", key="order_notes_input", height=180)
        else:
            st.subheader("Review your idea")
            summary = [
                ("Category", data.get("category", "")),
                ("Product", data.get("product", "")),
                ("Customer", data.get("customer_name", "")),
                ("Phone", data.get("phone", "")),
                ("Email", data.get("email", "")),
                ("City", data.get("city", "")),
                ("Recipient", data.get("recipient_name", "")),
                ("Occasion", data.get("occasion", "")),
                ("Custom text", data.get("required_text", "")),
                ("Colours", data.get("preferred_colours", "")),
                ("Required date", data.get("required_date", "")),
                ("Budget", data.get("budget", "")),
                ("Notes", data.get("notes", "")),
            ]
            for label, value in summary:
                if value and value != "Choose a product" and value != "Choose a category":
                    st.write(f"**{label}:** {value}")
        submitted = st.form_submit_button("Continue" if step < 4 else "Save enquiry", type="primary")

    nav_col_a, nav_col_b = st.columns(2)
    if step > 0:
        nav_col_a.button("← Back", on_click=order_back, use_container_width=True)
    if submitted:
        if step == 0:
            if category == "Choose a category":
                st.session_state.custom_order_error = "Please choose a category to continue."
            else:
                data["category"] = category
                order_next()
        elif step == 1:
            if product_name == "Choose a product":
                st.session_state.custom_order_error = "Please choose a product to continue."
            else:
                data["product"] = product_name
                order_next()
        elif step == 2:
            required_data = {
                "customer_name": name,
                "phone": phone,
                "email": email,
                "city": city,
                "product": data.get("product", ""),
            }
            basic_errors = validate_order(required_data)
            if basic_errors:
                st.session_state.custom_order_error = " ".join(basic_errors)
            else:
                data.update(required_data)
                order_next()
        elif step == 3:
            data.update({
                "recipient_name": recipient,
                "occasion": occasion,
                "required_text": required_text,
                "preferred_colours": colours,
                "required_date": required_date.isoformat() if required_date else "",
                "budget": budget,
                "notes": notes,
            })
            order_next()
        elif step == 4:
            errors = validate_order(data)
            if errors:
                st.session_state.custom_order_error = " ".join(errors)
            else:
                try:
                    st.session_state.saved_order_id = save_order(data)
                    st.session_state.custom_order_error = ""
                except (OSError, ValueError, sqlite3.Error) as error:
                    st.session_state.custom_order_error = f"We couldn’t save your enquiry. Please try again or contact us on WhatsApp. Details: {error}"
        else:
            order_next()

    if st.session_state.get("saved_order_id"):
        customer_name = data.get("customer_name", "")
        product_name = data.get("product", "")
        city = data.get("city", "")
        st.success(f"Thanks, {customer_name}! Your enquiry is saved privately (reference #{st.session_state.saved_order_id}).")
        message = (
            f"Hello DityArt Studio 👋\n\nI would like to place a custom order.\n\n"
            f"Category: {data.get('category', '')}\nProduct: {product_name}\n"
            f"Customer Name: {customer_name}\nPhone: {data.get('phone', '')}\nCity: {city}\n"
            f"Recipient Name: {data.get('recipient_name', '')}\nOccasion: {data.get('occasion', '')}\n"
            f"Required Text: {data.get('required_text', '')}\nPreferred Colours: {data.get('preferred_colours', '')}\n"
            f"Required Date: {data.get('required_date', '')}\nBudget: {data.get('budget', '')}\n"
            f"Special Instructions: {data.get('notes', '')}\n\nPlease guide me with the next steps."
        )
        st.link_button("Continue on WhatsApp", wa_link(message), type="primary")


def faq_page() -> None:
    heading("Helpful details", "A few questions, answered.")
    for question, answer in FAQS:
        with st.expander(question, expanded=False):
            st.write(answer)
    st.link_button("Ask us on WhatsApp", wa_link("Hi DityArt Studio! I have a question."))


def privacy_page() -> None:
    heading("Privacy Policy")
    st.caption("Effective date: August 01, 2025")
    st.write("At DityArt Studio, we value your privacy and are committed to protecting your personal information.")
    sections = [
        ("Information We Collect", "When you place an order, we may collect details such as your name, email address, contact number, shipping address, and order preferences."),
        ("How We Use Your Information", "This information is used solely to process and deliver your orders, communicate with you regarding your purchase or inquiries, and improve our products and services."),
        ("Information Sharing", "We do not sell, rent, or share your personal information with third parties except as required to deliver your order, such as courier companies, or when required by law."),
        ("Data Security", "We take reasonable measures to protect your information from unauthorized access, alteration, or disclosure."),
        ("Cookies & Analytics", "Our website may use cookies or analytics tools to enhance your browsing experience. These tools collect non-identifiable data such as page visits and device type."),
        ("Your Rights", f"You may request to update, correct, or delete your personal data by contacting us at {EMAIL}."),
        ("Contact", f"Questions? Email {EMAIL} or WhatsApp +91 90819 13600."),
    ]
    for title, body in sections:
        st.subheader(title)
        st.write(body)


def terms_page() -> None:
    heading("Terms and Conditions")
    st.caption("Effective date: August 01, 2025")
    st.write("By placing an order with DityArt Studio, you agree to the following terms:")
    sections = [
        ("1. Products & Services", "We create customized designs and gift products as per customer specifications. Product images are for reference; final products may vary slightly due to printing, materials, or design adjustments."),
        ("2. Orders & Payment", "Full payment is required before order processing. Orders are confirmed only after successful payment and receipt of all necessary design inputs from the customer."),
        ("3. Design Approval", "We provide digital previews for customized orders. Once a design is approved by the customer, no further changes or cancellations will be accepted."),
        ("4. Shipping & Delivery", "Delivery timelines may vary based on location and courier service. DityArt Studio is not responsible for delays caused by third-party courier companies."),
        ("5. Returns & Refunds", "Since our products are custom-made, returns and refunds are not applicable except in the case of manufacturing defects or damage during shipping. Such cases must be reported within 48 hours of delivery with photo proof."),
        ("6. Intellectual Property", "All designs created by DityArt Studio remain our intellectual property and may not be reproduced, resold, or redistributed without our written permission."),
        ("7. Changes to Terms", "We may update these Terms of Service from time to time. Continued use of our services after changes means you accept the updated terms."),
    ]
    for title, body in sections:
        st.subheader(title)
        st.write(body)


def main() -> None:
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    current = st.session_state.page
    options = PAGES + (["Product Details"] if current == "Product Details" else [])
    if current not in options:
        current = "Home"
    if "navigation" not in st.session_state:
        st.session_state.navigation = current
    top = st.columns([1.25, 1, 1, 1, 1, 1.8])
    with top[0]:
        st.image(ROOT / "assets" / "dityart-circle-logo.png", width=94)
    for column, label in zip(top[1:5], ["Home", "Products", "About", "Contact"]):
        with column:
            st.button(label, type="primary" if current == label else "secondary", use_container_width=True, on_click=go_to, args=(label,))
    with top[5]:
        st.button("Start a custom order", type="primary" if current == "Custom Order" else "secondary", use_container_width=True, on_click=go_to, args=("Custom Order",))
    st.sidebar.caption("DityArt Studio · Where Creativity Meets Craftsmanship.")
    selected = st.sidebar.selectbox("Explore all pages", options, index=options.index(current), key="navigation", on_change=lambda: st.session_state.update(page=st.session_state.navigation))
    st.session_state.page = selected
    st.sidebar.divider()
    st.sidebar.caption("Rajkot, Gujarat, India")
    st.sidebar.link_button("WhatsApp the studio", wa_link("Hi DityArt Studio!"), use_container_width=True)

    routes = {
        "Home": home_page, "Products": products_page, "Categories": categories_page,
        "Product Details": product_detail_page, "About": about_page, "Contact": contact_page,
        "Custom Order": custom_order_page, "FAQ": faq_page, "Privacy Policy": privacy_page,
        "Terms and Conditions": terms_page,
    }
    routes[selected]()
    st.divider()
    footer_logo, footer_links = st.columns([1, 5])
    with footer_logo:
        st.image(ROOT / "assets" / "dityart-circle-logo.png", width=74)
    with footer_links:
        footer_nav = st.columns(7)
        for column, label, target in zip(footer_nav, ["About Us", "Categories", "Explore Products", "Custom Order", "FAQ", "Privacy Policy", "Terms of Service"], ["About", "Categories", "Products", "Custom Order", "FAQ", "Privacy Policy", "Terms and Conditions"]):
            with column:
                st.button(label, on_click=go_to, args=(target,), use_container_width=True)
        st.write(f"[WhatsApp]({wa_link('Hi DityArt Studio! I would like to customize something.')})  |  [Instagram]({INSTAGRAM})  |  [Facebook](https://facebook.com/DityArt%20Studio)  |  [Mail](mailto:{EMAIL})  |  [ +91 90819 13600](tel:+919081913600)")
        st.write("[Rajkot](https://www.google.com/maps/search/?api=1&query=DityArt+Studio+Rajkot)")
        st.caption(f"© {date.today().year} DityArt Studio. Made with a whole lot of heart. · {EMAIL}")
        st.caption("♥  Where Creativity Meets Craftsmanship.")


if __name__ == "__main__":
    main()
