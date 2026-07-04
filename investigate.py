"""
CASE FILE #001: The Mystery of Customers Who Leave
----------------------------------------------------
A customer churn prediction "investigation" using a Random Forest classifier.
Dataset: IBM Telco Customer Churn (7,043 customer records).
"""

import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, roc_auc_score, confusion_matrix,
    classification_report
)

RANDOM_STATE = 42

# Paths relative to the repo root, regardless of where the script is run from
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(REPO_ROOT, "data", "telco.csv")
RESULTS_PATH = os.path.join(REPO_ROOT, "results", "case_results.json")
CHART_PATH = os.path.join(REPO_ROOT, "assets", "evidence_board.png")

# ---------------------------------------------------------------------------
# 1. GATHER THE EVIDENCE (load + clean data)
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)

# TotalCharges has some blank strings for brand-new customers -> coerce & fill
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())

df = df.drop(columns=["customerID"])

target = "Churn"
y = (df[target] == "Yes").astype(int)
X = df.drop(columns=[target])

# Encode categorical "suspects"
cat_cols = X.select_dtypes(include="object").columns.tolist()
num_cols = X.select_dtypes(exclude="object").columns.tolist()

encoders = {}
X_enc = X.copy()
for col in cat_cols:
    le = LabelEncoder()
    X_enc[col] = le.fit_transform(X_enc[col])
    encoders[col] = le

# ---------------------------------------------------------------------------
# 2. INTERROGATE THE SUSPECTS (train/test split + model)
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_enc, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

clf = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_leaf=3,
    random_state=RANDOM_STATE,
    class_weight="balanced",
)
clf.fit(X_train, y_train)

# ---------------------------------------------------------------------------
# 3. DELIVER THE VERDICT (evaluate)
# ---------------------------------------------------------------------------
y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=["Stayed", "Churned"], output_dict=True)

print(f"Accuracy : {accuracy:.4f}")
print(f"ROC AUC  : {auc:.4f}")
print("Confusion matrix:\n", cm)
print(classification_report(y_test, y_pred, target_names=["Stayed", "Churned"]))

# ---------------------------------------------------------------------------
# 4. RANK THE SUSPECTS (feature importance = "who's guilty")
# ---------------------------------------------------------------------------
importances = pd.Series(clf.feature_importances_, index=X_enc.columns)
top_suspects = importances.sort_values(ascending=False).head(8)
print("\nTop suspects (feature importance):")
print(top_suspects)

# Save results to disk so the report-writer can quote exact numbers
results = {
    "n_records": int(len(df)),
    "n_features": int(X.shape[1]),
    "churn_rate": float(y.mean()),
    "accuracy": float(accuracy),
    "roc_auc": float(auc),
    "confusion_matrix": cm.tolist(),
    "classification_report": report,
    "top_suspects": {k: float(v) for k, v in top_suspects.items()},
}
os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
with open(RESULTS_PATH, "w") as f:
    json.dump(results, f, indent=2)

# ---------------------------------------------------------------------------
# 5. PIN THE EVIDENCE BOARD (feature importance chart, detective-styled)
# ---------------------------------------------------------------------------
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(8, 5.5))
colors = plt.cm.Wistia(np.linspace(0.3, 0.9, len(top_suspects)))
bars = ax.barh(top_suspects.index[::-1], top_suspects.values[::-1], color=colors[::-1], edgecolor="#c0392b", linewidth=1.2)
ax.set_facecolor("#1b1b1b")
fig.patch.set_facecolor("#1b1b1b")
ax.set_title("TOP SUSPECTS IN THE CHURN CASE", fontsize=14, fontweight="bold", color="#e8c675", fontfamily="serif")
ax.set_xlabel("Weight of Evidence (feature importance)", color="#d8d0c0", fontfamily="serif")
ax.tick_params(colors="#d8d0c0")
for spine in ax.spines.values():
    spine.set_color("#5a4a3a")
plt.tight_layout()
os.makedirs(os.path.dirname(CHART_PATH), exist_ok=True)
plt.savefig(CHART_PATH, dpi=150, facecolor=fig.get_facecolor())
print(f"\nSaved: {RESULTS_PATH}")
print(f"Saved: {CHART_PATH}")
