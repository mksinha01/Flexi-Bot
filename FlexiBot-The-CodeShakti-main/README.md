# FlexiBot: A PDF Chatbot 🤖📄  

Welcome to **FlexiBot**, an intelligent PDF chatbot built to simplify document interaction using advanced AI models like **Claude** and **Llama 3**. This project was developed during the **Prompt Builder Hackathon** by a team of passionate developers. FlexiBot allows users to upload PDFs, ask questions, and get detailed, context-aware responses for various use cases like summarizing medical reports, books, legal documents, and more.  

---

## 🚀 Features  

- **Multi-Use Case Support**: Handles medical reports, books, research papers, legal documents, and resume reviews.  
- **Advanced AI Models**: Powered by **Claude** and **Llama 3** via **AWS Bedrock** for accurate and context-aware responses.  
- **Vector Embeddings**: Uses **AWS Bedrock's Titan Embeddings** to process and understand document content.  
- **Chat History**: Keeps track of conversations for easy reference and revisiting.  
- **Typewriter Effect**: Displays responses with a fun and engaging typewriter effect.  
- **User-Friendly Interface**: Built with **Streamlit** for a seamless user experience.  

---

## 🛠️ Tech Stack  

- **AWS Bedrock**: For embeddings (Titan Embeddings) and language models (Claude, Llama 3).  
- **LangChain**: For document processing, text splitting, and retrieval-augmented generation.  
- **Streamlit**: For the interactive and user-friendly web interface.  
- **FAISS**: For efficient vector storage and similarity search.  
- **Python Libraries**:  
  - `boto3`: For interacting with AWS services.  
  - `hashlib`: For generating unique file IDs.  
  - `PyPDFLoader`: For loading and extracting text from PDFs.  

---

## 📂 Project Structure  

```
FlexiBot/  
├── app.py                  # Main Streamlit application  
├── requirements.txt        # List of dependencies  
├── README.md               # Project documentation  
├── faiss_index/            # Directory to store FAISS vector indices  
└── temp/                   # Temporary storage for uploaded files  
```

---

## 🚀 How It Works  

1. **Upload a PDF**: Users upload a PDF file through the Streamlit interface.  
2. **Process the PDF**:  
   - The PDF is split into smaller chunks using **RecursiveCharacterTextSplitter**.  
   - Text chunks are converted into vector embeddings using **AWS Bedrock's Titan Embeddings**.  
   - Embeddings are stored in a **FAISS vector store** for efficient similarity search.  
3. **Ask Questions**: Users can ask questions related to the PDF content.  
4. **Generate Responses**:  
   - The chatbot retrieves relevant text chunks from the FAISS vector store.  
   - The retrieved text is passed to **Claude** or **Llama 3** along with a use-case-specific prompt template.  
   - The AI model generates a response, which is displayed with a typewriter effect.  
5. **Chat History**: All questions and answers are saved in the chat history for future reference.  

---

## 🛠️ Installation  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/your-username/FlexiBot.git  
   cd FlexiBot  
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Set up AWS credentials:  
   - Ensure you have AWS CLI configured with access to **AWS Bedrock**.  

4. Run the Streamlit app:  
   ```bash  
   streamlit run app.py  
   ```  

5. Open your browser and navigate to `http://localhost:8501` to use FlexiBot.  

---

## 🧑‍💻 Team  

This project was built by:  
- Om singh
- Anjali  
- Vaishnavi Raj  
- Diya Sharma  

---

 

## 🤝 Contributing  

Contributions are welcome! If you'd like to contribute, please:  
1. Fork the repository.  
2. Create a new branch for your feature or bugfix.  
3. Submit a pull request.  

---

## 🙏 Acknowledgments  

- Thanks to **AWS Bedrock** for providing powerful AI models.  
- Thanks to **LangChain** for simplifying document processing and retrieval.  
- Thanks to **Streamlit** for making it easy to build interactive web apps.  

---

Let us know your thoughts and feedback! 🚀  

---
