# app_two_sides.py
import streamlit as st
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

RIGHT_SIDE_RULE = "On the right bears must have a peace sign with their hand, flowers in their hand, white bellies"

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
    return tokenizer, model

st.title("Bear Grouping Activity")

st.write("""
You will see an image split into **two sides**. Each side has 5 bears.
Your task is to **come up with 3 rules describing how the bears are grouped**.
Note: the right side has a strict rule; the left side is everything else.
""")

# --- Display image ---
st.image("A_digital_illustration_features_ten_cartoon-style_.png", caption="Two sides of bears", width='stretch')

# --- User input ---
user_input = st.text_area("Enter your rules", height=200)

# --- Button to submit ---
if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please enter your rules.")
    else:
        # --- Prepare the prompt for the model ---
        prompt = f"""Determine if the user's rules match this ground truth: '{RIGHT_SIDE_RULE}'.

User's rules: {user_input.strip()}

If the user mentions peace signs, flowers, and white bellies for the right side, respond with: {{"matches_right_side": true, "score": 5}}
Otherwise respond with: {{"matches_right_side": false, "score": 0}}

Output only valid JSON:"""

        # --- Use model for evaluation ---
        tokenizer, model = load_model()
        
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(**inputs, max_length=100)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        try:
            eval_json = json.loads(response)
        except:
            # Fallback: simple keyword matching
            user_lower = user_input.lower()
            matches = ("peace" in user_lower or "✌" in user_lower) and \
                     ("flower" in user_lower) and \
                     ("white" in user_lower and "bell" in user_lower)
            eval_json = {"matches_right_side": matches, "score": 5 if matches else 0}
        
        st.subheader("Evaluation Result")
        st.json(eval_json)