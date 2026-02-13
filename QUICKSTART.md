# 🚀 Quick Start Guide

Get your Multi-Disease Risk Analytics System up and running in minutes!

## ⚡ Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum
- Internet connection (for downloading datasets)

---

## 📦 Step-by-Step Installation

### 1️⃣ Navigate to Project Directory

```powershell
cd "C:\Users\Ranjith\Final project"
```

### 2️⃣ Create Virtual Environment

```powershell
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

```powershell
.\venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 4️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install all required packages (~5 minutes).

---

## 📊 Download Datasets

### Quick Start (Use Sample Data)

The training scripts will automatically create sample data if real datasets are not found. Skip to Step 6 if you want to test quickly!

### For Real Data (Recommended for Final Project)

Download datasets from Kaggle and place them in `data/raw/`:

1. **Diabetes**: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database
   - Save as: `data/raw/diabetes.csv`

2. **Heart**: https://www.kaggle.com/datasets/aavigan/cleveland-clinic-heart-disease-dataset
   - Save as: `data/raw/heart.csv`

3. **Kidney**: https://www.kaggle.com/datasets/mansoordaku/ckdisease
   - Save as: `data/raw/kidney.csv`

4. **Liver**: https://www.kaggle.com/datasets/uciml/indian-liver-patient-records
   - Save as: `data/raw/liver.csv`

5. **Breast Cancer**: Built-in with scikit-learn (no download needed)

See `data/dataset_info.md` for detailed instructions.

---

## 🤖 Train Machine Learning Models

Train models for each disease (do this before running the app):

### Train All Models

```powershell
# Diabetes
python models/diabetes/train_diabetes.py

# Heart Disease
python models/heart/train_heart.py

# Kidney Disease
python models/kidney/train_kidney.py

# Liver Disease
python models/liver/train_liver.py

# Breast Cancer
python models/breast_cancer/train_breast_cancer.py
```

Each training script will:
- Load and preprocess data
- Train 6 different ML algorithms
- Compare and select the best model
- Save the model and scaler as `.pkl` files
- Show accuracy and evaluation metrics

**Training Time**: ~2-5 minutes per model

---

## 🌐 Launch the Application

Once at least one model is trained:

```powershell
streamlit run app.py
```

The app will automatically open in your browser at: `http://localhost:8501`

---

## 🎯 First Time Usage

### 1. Create Account

- Click "Sign Up"
- Enter username, email, and password
- Fill optional profile information
- Click "Create Account"

### 2. Login

- Enter your username and password
- Click "Login"

### 3. Make a Prediction

- Use the sidebar to select a disease
- Fill in the health parameters
- Click "Predict Risk"
- View results and download PDF report

### 4. View Analytics

- Go to "Analytics Dashboard" from sidebar
- See your prediction history
- View charts and statistics

---

## 📱 Application Pages

| Page | Description |
|------|-------------|
| 🏠 Home | Dashboard overview and recent activity |
| 💉 Diabetes | Test diabetes risk |
| ❤️ Heart Disease | Test heart disease risk |
| 🫘 Kidney Disease | Test kidney disease risk |
| 🫀 Liver Disease | Test liver disease risk |
| 🎀 Breast Cancer | Test breast cancer risk |
| 📊 Analytics | View prediction history and stats |
| 👤 Profile | Manage your account |

---

## ⚠️ Troubleshooting

### Issue: "Model not available"

**Solution**: Train the model first using the training script for that disease.

```powershell
python models/diabetes/train_diabetes.py
```

### Issue: "Dataset not found"

**Solution**: Either download the real dataset or let the script create sample data automatically.

### Issue: "Module not found"

**Solution**: Make sure virtual environment is activated and dependencies are installed.

```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Port already in use

**Solution**: Use a different port:

```powershell
streamlit run app.py --server.port 8502
```

### Issue: Database error

**Solution**: Delete `database.db` and restart the app to create a fresh database.

---

## 🎓 For Presentation/Demo

### Demo Flow

1. **Introduction** (2 min)
   - Show the homepage
   - Explain the 5 disease modules

2. **Feature Demo** (5 min)
   - Create a test account (live)
   - Make a diabetes prediction
   - Show risk visualization
   - Download PDF report
   - Show analytics dashboard

3. **Technical Overview** (3 min)
   - Show code structure
   - Explain ML models
   - Show training results

### Sample Test Values

Use these for quick demos:

**Diabetes** (High Risk):
- Pregnancies: 6, Glucose: 148, BP: 72
- Skin: 35, Insulin: 0, BMI: 33.6
- DPF: 0.627, Age: 50

**Heart** (Low Risk):
- Age: 30, Male, Chest Pain: 0
- BP: 120, Cholesterol: 180
- Max HR: 150

---

## 💡 Tips for Final Year Project

### Documentation Checklist

- [x] Project code complete
- [x] README.md with overview
- [x] Dataset documentation
- [x] Quick start guide
- [ ] Create presentation slides
- [ ] Record demo video
- [ ] Write project report

### Presentation Tips

1. **Start with Problem Statement**: Why multiple disease prediction?
2. **Show Live Demo**: Most impactful part
3. **Explain Technology**: ML algorithms, web framework
4. **Discuss Results**: Model accuracies, comparison
5. **Future Scope**: What can be improved

### Report Sections

1. Abstract
2. Introduction & Problem Statement
3. Literature Survey
4. System Design & Architecture
5. Implementation Details
6. Results & Analysis
7. Conclusion & Future Scope
8. References

---

## 📞 Need Help?

- Check `README.md` for detailed information
- Review `data/dataset_info.md` for dataset details
- Look at training script outputs for model performance
- Check configuration in `config.py`

---

## 🎉 You're All Set!

Your Multi-Disease Risk Analytics System is ready to use!

```powershell
# Quick commands to remember:
.\venv\Scripts\activate          # Activate virtual environment
streamlit run app.py              # Run the application
python models/[disease]/train_*   # Train a model
```

**Good luck with your final year project! 🚀**
