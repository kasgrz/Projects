# 🛒 Amazon Customer Review Intelligence Dashboard

A Streamlit dashboard that transforms **158,000+ Amazon customer reviews** into actionable business insights using **Natural Language Processing (NLP)**.

Developed as the final project for the **Ironhack Data Analytics Bootcamp**.

---

## 📖 Project Overview

Customer reviews contain valuable information about customer satisfaction, product quality and recurring issues. However, manually analysing thousands of reviews is time-consuming and often impractical.

This project combines NLP techniques with interactive visualisations to automatically organise customer feedback, identify recurring themes, detect sentiment and prioritise high-risk reviews.

The result is an interactive dashboard that enables users to move from thousands of unstructured reviews to meaningful business insights within seconds.

---

## 🎯 Business Objectives

The dashboard helps businesses:

- 📈 Monitor review trends and product performance
- 💬 Understand why customers leave positive or negative reviews
- ⚠️ Identify reviews that may require immediate attention
- 📊 Support faster, data-driven business decisions

---

## 🧠 NLP Pipeline

To enrich the original dataset, the review text was preprocessed by:

- Converting text to lowercase
- Removing punctuation using regular expressions (Regex)
- Removing stop words
- Lemmatizing text using **spaCy**

A rule-based NLP pipeline was then applied using:

- Custom dictionaries
- Phrase matching
- Keyword matching
- Negation handling

This generated the following variables:

- **Primary Review Category**
- **Primary Customer Finding**
- **Overall Sentiment**

Additional engineered variables were created:

- **Escalation Score**
- **Overall Risk Level**

These enriched variables power all visualisations within the dashboard.

---

## 📊 Dashboard Features

### 📈 Product Analytics

- Monthly review trends
- Product comparison
- Brand comparison
- Interactive filtering

### 💬 Voice of Customer

- NLP-based review categorisation
- Customer findings
- Rating distribution by category
- Interactive Review Explorer
- Access to original customer reviews

### ⚠️ Risk Monitoring

- Risk KPIs
- Escalation score
- Overall risk level
- High-risk review identification
- Download filtered reviews

---

## 📂 Dataset

This project is based on the **Amazon Reviews 2023** dataset by McAuley Lab.

The original dataset is available at:
https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/tree/main/raw/meta_categories (meta_Sports_and_Outdoors.jsonl)
and https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/tree/main/raw/review_categories (Sports_and_Outdoors.jsonl)

The processed dataset used by the dashboard is not included in this repository because it exceeds GitHub's file size limit (100 MB).

To reproduce the dashboard data:
1. Download the original dataset.
2. Run the preprocessing and NLP notebook included in this repository.
3. The notebook generates the processed dataset required by the Streamlit dashboard.

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- spaCy
- Regular Expressions (Regex)
- Git & GitHub

---

## 📁 Project Structure


.
├── app.py (Product Analytics)
├── pages/
│   ├── Voice_of_Customer.py
│   └── Risk_Monitoring.py
├── requirements.txt
└── README.md
```

---

## 🚀 Running the Project

Clone the repository:

```bash
git clone https://github.com/kasgrz/Projects.git
```

Navigate to the project folder


Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

---

## 💼 Business Value

This solution enables organisations to:

- Reduce the effort required to analyse customer reviews manually.
- Detect recurring product and service issues.
- Understand the reasons behind customer satisfaction and dissatisfaction.
- Prioritise reviews that may represent reputational risk.
- Support faster and more informed business decisions.

---

## 🔮 Future Improvements

Potential future enhancements include:

- Transformer-based NLP models (e.g. BERT)
- Expanded product categories
- Improved custom dictionaries
- Automated alerts for critical reviews
- Predictive analytics for emerging customer issues

---

## 👩‍💻 Author

**Katarzyna Grzyb**

Final Project – Ironhack Data Analytics Bootcamp