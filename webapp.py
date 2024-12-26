import streamlit as st
import os
from ollama import chat
from ollama import ChatResponse
import pandas as pd 


majors = pd.read_excel("majors.xlsx")

def filter(df: pd.DataFrame, query: dict):
    for key, value in query.items():
        if value != None:
            if type(value) != list:
                value = list(value)
            df = df[df[key].isin(value)]
        
    return df 

# Custom CSS to change title color
st.markdown(
    """
    <style>
    body {
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .title {
        color: #2F428F;
        font-size: 2.5rem;
        text-align: center;  /* Centers the text */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display image before the title
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("D:/youtab/major_selection_talent_predictor/Vector.jpg", width=146)

# Custom title with class for styling
st.markdown('<h1 class="title">دستیار هوش مصنوعی یوتاب</h1>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("از یوتاب بپرس ..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        input = {
            "prompt": f"""
            Extract the following details from the user's input and only give me dict of the values that has been extracted
            from user and say nothing else, i also want all values of dict be in a list if we have multiple value of a key for 
            example if we have mechanical and computer engineering in users prompt
            put it like this StudyName: ["mechanical engineering", "computer engineering"]:
            1. StudyName (major name)
            2. rating (as a number) 
            3. Province (if mentioned)
            4. Gender (if mentioned)
            5. AcceptancePeriod like روزانه or نوبت دوم and ... (if mentioned)
            6. UniversityTitle (university name)

            User query: "{prompt}"
            """,
            "max_new_tokens": 512,
            "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>/n/n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>/n/n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>/n/n"
        }
        
        response: ChatResponse = chat(model='llama3.2:latest', messages=[
                {
                    'role': 'user',
                    'content': input["prompt"],
                },
                ])
                
        # st.markdown(response['message']['content'])
        
        response_dict = eval(response['message']['content'])
        print(response_dict)
        df = filter(majors, response_dict)
        st.dataframe(df)
        st.session_state.messages.append({"role": "assistant", "content": response['message']['content']})
