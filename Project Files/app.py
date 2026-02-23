import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Safety Check for API Key
if not api_key or "AIza" not in api_key:
    st.error("Invalid API Key found in .env file. Please check Step 3 below.")
    st.stop()

genai.configure(api_key=api_key)

# 3. Page UI
st.set_page_config(page_title="Advancing Nutrition Science Through Gemini AI" )
st.title(" Advancing Nutrition Science Through Gemini Ai")

food_items = st.text_area("What did you eat today?", placeholder="Example: 2 Chapatis, 1 bowl of Dal, 1 Salad")

# Professional Nutritionist System Prompt
system_prompt = """
You are a professional Nutritionist. Analyze the user's food and provide:
1. HEALTH_SCORE: [A single number from 1 to 10]/10
2. A table of calories for each item.
3. Total Macros (Protein, Carbs, Fats).
4. A 'Pro Tip' for a healthier version of this meal.
"""

if st.button("Analyze & Score My Meal"):
    if food_items:
        with st.spinner("AI is analyzing..."):
            try:
                # Try the most stable model name first
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content([system_prompt, food_items])
                
                # Display Score logic
                res_text = response.text
                if "HEALTH_SCORE:" in res_text:
                    # Extracts the number from "HEALTH_SCORE: 8/10"
                    score = res_text.split("HEALTH_SCORE:")[1].split("/")[0].strip()
                    st.metric("Meal Health Score", f"{score}/10")
                
                st.markdown("### 📊 Nutritional Report")
                st.write(res_text)

            except Exception as e:
                st.error(f"Technical Error: {e}")
                st.info("Try running 'pip install -U google-generativeai' in your terminal and restart.")
    else:
        st.warning("Please enter food items first.")