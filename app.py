
import streamlit as st
import openai
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Startup & Scaleup AI Evaluator")

st.markdown("Enter a brief description of a startup or scaleup you'd like to evaluate.")

company_name = st.text_input("Company Name")
description = st.text_area("Short Description / Pitch")
special_focus = st.text_input("Optional: Focus (e.g. team, market, risks)")

if st.button("Evaluate"):
    with st.spinner("AI is analyzing..."):
        prompt = f"""
        You are an experienced investor. Evaluate the following company:

        Company: {company_name}
        Description: {description}
        Focus: {special_focus if special_focus else 'None'}

        Format:
        1. What the company does
        2. Strengths
        3. Weaknesses / Risks
        4. Market potential
        5. Team assessment
        6. Final verdict: Promising / Neutral / Risky
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )

        result = response["choices"][0]["message"]["content"]
        st.subheader("AI Evaluation Result:")
        st.write(result)
