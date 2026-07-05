"""
Montee - İlk Harcama Sınıflandırma Modeli (TF-IDF + Random Forest)
====================================================================
İşlem açıklamasından (description) harcama kategorisini (category) tahmin
eden ilk temel modeli eğitir.

Girdi : budgetwise_enriched.csv  (category + description kolonları)
Çıktı : model.pkl (eğitilmiş pipeline), classification_report.txt
"""

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, f1_score


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Kategorisi olmayan (label eksik) satırlar eğitim için kullanılamaz
    df = df.dropna(subset=["category", "description"])
    return df


def build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),   # tekli ve ikili kelime grupları (örn. "grocery store")
            max_features=5000,
        )),
        ("rf", RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced",  # kategoriler dengesiz olduğu için önemli
        )),
    ])


def train_and_evaluate(data_path: str, model_out: str, report_out: str):
    df = load_data(data_path)

    X = df["description"]
    y = df["category"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average="macro")
    report = classification_report(y_test, y_pred)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 (macro): {f1_macro:.4f}")
    print()
    print(report)

    joblib.dump(pipeline, model_out)
    with open(report_out, "w") as f:
        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(f"F1 (macro): {f1_macro:.4f}\n\n")
        f.write(report)

    return pipeline, accuracy, f1_macro


if __name__ == "__main__":
    train_and_evaluate(
        data_path="budgetwise_enriched.csv",
        model_out="expense_classifier.pkl",
        report_out="classification_report.txt",
    )
