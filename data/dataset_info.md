# Datasets Information

This document contains information about the datasets used in this project.

## 📊 Dataset Sources

### 1. Diabetes Dataset (PIMA Indian)

**Source**: [Kaggle - PIMA Indians Diabetes Database](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)

**Description**: This dataset is originally from the National Institute of Diabetes and Digestive and Kidney Diseases. The objective is to predict whether or not a patient has diabetes based on certain diagnostic measurements.

**Features** (8):
- Pregnancies: Number of times pregnant
- Glucose: Plasma glucose concentration (mg/dL)
- BloodPressure: Diastolic blood pressure (mm Hg)
- SkinThickness: Triceps skin fold thickness (mm)
- Insulin: 2-Hour serum insulin (μU/mL)
- BMI: Body mass index (weight in kg/(height in m)^2)
- DiabetesPedigreeFunction: Diabetes pedigree function
- Age: Age in years

**Target**: Outcome (0 or 1)

**Samples**: 768

---

### 2. Heart Disease Dataset (Cleveland)

**Source**: [Kaggle - Cleveland Heart Disease Dataset](https://www.kaggle.com/datasets/aavigan/cleveland-clinic-heart-disease-dataset)

**Description**: This database contains 76 attributes, but all published experiments refer to using a subset of 14 of them.

**Features** (11):
- Age: Age in years
- Sex: (1 = male; 0 = female)
- ChestPainType: Chest pain type (0-3)
- RestingBP: Resting blood pressure (mm Hg)
- Cholesterol: Serum cholesterol (mg/dL)
- FastingBS: Fasting blood sugar > 120 mg/dL (1 = true; 0 = false)
- RestingECG: Resting electrocardiographic results (0-2)
- MaxHR: Maximum heart rate achieved
- ExerciseAngina: Exercise induced angina (1 = yes; 0 = no)
- Oldpeak: ST depression induced by exercise
- ST_Slope: Slope of the peak exercise ST segment

**Target**: Heart disease (0 or 1)

**Samples**: ~920

---

### 3. Kidney Disease Dataset

**Source**: [Kaggle - Chronic Kidney Disease Dataset](https://www.kaggle.com/datasets/mansoordaku/ckdisease)

**Description**: Chronic kidney disease dataset with various clinical parameters.

**Features** (18):
- Age, Blood Pressure, Specific Gravity
- Albumin, Sugar, Red Blood Cells
- Pus Cell, Pus Cell Clumps, Bacteria
- Blood Glucose Random, Blood Urea
- Serum Creatinine, Sodium, Potassium
- Hemoglobin, Packed Cell Volume
- White Blood Cell Count, Red Blood Cell Count

**Target**: CKD (0 = no, 1 = yes)

**Samples**: 400

---

### 4. Liver Disease Dataset

**Source**: [Kaggle - Indian Liver Patient Records](https://www.kaggle.com/datasets/uciml/indian-liver-patient-records)

**Description**: This dataset contains liver patient records collected from North East of Andhra Pradesh, India.

**Features** (10):
- Age: Age of the patient
- Gender: Gender of the patient
- Total Bilirubin: Total bilirubin
- Direct Bilirubin: Direct bilirubin
- Alkaline Phosphatase: Alkaline phosphotase
- Alamine Aminotransferase: Alamine aminotransferase
- Aspartate Aminotransferase: Aspartate aminotransferase
- Total Proteins: Total proteins
- Albumin: Albumin
- Albumin and Globulin Ratio: Ratio of albumin and globulin

**Target**: Liver disease (1 or 2)

**Samples**: 583

---

### 5. Breast Cancer Dataset (Wisconsin)

**Source**: Built-in Scikit-learn dataset / [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic))

**Description**: Features computed from digitized images of fine needle aspirate (FNA) of breast mass.

**Features** (10 mean values):
- MeanRadius: Mean radius
- MeanTexture: Mean texture
- MeanPerimeter: Mean perimeter
- MeanArea: Mean area
- MeanSmoothness: Mean smoothness
- MeanCompactness: Mean compactness
- MeanConcavity: Mean concavity
- MeanConcavePoints: Mean concave points
- MeanSymmetry: Mean symmetry
- MeanFractalDimension: Mean fractal dimension

**Target**: Diagnosis (0 = benign, 1 = malignant)

**Samples**: 569

---

## 📥 How to Download Datasets

### Option 1: Manual Download (Recommended)

1. **Diabetes Dataset**:
   - Go to: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database
   - Download `diabetes.csv`
   - Save to: `data/raw/diabetes.csv`

2. **Heart Disease Dataset**:
   - Go to: https://www.kaggle.com/datasets/aavigan/cleveland-clinic-heart-disease-dataset
   - Download the CSV file
   - Save to: `data/raw/heart.csv`

3. **Kidney Disease Dataset**:
   - Go to: https://www.kaggle.com/datasets/mansoordaku/ckdisease
   - Download the dataset
   - Save to: `data/raw/kidney.csv`

4. **Liver Disease Dataset**:
   - Go to: https://www.kaggle.com/datasets/uciml/indian-liver-patient-records
   - Download `indian_liver_patient.csv`
   - Save to: `data/raw/liver.csv`

5. **Breast Cancer Dataset**:
   - This is available in scikit-learn
   - The training script will automatically load it
   - No manual download needed

### Option 2: Using Kaggle API

If you have Kaggle API configured:

```bash
# Install Kaggle API
pip install kaggle

# Download datasets
kaggle datasets download -d uciml/pima-indians-diabetes-database -p data/raw/
kaggle datasets download -d aavigan/cleveland-clinic-heart-disease-dataset -p data/raw/
kaggle datasets download -d mansoordaku/ckdisease -p data/raw/
kaggle datasets download -d uciml/indian-liver-patient-records -p data/raw/
```

---

## 🔍 Data Preprocessing Notes

All datasets require preprocessing:

1. **Handling Missing Values**: Some datasets have 0 values that represent missing data
2. **Feature Scaling**: StandardScaler is used for all datasets
3. **Encoding**: Categorical variables are encoded as numerical
4. **Train-Test Split**: 80-20 split used for all datasets

---

## 📌 Important Notes

- **Sample Data**: If datasets are not available, the training scripts will create sample data for demonstration purposes
- **Data Privacy**: All datasets are anonymized and publicly available
- **Research Use**: These datasets are primarily for educational and research purposes
- **Real Deployment**: For real medical applications, always use certified datasets and models

---

## 📖 References

1. UCI Machine Learning Repository: https://archive.ics.uci.edu/ml/index.php
2. Kaggle Datasets: https://www.kaggle.com/datasets
3. PIMA Indians Diabetes Database
4. Cleveland Heart Disease Database
5. Chronic Kidney Disease Dataset
6. Indian Liver Patient Records
7. Wisconsin Breast Cancer Diagnostic Dataset
