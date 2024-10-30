import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


def process_with_gemini(content, question):
    """
    Process scraped beauty product content with Gemini API to provide the single best recommendation
    Args:
        content (str): The scraped and cleaned Nykaa product data
        question (str): User's beauty/skincare related question
    Returns:
        str: Single best product recommendation with detailed explanation
    """
    try:
        prompt = f"""You are a knowledgeable beauty and skincare advisor. Analyze the provided Nykaa 
        product information and recommend only the SINGLE BEST product for the customer's needs.

        Product Information from Nykaa:
        {content}

        Customer Query: {question}

        Please provide ONE recommendation following this format:

        RECOMMENDED PRODUCT:
        [Product name and brief description]

        WHY THIS IS THE BEST CHOICE:
        - Explain why this specific product is the best match for their needs
        - Highlight key ingredients that address their concerns
        - Mention price point if available

        HOW TO USE:
        [Provide clear usage instructions]

        If you cannot find a suitable product in the provided data, explain what specific type of 
        product they should look for instead and why.

        Remember: Provide only ONE product recommendation - the absolute best match for their needs.
        """

        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }

        response = model.generate_content(prompt, generation_config=generation_config)

        return response.text.strip()

    except Exception as e:
        return f"Error processing with Gemini: {str(e)}"
