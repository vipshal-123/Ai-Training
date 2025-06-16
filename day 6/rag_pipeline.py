import os
from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from prompts import ELEVATOR_PITCH_PROMPT, HR_QUESTION_PROMPT, KEYWORD_EXTRACTION_PROMPT 

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# Initialize Gemini Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",  # Recommended default
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def generate_outputs(resume_text, jd_text):
    # Split text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    resume_chunks = text_splitter.split_text(resume_text)
    jd_chunks = text_splitter.split_text(jd_text)
    all_docs = resume_chunks + jd_chunks

    # Create FAISS vectorstore
    vectorstore = FAISS.from_texts(all_docs, embedding=embeddings)

    # Search for relevant context
    relevant_docs = vectorstore.similarity_search(jd_text, k=5)
    context = "\n".join([doc.page_content for doc in relevant_docs])

    # Generate function using RunnableSequence
    def generate(prompt_template):
        prompt = PromptTemplate(input_variables=["context"], template=prompt_template)
        chain = prompt | llm
        response = chain.invoke({"context": context})
        content = getattr(response, "content", str(response))
        return content.strip()


    # Generate pitch, keywords, and questions
    pitch = generate(ELEVATOR_PITCH_PROMPT).strip()
    keywords = [k.strip() for k in generate(KEYWORD_EXTRACTION_PROMPT).split(",")]
    questions = [
        q.strip("- ").strip()
        for q in generate(HR_QUESTION_PROMPT).split("\n") if q.strip()
    ]

    return pitch, keywords, questions
