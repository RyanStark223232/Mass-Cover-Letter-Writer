import PyPDF2
import openai
import requests

# Local API of a LLM
LOCAL_API_URL = "http://127.0.0.1:5000"

def send_prompt(prompt, openai_key = None):
	if openai_key is None:
		params = {'prompt': prompt}
		response = requests.get(f"{LOCAL_API_URL}/generate", params=params)
		return response.json() if response.status_code == 200 else None
	else:
		openai.api_key = openai_key
		response = openai.ChatCompletion.create(
		  model="gpt-3.5-turbo",
		  messages=[
		        {"role": "system", "content": "You are a helpful assistant."},
		        {"role": "user", "content": prompt},
		    ]
		)
		return response['choices'][0]['message']['content']

def read_document(file_path):
    if file_path.endswith('.txt'):
        with open(file_path, 'r', errors='ignore') as file:
            document = file.read()
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            document = ""
            for page in pdf_reader.pages:
                document += page.extract_text() + "\n\n"
    return document