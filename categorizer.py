"""
categorizer.py — Rule-based transaction categorizer
Matches transaction descriptions to spending categories using keywords.
"""

CATEGORY_RULES = {
    "Food & Dining": [
        "zomato", "swiggy", "restaurant", "cafe", "hotel", "food", "pizza",
        "burger", "biryani", "dhaba", "mess", "canteen", "dominos", "mcdonald",
        "kfc", "subway", "barbeque", "juice", "tea", "coffee"
    ],
    "Transport": [
        "uber", "ola", "rapido", "auto", "bus", "metro", "train", "irctc",
        "petrol", "fuel", "diesel", "parking", "toll", "cab", "taxi", "bike"
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "meesho", "ajio", "nykaa", "shopsy",
        "mall", "market", "store", "shop", "clothes", "footwear", "fashion"
    ],
    "Education": [
        "udemy", "coursera", "college", "university", "fees", "book", "library",
        "course", "class", "tuition", "exam", "stationary", "pen", "notebook"
    ],
    "Health & Medicine": [
        "pharmacy", "medicine", "medical", "hospital", "clinic", "doctor",
        "lab", "test", "apollo", "netmeds", "1mg", "medplus", "health"
    ],
    "Entertainment": [
        "netflix", "hotstar", "amazon prime", "spotify", "youtube", "movie",
        "cinema", "pvr", "inox", "game", "play", "event", "concert", "ott"
    ],
    "Utilities & Bills": [
        "electricity", "water", "gas", "internet", "broadband", "airtel", "jio",
        "vi", "vodafone", "bsnl", "recharge", "bill", "dth", "dish", "utility"
    ],
    "Rent & Housing": [
        "rent", "house", "flat", "apartment", "pg", "hostel", "maintenance",
        "society", "deposit", "landlord"
    ],
    "Groceries": [
        "blinkit", "zepto", "bigbasket", "dmart", "reliance fresh", "grocery",
        "vegetables", "fruits", "dairy", "milk", "rice", "flour", "dal", "oil"
    ],
    "Transfer & ATM": [
        "upi", "neft", "imps", "rtgs", "atm", "withdrawal", "transfer",
        "payment", "sent to", "received from", "bank"
    ]
}

def categorize_transaction(description: str) -> str:
    """
    Match a transaction description to a spending category.
    Returns 'Other' if no match found.
    """
    description_lower = description.lower()

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in description_lower:
                return category

    return "Other"
