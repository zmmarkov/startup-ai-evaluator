
import streamlit as st
import openai
import os
import PyPDF2

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Startup & Scaleup AI Evaluator")

st.markdown("Upload a pitch deck **or** type a description below.")

uploaded_file = st.file_uploader("Upload PDF Pitch Deck", type="pdf")
manual_description = st.text_area("Or paste a short description / pitch here")
company_name = st.text_input("Company Name")
special_focus = st.text_input("Optional: Focus (e.g. team, market, risks)")

description = ""

if uploaded_file:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        description = text
        st.success("Pitch deck uploaded and processed successfully!")
    except:
        st.error("There was a problem reading the PDF file.")
elif manual_description:
    description = manual_description

if st.button("Evaluate") and description:
    with st.spinner("AI is analyzing..."):
        prompt = f"""
        You are an experienced investor. Evaluate the following startup or scaleup:

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
            max_tokens=1000
        )

        result = response["choices"][0]["message"]["content"]
        st.subheader("AI Evaluation Result:")
        st.write(result)
