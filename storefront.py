"""Small, dependency-free helpers shared by the storefront and tests."""

from urllib.parse import quote


def filter_products(products: list[dict], category: str = "All categories", search: str = "") -> list[dict]:
    """Filter catalog records by display category and case-insensitive text."""
    filtered = products
    if category != "All categories":
        filtered = [item for item in filtered if item["category_label"] == category]
    term = search.strip().casefold()
    if term:
        filtered = [item for item in filtered if term in item["name"].casefold()
                    or term in item["short_description"].casefold()
                    or term in item["category_label"].casefold()]
    return filtered


def whatsapp_link(message: str, phone: str = "919081913600") -> str:
    """Build a WhatsApp click-to-chat URL with safely encoded message text."""
    return f"https://wa.me/{phone}?text={quote(message)}"
