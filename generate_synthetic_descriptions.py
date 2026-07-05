"""
Montee - Sentetik İşlem Açıklaması Üretici
============================================
Temizlenmiş BudgetWise verisindeki (budgetwise_cleaned.csv) her satıra,
kategorisine uygun, gerçekçi banka ekstresi tarzında İngilizce bir
işlem açıklaması (transaction description) üretir ve ekler.

Bu, TF-IDF + Random Forest modelinin öğreneceği asıl metin sinyalini sağlar
(gerçek veri setlerindeki 'notes' alanı kategoriyle ilişkisiz çıktığı için).

Girdi : budgetwise_cleaned.csv
Çıktı : budgetwise_enriched.csv  (yeni 'description' kolonu eklenmiş hali)
"""

import random
import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# ---------------------------------------------------------------------------
# Kategori bazlı gerçekçi merchant / işlem şablonları
# {merchant} yerine rastgele bir marka ismi konur, {ref} yerine rastgele bir
# referans/işlem numarası konur.
# ---------------------------------------------------------------------------
CATEGORY_TEMPLATES = {
    "Food": [
        "{merchant} PURCHASE", "SWIGGY ORDER #{ref}", "ZOMATO DELIVERY #{ref}",
        "{merchant} SUPERMARKET", "GROCERY STORE - {merchant}", "{merchant} RESTAURANT",
        "STARBUCKS #{ref}", "DOMINOS PIZZA ORDER", "{merchant} CAFE PAYMENT",
    ],
    "Rent": [
        "MONTHLY RENT PAYMENT", "RENT - APT {ref}", "HOUSE RENT TRANSFER",
        "LANDLORD PAYMENT REF {ref}", "RENTAL PAYMENT - UNIT {ref}",
    ],
    "Travel": [
        "UBER TRIP #{ref}", "OLA CAB RIDE", "IRCTC TICKET BOOKING",
        "{merchant} AIRLINES BOOKING", "MAKEMYTRIP HOTEL BOOKING",
        "PETROL PUMP - {merchant}", "TOLL PAYMENT #{ref}", "METRO CARD RECHARGE",
    ],
    "Utilities": [
        "ELECTRICITY BILL PAYMENT", "{merchant} POWER CORP BILL",
        "WATER BILL PAYMENT", "INTERNET BILL - {merchant} FIBER",
        "MOBILE RECHARGE #{ref}", "GAS BILL PAYMENT REF {ref}",
    ],
    "Entertainment": [
        "NETFLIX SUBSCRIPTION", "SPOTIFY PREMIUM", "{merchant} CINEMA TICKETS",
        "AMAZON PRIME VIDEO", "BOOKMYSHOW ORDER #{ref}", "DISNEY+ SUBSCRIPTION",
    ],
    "Education": [
        "{merchant} ONLINE COURSE", "UDEMY COURSE PURCHASE", "SCHOOL FEE PAYMENT",
        "COURSERA SUBSCRIPTION", "{merchant} TUITION FEE", "BOOKSTORE - {merchant}",
    ],
    "Health": [
        "{merchant} PHARMACY", "DOCTOR CONSULTATION FEE", "{merchant} HOSPITAL BILL",
        "GYM MEMBERSHIP - {merchant}", "MEDICAL LAB TEST #{ref}", "HEALTH INSURANCE PREMIUM",
    ],
    "Others": [
        "MISC PAYMENT #{ref}", "{merchant} GENERAL STORE", "ATM WITHDRAWAL",
        "MISCELLANEOUS EXPENSE",
    ],
    "Other Income": [
        "GIFT RECEIVED VIA APP", "CASHBACK CREDIT #{ref}", "REFUND - {merchant}",
        "MISC INCOME CREDIT",
    ],
    "Bonus": [
        "ANNUAL BONUS CREDIT", "PERFORMANCE BONUS #{ref}", "{merchant} BONUS PAYOUT",
    ],
    "Salary": [
        "SALARY CREDIT - {merchant}", "MONTHLY SALARY PAYMENT", "PAYROLL DEPOSIT #{ref}",
    ],
    "Savings": [
        "RECURRING DEPOSIT TRANSFER", "SAVINGS ACCOUNT TRANSFER", "FIXED DEPOSIT #{ref}",
    ],
    "Freelance": [
        "FREELANCE PAYMENT - {merchant}", "UPWORK PAYOUT #{ref}", "CLIENT PAYMENT RECEIVED",
    ],
    "Investment": [
        "MUTUAL FUND SIP - {merchant}", "STOCK PURCHASE #{ref}", "ZERODHA INVESTMENT",
    ],
    "Misc": [
        "MISC TRANSACTION #{ref}", "GENERAL PAYMENT", "UNCATEGORIZED EXPENSE",
    ],
}

# Her kategoriye özel, bağlamsal olarak anlamlı marka/merchant havuzu.
# (Genel bir havuz kullanmak "VODAFONE ONLINE COURSE" gibi saçma eşleşmeler
# üretiyordu - bunu önlemek için kategoriye özel isimler tanımlandı.)
CATEGORY_MERCHANTS = {
    "Food": ["BIG BAZAAR", "RELIANCE FRESH", "MORE SUPERMARKET", "SPENCER'S", "NATURE'S BASKET"],
    "Rent": [],  # şablonlarda merchant kullanılmıyor
    "Travel": ["INDIGO", "SPICEJET", "AIR INDIA", "VISTARA", "SHELL", "BHARAT PETROLEUM"],
    "Utilities": ["TATA POWER", "ADANI ELECTRICITY", "JIO FIBER", "AIRTEL BROADBAND", "BSES"],
    "Entertainment": ["PVR", "INOX", "CINEPOLIS"],
    "Education": ["UDEMY", "COURSERA", "BYJU'S", "UNACADEMY", "CROSSWORD BOOKSTORE"],
    "Health": ["APOLLO PHARMACY", "MEDPLUS", "FORTIS HOSPITAL", "MAX HOSPITAL", "CULT FIT"],
    "Others": ["LOCAL STORE", "GENERAL MART"],
    "Other Income": ["PAYTM", "GOOGLE PAY"],
    "Bonus": ["INFOSYS", "TCS", "WIPRO", "ACCENTURE"],
    "Salary": ["INFOSYS", "TCS", "WIPRO", "ACCENTURE", "HCL"],
    "Savings": [],
    "Freelance": ["UPWORK", "FIVERR", "TOPTAL"],
    "Investment": ["ZERODHA", "GROWW", "UPSTOX", "ICICI DIRECT"],
    "Misc": [],
}


def generate_description(category: str) -> str:
    templates = CATEGORY_TEMPLATES.get(category)
    if not templates:
        return "TRANSACTION"
    template = random.choice(templates)
    merchants = CATEGORY_MERCHANTS.get(category, [])
    merchant = random.choice(merchants) if merchants else ""
    return template.format(
        merchant=merchant,
        ref=fake.random_number(digits=5, fix_len=True),
    ).replace("  ", " ").strip()


def enrich_with_synthetic_descriptions(input_path: str, output_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    df["description"] = df["category"].apply(
        lambda c: generate_description(c) if pd.notna(c) else None
    )
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    result = enrich_with_synthetic_descriptions(
        "budgetwise_cleaned.csv", "budgetwise_enriched.csv"
    )
    print("Zenginleştirilmiş veri kaydedildi: budgetwise_enriched.csv")
    print("Satır sayısı:", len(result))
    print()
    print(result[["category", "description"]].dropna().sample(15, random_state=7).to_string())
