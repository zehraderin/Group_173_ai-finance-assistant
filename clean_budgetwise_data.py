"""
Montee - BudgetWise Veri Temizleme Script'i
=============================================
Bu script, Kaggle'dan indirilen iki BudgetWise CSV dosyasını birleştirir ve temizler:
- budgetwise_finance_dataset.csv
- budgetwise_synthetic_dirty.csv

Temizlenen alanlar:
- category: 200+ yazım hatası varyantı -> 15 kanonik kategori (fuzzy matching)
- date: karışık tarih formatları -> tek standart format (YYYY-MM-DD)
- amount: para birimi sembolleri / virgüller / placeholder outlier'lar temizlenir -> float
- payment_mode: yazım hataları -> 4 kanonik ödeme yöntemi (fuzzy matching)
- location: kısaltmalar ve büyük/küçük harf tutarsızlıkları -> tam şehir ismi
- notes: anlamsız/rastgele karakter dizileri (test verisi kalıntıları) -> NaN

Çıktı: budgetwise_cleaned.csv
"""

import re
import pandas as pd
from rapidfuzz import process, fuzz

# ---------------------------------------------------------------------------
# 1. Veriyi yükle ve birleştir
# ---------------------------------------------------------------------------
def load_and_combine(path_a: str, path_b: str) -> pd.DataFrame:
    df_a = pd.read_csv(path_a)
    df_b = pd.read_csv(path_b)
    combined = pd.concat([df_a, df_b], ignore_index=True)
    return combined


# ---------------------------------------------------------------------------
# 2. Kategori normalizasyonu (fuzzy matching)
# ---------------------------------------------------------------------------
CANONICAL_CATEGORIES = [
    "Bonus", "Education", "Entertainment", "Food", "Freelance", "Health",
    "Investment", "Misc", "Other Income", "Others", "Rent", "Salary",
    "Savings", "Travel", "Utilities",
]
# Kısaltmalar gibi fuzzy matching'in yakalayamayacağı özel durumlar
CATEGORY_MANUAL_OVERRIDES = {
    "EDU": "Education",
}
_CANON_LOWER = [c.lower() for c in CANONICAL_CATEGORIES]


def normalize_category(raw_value) -> str | None:
    if pd.isna(raw_value):
        return None
    value = str(raw_value).strip()
    if value.upper() in CATEGORY_MANUAL_OVERRIDES:
        return CATEGORY_MANUAL_OVERRIDES[value.upper()]
    match, score, idx = process.extractOne(value.lower(), _CANON_LOWER, scorer=fuzz.ratio)
    return CANONICAL_CATEGORIES[idx] if score >= 60 else "Unknown"


# ---------------------------------------------------------------------------
# 3. Tarih normalizasyonu (çoklu format algılama)
# ---------------------------------------------------------------------------
def normalize_date(raw_value):
    if pd.isna(raw_value):
        return None
    parsed = pd.to_datetime(raw_value, errors="coerce", dayfirst=False)
    if pd.isna(parsed):
        # dayfirst formatlarını da (örn. 31-12-23) dene
        parsed = pd.to_datetime(raw_value, errors="coerce", dayfirst=True)
    return parsed


# ---------------------------------------------------------------------------
# 4. Tutar normalizasyonu (para birimi sembolleri, virgüller, outlier'lar)
# ---------------------------------------------------------------------------
AMOUNT_OUTLIER_PLACEHOLDER = 999_999_999
# Rs., ₹, $ gibi para birimi sembollerini ve binlik ayıraç virgüllerini
# tek bir regex ile temizler (birden fazla .replace() çağrısı yerine).
_CURRENCY_NOISE_PATTERN = re.compile(r"(Rs\.?|₹|\$|,)")


def normalize_amount(raw_value):
    if pd.isna(raw_value):
        return None
    text = _CURRENCY_NOISE_PATTERN.sub("", str(raw_value)).strip()
    try:
        value = float(text)
    except ValueError:
        return None
    if value == AMOUNT_OUTLIER_PLACEHOLDER:
        return None  # bariz placeholder / hatalı giriş
    return value


# ---------------------------------------------------------------------------
# 5. Ödeme yöntemi normalizasyonu (fuzzy matching)
# ---------------------------------------------------------------------------
CANONICAL_PAYMENT_MODES = ["Card", "Cash", "UPI", "Bank Transfer"]
_PAYMENT_LOWER = [p.lower() for p in CANONICAL_PAYMENT_MODES]


def normalize_payment_mode(raw_value):
    if pd.isna(raw_value):
        return None
    value = str(raw_value).strip()
    match, score, idx = process.extractOne(value.lower(), _PAYMENT_LOWER, scorer=fuzz.ratio)
    return CANONICAL_PAYMENT_MODES[idx] if score >= 55 else "Unknown"


# ---------------------------------------------------------------------------
# 6. Lokasyon normalizasyonu (kısaltmalar + büyük/küçük harf)
# ---------------------------------------------------------------------------
CITY_ABBREVIATIONS = {
    "BAN": "Bangalore", "BANGALORE": "Bangalore",
    "AHM": "Ahmedabad", "AHMEDABAD": "Ahmedabad",
    "LUC": "Lucknow", "LUCKNOW": "Lucknow",
    "KOL": "Kolkata", "KOLKATA": "Kolkata",
    "DEL": "Delhi", "DELHI": "Delhi",
    "CHE": "Chennai", "CHENNAI": "Chennai",
    "MUM": "Mumbai", "MUMBAI": "Mumbai",
    "JAI": "Jaipur", "JAIPUR": "Jaipur",
    "PUNE": "Pune", "HYDERABAD": "Hyderabad",
}


def normalize_location(raw_value):
    if pd.isna(raw_value):
        return None
    value = str(raw_value).strip()
    key = value.upper()
    return CITY_ABBREVIATIONS.get(key, value.title())


# ---------------------------------------------------------------------------
# 7. Notes alanındaki anlamsız/test verisi kalıntılarını temizleme
# ---------------------------------------------------------------------------
NOTES_JUNK_VALUES = {"test", "asdfgh", "xyz123", "...", "!!!", "misc"}
# Harf+rakam karışık, boşluksuz, 8 karakterden uzun rastgele string'leri yakalar
# (örn. 'hZtATyn1UX55solCMr1') - gerçek bir işlem notu bu formatta olmaz.
_RANDOM_STRING_PATTERN = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]{9,}$")


def clean_notes(raw_value):
    if pd.isna(raw_value):
        return None
    value = str(raw_value).strip()
    if value.lower() in NOTES_JUNK_VALUES:
        return None
    if _RANDOM_STRING_PATTERN.match(value):
        return None
    return value


# ---------------------------------------------------------------------------
# Ana pipeline
# ---------------------------------------------------------------------------
def clean_budgetwise(path_a: str, path_b: str) -> pd.DataFrame:
    df = load_and_combine(path_a, path_b)

    df["category_clean"] = df["category"].apply(normalize_category)
    df["date_clean"] = df["date"].apply(normalize_date)
    df["amount_clean"] = df["amount"].apply(normalize_amount)
    df["payment_mode_clean"] = df["payment_mode"].apply(normalize_payment_mode)
    df["location_clean"] = df["location"].apply(normalize_location)
    df["notes_clean"] = df["notes"].apply(clean_notes)

    result = df[[
        "transaction_id", "user_id", "date_clean", "transaction_type",
        "category_clean", "amount_clean", "payment_mode_clean",
        "location_clean", "notes_clean",
    ]].rename(columns={
        "date_clean": "date",
        "category_clean": "category",
        "amount_clean": "amount",
        "payment_mode_clean": "payment_mode",
        "location_clean": "location",
        "notes_clean": "notes",
    })
    return result


if __name__ == "__main__":
    cleaned = clean_budgetwise(
        "budgetwise_finance_dataset.csv",
        "budgetwise_synthetic_dirty.csv",
    )
    cleaned.to_csv("budgetwise_cleaned.csv", index=False)
    print("Temizlenmiş veri kaydedildi: budgetwise_cleaned.csv")
    print("Satır sayısı:", len(cleaned))
    print(cleaned.head(10))
