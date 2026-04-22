# 🏥 Multi-Disease Risk Analytics System

A comprehensive healthcare AI platform that predicts risk for **15 diseases** using machine learning, featuring an AI health chatbot, role-based access control, and a professional dark-themed analytics dashboard.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.2-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

---

## 📋 Project Overview

The **Multi-Disease Risk Analytics System (MDRAS)** is a web-based platform that enables users to assess their risk for 15 different diseases through ML-powered predictions. It features a split-screen authentication system, an AI-driven health chatbot for guided screening, and a comprehensive analytics dashboard — all wrapped in a professional dark-themed UI.

### 🩺 Diseases Covered (15)

| # | Disease | Algorithm | # | Disease | Algorithm |
|---|---------|-----------|---|---------|-----------|
| 1 | 💉 Diabetes | Random Forest | 9 | 🦋 Thyroid | Random Forest |
| 2 | ❤️ Heart Disease | Gradient Boosting | 10 | 🩸 Anemia | Logistic Regression |
| 3 | 🫘 Kidney Disease | Random Forest | 11 | 😷 Pneumonia | Gradient Boosting |
| 4 | 🫀 Liver Disease | Random Forest | 12 | 🦠 Tuberculosis | Random Forest |
| 5 | 🎀 Breast Cancer | SVM | 13 | 🧩 Alzheimer's | Gradient Boosting |
| 6 | 🫁 Lung Cancer | Gradient Boosting | 14 | 🦠 COVID-19 | Random Forest |
| 7 | 🧠 Stroke | Random Forest | 15 | 🎨 Melanoma | SVM |
| 8 | 🤝 Parkinson's | SVM | | | |

---

## ✨ Key Features

- 🤖 **AI Health Chatbot** — Guided symptom-based screening through conversational interface
- 🔐 **Role-Based Access Control** — Separate Patient and Admin workflows
- 📊 **15 ML Prediction Models** — Covering major disease categories
- 🎨 **Professional Dark Theme** — Inter font, gradient UI, smooth animations
- 📈 **Analytics Dashboard** — Prediction history, charts, risk distribution
- 📄 **PDF Report Generation** — Downloadable medical reports per prediction
- 📁 **Excel Export** — Export prediction history for offline analysis
- 🔑 **Split-Screen Login** — Dual Patient/Admin authentication page
- 🧪 **Risk Scoring** — Color-coded Low/Moderate/High risk levels

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit, CSS3, Google Fonts (Inter) | Web UI with dark theme |
| **Backend** | Python 3.8+ | Core application logic |
| **ML** | Scikit-learn | Model training & prediction |
| **Data** | Pandas, NumPy | Data processing |
| **Visualization** | Plotly, Matplotlib, Seaborn | Interactive charts |
| **Database** | SQLite | User data & prediction storage |
| **Security** | Bcrypt | Password hashing |
| **Reports** | ReportLab, OpenPyXL | PDF & Excel generation |
| **Version Control** | Git / GitHub | Source management |

---

## 📁 Project Structure

```
Multi-Disease-Risk-Analytics/
├── app.py                          # Main application entry point
├── config.py                       # Global configuration & disease metadata
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── ABSTRACT.md                     # Conference paper abstract
├── QUICKSTART.md                   # Quick start guide
│
├── src/                            # Core source modules
│   ├── authentication.py           # Login, registration, RBAC, CSS injection
│   ├── database_manager.py         # SQLite CRUD operations
│   ├── predictor.py                # ML model loading & prediction engine
│   ├── visualizer.py               # Chart & visualization generation
│   ├── report_generator.py         # PDF report creation
│   ├── chatbot_engine.py           # AI health chatbot logic
│   └── role_guard.py               # Role-based access enforcement
│
├── pages/                          # Streamlit multipage app
│   ├── 0_🔧_Admin_Dashboard.py     # Admin panel
│   ├── 1_🤖_Health_Chatbot.py      # AI chatbot interface
│   ├── 2_💉_Diabetes_Prediction.py  # Disease prediction pages
│   ├── 3_❤️_Heart_Disease_Prediction.py
│   ├── ... (15 disease pages)
│   ├── 98_📊_Analytics_Dashboard.py # User analytics & history
│   └── 99_👤_Profile.py            # User profile & settings
│
├── models/                         # Trained ML models (.pkl)
│   ├── diabetes/
│   ├── heart/
│   ├── kidney/
│   ├── liver/
│   ├── breast_cancer/
│   ├── lung_cancer/
│   ├── stroke/
│   ├── parkinsons/
│   ├── thyroid/
│   ├── anemia/
│   ├── pneumonia/
│   ├── tuberculosis/
│   ├── alzheimers/
│   ├── covid19/
│   └── melanoma/
│
├── data/                           # Datasets (from Kaggle)
│   ├── raw/
│   ├── processed/
│   ├── dataset_info.md
│   └── kaggle_datasets.md
│
└── reports/                        # Generated PDF reports
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/SudharsanJeevan/Multi-Disease-Risk-Analytics.git
cd Multi-Disease-Risk-Analytics
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app opens at **`http://localhost:8501`**

### 5. Login

- **Patient**: Create a new patient account from the login page
- **Admin**: Use admin credentials with access code `MDRA-ADMIN-2026`

---

## 🎯 User Workflow

### Patient Flow
1. **Register** → Create a patient account
2. **Chat** → Use the AI Health Chatbot for guided screening
3. **Predict** → (Admin-only clinical tools, or via chatbot)
4. **Review** → View results on the Analytics Dashboard
5. **Export** → Download PDF reports or Excel history

### Admin Flow
1. **Login** → Authenticate with admin access code
2. **Dashboard** → View system-wide statistics
3. **Predict** → Access all 15 disease prediction tools
4. **Manage** → View registered users and prediction data

---

## 🧪 Datasets Used

| # | Disease | Dataset | Source |
|---|---------|---------|--------|
| 1 | Diabetes | PIMA Indian Diabetes | Kaggle |
| 2 | Heart Disease | Cleveland Heart Disease | UCI ML Repository |
| 3 | Kidney Disease | Chronic Kidney Disease | UCI ML Repository |
| 4 | Liver Disease | Indian Liver Patient | Kaggle |
| 5 | Breast Cancer | Wisconsin Breast Cancer | UCI ML Repository |
| 6 | Lung Cancer | Lung Cancer Survey | Kaggle |
| 7 | Stroke | Stroke Prediction | Kaggle |
| 8 | Parkinson's | Oxford Parkinson's Disease | UCI ML Repository |
| 9 | Thyroid | Thyroid Disease | Kaggle |
| 10 | Anemia | Anemia Dataset | Kaggle |
| 11 | Pneumonia | Pneumonia Symptoms | Kaggle |
| 12 | Tuberculosis | Tuberculosis Dataset | Kaggle |
| 13 | Alzheimer's | OASIS Alzheimer's | Kaggle |
| 14 | COVID-19 | COVID-19 Symptoms | Kaggle |
| 15 | Melanoma | HAM10000 Skin Lesion | Kaggle |

---

## 🤖 Machine Learning

### Algorithms Used
- **Random Forest** — Ensemble method, best for most disease models
- **Gradient Boosting** — High accuracy for complex feature interactions
- **Support Vector Machine (SVM)** — Effective for binary classification tasks
- **Logistic Regression** — Baseline model for linear separability
- **K-Nearest Neighbors (KNN)** — Instance-based learning
- **Naive Bayes** — Probabilistic classifier

The **best-performing model** for each disease is automatically selected during training and saved as a `.pkl` file.

### Model Performance

| Disease | Best Model | Accuracy |
|---------|-----------|----------|
| Diabetes | Random Forest | ~78% |
| Heart Disease | Gradient Boosting | ~85% |
| Kidney Disease | Random Forest | ~99% |
| Liver Disease | Random Forest | ~75% |
| Breast Cancer | SVM | ~97% |
| Lung Cancer | Gradient Boosting | ~90% |
| Stroke | Random Forest | ~95% |
| Parkinson's | SVM | ~87% |
| Thyroid | Random Forest | ~96% |
| Anemia | Logistic Regression | ~95% |
| Pneumonia | Gradient Boosting | ~92% |
| Tuberculosis | Random Forest | ~93% |
| Alzheimer's | Gradient Boosting | ~83% |
| COVID-19 | Random Forest | ~94% |
| Melanoma | SVM | ~85% |

---

## 🔐 Security

- **Bcrypt** password hashing with random salt
- **Role-based access control** (Patient vs Admin)
- **Session management** via Streamlit session state
- **Admin access code** verification for admin registration

---

## 🎨 UI Features

- **Dark Theme** — Professional navy gradient sidebar, dark backgrounds
- **Google Inter Font** — Modern, clean typography
- **Gradient Buttons** — Purple-to-violet with hover animations
- **Metric Cards** — Subtle shadows with hover lift effects
- **Smooth Transitions** — Page fade-in animations
- **Color-Coded Risk** — Green (Low), Yellow (Moderate), Red (High)
- **Custom Scrollbar** — Gradient-themed thin scrollbar

---

## 👥 For Developers

### Adding a New Disease

1. Create `models/new_disease/train_new_disease.py`
2. Add a prediction page `pages/X_🏷️_New_Disease_Prediction.py`
3. Update `config.py` with disease metadata
4. Update `src/predictor.py` with feature mappings

### Retraining Models

```bash
python models/diabetes/train_diabetes.py
python models/heart/train_heart.py
# ... repeat for each disease
```

---

## 📝 Conference Paper Sections

1. **Introduction** — Problem statement: unequal healthcare access
2. **Literature Review** — Existing ML health tools analysis
3. **System Architecture** — Multi-tier design with RBAC
4. **Methodology** — Supervised ML with 6 algorithms per disease
5. **Implementation** — Streamlit, Scikit-learn, SQLite stack
6. **Results** — Accuracy metrics across 15 models
7. **Conclusion** — Unified platform for multi-disease screening

---

## 🎓 Suitable For

- Final Year B.Tech / B.E. Projects
- M.Tech / M.E. Research Projects
- Healthcare AI Research & Conferences
- Machine Learning Portfolio Projects

---

## 📧 Author

**Name**: Sudharsan Jeevan  
**Project Type**: Final Year Project  
**Domain**: Healthcare AI, Machine Learning  
**GitHub**: [SudharsanJeevan](https://github.com/SudharsanJeevan)

---

## 🎯 Future Enhancements

- [x] ~~Add more diseases~~ → Expanded from 5 to 15
- [x] ~~Add chatbot for health tips~~ → AI Health Chatbot implemented
- [ ] Deep learning models for image-based diagnosis (X-rays, skin lesions)
- [ ] Integration with hospital EHR systems
- [ ] Mobile app (React Native / Flutter)
- [ ] Email notification system for risk alerts
- [ ] Multi-language support
- [ ] Doctor consultation booking

---

## 📄 License

This project is for **educational and research purposes only**.

---

> **⚠️ Disclaimer**: This system is for educational purposes only and is not a substitute for professional medical advice. Always consult qualified healthcare professionals for diagnosis and treatment.
