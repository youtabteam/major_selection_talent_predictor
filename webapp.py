import streamlit as st
import os
from ollama import chat
from ollama import ChatResponse
import pandas as pd 


majors = pd.read_excel("majors.xlsx")

def filter(df: pd.DataFrame, query: dict):
    for key, value in query.items():
        if value != None:
            df = df[df[key].isin(value)]
        
    return df 

st.title("Youtab AI assistant.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
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
            from user and say nothing else, i also want all values of dict be in a list:
            1. StudyName ('StudyName': ['second major', 'first major', ...])
            2. rating (as a number) 
            3. Province
            4. Gender (if mentioned)
            5. AcceptancePeriod like روزانه or نوبت دوم and ... (if mentioned)
            6. Shift (Acceptance half year that would be first or second (if mentioned))
            7. UniversityTitle (university name)

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
        df = filter(majors, response_dict)
        st.dataframe(df)
        st.session_state.messages.append({"role": "assistant", "content": response['message']['content']})
