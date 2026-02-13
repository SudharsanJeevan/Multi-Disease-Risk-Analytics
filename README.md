# 🏥 Multi-Disease Risk Analytics System

A comprehensive healthcare AI platform that predicts risk for multiple diseases using machine learning and data analytics.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.2-orange.svg)

## 📋 Project Overview

This system provides intelligent disease risk prediction for **5 major diseases**:

1. 💉 **Diabetes Prediction**
2. ❤️ **Heart Disease Prediction**
3. 🫘 **Kidney Disease Prediction**
4. 🫀 **Liver Disease Prediction**
5. 🎀 **Breast Cancer Prediction**

## ✨ Key Features

- ✅ **Multi-Disease Prediction** - Single platform for 5 different diseases
- ✅ **Machine Learning Models** - Trained with 6+ algorithms per disease
- ✅ **User Authentication** - Secure login and signup system
- ✅ **Interactive Dashboard** - Real-time analytics and visualizations
- ✅ **Risk Analysis** - Color-coded risk levels (Low/Moderate/High)
- ✅ **PDF Reports** - Professional medical report generation
- ✅ **Prediction History** - Track all your test results
- ✅ **Beautiful UI** - Modern, responsive Streamlit interface

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| Web Framework | Streamlit |
| ML Library | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Database | SQLite |
| Reports | ReportLab |

## 📁 Project Structure

```
Final project/
├── app.py                      # Main application
├── config.py                   # Configuration
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
│
├── data/                      # Datasets
│   ├── raw/
│   ├── processed/
│   └── dataset_info.md
│
├── models/                    # ML Models
│   ├── diabetes/
│   ├── heart/
│   ├── kidney/
│   ├── liver/
│   └── breast_cancer/
│
├── notebooks/                 # Jupyter notebooks
│
├── src/                       # Source code
│   ├── authentication.py
│   ├── database_manager.py
│   ├── predictor.py
│   ├── visualizer.py
│   └── report_generator.py
│
├── pages/                     # Streamlit pages
│   ├── 1_🏠_Home.py
│   ├── 2_💉_Diabetes_Prediction.py
│   ├── 3_❤️_Heart_Disease_Prediction.py
│   └── ...
│
├── assets/                    # Images & styles
├── reports/                   # Generated reports
└── tests/                     # Test data
```

## 🚀 Installation

### 1. Clone or Download Project

```bash
cd "Final project"
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Datasets

Place datasets in `data/raw/` folder or they will be downloaded automatically.

### 5. Train Models

```bash
python models/diabetes/train_diabetes.py
python models/heart/train_heart.py
python models/kidney/train_kidney.py
python models/liver/train_liver.py
python models/breast_cancer/train_breast_cancer.py
```

## 🎯 Usage

### Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Workflow

1. **Sign Up** - Create a new account
2. **Login** - Access your dashboard
3. **Select Disease** - Choose which disease to test
4. **Enter Parameters** - Input your medical data
5. **Get Prediction** - View risk assessment
6. **Download Report** - Save PDF report
7. **View Analytics** - Check prediction history

## 🧪 Datasets Used

| Disease | Dataset | Source |
|---------|---------|--------|
| Diabetes | PIMA Indian Diabetes | Kaggle |
| Heart Disease | Cleveland Heart Disease | UCI ML Repository |
| Kidney Disease | Chronic Kidney Disease | UCI ML Repository |
| Liver Disease | Indian Liver Patient | Kaggle |
| Breast Cancer | Wisconsin Breast Cancer | UCI ML Repository |

## 🤖 Machine Learning Models

Each disease module tests **6 algorithms**:

- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- Naive Bayes

**Best performing model** for each disease is automatically selected and saved.

## 📊 Model Performance

| Disease | Best Model | Accuracy |
|---------|-----------|----------|
| Diabetes | Random Forest | 78%+ |
| Heart Disease | Random Forest | 85%+ |
| Kidney Disease | Random Forest | 99%+ |
| Liver Disease | Logistic Regression | 75%+ |
| Breast Cancer | SVM | 97%+ |

*Actual accuracies will be determined after training*

## 🎨 Features in Detail

### Disease Prediction
- Input medical parameters through user-friendly forms
- Real-time prediction with probability scores
- Visual risk indicators with color coding
- Personalized health recommendations

### Analytics Dashboard
- Comprehensive prediction history
- Interactive charts and graphs
- Risk trend analysis
- Comparative disease risk overview

### PDF Reports
- Professional medical report format
- Patient information and test parameters
- Prediction results and risk assessment
- Doctor's notes section
- Automated timestamp and ID generation

## 👥 For Developers

### Adding New Disease

1. Create folder in `models/new_disease/`
2. Add training script `train_new_disease.py`
3. Create prediction page in `pages/`
4. Update `src/predictor.py`
5. Add route in `app.py`

### Testing

```bash
pytest tests/ -v
```

## 📝 Project Report Sections

This project covers:

1. **Introduction** - Problem statement and objectives
2. **Literature Review** - Existing solutions analysis
3. **System Design** - Architecture and flowcharts
4. **Implementation** - Code and algorithms
5. **Results** - Model accuracy and screenshots
6. **Conclusion** - Summary and future scope

## 🎓 Suitable For

- Final Year B.Tech/B.E. Projects
- M.Tech/M.E. Projects
- Research Projects
- Healthcare AI Applications
- Portfolio Projects

## 📧 Author

**Name**: Ranjith  
**Project Type**: Final Year Project  
**Domain**: Healthcare AI, Machine Learning

## 📄 License

This project is for educational purposes.

## 🎯 Future Enhancements

- [ ] Add more diseases
- [ ] Implement deep learning models
- [ ] Add chatbot for health tips
- [ ] Email notification system
- [ ] Mobile app integration
- [ ] Multi-language support
- [ ] Doctor consultation booking

---

**⚠️ Disclaimer**: This system is for educational purposes only. Always consult qualified healthcare professionals for medical advice.
