import streamlit as st
from datetime import datetime
from streamlit_js_eval import streamlit_js_eval
from data_loader import setup_mongodb
from ui_components import apply_custom_css, render_chat_message, render_quick_info
from config import load_environment_variables
from htmlTemplates import CSS_STYLES, LOGO_TITLE_HTML
from query_generator import load_prompt_template, setup_langchain, generate_and_execute_query

def initialize_session_state():
    if 'collection' not in st.session_state:
        try:
            st.session_state.collection = setup_mongodb()
        except Exception as e:
            st.error(f"Failed to connect to MongoDB: {str(e)}")
            st.session_state.collection = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def main():
    st.set_page_config(page_title="Calibration Certificate Chatbot", layout="wide")
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    st.markdown(LOGO_TITLE_HTML, unsafe_allow_html=True)
    
    apply_custom_css()
    load_environment_variables()
    initialize_session_state()

    with st.sidebar:
        st.markdown("<h3 style='text-align: center;'>Settings</h3>", unsafe_allow_html=True)
        render_quick_info()
        
        if st.button("Reload Data", key="reload"):
            st.session_state.collection = setup_mongodb()
            st.success("Data loaded and connection established successfully!")

        if st.button("Clear Chat", key="clear"):
            st.session_state.messages = []

    prompt = load_prompt_template()
    chain = setup_langchain(prompt)

    chat_container = st.container()
    
    with st.container():
        col1, col2 = st.columns([6,1])
        with col1:
            user_input = st.text_input("Ask a question about the calibration certificates:", key="user_input")
        with col2:
            submit_button = st.button("Submit", key="submit")

    if submit_button and user_input:
        with st.spinner("Thinking..."):
            results = generate_and_execute_query(chain, user_input, st.session_state.collection)
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        if results:
            response = str(results)  # Convert results to string for display
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "No results found or an error occurred."})

    with chat_container:
        for message in st.session_state.messages:
            render_chat_message(message)

    if st.session_state.messages:
        streamlit_js_eval(js_expressions="window.scrollTo(0, document.body.scrollHeight);", key=f"scroll_{len(st.session_state.messages)}")

if __name__ == "__main__":
    main()