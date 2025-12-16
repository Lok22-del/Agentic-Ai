import streamlit as st
import dotenv
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
import os
import zipfile

st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    .stApp {
        background: #0f2027; 
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }

    /* Title Style */
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #FFD700;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
        padding-bottom: 10px;
    }

    /* Text area */
    textarea {
        border-radius: 10px !important;
        font-size: 16px !important;
        padding: 12px !important;
    }

    /* Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ff7e5f, #feb47b);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 600;
        border: none;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        transition: 0.2s ease;
        opacity: 0.95;
    }

    /* Code Box */
    .stCodeBlock {
        border-radius: 10px !important;
        background: rgba(255,255,255,0.1) !important;
            
    }
    </style>
""", unsafe_allow_html=True)
os.environ["GOOGLE_API_KEY"]=os.getenv("gemini")

st.set_page_config(page_title="Portifoli")

st.title("AI AUTOMATION WEBSITE CREATION")

prompt = st.text_area("write here about your website")


if st.button("generate"):
    message=[("system",""" you are a expert in web development creating professional website.
              so create html,css,java scripts code for creating a frontend based website based on the user prompt
              
              the output should be in the below formate:
              
              --html--
              [html code]
              --html--

              --css--
              [css code]
              --css--

               --js--
              [java script code]
              --js--

              """)]
    message.append(("user",prompt))

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
    response = model.invoke(message)

    # with open("file.txt","w") as file:
    #     file.write(response.content)
    with open("page.html","w") as file:
        file.write(response.content.split("--html--")[1])

    with open("style.css","w") as file:
        file.write(response.content.split("--css--")[1])  

    with open("script.js","w") as file:
        file.write(response.content.split("--js--")[1])      
    
    
    with zipfile.ZipFile("website.zip","w") as zip:
        zip.write("page.html")
        zip.write("style.css")
        zip.write("script.js")

    st.download_button("click to download",
                          data=open("website.zip","rb"),
                          file_name="website.zip")
    st.write("success")    
   