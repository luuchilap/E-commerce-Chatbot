import os

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate,
                               SystemMessagePromptTemplate)
from langchain.vectorstores import Chroma

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def init_conversation(file_path: str):
    # Load data
    loader = CSVLoader(file_path=file_path)
    data = loader.load()

    # Embedding and vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(data, embeddings)

    # Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Choose LLM Model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)

    # Define the system message template
    system_template = """The provided {context} is about the product information.
    This dataset includes the following columns:
    'product_name': name of the product,
    'product_price': the price of the product
    
    ----------------
    {context}"""

    # Create the chat prompt templates
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
    qa_prompt = ChatPromptTemplate.from_messages(messages)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=False,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        memory=memory,
        verbose=False,
    )

    return qa


def chat_with_llm(qa, query: str):
    return qa.run({"question": query})
