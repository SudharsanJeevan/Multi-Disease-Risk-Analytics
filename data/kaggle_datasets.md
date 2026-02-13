# Kaggle Dataset Links for Platform Expansion

This document lists all **Kaggle dataset** links for the 15 disease prediction models in the Multi-Disease Risk Analytics Platform.

## Original 5 Diseases

### 1. Diabetes
- **Dataset**: Pima Indians Diabetes Database
- **URL**: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database
-**Status**: ✅ Downloaded & Integrated

### 2. Heart Disease
- **Dataset**: Cleveland Clinic Heart Disease Dataset
- **URL**: https://www.kaggle.com/datasets/aavigan/cleveland-clinic-heart-disease-dataset
- **Status**: ✅ Downloaded & Integrated

### 3. Kidney Disease (CKD)
- **Dataset**: Chronic Kidney Disease Dataset
- **URL**: https://www.kaggle.com/datasets/mansoordaku/ckdisease
- **Status**: ✅ Downloaded & Integrated

### 4. Liver Disease
- **Dataset**: Indian Liver Patient Records
- **URL**: https://www.kaggle.com/datasets/uciml/indian-liver-patient-records
- **Status**: ✅ Downloaded & Integrated

### 5. Breast Cancer
- **Dataset**: Built-in sklearn Wisconsin Breast Cancer Dataset
- **URL**: `from sklearn.datasets import load_breast_cancer`
- **Status**: ✅ Integrated

---

## New 10 Diseases

### 6. Lung Cancer 🫁
- **Dataset**: Lung Cancer Prediction Dataset
- **URL**: https://www.kaggle.com/datasets/mysarahmadbhat/lung-cancer
- **Features**: 15 features including Gender, Age, Smoking, Yellow Fingers, Anxiety, Chronic Disease, etc.
- **Status**: ⏳ Pending Download

### 7. Stroke Risk 🧠
- **Dataset**: Stroke Prediction Dataset
- **URL**: https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset
- **Features**: 10 features including Gender, Age, Hypertension, Heart Disease, BMI, Smoking Status, etc.
- **Status**: ⏳ Pending Download

### 8. Parkinson's Disease 🤝
- **Dataset**: Parkinson's Disease Data Set
- **URL**: https://www.kaggle.com/datasets/vikasukani/parkinsons-disease-data-set
- **Features**: 22 voice measurement features (MDVP, Jitter, Shimmer, HNR, etc.)
- **Status**: ⏳ Pending Download

### 9. Thyroid Disorder 🦋
- **Dataset**: Thyroid Disease Data
- **URL**: https://www.kaggle.com/datasets/emmanuelfwerr/thyroid-disease-data
- **Features**: 11 features including Age, Sex, TSH, T3, TT4, T4U, FTI, etc.
- **Status**: ⏳ Pending Download

### 10. Anemia 🩸
- **Dataset**: Anemia Dataset
- **URL**: https://www.kaggle.com/datasets/biswaranjanrao/anemia-dataset
- **Features**: 5 features including Gender, Hemoglobin, MCH, MCHC, MCV
- **Status**: ⏳ Pending Download

### 11. Pneumonia 😷
- **Dataset**: Synthetic (Clinical Symptoms Based)
- **URL**: Will generate synthetic dataset
- **Features**: Age, Gender, Fever, Cough, Chest Pain, Difficulty Breathing, etc.
- **Note**: X-ray image datasets exist, but we're using symptom-based prediction
- **Status**: ⏳ To be generated

### 12. Tuberculosis (TB) 🦠
- **Dataset**: Synthetic (WHO Guidelines Based)
- **URL**: Will generate synthetic dataset
- **Features**: Age, Gender, Cough Duration, Night Sweats, Weight Loss, HIV Status, etc.
- **Note**: Creating based on WHO TB diagnosis criteria
- **Status**: ⏳ To be generated

### 13. Alzheimer's Risk 🧩
- **Dataset**: Alzheimer's Features
- **URL**: https://www.kaggle.com/datasets/brsdincer/alzheimer-features
- **Features**: Age, Gender, Education, MMSE Score, Functional Assessment, Memory, etc.
- **Status**: ⏳ Pending Download

### 14. COVID-19 Severity 🦠
- **Dataset**: COVID-19 Dataset
- **URL**: https://www.kaggle.com/datasets/meirnizri/covid19-dataset
- **Features**: Age, Gender, COVID Contact, Symptoms, Chronic Diseases, Pneumonia, etc.
- **Status**: ⏳ Pending Download

### 15. Skin Cancer (Melanoma) 🎨
- **Dataset**: Skin Cancer Malignant vs Benign
- **URL**: https://www.kaggle.com/datasets/fanconic/skin-cancer-malignant-vs-benign
- **Features**: Can use symptom-based or create from clinical data
- **Alternative**: Create synthetic with Age, Gender, Family History, Sun Exposure, Mole characteristics
- **Status**: ⏳ Pending Download

---

## Download Instructions

1. **Install Kaggle API**:
   ```bash
   pip install kaggle
   ```

2. **Set up Kaggle Credentials**:
   - Go to https://www.kaggle.com/account
   - Click "Create New API Token"
   - Save `kaggle.json` to `~/.kaggle/`

3. **Download Datasets** (I can provide individual commands):
   ```bash
   kaggle datasets download -d mysarahmadbhat/lung-cancer
   kaggle datasets download -d fedesoriano/stroke-prediction-dataset
   # ... etc
   ```

**OR** manually download from the URLs above and place in `data/raw/` directory.

---

## Next Steps

Once you download the datasets:
1. Place CSV files in `data/raw/` directory
2. I'll create training scripts for each
3. Train all models
4. Create prediction pages
5. Test the complete platform
