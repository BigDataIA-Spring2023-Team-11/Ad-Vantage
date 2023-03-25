import streamlit as st

from api_main import get_grammer_corrected_text, keyword_generator

st.markdown(
        "<h3 style='text-align: center'><span style='color: #2A76BE;'>AI Marketing Assistant</span></h3>",
        unsafe_allow_html=True)

product_description = st.text_input("product_description")
grammer_corrected_description = get_grammer_corrected_text(product_description)
st.markdown(f"{grammer_corrected_description}")

# keywords are seed words
keywords_from_description = keyword_generator(grammer_corrected_description)

st.markdown(keywords_from_description)

