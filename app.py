
import streamlit as st
import openai
import PyPDF2

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("📊 Startup & Scaleup AI Evaluator")

st.markdown("Upload a **PDF pitch deck** or enter a description manually for AI analysis.")

# PDF upload section
uploaded_file = st.file_uploader("Upload PDF Pitch Deck", type="pdf")

# Manual entry fallback
manual_description = st.text_area("Or paste a short description / pitch here")

# Company name and focus
company_name = st.text_input("Company Name")
special_focus = st.text_input("Optional: Focus (e.g. team, market, risks)")

description = ""

# Extract text from PDF if uploaded
if uploaded_file:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        description = text.strip()
        st.success("✅ Pitch deck processed successfully!")
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")

elif manual_description:
    description = manual_description.strip()

# Evaluate button
if st.button("Evaluate") and description:
    with st.spinner("🤖 AI is analyzing the company..."):
        prompt = f"""
        You are an experienced investor. Please evaluate the following company:

        Company Name: {company_name}
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

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            result = response["choices"][0]["message"]["content"]
            st.subheader("🔍 AI Evaluation:")
            st.write(result)
        except Exception as e:
            st.error(f"❌ OpenAI API error: {e}")
elif st.button("Evaluate") and not description:
    st.warning("⚠️ Please upload a PDF or enter a description first.")
