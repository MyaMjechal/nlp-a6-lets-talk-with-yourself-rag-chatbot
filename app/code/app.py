from flask import Flask, request, render_template, jsonify
import os
import torch
from langchain import PromptTemplate
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def initialize_chain():
    # Define prompt template
    prompt_template = """
        I'm your friendly NLP chatbot named GrokBot, here to answer questions based on provided documents.
        The current year is 2025, and all answers should reflect this year unless otherwise specified.
        I'll provide accurate and helpful responses using the information I have.
        If I don't know something, I'll let you know kindly. Just let me know what you're wondering about!
        {context}
        Question: {question}
        Answer:
        """.strip()

    PROMPT = PromptTemplate.from_template(template=prompt_template)

    # Load and process document
    cv_file = '../../data/MyaMjechal-CV.txt'
    loader = TextLoader(cv_file)
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    doc = text_splitter.split_documents(documents)

    # Initialize embeddings
    model_name = "all-MiniLM-L6-v2"
    embedding_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device}
    )

    # Create vector store
    vector_store = FAISS.from_documents(doc, embedding_model)

    # Load LLM
    llm = ChatGroq(
        model="gemma2-9b-it",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other parameters as needed
    )

    # Set up conversational retrieval chain
    retriever = vector_store.as_retriever()

    question_generator = LLMChain(
        llm=llm,
        prompt=CONDENSE_QUESTION_PROMPT,
        verbose=True
    )

    doc_chain = load_qa_chain(
        llm=llm,
        chain_type='stuff',
        prompt=PROMPT,
        verbose=True
    )

    memory = ConversationBufferWindowMemory(
        k=3,
        memory_key="chat_history",
        return_messages=True,
        output_key='answer'
    )

    chain = ConversationalRetrievalChain(
        retriever=retriever,
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        return_source_documents=True,
        memory=memory,
        verbose=True,
        get_chat_history=lambda h: h
    )

    return chain

# Initialize the chain
chain = initialize_chain()

# Store chat history
chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    data = request.get_json()
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'response': 'Please ask a question!', 'sources': []})

    # Run the chain with the user message and chat history
    result = chain({"question": user_message, "chat_history": chat_history})
    answer = result["answer"]
    source_docs = result["source_documents"]

    # Extract sources
    # sources = [doc.metadata.get('source', 'Unknown') for doc in source_docs]
    sources = list({doc.metadata.get('source', 'Unknown') for doc in source_docs})

    # Update chat history
    chat_history.append((user_message, answer))
    # Limit history to last 5 exchanges to manage memory
    if len(chat_history) > 5:
        chat_history = chat_history[-5:]

    return jsonify({
        'user_message': user_message,
        'response': answer,
        'sources': sources
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
