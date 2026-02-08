# app_two_sides.py
import streamlit as st
import openai
import os

# --- Set your OpenAI API key ---
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set this in your environment

# --- Ground truth rule for the right side ---
RIGHT_SIDE_RULE = "Bears holding flowers, showing a peace sign, with white bellies and black noses"

st.title("Bear Grouping Activity")
st.write("""
You will see an image split into **two sides**. Each side has 5 bears.
Your task is to **come up with 5 rules describing how the bears are grouped**. 
Type your 5 rules below (one per line). Note: the right side has a strict rule; the left side is everything else.
""")

# --- Display image ---
st.image("A_digital_illustration_features_ten_cartoon-style_.png", caption="Two sides of bears", use_column_width=True)

# --- User input ---
user_input = st.text_area("Enter your 5 rules (one per line)", height=200)

# --- Button to submit ---
if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please enter your 5 rules.")
    else:
        user_rules = [line.strip() for line in user_input.strip().split("\n") if line.strip()]

        if len(user_rules) != 5:
            st.warning("Please enter exactly 5 rules.")
        else:
            # --- Prepare the prompt for GPT ---
            prompt = f"""
You are an evaluator. The right side of the image has a strict rule:

{RIGHT_SIDE_RULE}

Left side bears can have some but not all of those features. The user submitted these 5 rules:

{user_rules}

Evaluate each rule: 
- Does it correctly describe the right side? 
- Is it applicable to the left side? 
- Give an overall score from 0 to 5, where 5 means all rules correctly describe the sides.

Respond in JSON format:

{{
  "evaluations": [
    {{"user_rule": "...", "matches_right_side": "...", "matches_left_side": "...", "score": ...}},
    ...
  ],
  "overall_score": ...
}}
"""

            # --- Call OpenAI API ---
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an evaluator of grouping rules."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )

                eval_output = response.choices[0].message['content']
                st.subheader("Evaluation Result")
                st.code(eval_output)
            except Exception as e:
                st.error(f"Error: {e}")