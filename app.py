import os
import boto3
import streamlit as st
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import hashlib
import time 

# Initialize Bedrock clients
bedrock = boto3.client(service_name="bedrock-runtime")
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock)

# Generate a unique identifier for the uploaded file
def generate_file_id(uploaded_file):
    file_hash = hashlib.sha256(uploaded_file.getvalue()).hexdigest()
    return file_hash

# Data Ingestion for Uploaded PDF
def data_ingestion(uploaded_file):
    # Save the uploaded file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load the PDF
    loader = PyPDFLoader("temp.pdf")  # Load the uploaded PDF
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=1000
    )
    docs = text_splitter.split_documents(documents)
    
    # Clean up the temporary file
    os.remove("temp.pdf")
    return docs

# Vector Embedding and Vector Store
def get_vector_store(docs, file_id):
    vectorstore_faiss = FAISS.from_documents(
        docs,
        bedrock_embeddings
    )
    vectorstore_faiss.save_local(f"faiss_index_{file_id}")  # Save the FAISS index locally with a unique name

# Initialize Claude LLM
def get_claude_llm():
    llm = Bedrock(
        model_id="anthropic.claude-v2:1",
        client=bedrock,
        model_kwargs={
            "max_tokens_to_sample": 512,
            "temperature": 0.5,
            "top_k": 250,
            "top_p": 0.9, ## Output ki diversity control karte hain
            "stop_sequences": ["\n\nHuman:"], ##odel ko batata hai ki kahan rukna hai 
            "anthropic_version": "bedrock-2023-05-31"
        }
    )
    return llm

# Initialize Llama 3 LLM
def get_llama3_llm():
    llm = Bedrock(
        model_id="meta.llama3-70b-instruct-v1:0",
        client=bedrock,
        model_kwargs={
            "max_gen_len": 512,
            "temperature": 0.5,
            "top_p": 0.9
        }
    )
    return llm

# Prompt Templates for Different Use Cases
def get_prompt_template(use_case):
    if use_case == "Medical Report Chat":
        return """
        Human: You are a medical assistant with expertise in analyzing medical reports. Your task is to analyze the following medical report and provide a concise yet comprehensive summary. Follow these guidelines:
        1. Highlight key findings, diagnoses, and recommendations.
        2. If the report is incomplete or lacks sufficient information, provide related information based on the available data and suggest what additional details are needed.
        3. Use clear and professional language, avoiding jargon unless necessary.
        4. Structure your response with headings: "Key Findings", "Diagnoses", "Recommendations", and "Additional Information Needed" (if applicable).
        5. If the user asks a question, provide accurate and relevant information based on the context. If you don't know the answer, say so and avoid speculation.

        <context>
        {context}
        </context>

        Question: {question}

        Assistant:"""
    
    elif use_case == "Book Summarizer":
        return """
        Human: You are a literary expert. Summarize the following book content in a concise yet engaging manner. Follow these guidelines:
        1. Highlight the main themes, key characters, and important events.
        2. Provide a summary suitable for someone who hasn't read the book.
        3. Keep the summary between 150-200 words.
        4. Use a neutral tone and avoid spoilers unless explicitly requested.
        5. If the user asks a question, provide accurate and relevant information based on the context. If you don't know the answer, say so and avoid speculation.

        <context>
        {context}
        </context>

        Question: {question}

        Assistant:"""
    
    elif use_case == "Research Paper Summarizer":
        return """
        Human: You are a research analyst. Summarize the following research paper for a non-expert audience. Follow these guidelines:
        1. Focus on the research question, methodology, key findings, and conclusions.
        2. Explain technical terms in simple language.
        3. Keep the summary between 200-250 words.
        4. Structure your response with headings: "Research Question", "Methodology", "Key Findings", and "Conclusions".
        5. If the user asks a question, provide accurate and relevant information based on the context. If you don't know the answer, say so and avoid speculation.

        <context>
        {context}
        </context>

        Question: {question}

        Assistant:"""
    
    elif use_case == "Legal Document Summarizer":
        return """
        Human: You are a legal expert. Analyze the following legal document and provide a concise summary. Follow these guidelines:
        1. Highlight key clauses, obligations, and legal implications.
        2. If the document is unclear, ask for clarification.
        3. Use plain language to explain complex legal terms.
        4. Structure your response with headings: "Key Clauses", "Obligations", "Legal Implications", and "Clarifications Needed" (if applicable).
        5. If the user asks a question, provide accurate and relevant information based on the context. If you don't know the answer, say so and avoid speculation.

        <context>
        {context}
        </context>

        Question: {question}

        Assistant:"""
    
    elif use_case == "Resume Reviewer":
        return """
        Human: You are a professional resume reviewer. Analyze the following resume and provide a detailed review. Follow these guidelines:
        1. Highlight the good points, areas for improvement, pros, cons, and suggestions for enhancing the resume.
        2. Provide actionable feedback to make the resume stand out.
        3. Structure your response with headings: "Strengths", "Areas for Improvement", "Suggestions", and "Overall Rating".
        4. Be specific and provide examples where applicable.
        5. If the user asks a question, provide accurate and relevant information based on the context. If you don't know the answer, say so and avoid speculation.

        <context>
        {context}
        </context>

        Question: {question}

        Assistant:"""
    
    else:
        return """
        Human: Use the following pieces of context to provide a concise and detailed answer to the question at the end. Follow these guidelines:
        1. Summarize with at least 250 words and provide detailed explanations.
        2. If you don't know the answer, just say that you don't know, and do not make up an answer.
        3. Structure your response logically, using paragraphs and bullet points where appropriate.
        4. Ensure the tone is professional and informative.
        5. If the user asks a question, provide accurate and relevant information based on the context. If you don't know the answer, say so and avoid speculation.

        <context>
        {context}
        </context>

        Question: {question}

        Assistant:"""
    # Function to display text with typewriter effect
 

# Function to display text with typewriter effect
def typewriter_effect(text, delay=0.005):
    placeholder = st.empty()  # Create an empty placeholder
    full_text = ""
    for char in text:
        full_text += char  # Add one character at a time
        placeholder.markdown(f"**Response:**\n\n{full_text}")  # Update the placeholder
        time.sleep(delay)  # Add a small delay

# Get Response from LLM (Updated with Spinner and Typewriter Effect)
 # Get Response from LLM (Updated with Spinner and Typewriter Effect)
def get_response_llm(llm, vectorstore_faiss, query, use_case):
    prompt_template = get_prompt_template(use_case)
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore_faiss.as_retriever(
            search_type="similarity", search_kwargs={"k": 3}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    # Step 1: Show loader while generating response
    with st.spinner("Generating response..."):
        answer = qa({"query": query})  # Generate the response
        response = answer['result']
    
    # Step 2: Display response with typewriter effect
    typewriter_effect(response)
    
# Streamlit App
def main():
    st.set_page_config(page_title="Chat PDF", layout="wide")
    
    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = []
    if "use_case" not in st.session_state:
        st.session_state.use_case = "General Chat"
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    # Sidebar for chat history
    with st.sidebar:
        st.title("Chat History")
        st.write("---")
        
        # Button to start a new chat
        if st.button("Start New Chat"):
            st.session_state.current_chat = []
            st.success("New chat started!")
        
        # Button to clear chat history
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.current_chat = []
            st.success("Chat history cleared!")
        
        # Display chat history
        for i, chat in enumerate(st.session_state.chat_history):
            with st.expander(f"Chat {i+1}"):
                for q, a in chat:
                    st.markdown(f"**Q:** {q}")
                    st.markdown(f"**A:** {a}")
                    st.write("---")
                
                # Button to revisit this chat
                if st.button(f"Revisit Chat {i+1}"):
                    st.session_state.current_chat = chat
                    st.success(f"Switched to Chat {i+1}")
                
                # Button to delete this chat
                if st.button(f"Delete Chat {i+1}"):
                    st.session_state.chat_history.pop(i)
                    st.success(f"Deleted Chat {i+1}")
                    st.rerun()

    # Main content area
    st.header("FlexiBot💁")
    st.write("Upload a PDF file and ask questions about its content.")

    # Use case dropdown
    use_case = st.selectbox(
        "Select Use Case",
        ["General Chat", "Medical Report Chat", "Book Summarizer", "Research Paper Summarizer", "Legal Document Summarizer", "Resume Reviewer"],
        key="use_case_selector"
    )

    # Reset app state if use case changes
    if use_case != st.session_state.use_case:
        st.session_state.use_case = use_case
        st.session_state.uploaded_file = None
        st.session_state.current_chat = []
        st.rerun()

    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf", key="file_uploader")
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

        # Generate a unique identifier for the uploaded file
        file_id = generate_file_id(uploaded_file)
        
        # Check if the vector store already exists
        if not os.path.exists(f"faiss_index_{file_id}"):
            # Process the uploaded PDF
            with st.spinner("Processing PDF..."):
                docs = data_ingestion(uploaded_file)
                get_vector_store(docs, file_id)
                st.success("PDF processed successfully! You can now ask questions.")
        else:
            st.success("PDF already processed! You can now ask questions.")

        # Ask questions
        user_question = st.text_input("Ask a Question from the PDF")

        if st.button("Claude Output"):
            ##with st.spinner("Generating response..."):
                try:
                    # Load the vector store
                    faiss_index = FAISS.load_local(
                        f"faiss_index_{file_id}",
                        bedrock_embeddings,
                        allow_dangerous_deserialization=True  # Enable deserialization
                    )
                    llm = get_claude_llm()
                    response = get_response_llm(llm, faiss_index, user_question, use_case)
                    
                    # Add question and answer to current chat
                    st.session_state.current_chat.append((user_question, response))
                    
                    # Add current chat to chat history if not already present
                    if st.session_state.current_chat not in st.session_state.chat_history:
                        st.session_state.chat_history.append(st.session_state.current_chat)
                    
                    # Display response
                    st.write("---")
                    # st.markdown("**Response:**")
                    # st.write(response)
                    st.success("Done")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        if st.button("Llama3 Output"):
            with st.spinner("Generating response..."):
                try:
                    # Load the vector store
                    faiss_index = FAISS.load_local(
                        f"faiss_index_{file_id}",
                        bedrock_embeddings,
                        allow_dangerous_deserialization=True  # Enable deserialization
                    )
                    llm = get_llama3_llm()
                    response = get_response_llm(llm, faiss_index, user_question, use_case)
                    
                    # Add question and answer to current chat
                    st.session_state.current_chat.append((user_question, response))
                    
                    # Add current chat to chat history if not already present
                    if st.session_state.current_chat not in st.session_state.chat_history:
                        st.session_state.chat_history.append(st.session_state.current_chat)
                    
                    # Display response
                    st.write("---")
                    st.markdown("**Response:**")
                    st.write(response)
                    st.success("Done")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()