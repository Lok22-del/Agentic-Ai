import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

st.set_page_config(page_title="DS AI Mentor",layout="wide")


@st.cache_resource
def load_llm():
     return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite",
                                   temperature=0.4,
                                   max_output_tokens=350)
llm=load_llm()

def chat_to_text(chat_text):
    return chat_text.encode("utf-8")

if "experience" not in st.session_state:
    st.session_state.experience = ""

if "theme" not in st.session_state:
    st.session_state.theme = "dark"    
    
if "chat" not in st.session_state:
    st.session_state.chat = {
        "python": {"conv": [], "ended": False, "greeting": False},
        "eda": {"conv": [], "ended": False, "greeting": False},
        "stats": {"conv": [], "ended": False, "greeting": False},
        "sql": {"conv": [], "ended": False, "greeting": False},
        "power bi": {"conv": [], "ended": False, "greeting": False},
        "ml": {"conv": [], "ended": False, "greeting": False},
        "ann": {"conv": [], "ended": False, "greeting": False},
        "cnn": {"conv": [], "ended": False, "greeting": False},
        "rnn": {"conv": [], "ended": False, "greeting": False},
        "gen ai": {"conv": [], "ended": False, "greeting": False},
        "agentic ai": {"conv": [], "ended": False, "greeting": False}
    }


if st.session_state.theme == "dark":
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    h1, h2, h3 {
        color: #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {
        background: #f4f6f8;
        color: black;
    }
    h1, h2, h3 {
        color: #1f4ed8;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("Navigation")
st.sidebar.markdown("### 🎨 Theme")
st.session_state.theme = st.sidebar.radio(
    "Choose Theme",
    ["dark", "light"],
    index=0 if st.session_state.theme == "dark" else 1
)

page = st.sidebar.radio(
     "Go to",
     ["Home","Python","EDA","Stats","SQL","Power Bi","ML","ANN","CNN","RNN","Gen AI","Agentic AI"])
#st.write("Current Page:", page)
if page.lower() in st.session_state.chat:
    st.sidebar.subheader("🕘 History")
    for msg in st.session_state.chat[page.lower()]["conv"]:
        if msg["role"] == "user":
            st.sidebar.write("•", msg["content"][:40])


if page == "Home":
     st.title("""👋 Welcome to Data Science AI Mentor
Your personalized AI learning assistant.
Please select a learning module to begin your mentoring session
""")
     
     st.session_state.experience = st.text_input(
        "Enter your experience (years)",
        st.session_state.experience
    )

     st.info("Select a Module from the sidebar to start chatting")

def build_prompt(topic, experience, question):
    return f"""
You have {experience} years of experience.
You are an expert trainer ONLY in {topic}.

STRICT RULES:
- Answer ONLY if the question is related to {topic}
- If NOT related, reply exactly:
  "❌ Please ask questions only related to {topic}."
- Use simple English
- Max 550 tokens

User Question:
{question}
"""

def chat_topic(topic_key,topic_name):
    # topic_key is program use like python,topic_name is diplace purpose
     chat = st.session_state.chat[topic_key]
     st.title(f"{topic_name} AI Mentor")
     st.write(f"**Experience:** {st.session_state.experience} years")

     if not chat["greeting"]:
          greeting=f"""Welcome to {topic_name} AI Mentor 
                    I am your dedicated mentor for {topic_name}.
                    How can I help you today?
                    """
          chat["conv"].append({"role":"ai","content":greeting})
          chat["greeting"]= True

    # Display the chat
     for msg in chat["conv"]:
          with st.chat_message(msg["role"]):
               st.write(msg["content"])

           
     user_input = st.chat_input(
         f"Ask your {topic_name} question (type bye to end)") 
     if user_input and not chat["ended"]: 
        chat["conv"].append({"role":"user","content":user_input}) 

        with st.chat_message("user"):
            st.write(user_input)   


        if user_input.lower().strip() == "bye":
             farewell = "Chat session has been paused. You may download the conversation as a text file for future reference."
             chat["conv"].append({"role":"ai","content":farewell})
             chat["ended"]=True

             with st.chat_message("ai"):
                  st.write(farewell)
        else :
              prompt=build_prompt(topic_name,
                                  st.session_state.experience,
                                  user_input) 
              response = llm.invoke(prompt).content
              chat["conv"].append({"role":"ai","content":response})
              with st.chat_message("ai"):
                st.write(response)
     
     if chat["ended"]:
        chat_text = "\n\n".join(
            [f"{m['role'].upper()}: {m['content']}" for m in chat["conv"]]
        )

        text_file = chat_to_text(chat_text)

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "⬇️ Download Chat (.txt)",
                text_file,
                file_name=f"{topic_key}_chat.txt",
                mime="text/plain"
            )

        with col2:
            if st.button("▶️ Continue Chat"):
                chat["ended"] = False

if page == "Python":
    chat_topic("python", "Python")

elif page == "EDA":
    chat_topic("eda", "EDA")

elif page == "SQL":
    chat_topic("sql", "SQL")

elif page == "Stats":
    chat_topic("stats", "Stats")    

elif page == "Power Bi":
    chat_topic("power bi", "Power Bi")

elif page == "ML":
    chat_topic("ml", "Machine Learning")

elif page == "ANN":
    chat_topic("ann", "Artificial Neural Networks")

elif page == "CNN":
    chat_topic("cnn", "Convolutional Neural Networks")

elif page == "RNN":
    chat_topic("rnn", "Recurrent Neural Networks")

elif page == "Gen AI":
    chat_topic("gen ai", "Generative AI")

elif page == "Agentic AI":
    chat_topic("agentic ai", "Agentic AI")

     
