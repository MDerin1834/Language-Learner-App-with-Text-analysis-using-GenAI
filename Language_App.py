import streamlit as st
import google.generativeai as genai

# Configure the AI model
genai.configure(api_key="YOUR_API_KEY")

# Define generation and safety settings
generation_config = {
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096
}

# Safety settings to filter harmful content
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

# Prompts for the Gemini AI model
prompts = {
    "English": """
    Your Objective: Your task is to assist the user in learning a new language by processing the provided text and performing the following:
    
    Identify Important Points: Extract the key points or main ideas from the given text. Highlight the crucial pieces of information that are central to understanding the content. Provide a simple explanation for challenging phrases.

    Elaborate on Key Points: Once the important points are identified, provide a detailed explanation for each. This should involve expanding on these points by providing examples, context, and any necessary background information.

    Define Crucial Words: Identify any critical words in the text that might be challenging for the user to understand. For each of these words, provide:

    A clear and simple definition.
    The context in which the word is used within the text.
    A sentence example showing how the word can be used in different contexts, if applicable.

    Learning Focus: The goal is to help the user learn and understand the language more effectively. The explanations should be tailored to a learner’s level and aim to deepen their comprehension of both the vocabulary and the structure of the language.
    """
}

# Initialize the model
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
except Exception as e:
    st.error(f"Error initializing the model: {e}")

# Set Streamlit page configuration
st.set_page_config(page_title="Language Learning App", page_icon=":translator:")

# Header for the app
st.markdown("<h1 style='text-align: center;'>🗺️ Language Learning App 🗺️</h1>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)

# Subheading for app functionality
st.subheader("This is an AI-powered app to help Language Learners analyze the provided text contextually and grammatically.")

# Text input area for users to enter text directly
user_input = st.text_area("Enter the text you'd like to analyze", height=300)

# Button to trigger the analysis
submit_button = st.button("Generate the Analysis")

if submit_button:
    if user_input.strip():  # Check if the input text is not empty
        system_prompt = prompts["English"]

        # Combine user input with the system prompt
        prompt_parts = [user_input, system_prompt]

        try:
            # Display loading spinner while the model processes the request
            with st.spinner("Generating analysis..."):
                response = model.generate_content(prompt_parts)

            # Check if the response is valid and not None
            if response and hasattr(response, 'text') and response.text:
                st.header("Here is the analysis:")
                st.write(response.text)
            else:
                st.warning("The model returned no valid analysis. Please try again.")
        except Exception as e:
            st.error(f"Error during content generation: {e}")
    else:
        st.warning("Please enter some text to analyze.")
