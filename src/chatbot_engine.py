"""
Health Chatbot Engine
Provides both clinical and symptom-based questions.
Maps symptom answers heuristically to clinical feature dicts for predictor.py.
"""

# ── 1. Admin Clinical Questions (Old DISEASE_QUESTIONS) ──
CLINICAL_QUESTIONS = {
    "diabetes": [
        {"key": "Pregnancies",  "question": "How many pregnancies have you had?", "type": "number", "min": 0, "max": 20, "default": 0},
        {"key": "Glucose",      "question": "What is your fasting blood glucose level (mg/dL)?", "type": "number", "min": 0, "max": 300, "default": 100},
        {"key": "BloodPressure", "question": "What is your resting blood pressure (mm Hg)?", "type": "number", "min": 0, "max": 200, "default": 70},
        {"key": "SkinThickness", "question": "Triceps skin fold thickness (mm)?", "type": "number", "min": 0, "max": 100, "default": 20},
        {"key": "Insulin",      "question": "2-hour serum insulin level (mu U/ml)?", "type": "number", "min": 0, "max": 900, "default": 80},
        {"key": "BMI",          "question": "What is your BMI?", "type": "number_float", "min": 10.0, "max": 70.0, "default": 25.0},
        {"key": "DiabetesPedigreeFunction", "question": "Diabetes pedigree function value?", "type": "number_float", "min": 0.0, "max": 2.5, "default": 0.5},
        {"key": "Age",          "question": "What is your age?", "type": "number", "min": 1, "max": 120, "default": 30},
    ],
    "heart": [
        {"key": "Age",            "question": "What is your age?", "type": "number", "min": 1, "max": 120, "default": 50},
        {"key": "Sex",            "question": "What is your sex?", "type": "select", "options": {"Male": 1, "Female": 0}},
        {"key": "ChestPainType",  "question": "Chest pain type?", "type": "select", "options": {"No pain": 0, "Mild": 1, "Moderate": 2, "Severe": 3}},
        {"key": "RestingBP",      "question": "Resting blood pressure (mm Hg)?", "type": "number", "min": 80, "max": 200, "default": 120},
        {"key": "Cholesterol",    "question": "Cholesterol level (mg/dL)?", "type": "number", "min": 100, "max": 600, "default": 200},
        {"key": "FastingBS",      "question": "Fasting blood sugar > 120 mg/dL?", "type": "yesno"},
        {"key": "RestingECG",     "question": "Any resting ECG abnormalities?", "type": "select", "options": {"Normal": 0, "ST-T": 1, "LVH": 2}},
        {"key": "MaxHR",          "question": "Maximum heart rate achieved?", "type": "number", "min": 60, "max": 250, "default": 150},
        {"key": "ExerciseAngina", "question": "Chest pain during exercise?", "type": "yesno"},
        {"key": "Oldpeak",        "question": "ST depression during exercise?", "type": "number_float", "min": 0.0, "max": 10.0, "default": 1.0},
        {"key": "ST_Slope",       "question": "ST segment slope?", "type": "select", "options": {"Upsloping": 0, "Flat": 1, "Downsloping": 2}},
    ],
    "kidney": [
        {"key": "Age", "question": "Age?", "type": "number", "min": 1, "max": 120, "default": 50},
        {"key": "BloodPressure", "question": "BP (mm Hg)?", "type": "number", "min": 50, "max": 200, "default": 80},
        {"key": "SpecificGravity", "question": "Specific gravity?", "type": "number_float", "min": 1.0, "max": 1.03, "default": 1.02},
        {"key": "Albumin", "question": "Albumin (0-5)?", "type": "number", "min": 0, "max": 5, "default": 0},
        {"key": "Sugar", "question": "Sugar (0-5)?", "type": "number", "min": 0, "max": 5, "default": 0},
        {"key": "BloodGlucoseRandom", "question": "Blood glucose (mg/dL)?", "type": "number", "min": 50, "max": 500, "default": 120},
        {"key": "BloodUrea", "question": "Blood urea?", "type": "number", "min": 1, "max": 200, "default": 30},
        {"key": "SerumCreatinine", "question": "Serum creatinine?", "type": "number_float", "min": 0.1, "max": 15.0, "default": 1.0},
        {"key": "Sodium", "question": "Sodium?", "type": "number", "min": 100, "max": 170, "default": 140},
        {"key": "Potassium", "question": "Potassium?", "type": "number_float", "min": 2.0, "max": 8.0, "default": 4.5},
        {"key": "Hemoglobin", "question": "Hemoglobin?", "type": "number_float", "min": 3.0, "max": 20.0, "default": 13.0},
        {"key": "PackedCellVolume", "question": "PCV (%)?", "type": "number", "min": 10, "max": 55, "default": 40},
        {"key": "WBC", "question": "WBC?", "type": "number", "min": 2000, "max": 25000, "default": 8000},
        {"key": "RBC", "question": "RBC?", "type": "number_float", "min": 2.0, "max": 8.0, "default": 5.0},
        {"key": "Hypertension", "question": "Hypertension?", "type": "yesno"},
        {"key": "DiabetesMellitus", "question": "Diabetes?", "type": "yesno"},
        {"key": "CoronaryArteryDisease", "question": "CAD?", "type": "yesno"},
        {"key": "Appetite", "question": "Appetite?", "type": "select", "options": {"Good": 0, "Poor": 1}},
    ],
    "liver": [
        {"key": "Age", "question": "Age?", "type": "number", "min": 1, "max": 120, "default": 40},
        {"key": "Gender", "question": "Gender?", "type": "select", "options": {"Male": 1, "Female": 0}},
        {"key": "TotalBilirubin", "question": "Total bilirubin?", "type": "number_float", "default": 1.0},
        {"key": "DirectBilirubin", "question": "Direct bilirubin?", "type": "number_float", "default": 0.3},
        {"key": "AlkalinePhosphatase", "question": "Alkaline phosphatase?", "type": "number", "default": 200},
        {"key": "AlamineAminotransferase", "question": "ALT/SGPT?", "type": "number", "default": 30},
        {"key": "AspartateAminotransferase", "question": "AST/SGOT?", "type": "number", "default": 30},
        {"key": "TotalProteins", "question": "Total proteins?", "type": "number_float", "default": 7.0},
        {"key": "Albumin", "question": "Albumin?", "type": "number_float", "default": 4.0},
        {"key": "AlbuminGlobulinRatio", "question": "A/G ratio?", "type": "number_float", "default": 1.0},
    ],
    "stroke": [
        {"key": "Gender", "question": "Gender?", "type": "select", "options": {"Male": 1, "Female": 0}},
        {"key": "Age", "question": "Age?", "type": "number", "min": 1, "default": 50},
        {"key": "Hypertension", "question": "Hypertension?", "type": "yesno"},
        {"key": "HeartDisease", "question": "Heart disease?", "type": "yesno"},
        {"key": "EverMarried", "question": "Ever married?", "type": "yesno"},
        {"key": "WorkType", "question": "Work type?", "type": "select", "options": {"Private": 0, "Self": 1, "Govt": 2, "Other": 3}},
        {"key": "ResidenceType", "question": "Residence?", "type": "select", "options": {"Urban": 1, "Rural": 0}},
        {"key": "AvgGlucoseLevel", "question": "Avg glucose?", "type": "number_float", "default": 100.0},
        {"key": "BMI", "question": "BMI?", "type": "number_float", "default": 25.0},
        {"key": "SmokingStatus", "question": "Smoking?", "type": "select", "options": {"Never": 0, "Former": 1, "Current": 2}},
    ],
    "thyroid": [
        {"key": "Age", "question": "Age?", "type": "number", "default": 40},
        {"key": "Sex", "question": "Sex?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "OnThyroxine", "question": "On thyroxine?", "type": "yesno"},
        {"key": "QueryOnThyroxine", "question": "Prescribed thyroxine?", "type": "yesno"},
        {"key": "ThyroidSurgery", "question": "Thyroid surgery?", "type": "yesno"},
        {"key": "Tumor", "question": "Tumor?", "type": "yesno"},
        {"key": "TSH", "question": "TSH?", "type": "number_float", "default": 2.0},
        {"key": "T3", "question": "T3?", "type": "number_float", "default": 2.0},
        {"key": "TT4", "question": "Total T4?", "type": "number_float", "default": 100.0},
        {"key": "T4U", "question": "T4 utilization?", "type": "number_float", "default": 1.0},
        {"key": "FTI", "question": "Free Thyroxine Index?", "type": "number_float", "default": 100.0},
    ],
    "anemia": [
        {"key": "Gender", "question": "Gender?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "Hemoglobin", "question": "Hemoglobin?", "type": "number_float", "default": 13.0},
        {"key": "MCH", "question": "MCH?", "type": "number_float", "default": 27.0},
        {"key": "MCHC", "question": "MCHC?", "type": "number_float", "default": 33.0},
        {"key": "MCV", "question": "MCV?", "type": "number_float", "default": 85.0},
    ],
    "pneumonia": [
        {"key": "Age", "question": "Age?", "type": "number", "default": 40},
        {"key": "Gender", "question": "Gender?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "Fever", "question": "Fever?", "type": "yesno"},
        {"key": "Cough", "question": "Cough?", "type": "yesno"},
        {"key": "ChestPain", "question": "Chest pain?", "type": "yesno"},
        {"key": "DifficultyBreathing", "question": "Difficulty breathing?", "type": "yesno"},
        {"key": "Fatigue", "question": "Fatigue?", "type": "yesno"},
        {"key": "SputumProduction", "question": "Sputum?", "type": "yesno"},
        {"key": "DurationOfSymptoms", "question": "Days of symptoms?", "type": "number", "default": 5},
        {"key": "SmokingHistory", "question": "Smoking history?", "type": "yesno"},
    ],
    "tuberculosis": [
        {"key": "Age", "question": "Age?", "type": "number", "default": 30},
        {"key": "Gender", "question": "Gender?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "CoughDuration", "question": "Cough weeks?", "type": "number", "default": 0},
        {"key": "NightSweats", "question": "Night sweats?", "type": "yesno"},
        {"key": "WeightLoss", "question": "Weight loss?", "type": "yesno"},
        {"key": "Fever", "question": "Fever?", "type": "yesno"},
        {"key": "ChestPain", "question": "Chest pain?", "type": "yesno"},
        {"key": "BloodInSputum", "question": "Blood in sputum?", "type": "yesno"},
        {"key": "HIVStatus", "question": "HIV positive?", "type": "yesno"},
        {"key": "PreviousTB", "question": "Previous TB?", "type": "yesno"},
        {"key": "BCGVaccination", "question": "BCG vaccine?", "type": "yesno"},
    ],
    "alzheimers": [
        {"key": "Age", "question": "Age?", "type": "number", "default": 70},
        {"key": "Gender", "question": "Gender?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "EducationLevel", "question": "Education years?", "type": "number", "default": 12},
        {"key": "MMSEScore", "question": "MMSE score (0-30)?", "type": "number", "default": 25},
        {"key": "FunctionalAssessment", "question": "Functional (0-30)?", "type": "number", "default": 20},
        {"key": "MemoryComplaints", "question": "Memory complaints?", "type": "yesno"},
        {"key": "BehavioralProblems", "question": "Behavioral problems?", "type": "yesno"},
        {"key": "ADL", "question": "ADL (0-28)?", "type": "number", "default": 20},
        {"key": "IADL", "question": "IADL (0-8)?", "type": "number", "default": 6},
        {"key": "CDR", "question": "Clinical Dementia Rating?", "type": "number_float", "default": 0.0},
    ],
    "covid19": [
        {"key": "Age", "question": "Age?", "type": "number", "default": 40},
        {"key": "Gender", "question": "Gender?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "COVIDContact", "question": "COVID contact?", "type": "yesno"},
        {"key": "Fever", "question": "Fever?", "type": "yesno"},
        {"key": "Cough", "question": "Cough?", "type": "yesno"},
        {"key": "SoreThroat", "question": "Sore throat?", "type": "yesno"},
        {"key": "ShortnessOfBreath", "question": "Shortness of breath?", "type": "yesno"},
        {"key": "HeadAche", "question": "Headache?", "type": "yesno"},
        {"key": "Diabetes", "question": "Diabetes?", "type": "yesno"},
        {"key": "Hypertension", "question": "Hypertension?", "type": "yesno"},
        {"key": "CardiovascularDisease", "question": "Cardiovascular?", "type": "yesno"},
        {"key": "Obesity", "question": "Obesity?", "type": "yesno"},
        {"key": "ChronicPulmonary", "question": "COPD?", "type": "yesno"},
        {"key": "Pneumonia", "question": "Pneumonia diagnosis?", "type": "yesno"},
    ],
    "melanoma": [
        {"key": "Age", "question": "Age?", "type": "number", "default": 40},
        {"key": "Gender", "question": "Gender?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "FamilyHistory", "question": "Family history?", "type": "yesno"},
        {"key": "SunExposure", "question": "Sun exposure (0-10)?", "type": "number", "default": 5},
        {"key": "MolesCount", "question": "Mole count?", "type": "number", "default": 10},
        {"key": "MoleChanges", "question": "Mole changes?", "type": "yesno"},
        {"key": "IrregularBorders", "question": "Irregular borders?", "type": "yesno"},
        {"key": "ColorVariation", "question": "Color variation?", "type": "yesno"},
        {"key": "Diameter", "question": "Diameter > 6mm?", "type": "yesno"},
        {"key": "Evolution", "question": "Evolution/Changing?", "type": "yesno"},
    ],
}


# ── 2. Patient Symptom Questions (Chatbot) ──
SYMPTOM_QUESTIONS = {
    "diabetes": [
        {"key": "s_age", "question": "First, what is your age?", "type": "number", "default": 30},
        {"key": "s_thirst", "question": "Have you been feeling excessively thirsty lately?", "type": "frequency"},
        {"key": "s_urine", "question": "Do you find yourself needing to urinate much more frequently than usual?", "type": "frequency"},
        {"key": "s_fatigue", "question": "Are you feeling unusually tired or fatigued during the day?", "type": "frequency"},
        {"key": "s_weight", "question": "Have you experienced any unexplained weight loss despite eating normally?", "type": "frequency"},
        {"key": "s_vision", "question": "Has your vision been blurry recently?", "type": "frequency"},
        {"key": "s_heal", "question": "Are you noticing that cuts or bruises are taking longer to heal?", "type": "frequency"},
        {"key": "s_family", "question": "Does anyone in your immediate family have diabetes?", "type": "yesno"},
        {"key": "s_overweight", "question": "Would you consider yourself overweight or obese?", "type": "yesno"},
    ],
    "heart": [
        {"key": "s_age", "question": "What is your age?", "type": "number", "default": 50},
        {"key": "s_gender", "question": "Are you male or female?", "type": "select", "options": {"Male": 1, "Female": 0}},
        {"key": "s_chest_pain", "question": "Do you experience any pain, pressure, or tightness in your chest?", "type": "frequency"},
        {"key": "s_chest_severe", "question": "If yes, is the pain severe or does it radiate to your arm/jaw?", "type": "yesno"},
        {"key": "s_breath", "question": "Do you get short of breath easily, especially during mild physical activity?", "type": "frequency"},
        {"key": "s_palp", "question": "Do you feel your heart racing, fluttering, or skipping beats?", "type": "frequency"},
        {"key": "s_dizzy", "question": "Do you ever feel dizzy or lightheaded, like you might faint?", "type": "frequency"},
        {"key": "s_bp_history", "question": "Have you ever been told by a doctor that you have high blood pressure?", "type": "yesno"},
        {"key": "s_chol_history", "question": "Have you ever been told you have high cholesterol?", "type": "yesno"},
    ],
    "kidney": [
        {"key": "s_age", "question": "What is your age?", "type": "number", "default": 50},
        {"key": "s_urine_color", "question": "Have you noticed your urine being dark, foamy, or bloody?", "type": "frequency"},
        {"key": "s_swelling", "question": "Have you experienced swelling in your hands, feet, or around your eyes?", "type": "frequency"},
        {"key": "s_fatigue", "question": "Are you feeling extremely exhausted and weak lately?", "type": "frequency"},
        {"key": "s_appetite", "question": "Have you lost your appetite, or do you feel a metallic taste in your mouth?", "type": "frequency"},
        {"key": "s_bp_history", "question": "Do you have a history of high blood pressure?", "type": "yesno"},
        {"key": "s_diabetes_history", "question": "Do you have a history of diabetes?", "type": "yesno"},
    ],
    "liver": [
        {"key": "s_age", "question": "What is your age?", "type": "number", "default": 40},
        {"key": "s_gender", "question": "Are you male or female?", "type": "select", "options": {"Male": 1, "Female": 0}},
        {"key": "s_jaundice", "question": "Have you noticed any yellowish tint to your skin or the whites of your eyes?", "type": "frequency"},
        {"key": "s_abdomen", "question": "Are you experiencing pain or swelling in your upper right abdomen?", "type": "frequency"},
        {"key": "s_fatigue", "question": "Do you feel constantly tired or fatigued?", "type": "frequency"},
        {"key": "s_nausea", "question": "Have you been experiencing nausea or vomiting?", "type": "frequency"},
        {"key": "s_stool", "question": "Have you noticed your urine being unusually dark or your stool being pale/clay-colored?", "type": "frequency"},
    ],
    "stroke": [
        {"key": "s_age", "question": "What is your age?", "type": "number", "default": 55},
        {"key": "s_gender", "question": "Are you male or female?", "type": "select", "options": {"Male": 1, "Female": 0}},
        {"key": "s_face", "question": "Have you experienced sudden numbness or drooping on one side of your face?", "type": "yesno"},
        {"key": "s_arm", "question": "Have you had sudden weakness or numbness in one arm or leg?", "type": "yesno"},
        {"key": "s_speech", "question": "Are you having trouble speaking or understanding speech?", "type": "yesno"},
        {"key": "s_vision", "question": "Have you had sudden blurred or decreased vision in one or both eyes?", "type": "yesno"},
        {"key": "s_headache", "question": "Have you experienced a sudden, severe headache with no known cause?", "type": "yesno"},
        {"key": "s_bp", "question": "Do you have a history of high blood pressure?", "type": "yesno"},
        {"key": "s_smoke", "question": "Do you currently smoke?", "type": "yesno"},
    ],
    "thyroid": [
        {"key": "s_age", "question": "What is your age?", "type": "number", "default": 40},
        {"key": "s_gender", "question": "Are you male or female?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "s_weight", "question": "Have you had unexplained weight gain or weight loss recently?", "type": "frequency"},
        {"key": "s_temp", "question": "Are you unusually sensitive to cold or heat?", "type": "frequency"},
        {"key": "s_fatigue", "question": "Do you feel excessively tired, sluggish, or conversely, overly jittery and anxious?", "type": "frequency"},
        {"key": "s_hair", "question": "Have you noticed your hair becoming dry, brittle, or thinning?", "type": "frequency"},
        {"key": "s_neck", "question": "Do you have any swelling or a noticeable lump in your neck (goiter)?", "type": "yesno"},
    ],
    "anemia": [
        {"key": "s_gender", "question": "Are you male or female?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "s_fatigue", "question": "Are you feeling constantly tired or weak?", "type": "frequency"},
        {"key": "s_pale", "question": "Does your skin appear paler or more yellowish than usual?", "type": "frequency"},
        {"key": "s_breath", "question": "Do you get short of breath easily, even with minor exertion?", "type": "frequency"},
        {"key": "s_cold", "question": "Do your hands and feet frequently feel unusually cold?", "type": "frequency"},
        {"key": "s_dizzy", "question": "Do you experience dizziness or lightheadedness upon standing?", "type": "frequency"},
    ],
    "pneumonia": [
        {"key": "s_age", "question": "What is your age?", "type": "number", "default": 40},
        {"key": "s_gender", "question": "Are you male or female?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "s_fever", "question": "Do you have a high fever, sweating, or shaking chills?", "type": "frequency"},
        {"key": "s_cough", "question": "Do you have a cough that produces greenish, yellow, or even bloody mucus?", "type": "frequency"},
        {"key": "s_chest", "question": "Do you feel sharp chest pain that gets worse when you breathe deeply or cough?", "type": "frequency"},
        {"key": "s_breath", "question": "Are you experiencing shortness of breath, even while resting?", "type": "frequency"},
        {"key": "s_duration", "question": "How many days have you felt this way?", "type": "number", "default": 3},
    ],
    "tuberculosis": [
        {"key": "s_age", "question": "What is your age?", "type": "number", "default": 30},
        {"key": "s_gender", "question": "Are you male or female?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "s_cough_weeks", "question": "How many weeks have you had a persistent cough?", "type": "number", "default": 0},
        {"key": "s_blood_cough", "question": "Have you been coughing up blood or thick mucus?", "type": "frequency"},
        {"key": "s_night_sweats", "question": "Do you wake up drenched in sweat during the night?", "type": "frequency"},
        {"key": "s_weight_loss", "question": "Have you lost significant weight without trying?", "type": "frequency"},
        {"key": "s_fever", "question": "Do you have a low-grade fever that won't go away?", "type": "frequency"},
    ],
    "alzheimers": [
        {"key": "s_age", "question": "What is the patient's age?", "type": "number", "default": 70},
        {"key": "s_gender", "question": "Is the patient male or female?", "type": "select", "options": {"Male": 0, "Female": 1}},
        {"key": "s_memory", "question": "Is the patient experiencing frequent memory loss that disrupts daily life?", "type": "frequency"},
        {"key": "s_tasks", "question": "Do they have difficulty completing familiar tasks at home or work?", "type": "frequency"},
        {"key": "s_confusion", "question": "Are they frequently confused about time or place?", "type": "frequency"},
        {"key": "s_words", "question": "Are they struggling to find the right words or follow a conversation?", "type": "frequency"},
        {"key": "s_behavior", "question": "Have you noticed significant changes in their mood or personality?", "type": "frequency"},
    ],
    "covid19": [
        {"key": "s_age", "question": "What is your age?", "type": "number", "default": 40},
        {"key": "s_fever", "question": "Do you have a fever or chills?", "type": "yesno"},
        {"key": "s_cough", "question": "Do you have a new, continuous dry cough?", "type": "frequency"},
        {"key": "s_taste_smell", "question": "Have you lost your sense of taste or smell?", "type": "yesno"},
        {"key": "s_breath", "question": "Are you experiencing shortness of breath or difficulty breathing?", "type": "frequency"},
        {"key": "s_contact", "question": "Have you been in close contact with someone who tested positive for COVID-19?", "type": "yesno"},
        {"key": "s_throat_body", "question": "Do you have a sore throat, muscle aches, or severe headache?", "type": "frequency"},
    ],
    "melanoma": [
        {"key": "s_age", "question": "What is your age?", "type": "number", "default": 40},
        {"key": "s_sun", "question": "Do you have a history of severe sunburns or frequent tanning?", "type": "yesno"},
        {"key": "s_moles_many", "question": "Do you have a large number of moles (more than 50) on your body?", "type": "yesno"},
        {"key": "s_mole_change", "question": "Have you noticed any mole change its size, shape, or color recently?", "type": "yesno"},
        {"key": "s_mole_asym", "question": "Does the mole look asymmetrical or have jagged, irregular borders?", "type": "yesno"},
        {"key": "s_mole_color", "question": "Does the mole have uneven coloring (shades of brown, black, or red)?", "type": "yesno"},
        {"key": "s_mole_bleed", "question": "Is the mole itching, oozing, or bleeding?", "type": "yesno"},
    ],
}


# ── 3. Processing Functions ──

def get_questions(disease_type, is_admin=False):
    """Returns clinical questions for Admin, symptom questions for Patient."""
    if is_admin:
        return CLINICAL_QUESTIONS.get(disease_type, [])
    return SYMPTOM_QUESTIONS.get(disease_type, [])

def process_clinical_answers(disease_type, answers):
    """Direct mapping (for exact admin form inputs)."""
    questions = get_questions(disease_type, is_admin=True)
    features = {}
    for q in questions:
        key = q["key"]
        raw = answers.get(key)
        if q["type"] == "yesno":
            features[key] = 1 if raw == "Yes" else 0
        elif q["type"] == "select":
            features[key] = q["options"].get(raw, 0)
        else:
            features[key] = raw if raw is not None else q.get("default", 0)
    return features


def get_severity(ans):
    """Maps nuanced frequency answers to a severity scale."""
    mapping = {"Never": 0, "No": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Yes": 3}
    return mapping.get(str(ans).strip(), 0)

def is_present(ans):
    """True if symptom is at least 'Sometimes' or 'Yes'."""
    return get_severity(ans) >= 2


def process_symptom_answers(disease_type, answers):
    """
    Heuristic rule engine:
    Takes symptom Yes/No/Frequency answers and maps them to ESTIMATED numerical/categorical 
    clinical values required by the ML models.
    """
    f = {}
    
    if disease_type == "diabetes":
        # Base clinical defaults
        f["Pregnancies"] = 0
        f["Glucose"] = 90
        f["BloodPressure"] = 70
        f["SkinThickness"] = 20
        f["Insulin"] = 50
        f["BMI"] = 23.0
        f["DiabetesPedigreeFunction"] = 0.3
        f["Age"] = int(answers.get("s_age", 30))
        
        # Thirst & Urine are strong indicators
        thirst_sev = get_severity(answers.get("s_thirst"))
        urine_sev = get_severity(answers.get("s_urine"))
        if thirst_sev >= 2 or urine_sev >= 2:
            f["Glucose"] += (20 * max(thirst_sev, urine_sev))
            f["Insulin"] += 80
            
        if is_present(answers.get("s_fatigue")) or is_present(answers.get("s_vision")):
            f["Glucose"] += 30
            
        if is_present(answers.get("s_overweight")):
            f["BMI"] = 32.0
            f["BloodPressure"] += 15
            
        if is_present(answers.get("s_family")):
            f["DiabetesPedigreeFunction"] = 1.2
            
    elif disease_type == "heart":
        # Order: Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope
        chest_pain_sev = get_severity(answers.get("s_chest_pain"))
        if is_present(answers.get("s_chest_severe")):
            cpt = 3; ea = 1; op = 3.0; sts = 2
        elif chest_pain_sev >= 2:
            cpt = chest_pain_sev - 1; ea = 1; op = 1.5; sts = 1
        else:
            cpt = 0; ea = 0; op = 0.5; sts = 1

        f["Age"] = int(answers.get("s_age", 50))
        f["Sex"] = answers.get("s_gender", 1)
        f["ChestPainType"] = cpt
        f["RestingBP"] = 150 if is_present(answers.get("s_bp_history")) else 120
        f["Cholesterol"] = 260 if is_present(answers.get("s_chol_history")) else 190
        f["FastingBS"] = 0
        f["RestingECG"] = 0
        f["MaxHR"] = 110 if is_present(answers.get("s_breath")) else 150
        f["ExerciseAngina"] = ea
        f["Oldpeak"] = op
        f["ST_Slope"] = sts
            
    elif disease_type == "kidney":
        # Order: Age, BloodPressure, SpecificGravity, Albumin, Sugar, RedBloodCells, PusCell, PusCellClumps, Bacteria,
        #        BloodGlucoseRandom, BloodUrea, SerumCreatinine, Sodium, Potassium, Hemoglobin, PackedCellVolume,
        #        WhiteBloodCellCount, RedBloodCellCount
        has_urine_issue = is_present(answers.get("s_urine_color")) or is_present(answers.get("s_swelling"))
        has_fatigue = is_present(answers.get("s_fatigue"))

        f["Age"] = int(answers.get("s_age", 50))
        f["BloodPressure"] = 80
        f["SpecificGravity"] = 1.01 if has_urine_issue else 1.02
        f["Albumin"] = 3 if has_urine_issue else 0
        f["Sugar"] = 0
        f["RedBloodCells"] = 0  # 0=normal
        f["PusCell"] = 0  # 0=normal
        f["PusCellClumps"] = 1 if has_urine_issue else 0
        f["Bacteria"] = 0
        f["BloodGlucoseRandom"] = 110
        f["BloodUrea"] = 80 if has_urine_issue else 35
        f["SerumCreatinine"] = 3.5 if has_urine_issue else 1.0
        f["Sodium"] = 140
        f["Potassium"] = 4.5
        f["Hemoglobin"] = 9.0 if has_fatigue else 14.0
        f["PackedCellVolume"] = 28 if has_fatigue else 42
        f["WhiteBloodCellCount"] = 7000
        f["RedBloodCellCount"] = 3.5 if has_fatigue else 5.2
        
        if is_present(answers.get("s_bp_history")):
            f["BloodPressure"] = 100
            
    elif disease_type == "liver":
        f["Age"] = int(answers.get("s_age", 40))
        f["Gender"] = answers.get("s_gender", 1)
        f["TotalBilirubin"] = 1.0
        f["DirectBilirubin"] = 0.3
        f["AlkalinePhosphatase"] = 180
        f["AlamineAminotransferase"] = 30
        f["AspartateAminotransferase"] = 30
        f["TotalProteins"] = 7.0
        f["Albumin"] = 4.0
        f["AlbuminGlobulinRatio"] = 1.2
        
        if is_present(answers.get("s_jaundice")) or is_present(answers.get("s_stool")):
            f["TotalBilirubin"] = 6.0
            f["DirectBilirubin"] = 3.5
            f["AlkalinePhosphatase"] = 450
        if is_present(answers.get("s_abdomen")):
            f["AlamineAminotransferase"] = 150
            f["AspartateAminotransferase"] = 120
        if is_present(answers.get("s_fatigue")):
            f["Albumin"] = 2.8
            f["AlbuminGlobulinRatio"] = 0.8
            
    elif disease_type == "stroke":
        # Order: Gender, Age, Hypertension, HeartDisease, EverMarried, WorkType, ResidenceType, AvgGlucoseLevel, BMI, SmokingStatus
        age_val = int(answers.get("s_age", 55))
        f["Gender"] = answers.get("s_gender", 1)
        f["Age"] = age_val
        f["Hypertension"] = 1 if is_present(answers.get("s_bp")) else 0
        f["HeartDisease"] = 0
        f["EverMarried"] = 1 if age_val > 30 else 0
        f["WorkType"] = 0
        f["ResidenceType"] = 1
        f["AvgGlucoseLevel"] = 95.0
        f["BMI"] = 26.0
        f["SmokingStatus"] = 2 if is_present(answers.get("s_smoke")) else 0
        
        risk_score = 0
        if is_present(answers.get("s_face")): risk_score += 1
        if is_present(answers.get("s_arm")): risk_score += 1
        if is_present(answers.get("s_speech")): risk_score += 1
        
        if risk_score >= 1:
            f["Hypertension"] = 1
            f["HeartDisease"] = 1
            f["AvgGlucoseLevel"] = 180.0
            f["BMI"] = 33.0
            
    elif disease_type == "thyroid":
        f["Age"] = int(answers.get("s_age", 40))
        f["Sex"] = answers.get("s_gender", 1)
        f["OnThyroxine"] = 0
        f["QueryOnThyroxine"] = 0
        f["ThyroidSurgery"] = 0
        f["Tumor"] = 0
        f["TSH"] = 2.0
        f["T3"] = 2.0
        f["TT4"] = 100.0
        f["T4U"] = 1.0
        f["FTI"] = 100.0
        
        if is_present(answers.get("s_neck")):
            f["Tumor"] = 1
            
        if is_present(answers.get("s_weight")) and is_present(answers.get("s_fatigue")):
            f["TSH"] = 20.0  
            f["T3"] = 0.5
            f["TT4"] = 40.0
            f["FTI"] = 40.0
            
    elif disease_type == "anemia":
        f["Gender"] = answers.get("s_gender", 1)
        f["Hemoglobin"] = 13.0 if f["Gender"]==0 else 12.0
        f["MCH"] = 28.0
        f["MCHC"] = 33.0
        f["MCV"] = 85.0
        
        symp_count = 0
        if is_present(answers.get("s_fatigue")): symp_count += 1
        if is_present(answers.get("s_pale")): symp_count += 2
        if is_present(answers.get("s_breath")): symp_count += 1
        if is_present(answers.get("s_dizzy")): symp_count += 1
        
        if symp_count >= 2:
            f["Hemoglobin"] -= 4.0
            f["MCH"] -= 8.0
            f["MCHC"] -= 4.0
            f["MCV"] -= 15.0
            
    elif disease_type == "pneumonia":
        f["Age"] = int(answers.get("s_age", 40))
        f["Gender"] = answers.get("s_gender", 1)
        f["Fever"] = 1 if is_present(answers.get("s_fever")) else 0
        f["Cough"] = 1 if is_present(answers.get("s_cough")) else 0
        f["ChestPain"] = 1 if is_present(answers.get("s_chest")) else 0
        f["DifficultyBreathing"] = 1 if is_present(answers.get("s_breath")) else 0
        f["Fatigue"] = f["Fever"]
        f["SputumProduction"] = f["Cough"]
        f["DurationOfSymptoms"] = int(answers.get("s_duration", 3))
        f["SmokingHistory"] = 0
        
    elif disease_type == "tuberculosis":
        f["Age"] = int(answers.get("s_age", 30))
        f["Gender"] = answers.get("s_gender", 1)
        f["CoughDuration"] = int(answers.get("s_cough_weeks", 0))
        f["NightSweats"] = 1 if is_present(answers.get("s_night_sweats")) else 0
        f["WeightLoss"] = 1 if is_present(answers.get("s_weight_loss")) else 0
        f["Fever"] = 1 if is_present(answers.get("s_fever")) else 0
        f["ChestPain"] = 1 if f["CoughDuration"] > 2 else 0
        f["BloodInSputum"] = 1 if is_present(answers.get("s_blood_cough")) else 0
        f["HIVStatus"] = 0
        f["PreviousTB"] = 0
        f["BCGVaccination"] = 0
        
    elif disease_type == "alzheimers":
        f["Age"] = int(answers.get("s_age", 70))
        f["Gender"] = answers.get("s_gender", 1)
        f["EducationLevel"] = 12
        f["MMSEScore"] = 28
        f["FunctionalAssessment"] = 25
        f["MemoryComplaints"] = 1 if is_present(answers.get("s_memory")) else 0
        f["BehavioralProblems"] = 1 if is_present(answers.get("s_behavior")) else 0
        f["ADL"] = 26
        f["IADL"] = 8
        f["CDR"] = 0.0
        
        if is_present(answers.get("s_confusion")) or is_present(answers.get("s_tasks")):
            f["MMSEScore"] = 18
            f["FunctionalAssessment"] = 12
            f["ADL"] = 15
            f["IADL"] = 3
            f["CDR"] = 1.0
            
    elif disease_type == "covid19":
        # Order: Age, Gender, COVIDContact, Fever, Cough, SoreThroat, ShortnessOfBreath, HeadAche,
        #        Diabetes, Hypertension, CardiovascularDisease, Obesity, ChronicPulmonary, Pneumonia
        fever_val = 1 if (is_present(answers.get("s_fever")) or is_present(answers.get("s_taste_smell"))) else 0
        cough_val = 1 if (is_present(answers.get("s_cough")) or is_present(answers.get("s_taste_smell"))) else 0
        f["Age"] = int(answers.get("s_age", 40))
        f["Gender"] = answers.get("s_gender", 1)
        f["COVIDContact"] = 1 if is_present(answers.get("s_contact")) else 0
        f["Fever"] = fever_val
        f["Cough"] = cough_val
        f["SoreThroat"] = 1 if is_present(answers.get("s_throat_body")) else 0
        f["ShortnessOfBreath"] = 1 if is_present(answers.get("s_breath")) else 0
        f["HeadAche"] = f["SoreThroat"]
        f["Diabetes"] = 0
        f["Hypertension"] = 0
        f["CardiovascularDisease"] = 0
        f["Obesity"] = 0
        f["ChronicPulmonary"] = 0
        f["Pneumonia"] = 0  # Missing feature that was causing the crash
            
    elif disease_type == "melanoma":
        f["Age"] = int(answers.get("s_age", 40))
        f["Gender"] = answers.get("s_gender", 1)
        f["FamilyHistory"] = 0
        f["SunExposure"] = 8 if is_present(answers.get("s_sun")) else 3
        f["MolesCount"] = 60 if is_present(answers.get("s_moles_many")) else 10
        f["MoleChanges"] = 1 if is_present(answers.get("s_mole_change")) else 0
        f["IrregularBorders"] = 1 if is_present(answers.get("s_mole_asym")) else 0
        f["ColorVariation"] = 1 if is_present(answers.get("s_mole_color")) else 0
        f["Diameter"] = 1 if is_present(answers.get("s_mole_bleed")) else 0
        f["Evolution"] = f["MoleChanges"]

    return f


# ── 4. Recommendations & Display Data ──

RECOMMENDATIONS = {
    "diabetes": {
        "Low":      ["Maintain a balanced diet rich in whole grains, vegetables, and lean proteins.",
                     "Stay active — aim for 30 minutes of exercise daily.",
                     "Monitor blood sugar annually.",
                     "Stay hydrated and limit sugary drinks."],
        "Moderate": ["Reduce sugar and refined carbohydrate intake.",
                     "Increase physical activity to 45-60 minutes daily.",
                     "Monitor fasting glucose every 3 months.",
                     "Consider consulting a dietitian.",
                     "Manage stress through yoga or meditation."],
        "High":     ["Consult an endocrinologist immediately.",
                     "Follow a strict diabetic diet plan.",
                     "Monitor blood sugar daily.",
                     "Take prescribed medications regularly.",
                     "Get regular eye and kidney check-ups.",
                     "Avoid alcohol and smoking."],
    },
    "heart": {
        "Low":      ["Maintain a heart-healthy diet (low salt, low fat).",
                     "Exercise regularly — walking, swimming, cycling.",
                     "Get annual cardiac check-ups.",
                     "Manage stress levels."],
        "Moderate": ["Reduce sodium intake below 2300mg/day.",
                     "Exercise 30-45 minutes, 5 days a week.",
                     "Monitor blood pressure and cholesterol regularly.",
                     "Quit smoking if applicable.",
                     "Limit alcohol consumption."],
        "High":     ["Seek immediate cardiology consultation.",
                     "Follow prescribed medication strictly.",
                     "Adopt a DASH diet plan.",
                     "Monitor BP daily.",
                     "Avoid strenuous activity until cleared by doctor.",
                     "Consider cardiac rehabilitation program."],
    },
    "_default": {
        "Low":      ["Maintain your current healthy lifestyle.",
                     "Continue regular health check-ups.",
                     "Stay physically active.",
                     "Eat a balanced, nutritious diet."],
        "Moderate": ["Schedule a follow-up with your doctor.",
                     "Improve diet and increase physical activity.",
                     "Monitor relevant health parameters regularly.",
                     "Reduce stress and get adequate sleep."],
        "High":     ["Consult a specialist as soon as possible.",
                     "Follow all prescribed treatment plans.",
                     "Monitor symptoms closely.",
                     "Make immediate lifestyle changes.",
                     "Seek support from family and health professionals."],
    },
}

def get_recommendations(disease_type, risk_level):
    disease_recs = RECOMMENDATIONS.get(disease_type, RECOMMENDATIONS["_default"])
    return disease_recs.get(risk_level, RECOMMENDATIONS["_default"].get(risk_level, []))

DISEASE_DISPLAY_NAMES = {
    "diabetes":     "💉 Diabetes",
    "heart":        "❤️ Heart Disease",
    "kidney":       "🫘 Kidney Disease",
    "liver":        "🫀 Liver Disease",
    "stroke":       "🧠 Stroke",
    "thyroid":      "🦋 Thyroid Disorder",
    "anemia":       "🩸 Anemia",
    "pneumonia":    "😷 Pneumonia",
    "tuberculosis": "🦠 Tuberculosis",
    "alzheimers":   "🧩 Alzheimer's",
    "covid19":      "🦠 COVID-19 Severity",
    "melanoma":     "🎨 Melanoma",
}
