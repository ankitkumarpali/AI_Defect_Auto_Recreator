import os
from dotenv import dotenv_values
from langchain_openai import AzureChatOpenAI

# Load environment variables directly from .env
config = dotenv_values(".env")

# Access variables directly from the `config` dictionary
api_version = config["API_VERSION"]
api_endpoint = config["API_ENDPOINT"]
api_key = config["API_KEY"]
model_name = config["MODEL_NAME"]

def create_azure_llm(api_version: str, api_endpoint: str, api_key: str, model_name: str):
    print(f"API_VERSION: {api_version}")
    print(f"API_ENDPOINT: {api_endpoint}")
    print(f"API_KEY: {api_key}")
    os.environ["LANGCHAIN_API_KEY"] = api_key
    return AzureChatOpenAI(
        api_version=api_version,
        azure_endpoint=api_endpoint,
        api_key=api_key,
        temperature=0.2,
        model=model_name,
    )

# Create a ChatOpenAI model
model = create_azure_llm(api_version, api_endpoint, api_key, model_name)

# Invoke the model with a message
result = model.invoke("What is 81 divided by 9?")
print("Full result:")
print(result)
print("Content only:")
print(result.content)
