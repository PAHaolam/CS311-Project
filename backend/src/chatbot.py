from llama_index.core import Settings, SummaryIndex, SimpleDirectoryReader
#from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.groq import Groq
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from decouple import config
import logging
import sys

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO
)  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# Set up the Groq class with the required model and API key
Settings.llm = Groq(model="llama3-8b-8192", api_key=config("GROQ_API_KEY"))


Settings.embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="my-custom-embedding",
    api_key=config("AZURE_OPENAI_API_KEY"),
    azure_endpoint=config("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview",
)

documents = SimpleDirectoryReader('src/data').load_data()
#loader = WikipediaReader()
#documents = loader.load_data(pages=["Messi Lionel"])
parser = SimpleNodeParser.from_defaults()
nodes = parser.get_nodes_from_documents(documents)
index = SummaryIndex(nodes)
query_engine = index.as_query_engine()


# #Hàm hỏi đáp
def ask_question(question: str):
    response = query_engine.query(question)
    return response.response