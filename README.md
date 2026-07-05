# 🗂️ Case File №001: The Mystery of Customers Who Leave

**Case Status:** Solved ✅

A customer churn "investigation" — Random Forest classifier trained on 7,043 real telecom customer records, wrapped in a detective-noir presentation.

🔗 **[View the interactive evidence board](./web/index.html)**

---

## The Case

**The Victim**
A telecom company, bleeding customers month after month, with no idea why.

**The Evidence**
7,043 customer records — contracts, bills, service history, the works. ([`data/telco.csv`](./data/telco.csv))

**The Suspects**
- 📜 Contract type
- 🕰️ Tenure (how long they'd been with us)
- 💳 Total & monthly charges
- 🛡️ Online security (or lack of it)
- 🛠️ Tech support (or lack of it)
- 🌐 Internet service type
- 💰 Payment method

**Lead Investigator**
Random Forest, 300 trees deep.

## The Verdict

| Metric | Reading |
|---|---|
| Accuracy | **76.9%** |
| ROC AUC | **0.84** |
| Churn recall | 73% |

Of the 374 customers who actually left, the model correctly flagged 273 of them.

## The Guilty Party (Ranked)

| Rank | Suspect | Weight of Evidence |
|---|---|---|
| 🥇 | Contract type | 18.6% |
| 🥈 | Tenure | 14.8% |
| 🥉 | Total charges | 12.5% |
| 4 | Monthly charges | 12.2% |
| 5 | Online security | 8.8% |
| 6 | Tech support | 6.8% |
| 7 | Internet service | 5.1% |
| 8 | Payment method | 4.3% |

The prime suspect isn't a mystery villain — it's the *month-to-month contract*. Customers with no commitment have no reason to stay. Combined with short tenure and no add-on services (security, tech support), the model can spot a flight risk almost as soon as they walk in.

## Repo Structure

```
churn-case-file/
├── README.md
├── requirements.txt
├── data/
│   └── telco.csv              # IBM Telco Customer Churn dataset
├── src/
│   └── investigate.py         # full ML pipeline (load → train → evaluate → chart)
├── results/
│   └── case_results.json      # metrics + feature importances from the last run
├── assets/
│   └── evidence_board.png     # noir-styled feature importance chart
└── web/
    ├── index.html             # interactive corkboard evidence board
    ├── style.css
    └── script.js
```

## Running the Investigation

```bash
git clone <this-repo>
cd churn-case-file
pip install -r requirements.txt
python src/investigate.py
```
unzip churn-case-file.zip
cd churn-case-file
git init
git add .
git commit -m "Case File №001: churn investigation"
git remote add origin <your-repo-url>
git push -u origin main

This regenerates `results/case_results.json` and `assets/evidence_board.png` from scratch.

To view the interactive evidence board, just open `web/index.html` in a browser (or serve the folder: `python3 -m http.server` from inside `web/`).

## Dataset

[IBM Telco Customer Churn](https://github.com/IBM/telco-customer-churn-on-icp4d) — 7,043 customers, 21 features, binary churn label.

---

📁 Case closed. Evidence filed above.
