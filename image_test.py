import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(
    layout="wide"
)

st.title("Gemini Vision ")

# API Key - Set your API key here
API_KEY = st.secrets["API_KEY"]


genai.configure(api_key=API_KEY)

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload & Prompt")
    
    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp']
    )
    
    prompt = st.text_area(
        "Enter your prompt:",
        placeholder="Provide all the fields you want in the image as json",
        height=100
    )
    
    # Submit button
    submit = st.button(" Ask Gemini", type="primary")
    
    # Display uploaded image
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width =True)

with col2:
    st.subheader("Gemini Response")
    
    if submit and uploaded_file and prompt:
        with st.spinner("Asking Gemini..."):
            try:
                # Initialize the model
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Prepare the image
                image = Image.open(uploaded_file)
                
                # Generate response
                response = model.generate_content([prompt, image])
                
                # Display response
                st.markdown("### Response:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure your API key is valid and you have access to Gemini API")
    
    elif submit:
        if not uploaded_file:
            st.warning("Please upload an image first!")
        if not prompt:
            st.warning("Please enter a prompt!")
