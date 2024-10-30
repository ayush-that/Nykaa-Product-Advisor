import streamlit as st
from parse import process_with_gemini
from scrape import scrape_website, extract_body_content, clean_body_content


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(
    page_title="Nykaa Product Advisor",
    page_icon="💄",
    layout="centered",  # Change layout back to 'centered'
    initial_sidebar_state="expanded",
)

st.image("images/top-image.jpg", use_column_width=True)

st.title("💄 Nykaa Product Advisor")
st.markdown(
    """
    Welcome to your personal beauty and skincare assistant! 🌟
    """
)

# Load custom CSS from file
load_css("styles.css")

url = st.text_input(
    "Enter Nykaa Product Page URL", placeholder="https://www.nykaa.com/..."
)
if st.button("Analyze Products"):
    with st.spinner("Analyzing product details..."):
        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)
        st.session_state.dom_content = cleaned_content

        with st.expander("Show Product Details"):
            st.text_area("Scraped Content", value=cleaned_content, height=300)

if "dom_content" in st.session_state:
    st.markdown("### Ask for Recommendations")
    st.write(
        "Tell us about your skincare needs, and we'll find the perfect product for you!"
    )

    user_question = st.text_area(
        "Your question",
        placeholder="I have oily skin and need a moisturizer that won't clog my pores.",
        height=100,
    )

    if st.button("Get Recommendations"):
        if user_question:
            with st.spinner("Finding the best product for you..."):
                try:
                    response = process_with_gemini(
                        st.session_state.dom_content, user_question
                    )
                    st.markdown("### Your Personalized Recommendation:")
                    st.markdown(response)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please enter a Nykaa product page URL to begin.")
