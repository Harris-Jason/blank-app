import streamlit as st

# --- SESSION STATE SETUP ---
if "screen" not in st.session_state:
    st.session_state.screen = "welcome"

if "symptoms" not in st.session_state:
    st.session_state.symptoms = []

# --- SYMPTOM DATABASE (grouped) ---
symptom_categories = {
    "Respiratory": [
        "shortness of breath", "persistent cough", "chest tightness", "coughing up blood/mucus"
    ],
    "Heart and Circulation": [
        "chest pain", "fatigue", "dizziness/fainting", "rapid heartbeat"
    ],
    "Neurological": [
        "severe headache", "dizziness", "confusion", "seizures"
    ],
    "Digestive": [
        "abdominal pain", "nausea/vomiting", "diarrhoea", "constipation"
    ],
    "Muscles and Joints": [
        "muscle pain", "stiffness", "swelling", "limited movement"
    ],
    "Skin and Allergies": [
        "rashes", "itching", "hives", "swelling", "dry/peeling"
    ]
}

# --- SCORING ---
symptom_weights = {
    "shortness of breath": 5,
    "persistent cough": 2,
    "chest tightness": 4,
    "coughing up blood/mucus": 5,
    "chest pain": 5,
    "fatigue": 2,
    "dizziness/fainting": 4,
    "rapid heartbeat": 4,
    "severe headache": 3,
    "dizziness": 2,
    "confusion": 5,
    "seizures": 5,
    "abdominal pain": 3,
    "nausea/vomiting": 2,
    "diarrhoea": 2,
    "constipation": 1,
    "muscle pain": 2,
    "stiffness": 2,
    "swelling": 3,
    "limited movement": 3,
    "rashes": 2,
    "itching": 1,
    "hives": 3,
    "dry/peeling": 1
}

# --- SCREEN 1: WELCOME ---
if st.session_state.screen == "welcome":
    st.title("Red Rhino Hospital Triage System")
    st.write("Welcome! This system helps assess your medical risk level.")

    if st.button("Start"):
        st.session_state.screen = "symptoms"
        st.rerun()

# --- SCREEN 2: SYMPTOMS ---
elif st.session_state.screen == "symptoms":
    st.title("Select Your Symptoms")

    selected = []

    for category, symptoms in symptom_categories.items():
        st.subheader(category)
        selected += st.multiselect(f"Choose from {category}:", symptoms, key=category)

    st.session_state.symptoms = selected

    if st.button("Next"):
        st.session_state.screen = "questions"
        st.rerun()

# --- SCREEN 3: QUESTIONS ---
elif st.session_state.screen == "questions":
    st.title("Answer Some Questions")

    duration = st.selectbox(
        "How long have you had symptoms?",
        ["Less than 1 day", "1-3 days", "More than 3 days"]
    )

    pain = st.slider("Rate your pain level", 1, 10, 1)

    medication = st.radio("Have you taken medication?", ["No", "Yes"])

    conditions = st.text_input("Any pre-existing conditions?")

    if st.button("Go to AI Chat"):
        st.session_state.duration = duration
        st.session_state.pain = pain
        st.session_state.medication = medication
        st.session_state.conditions = conditions
        st.session_state.screen = "chatbot"
        st.rerun()

# --- SCREEN 4: AI CHATBOT ---
elif st.session_state.screen == "chatbot":
    st.title("AI Chat Assistant")

    user_input = st.text_input("Ask anything about your symptoms:")

    if user_input:
        # Placeholder response (you can connect API here)
        st.write("AI Response:")
        st.write("Based on your symptoms, please monitor closely and consult a doctor if worsening.")

    if st.button("Get Diagnosis"):
        st.session_state.screen = "diagnosis"
        st.rerun()

# --- SCREEN 5: DIAGNOSIS ---
elif st.session_state.screen == "diagnosis":
    st.title("Diagnosis Result")

    # Calculate score
    symptom_score = sum([symptom_weights.get(s, 1) for s in st.session_state.symptoms])
    question_score = st.session_state.pain

    total_score = symptom_score + question_score

    # Determine risk
    if total_score <= 10:
        color = "green"
        text = "LOW RISK"
    elif total_score <= 20:
        color = "orange"
        text = "MEDIUM RISK"
    else:
        color = "red"
        text = "HIGH RISK"

    # BIG COLOR SCREEN
    st.markdown(
        f"""
        <div style="background-color:{color}; padding:100px; text-align:center;">
            <h1 style="color:white;">{text}</h1>
            <h2 style="color:white;">Score: {total_score}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Return to Home"):
        st.session_state.screen = "welcome"
        st.rerun()
