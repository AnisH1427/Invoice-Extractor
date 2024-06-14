from dotenv import load_dotenv 

load_dotenv() #load all the environment variables from the .env file 

import streamlit as st 
import os 
from PIL import Image 
import google.generativeai as genai 

#get the google api key from the environment variables
# os.getenv("GOOGLE_API_KEY") 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_prompt, image, user_input):
    #FUNCTIONS TO LOAD GEMINI PRO VISION MODEL 
    model = genai.GenerativeModel("gemini-pro-vision") 
    response = model.generate_content([input_prompt, image[0],user_input])
    return response.text 

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #read the image file into bytes 
        bytes_data = uploaded_file.getvalue() 
        
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts 
    else:
        raise FileNotFoundError("Please upload an image first") 

#initialize the streamlit app 
st.title("MultiLanguage Invoice Extractor") 

st.header("MultiLanguage Invoice Extractor") 
user_input = st.text_input("Enter the input text:", key="input") 
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "png", "jpeg"])  
image = None

if uploaded_file is not None: 
    image = Image.open(uploaded_file) 
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the invoice") 

input_prompt = """
               You are an Expert in understanding invoices of Multiple languages. Our User will Upload an image of the invoice and you have to  answer the questions based on the uploaded invoice.
               """

#if submit is clicked 
if submit:
    image_data = input_image_details(uploaded_file) 
    response = get_gemini_response(input_prompt, image_data, user_input)
    st.subheader("Response from the model")
    st.write(response) 
    
