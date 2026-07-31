# 🛡️ Credit Card Fraud Detection Using Machine Learning

## 📌 Project Overview

Financial institutions process millions of credit card transactions every day, making fraud detection a critical business challenge. The objective of this project was to evaluate multiple machine learning algorithms and recommend the most effective model for detecting fraudulent transactions while minimizing disruption to legitimate customers.

The project compares several classification models, evaluates their performance using appropriate metrics for an imbalanced dataset, and proposes a deployment strategy based on fraud risk scores.

---

## 🎯 Business Objective

Develop and evaluate machine learning models capable of:

- Maximizing fraud detection
- Minimizing false negatives
- Reducing unnecessary customer verification
- Supporting a risk-based fraud prevention strategy

---

## 📊 Dataset

The dataset contains:

- **1,000,000 credit card transactions**
- **7 fraud-related features**
- **Binary target variable (Fraud / Legitimate)**
- **No missing values**
- **Highly imbalanced classes**, reflecting real-world fraud detection scenarios

---

## 🔍 Project Workflow

### 1. Exploratory Data Analysis (EDA)

- Dataset exploration
- Feature correlation analysis
- Class imbalance assessment
- Distribution analysis

### 2. Data Preprocessing

- Train-test split (80/20)
- Feature scaling
- Oversampling of the minority class
- Comparison of preprocessing techniques

### 3. Model Development

The following machine learning models were evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- Bagging Classifier
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)
- Naive Bayes

---

## 📈 Model Evaluation

Models were compared using:

- Accuracy
- Precision
- Recall
- ROC-AUC
- Confusion Matrix
- 5-Fold Cross Validation

Because the dataset is highly imbalanced, particular emphasis was placed on **Precision**, **Recall**, and **ROC-AUC**, rather than overall accuracy.

---

## 🏆 Results

After evaluating all models:

✅ **Random Forest** achieved the best overall performance.

Key strengths:

- Highest Precision
- Excellent Recall
- Perfect ROC-AUC
- Stable cross-validation performance

---

## ⚙️ Threshold Optimization

Different decision thresholds were evaluated to understand the trade-off between fraud detection and customer experience.

| Decision Threshold | False Negatives | False Positives |
|-------------------|----------------:|----------------:|
| 0.50 (Default) | 2 | 0 |
| 0.40 | 1 | 0 |
| 0.10 | 0 | 26 |

The analysis showed that lowering the decision threshold eliminated missed fraud cases while requiring additional verification for only a small number of legitimate transactions.

---

## 💼 Business Recommendation

Deploy the **Random Forest** model as a **risk-scoring engine**.

Recommended decision strategy:

- 🟢 **Low Risk** → Approve transaction
- 🟡 **Medium Risk** → Additional verification (OTP / 2FA)
- 🔴 **High Risk** → Block transaction or send for manual review

This approach maximizes fraud detection while maintaining a positive customer experience.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Jupyter Notebook

---


## 👤 Author

**Katarzyna Grzyb**

Fraud Detection & Data Analytics Project