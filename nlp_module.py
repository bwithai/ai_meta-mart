import os
import time

import openai
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

from langchain.document_loaders import TextLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

template = """/ 
{context}: You are the Meta-Mart Assistant and your name is 'Hayathi'. No extra words or explanation just give the product name and quantity value. if not found just say `False`
Question: {question}
Answer: 
"""

PROMPT = PromptTemplate(template=template, input_variables=["context", 'question'])

# Text Splitter
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

embeddings = OpenAIEmbeddings()


def extract_tp_sl_values(file):
    loader = TextLoader(file)
    documents = loader.load()
    # print(documents)

    # Text Splitter
    docs = text_splitter.split_documents(documents)

    # Vectorstore: https://python.langchain.com/en/latest/modules/indexes/vectorstores.html
    db = FAISS.from_documents(docs, embeddings)
    retriever = db.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff",
                                           retriever=retriever,
                                           chain_type_kwargs={"prompt": PROMPT})

    query = "i am sanaullah. I need 5kg meet. can you help me with this."

    # Get the answer from the chain
    start = time.time()
    res = qa_chain(query)
    answer = res['result']
    end = time.time()

    # Print the result
    print("\n\n> Question:")
    print(query)
    print(f"\n> Answer (took {round(end - start, 2)} s.):")
    print(answer)

    return answer

extract_tp_sl_values("message.txt")
