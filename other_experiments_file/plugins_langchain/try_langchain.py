import os
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
import time

FILE_PATH = '/Users/nikunjbajaj/work/truefoundry/hackathon-fatt-se-ho-gya/transcripts/files'
os.environ["OPENAI_API_KEY"] = "API-KEY"

s = time.time()
loader = DirectoryLoader(path=FILE_PATH)
print(f"Step 1 {time.time() - s}")
s = time.time()
index = VectorstoreIndexCreator().from_loaders([loader])
print(f"Step 2 {time.time() - s}")
s = time.time()
query = "Bill will work together with you on the GPUs, like provisioning GPUs"
print(index.query(query))
print(f"Step 3 {time.time() - s}")
s = time.time()

query = "Bill will work together with you on the GPUs, like provisioning GPUs"
print(index.query_with_sources(query))
print(f"Step 4 {time.time() - s}")
s = time.time()

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9)
chain = load_qa_chain(llm, chain_type="stuff")
docs = loader.load()
print(f"Document loading and chain initialisation {time.time() - s}")
s = time.time()

query = "Why are companies using Sagemaker?"
print(chain.run(input_documents=docs, question=query))
print(f"Step 5 {time.time() - s}")
s = time.time()

query = "Which companies are using Sagemaker?"
print(chain.run(input_documents=docs, question=query))
print(f"Step 6 {time.time() - s}")
s = time.time()

query = "Which companies are using Kubeflow? Why are they using it?"
print(chain.run(input_documents=docs, question=query))
print(f"Step 7 {time.time() - s}")
s = time.time()

query = "Which part of ML stack is the most problematic?"
print(chain.run(input_documents=docs, question=query))
print(f"Step 8 {time.time() - s}")
s = time.time()