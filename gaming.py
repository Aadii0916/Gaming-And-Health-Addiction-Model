import streamlit as st
import pandas as pd
import joblib

model = joblib.load("SVM_gaming.pkl")
scaler = joblib.load("scaler.pkl")
expected_columns = joblib.load("columns.pkl")

# Place this after your joblib.load() calls
genre_map = {"Mobile Games": 0, "MOBA": 1, "FPS": 2, "RPG": 3, "MMO (or other)": 4, "Strategy": 5, "Battle Royale": 6}
platform_map = {"Mobile": 0, "PC": 1, "Multi-platform": 2, "Console": 3}
sleep_map = {"Very Poor": 0, "Poor": 1, "Fair": 2, "Insomnia": 3, "Good": 4}

st.title("Gaming and Health Prediction (ML Project)")
st.markdown("Provide the following details to check your  gaming_addiction_risk_level:")


age = st.slider("Age", 10, 100, 40)
sex = st.selectbox("Sex", ["M", "F"])

#Daily_gaming_hours = st.slider("Total Gaming Hours",0,7,13)
Daily_gaming_hours = st.slider(
    "Total Gaming Hours (Daily)", 
    min_value=0.0,    
    max_value=15.0,   
    value=6.0,   #it is the default starting value     
    step=0.1          
)
Game_genre= st.selectbox("Type of Genre", ["Mobile Games", "MOBA", "FPS", "RPG","MMO (or other)","Strategy","Battle Royale"])
Gaming_platform=st.selectbox("Platform",["Mobile","PC","Multi-platform","Console"])
Sleep_hours=st.slider("Total Sleeping",0,10,5)
Sleep_quality=st.selectbox("Sleeping Quality",["Very Poor","Poor","Fair","Insomnia","Good	"])
years_gaming=st.slider("total year of Gaming",1,7,15)
back_neck_pain	=st.selectbox("backpain",["True","False"]),

social_score = st.slider("Social Isolation Score (1-10)", 1, 10, 5)
productivity = st.slider("Work/Academic Productivity Score (1-10)", 1, 10, 5)
gpa = st.slider("Current GPA/Grades (1-10 scale)", 1.0, 10.0, 7.0)
withdrawal = st.slider("Withdrawal Symptoms (1-10)", 1, 10, 2)
loss_interest = st.slider("Loss of other interests (1-10)", 1, 10, 2)
mood_swings = st.slider("Mood Swing Frequency (1-10)", 1, 10, 2)







# if st.button("Predict"):
    
#     raw_input = {
#         'age': age,
#         'gender': 1 if sex == "M" else 0, 
#         'daily_gaming_hours': Daily_gaming_hours,
#         'game_genre': genre_map[Game_genre],
#         'gaming_platform': platform_map[Gaming_platform],
#         'sleep_hours': Sleep_hours,
#         'sleep_quality': sleep_map[Sleep_quality],
#         'years_gaming': years_gaming,  
#         'back_neck_pain': 1 if back_neck_pain == "True" else 0,	

#         'social_isolation_score': social_score,
#         'work_productivity_score': productivity,
#         'grades_gpa': gpa,
#         'withdrawal_symptoms': withdrawal,   
#         'loss_of_other_interests': loss_interest,
#         'mood_swing_frequency': mood_swings
# }
    

    
#     input_df = pd.DataFrame([raw_input])
#     for col in expected_columns:
#         if col not in input_df.columns:
#             input_df[col] = 0
#     input_df = input_df[expected_columns]
#     scaled_input = scaler.transform(input_df)

   
#     prediction = model.predict(scaled_input)[0]
#     probabilities = model.predict_proba(scaled_input)[0]
    
#    #this is copy from gpt
#     risk_labels = ["High", "Low", "Moderate", "Severe"] 
    
#     st.write("### 📊 Risk Probability Breakdown")
#     for label, prob in zip(risk_labels, probabilities):
#         col1, col2 = st.columns([1, 3])
#         with col1:
#             st.write(f"**{label}**")
#         with col2:
#             st.progress(float(prob))
#             st.write(f"{round(prob * 100, 2)}%")

    
#     st.divider()
#     if prediction == 0 or prediction == 3: 
#         st.error(f"⚠️ Result: {risk_labels[prediction]} Risk of Gaming Addiction")
#     elif prediction == 2:
#         st.warning("🟠 Result: Moderate Risk of Gaming Addiction")
#     else:
#         st.success("✅ Result: Low Risk of Gaming Addiction")



if st.button("Predict"):
    # Corrected Feature Names to match your training columns
    raw_input = {
        'age': age,
        'gender': 1 if sex == "M" else 0, 
        'daily_gaming_hours': Daily_gaming_hours,
        'game_genre': genre_map[Game_genre],
        'gaming_platform': platform_map[Gaming_platform],
        'sleep_hours': Sleep_hours,
        'sleep_quality': sleep_map[Sleep_quality],
        'years_gaming': years_gaming,  # Fixed naming
        'back_neck_pain': 1 if back_neck_pain == "True" else 0, # Fixed tuple logic
        'social_isolation_score': social_score,
        'work_productivity_score': productivity,
        'grades_gpa': gpa,
        'withdrawal_symptoms': withdrawal,   
        'loss_of_other_interests': loss_interest,
        'mood_swing_frequency': mood_swings
    }
    
    # Preprocessing and Alignment
    input_df = pd.DataFrame([raw_input])
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[expected_columns]
    scaled_input = scaler.transform(input_df)

    # Prediction
    prediction = model.predict(scaled_input)[0]
    probabilities = model.predict_proba(scaled_input)[0]
    
    # Alphabetical Order: High(0), Low(1), Moderate(2), Severe(3)
    risk_labels = ["High", "Low", "Moderate", "Severe"] 
    
    # Probability UI
    st.write("### 📊 Risk Probability Breakdown")
    for label, prob in zip(risk_labels, probabilities):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"**{label}**")
        with col2:
            st.progress(float(prob))
            st.write(f"{round(prob * 100, 2)}%")

    # Final Result Message
    st.divider()
    if prediction == 0 or prediction == 3: 
        st.error(f"⚠️ Result: {risk_labels[prediction]} Risk of Gaming Addiction")
    elif prediction == 2:
        st.warning("🟠 Result: Moderate Risk of Gaming Addiction")
    else:
        st.success("✅ Result: Low Risk of Gaming Addiction")

    # --- NEW INSIGHT BOX SECTION ---
    st.write("### 💡 AI Insights & Recommendations")
    
    with st.expander("See detailed analysis"):
        # Insight 1: Based on top feature 'Withdrawal'
        if withdrawal > 7:
            st.write("- **High Withdrawal:** Your symptoms suggest a strong dependency. Consider taking 'gaming-free' days to reset.")
        
        # Insight 2: Based on 'Social Isolation'
        if social_score > 7:
            st.write("- **Social Impact:** There is a strong link between your gaming and social isolation. Try engaging in one non-gaming social activity this week.")
        
        # Insight 3: Based on 'Daily Hours'
        if Daily_gaming_hours > 10:
            st.write(f"- **Usage Warning:** {Daily_gaming_hours} hours is significantly above the healthy average. High usage is the primary driver of your risk level.")

        if prediction == 1:
            st.write("🌟 **Great news!** Your gaming habits currently seem balanced with your daily life.")


