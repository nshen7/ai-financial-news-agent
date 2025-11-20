import vertexai

from vertexai.generative_models import GenerativeModel
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA

vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")
model = GenerativeModel("gemini-1.5-flash-001")  # Free tier

def build_rag(articles, depth='beginner'):
    texts = [a['content'] for a in articles]
    splitter = CharacterTextSplitter(chunk_size=500 if depth == 'beginner' else 1000)
    chunks = splitter.create_documents(texts)
    embeddings = VertexAIEmbeddings(model_name="textembedding-gecko@001")  # Free embeddings
    vectorstore = FAISS.from_documents(chunks, embeddings)
    qa_chain = RetrievalQA.from_chain_type(llm=model, retriever=vectorstore.as_retriever())
    query = "Summarize key financial news impacts on the stock, focusing on trends."
    return qa_chain.run(query)