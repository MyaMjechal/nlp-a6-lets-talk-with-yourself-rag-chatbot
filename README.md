# A6: Let’s Talk with Yourself  

**AT82.03: Machine Learning**  
**Instructors:** Professor Chaklam Silpasuwanchai, Todsavad Tangtortan

## Table of Contents  
- [Student Information](#student-information)  
- [Project Overview](#project-overview)  
- [Tasks](#tasks)  
  - [Task 1: Source Discovery](#task-1-source-discovery)  
  - [Task 2: Analysis and Problem Solving](#task-2-analysis-and-problem-solving)  
  - [Task 3: Chatbot Development - Web Application](#task-3-chatbot-development---web-application)  
- [Installation Setup](#installation-setup)  
- [Usage](#usage)  
- [Demo and Screenshots](#demo-and-screenshots)  
- [References](#references)  

## Student Information  
- **Name:** Mya Mjechal  
- **Student ID:** st125469  
- **Major:** AIT - Data Science and Artificial Intelligence (DSAI)  
- **Course:** AT82.03 Machine Learning  
- **Assignment:** A6: Let’s Talk with Yourself  

## Project Overview  

This project implements **Retrieval-Augmented Generation (RAG)** using the **LangChain framework** to create a chatbot named **MJBot**. The chatbot is designed to answer questions about myself based on personal data, such as my CV, resume, and other relevant documents. It leverages RAG to retrieve information from these sources and generate coherent, context-aware responses. The project includes a Jupyter notebook for development and a web application to demonstrate the chatbot's functionality interactively.  

The project is divided into three main tasks:  

1. **Source Discovery** – Collecting personal data sources and designing a prompt template for the chatbot.  
2. **Analysis and Problem Solving** – Evaluating retriever and generator models used in RAG and addressing potential issues.  
3. **Chatbot Development - Web Application** – Building a web app with a chat interface to showcase the chatbot’s capabilities.  

The chatbot is capable of answering a predefined set of 10 questions (listed in Task 3), with responses saved in a JSON file as part of the deliverables.  

## Tasks  

### Task 1: Source Discovery  
- **Objective:** Gather relevant personal data and design a prompt for the chatbot.  
- **Sources Used:**  
  - **MyaMjechal-CV.txt** – A text file containing my resume with details about education, work experience, skills, and personal information.  
  - **Reference Document:** The CV is the primary source loaded using `TextLoader` from LangChain.  
- **Prompt Design:**  
  - Created a custom prompt template for MJBot to provide friendly, accurate, and gentle responses based on my personal data.  
  - Example Prompt:  
    ```plaintext
    I'm your friendly NLP chatbot named MJBot, here to answer questions about Mya Mjechal myself based on my knowledge from my CV and personal data.
    The current year is 2025, and all answers should reflect this year unless otherwise specified.
    Whether you're curious about my education, work experience, or personal interests,
    I’ll provide accurate and gentle responses using the information I have.
    If I don't know something, I'll let you know kindly. Just let me know what you're wondering about, and I'll do my best to guide you through it!
    {context}
    Question: {question}
    Answer:
    ```  
- **Text-Generation Model Exploration:**  
  - Utilized the default generator model in the provided notebook but explored compatibility with **LLaMA3-70B** from Groq (limited request capacity). For this assignment, stuck with the notebook’s default setup due to resource constraints.  

### Task 2: Analysis and Problem Solving  
- **Retriever and Generator Models Used:**  
  - **Retriever Model:** `sentence-transformers` (version 2.2.2) for text embeddings, paired with `faiss-cpu` (version 1.7.4) for vector storage and retrieval.  
  - **Generator Model:** Default model from the LangChain setup (likely a transformer-based model like those from Hugging Face).  
- **Analysis of Issues:**  
  - **Retriever Issues:** Occasionally retrieved irrelevant chunks from the CV due to broad semantic similarity, especially with generic questions. For example, asking about "skills" might pull unrelated sections like hobbies.  
  - **Generator Issues:** Responses could be overly verbose or slightly off-topic if the retrieved context was not specific enough.  
  - **Mitigation:** Improved chunking strategy (future work) and refined prompt to focus on concise answers. Limited computational resources prevented extensive experimentation with alternative models.  

### Task 3: Chatbot Development - Web Application  
- **Objective:** Develop a web app showcasing MJBot with a chat interface.  
- **Features:**  
  - A text input box for users to type questions.  
  - Displays MJBot’s generated responses based on retrieved CV data.  
  - Provides source context (e.g., CV excerpts) alongside answers where applicable.  
- **Technologies Used:**  
  - **Backend:** Flask, LangChain, PyTorch, Transformers  
  - **Frontend:** HTML, Bootstrap  
- **Supported Questions:** MJBot can answer the following 10 questions:  
  1. How old are you?  
  2. What is your highest level of education?  
  3. What major or field of study did you pursue during your education?  
  4. How many years of work experience do you have?  
  5. What type of work or industry have you been involved in?  
  6. Can you describe your current role or job responsibilities?  
  7. What are your core beliefs regarding the role of technology in shaping society?  
  8. How do you think cultural values should influence technological advancements?  
  9. As a master’s student, what is the most challenging aspect of your studies so far?  
  10. What specific research interests or academic goals do you hope to achieve during your time as a master’s student?  
- **Sample JSON Output (qa_pairs.json):**  
  ```json
  [
    {
      "question": "How old are you?",
      "answer": "As of 2025, I am 25 years old."
    },
    {
      "question": "What is your highest level of education?",
      "answer": "My highest level of education will be a Master of Science in Data Science and Artificial Intelligence, expected in May 2025 from the Asian Institute of Technology."
    },
    ...
  ]
  ```

## Installation Setup  

1. **Clone the Repository:**  
   ```bash
   git clone https://github.com/MyaMjechal/nlp-a6-lets-talk-with-yourself.git
   cd nlp-a6-lets-talk-with-yourself
   ```  
2. **Environment Setup:**  
   - Navigate to the web application folder:  
     ```bash
     cd app/code
     ```  
   - Install dependencies:  
     ```bash
     pip install -r requirements.txt
     ```  
3. **Run the Web Application:**  
   - Start the Flask server:  
     ```bash
     python app.py
     ```  
   - Open your browser and navigate to [http://localhost:8000](http://localhost:8000).  

## Usage  

Once the web application is running:  
1. Open [http://localhost:8000](http://localhost:8000) in your browser.
2. Type a question from the supported list (or any related query) into the input box.
3. Click "Submit" to receive MJBot’s response, along with relevant context from my CV where applicable.

## Demo and Screenshots  

### Demo GIF  
![Demo GIF](images/mjbot_demo.gif)  
_GIF 1: Demonstration of MJBot answering questions about Mya Mjechal in the web application._  

### Screenshots  
**Web App Interface:**  
![mjbot_1](images/mjbot_1.png)  
_Figure 1: Initial web interface of MJBot._  

**Sample Response:**  
![mjbot_2](images/mjbot_2.png)  
_Figure 2: MJBot’s response to "What is your highest level of education?" with context from CV._  

## References  
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)  
- [RAG with LangChain](https://python.langchain.com/docs/integrations/chat/groq/)  
- [Sentence Transformers](https://huggingface.co/sentence-transformers)  
- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)  
