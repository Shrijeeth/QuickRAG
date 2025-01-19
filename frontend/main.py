# pylint: disable=line-too-long,invalid-name

import os
import json
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backend URL and secrets
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
SECRET_KEY = os.getenv("SECRET_KEY")

# Streamlit page configuration
st.set_page_config(page_title="PDF Q&A App", layout="wide")

# Define pages
PAGES = {
    "Upload PDF & Generate Embeddings": "upload_pdf",
    "Q&A Chat": "qa_chat",
    "Credentials": "credentials",
}

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", list(PAGES.keys()))

# Global state
if "api_credentials" not in st.session_state:
    st.session_state.api_credentials = {}

if "pdf_content" not in st.session_state:
    st.session_state.pdf_content = None

if "embedding_model_name" not in st.session_state:
    st.session_state.embedding_model_name = None

if "selected_credentials" not in st.session_state:
    st.session_state.selected_credentials = {}

# Provider-specific models
PROVIDERS = {
    "OpenAI": {
        "embedding_models": [
            "text-embedding-ada-002",
            "text-embedding-3-small",
            "text-embedding-3-large",
        ],
        "llms": ["gpt-3.5-turbo", "gpt-4", "gpt-4o", "gpt-4o-mini"],
    },
    "Ollama": {
        "embedding_models": [
            "all-minilm:22m",
            "all-minilm:33m",
            "nomic-embed-text",
            "mxbai-embed-large",
        ],
        "llms": [
            "gemma:2b",
            "gemma:7b",
            "gemma2:2b",
            "gemma2:9b",
            "llama3.1:8b",
            "llama3.2:1b",
            "llama3.2:3b",
            "qwen2.5:0.5b",
            "qwen2.5:1.5b",
            "qwen2.5:3b",
            "qwen2.5:7b",
        ],
    },
}

### Page 1: Upload PDF & Generate Embeddings ###
if page == "Upload PDF & Generate Embeddings":
    st.title("Upload PDF & Generate Embeddings")

    # Upload PDF
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    # Select provider
    selected_provider = st.selectbox(
        "Select Provider for Embedding", options=PROVIDERS.keys()
    )

    # Select credentials
    embedding_credentials = st.selectbox(
        "Select API Credentials for Embedding",
        options=[
            key
            for key, val in st.session_state.api_credentials.items()
            if val["provider"] == selected_provider
        ],
    )

    # Embedding selection (dynamically based on provider)
    embedding_model_name = None
    if PROVIDERS[selected_provider]["embedding_models"]:
        embedding_model_name = st.selectbox(
            "Select an Embedding Model",
            options=PROVIDERS[selected_provider]["embedding_models"],
        )
    else:
        st.warning(f"No embedding models available for {selected_provider}.")

    # Submit button
    if st.button("Submit"):
        if not uploaded_file:
            st.warning("Please upload a PDF file.")
        elif (
            not embedding_model_name
            and PROVIDERS[selected_provider]["embedding_models"]
        ):
            st.warning("Please select an embedding model.")
        elif not embedding_credentials:
            st.warning("Please select API credentials.")
        else:
            with st.spinner("Uploading PDF and generating embeddings..."):
                # Send file, embedding model, and credentials to backend
                files = {"file": uploaded_file}
                data = {
                    "provider_name": selected_provider,
                    "embedding_model_name": embedding_model_name,
                    "embedding_args": json.dumps(
                        st.session_state.api_credentials[embedding_credentials]
                    ),
                }
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/upload-and-generate-embeddings/",
                        files=files,
                        data=data,
                        headers={"x-api-key": SECRET_KEY},
                        timeout=30,  # Added timeout
                    )
                    response.raise_for_status()
                    result = response.json()
                    st.session_state.pdf_content = result
                    st.session_state.embedding_model_name = embedding_model_name
                    st.session_state.selected_credentials["embedding"] = (
                        embedding_credentials
                    )
                    st.success("PDF uploaded, and embeddings generated successfully!")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to process the PDF and generate embeddings: {e}")

    # Display PDF content if available
    if st.session_state.pdf_content:
        st.subheader("Extracted PDF Content")
        st.text_area("PDF Content", st.session_state.pdf_content, height=300)

### Page 2: Q&A Chat ###
elif page == "Q&A Chat":
    st.title("Q&A Chat")

    # Ensure embeddings are generated
    if not st.session_state.embedding_model_name:
        st.warning("Please upload a PDF and generate embeddings first!")
    else:
        # Display selected embedding model
        st.write(f"**Using Embedding Model:** {st.session_state.embedding_model_name}")

        # Select provider
        selected_provider = st.selectbox(
            "Select Provider for LLM", options=PROVIDERS.keys()
        )

        # Select credentials
        llm_credentials = st.selectbox(
            "Select API Credentials for LLM",
            options=[
                key
                for key, val in st.session_state.api_credentials.items()
                if val["provider"] == selected_provider
            ],
        )

        # Model selection (dynamically based on provider)
        llm_name = None
        if PROVIDERS[selected_provider]["llms"]:
            llm_name = st.selectbox(
                "Select a Language Model (LLM)",
                options=PROVIDERS[selected_provider]["llms"],
            )
        else:
            st.warning(f"No LLMs available for {selected_provider}.")

        # Parameters for LLM
        st.subheader("Model Parameters")
        top_k = st.slider("Top-K Answers", min_value=1, max_value=5, value=1)
        temperature = st.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1
        )

        # Ask a question
        st.subheader("Ask a Question")
        question = st.text_input("Enter your question:")

        if st.button("Get Answer"):
            if not question.strip():
                st.warning("Please enter a question!")
            elif not llm_name:
                st.warning("Please select a language model!")
            else:
                with st.spinner("Fetching answer..."):
                    data = {
                        "question": question,
                        "embedding_model_name": st.session_state.embedding_model_name,
                        "llm_name": llm_name,
                        "top_k": top_k,
                        "temperature": temperature,
                        "api_key": st.session_state.api_credentials[llm_credentials][
                            "api_key"
                        ],
                    }
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/get-answer/", data=data, timeout=30
                        )
                        response.raise_for_status()
                        answer = response.json()["answer"]
                        st.write(f"**Answer:** {answer}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Failed to fetch the answer: {e}")

### Page 3: Credentials ###
elif page == "Credentials":
    st.title("Manage API Credentials")

    # Initialize session state for provider selection
    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = None

    # Provider selection with dynamic UI
    provider = st.selectbox(
        "Provider Name",
        options=PROVIDERS.keys(),
        key="selected_provider",
        on_change=lambda: st.session_state.pop("provider_creds", None),
    )

    # Form for adding credentials
    with st.form("add_credentials_form"):
        st.subheader("Add New API Credentials")
        creds = {}

        if provider == "OpenAI":
            api_key = st.text_input(
                "API Key",
                type="password",
                help="Your OpenAI API Key",
                key="openai_api_key",
            )
            url = st.text_input(
                "URL (Optional)",
                value="https://api.openai.com/v1",
                help="OpenAI API base URL. Default is pre-filled.",
                key="openai_url",
            )
            creds = {"api_key": api_key, "url": url}

        elif provider == "Ollama":
            url = st.text_input(
                "URL (Mandatory)",
                value="http://localhost:11434",
                help="The base URL for Ollama. Provide the complete URL.",
                key="ollama_url",
            )
            creds = {"url": url}

        # Submit button
        submitted = st.form_submit_button("Add Credentials")

        if submitted:
            # Validate inputs based on the provider
            if provider == "OpenAI" and not creds["api_key"]:
                st.warning("Please provide the API Key for OpenAI.")
            elif provider == "Ollama" and not creds["url"]:
                st.warning("Please provide the URL for Ollama.")
            else:
                # Save credentials in session state
                st.session_state.api_credentials[f"{provider}_key"] = {
                    "provider": provider,
                    **creds,
                }
                st.success(f"Added credentials for {provider}.")

    # Display existing credentials
    if st.session_state.api_credentials:
        st.subheader("Existing Credentials")
        for key, val in st.session_state.api_credentials.items():
            if val["provider"] == "OpenAI":
                st.write(
                    f"**OpenAI:** API Key: {val['api_key'][:4]}{'*' * (len(val['api_key']) - 4)}",
                    f"(URL: {val.get('url', 'Default')})",
                )
            elif val["provider"] == "Ollama":
                st.write(f"**Ollama:** URL: {val['url']}")
