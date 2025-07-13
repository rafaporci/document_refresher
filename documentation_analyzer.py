import os
import requests
import glob 

from io import BytesIO
from openai import OpenAI

if not os.environ.get("OPENAI_API_KEY"):
    print(f"OPENAI_API_KEY environment variable empty")
    exit(-1)

def build_client():
    client = OpenAI()
    client.api_key = os.environ.get("OPENAI_API_KEY")
    return client

def create_file(client, vector_store_id, file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        # Download the file content from the URL
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)
        result = client.files.create(
            file=file_tuple,
            purpose="assistants"
        )
    else:
        # Handle local file path
        with open(file_path, "rb") as file_content:
            result = client.files.create(
                file=file_content,
                purpose="assistants"
            )
    print(result.id)

    client.vector_stores.files.create(
        vector_store_id=vector_store_id,
        file_id=result.id
    )

    return result.id

def create_vector_store():
    client = build_client()

    vector_store = client.vector_stores.create(
        name="knowledge_base"
    )
    print(vector_store.id)

    # Replace with your own file path or URL
    contents = glob.glob("./working-dir/py_files/**/*", recursive=True)

    for file in contents:
        if os.path.isfile(file):
            #print(file)
            file_id = create_file(client, vector_store.id, file)

    result = client.vector_stores.files.list(
        vector_store_id=vector_store.id
    )
    print(result)

    return vector_store.id

def analyze_document(path, vector_store_id):
    client = build_client()

    with open(path, 'r') as f:
        document = "".join(f.readlines())

    prompt_base = "Considering you are a Senior Business Analyst and you are analyzing the availble documentation for the application (cleaned_sample_classifieds_api.zip file). Propose meaningful changes for this page:"
    prompt = "\r\n".join([prompt_base, document])

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }]
    )
    print(response)

#create_vector_store()
analyze_document("./working-dir/sample_classifieds_api-main/docs/ad_slot_purchase.md", "vs_6873993b02688191bd7d56ea7eb1b208")

#### Next-Steps

# How to extract only the changes from the Chat output? 
# How to open a MR?
# Adapt the  in the working-dir the repo extracted (needed to read the md files in the vector_store step)