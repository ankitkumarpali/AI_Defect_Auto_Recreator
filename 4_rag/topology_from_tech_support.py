import os
import re
import json
from dotenv import dotenv_values
from langchain_openai import AzureChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.schema import Document
import subprocess

# Load environment variables directly from .env
config = dotenv_values(".env")

# Access variables directly from the `config` dictionary
api_version = config["API_VERSION"]
api_endpoint = config["API_ENDPOINT"]
api_key = config["API_KEY"]
model_name = config["MODEL_NAME"]

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "books", "switch_tec_support.txt")
db_dir = os.path.join(current_dir, "db")

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist. Please check the path.")

# Load text content from the file
loader = TextLoader(file_path)
documents = loader.load()

# Confirm loaded documents
print(f"Documents loaded: {len(documents)}")

# Initialize embeddings
embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-ada-002",
    api_version=api_version,
    azure_endpoint=api_endpoint, 
    api_key=api_key
)

def create_azure_llm(api_version: str, api_endpoint: str, api_key: str, model_name: str):
    os.environ["LANGCHAIN_API_KEY"] = api_key
    return AzureChatOpenAI(
        api_version=api_version,
        azure_endpoint=api_endpoint,
        api_key=api_key,
        temperature=0.2,
        model=model_name,
    )

# Create and persist vector store
def create_vector_store(docs, store_name):
    persistent_directory = os.path.join(db_dir, store_name)
    if not os.path.exists(persistent_directory):
        print(f"\n--- Creating vector store {store_name} ---")
        db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_directory)
        print(f"--- Finished creating vector store {store_name} ---")
        print(f"Number of documents in vector store: {len(docs)}")
    else:
        print(f"Vector store {store_name} already exists. No need to initialize.")

def custom_text_splitter(text):
    # Regex pattern with two separate capturing groups for start and end markers
    pattern = r"(----.* show .*)|(^end\b|^----.* show)"
    chunks = []
    current_chunk = []
    in_chunk = False  # Track if we're currently within a chunk

    # Iterate over each line to match start or end markers
    for line in text:
        match = re.search(pattern, line)
        
        # Check if the line matches the start pattern
        if match and match.group(1):
            # If we're already in a chunk, save the current chunk and start a new one
            if in_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
            in_chunk = True
            current_chunk.append(line)
        
        # Check if the line matches the end pattern
        elif match and match.group(2):
            if in_chunk:
                current_chunk.append(line)
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                in_chunk = False  # Reset the chunk status
        
        # If we're in a chunk, add the line to the current chunk
        elif in_chunk:
            current_chunk.append(line)

    # Append any remaining chunk if it didn’t end with the end marker
    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks

# rec_char_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
# rec_char_docs = rec_char_splitter(documents)

text_content = documents[0].page_content if isinstance(documents, list) and documents else documents

lines = text_content.splitlines() if isinstance(text_content, str) else []

rec_char_docs = custom_text_splitter(lines)
print("split is", rec_char_docs)
rec_char_docs = [Document(page_content=chunk) for chunk in rec_char_docs]


# Confirm split documents
print(f"Number of split documents: {len(rec_char_docs)}")

create_vector_store(rec_char_docs, "chroma_db_rec_char")
persistent_directory = os.path.join(db_dir, "chroma_db_rec_char")

# Query vector store function with added checks
def query_vector_store(query, embedding_function, search_type, search_kwargs):
    if os.path.exists(persistent_directory):
        db = Chroma(persist_directory=persistent_directory, embedding_function=embedding_function)
        retriever = db.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
        relevant_docs = retriever.invoke(query)
        if relevant_docs:
            print("Relevant documents found.")
            return relevant_docs
        else:
            print("No relevant documents found.")
            return []
    else:
        print("Vector store directory does not exist.")
        return []


def generate_connection():
    model = create_azure_llm(api_version, api_endpoint, api_key, model_name)

    # Define the messages for the model
    print("combined_input", combined_input)
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=combined_input),
    ]

    # Invoke the model with the combined input
    result = model.invoke(messages)
    cleaned_content = re.sub(r"```json|```", "", result.content).strip()
    print("----------The result is-------------", cleaned_content)
    # Attempt to parse the output as JSON to ensure valid format
    try:
        json_output = json.loads(cleaned_content)  # Validate JSON format
        print("Result is valid JSON:", json_output)
        return json_output  # Return as a JSON object
    except json.JSONDecodeError:
        print("Output was not valid JSON. Please check the format of the model response.")
        return None

def save_connections(connections):
    json_path = os.path.join(current_dir, "connections.json")
    with open(json_path, "w") as file:
        json.dump(connections, file)
    print(f"Connections saved to {json_path}")


query_for_document = (
    "Provide the details of all devices connected to it, \
    Provide the interface where switchport mode trunk is enabled, \
    Provide the interface where switchport mode access is enabled,  \
    Provide the interfaces where no switchport is enabled, \
    Provide the etherchannel summary details, \
    Provide the interface details on Vlans allowed on trunk.\
    provide the details of all interfaces."\
)
# query = "show me the show cdp neighbours"
relevant_docs = query_vector_store(query_for_document, embedding_function=embeddings, search_type="similarity", search_kwargs={"k": 8})
next_query = (
    "Provide the details of interfaces "
    )

query_for_result = (
    "Provide the neighbor list in JSON format as follows: "
    "{"
    "\"connections\": ["
    "{\"switch\": \"Switch_B\", \"interface_ip\": \"192.168.1.1\", \"interface_port\": \"Gig0/1\", \"outgoing_interface_port\": \"Gig0/2\", \"vlan\": \"1\", \"vlan_type\": \"native/trunk\", \"version\": \"17.06.01\", \"color\": \"lightblue\", \"switchhport_type\": \"L2 or L3\", \"ospf_features\":\"ipv6 ospf 100 area 0 ipv6 ospf network point-to-point\"(if ipv6 ospf present), \"bfd_interval\":\"50 min_rx 50 multiplier 3\"}, "
    "{\"switch\": \"Switch_C\", \"interface_ip\": \"192.168.1.2\", \"interface_port\": \"Gig0/2\", \"outgoing_interface_port\": \"Gig0/6\",  \"vlan\": \"1\", \"vlan_type\": \"native/trunk\", \"version\": \"17.06.01\", \"color\": \"lightblue\",\"switchport_type\": \"L2 or L3\", \"ospf_features\":\"\", \"bfd_interval\":\"750 min_rx 50 multiplier 3\", \"ospf area\":\"BBBB\", }, "
    "], "
    "\"switch_name\": \"Switch_A\","
    "\"switchport_enabled_ports\": [\"Po14\", \"Gig10/1\"],"
    "\"switchport_access_ports\": [\"Ten10/1\", \"Gig10/1\"],"
    "\"trunk_enabled_ports\": [\"Po10\", \"Ten5/1\"],"
    "\"vlan_enabled_ports\": [\"Ten0/1\", \"Ten5/1\"],"
    "\"Po15\": [\"Ten0/1\", \"Ten5/1\", \"Ten5/1\"](Interfaces under po(portchannel) will be mentioned under show etherchannel summary),"
    "\All Port Channels\" = [\"Po1\", \"Po2\"],"
    "\macsec_interfaces\": [\"Ten0/1\", \"Ten5/1\", \"Ten5/1\"],"
    "\ospf_interfaces\":[\"Ten0/1\", \"Ten5/1\", \"Ten5/1\"](ipv6 ospf is present under interfaces),"
    "\multicast_interfaces\":[\"Ten0/1\", \"Ten5/1\", \"Ten5/1\"](ip pim sparse mode is present under those interfaces),"
    "}"
    ". Provide only the JSON output in the format shown, without any additional explanation or text.\
    under switchport_enabled_ports, switchport_access_ports, trunk_enabled_ports, vlan_enabled_ports ports will be there either they will be interface or portchannel. Switch name will be present as hostname. . Interface is L3 if no switchport is present under the interface otherwise it is L2\
    Channel number present under the interface is the port channel one.\
    \n Macsec enabled interaces have this phrase macsec network-link"
    
)
# \n ospf enable interfaces have this phrase \"ipv6 ospf\".\
#     \n bfd interval of some interface is given not applicable for every interface assign 0 if it is not present.\
#     \n For mka key check under key chain and the particular key-chain is present under interface like this mka pre-shared-key key-chain"

print("the relevant doc is:", relevant_docs)
if relevant_docs:
    combined_input = (
        "Here are some documents that might help answer the question: "
        + query_for_result
        + "\n\nRelevant Documents:\n"
        + "\n\n".join([doc.page_content for doc in relevant_docs])
        + "\n\nPlease provide the response strictly in JSON format as specified above, with no additional text."
    )
else:
    combined_input = "No relevant documents found."



if relevant_docs:
    connections = generate_connection()
    save_connections(connections)
else:
    print("No connections to generate, as there are no relevant documents.")

# Launch Streamlit app
subprocess.run(["streamlit", "run", os.path.join(current_dir, "streamlit_ui.py")])
