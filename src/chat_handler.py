from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import sys
import requests
from googlesearch import search
import html2text
import json
from datetime import datetime

# import google.generativeai as genai
from google import genai
from google.genai import types

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config
from src.preprocessing import CryptoPreprocessor

load_dotenv()
# Cấu hình API
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model = "gemini-2.0-flash"

crypto_preprocessor = CryptoPreprocessor(config.CRYPTO_FILENAME)
crypto_symbols = crypto_preprocessor.get_tokens()
# Define the function declaration for the model
search_google = {
    "name": "search_google",
    "description": "Tra cứu thông tin trên google",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "enum": crypto_symbols[:100],
            },
        },
        "required": ["query"],
    },
}

tools_1 = types.Tool(function_declarations=[search_google])
tool_config_1 = types.ToolConfig(
    function_calling_config=types.FunctionCallingConfig(
        mode="ANY",
        allowed_function_names=[
            "search_google",
        ],
    )
)
config_1 = types.GenerateContentConfig(
    temperature=0,
    tools=[tools_1],
    tool_config=tool_config_1,
)

class Classification:
    def __init__(self, client):
        self.client = client
    def load_crypto_history_prompt(self, symbol):
        scraper = CryptoPreprocessor(config.CRYPTO_FILENAME)
        data = scraper.load_crypto_history(symbol)
        prompt = scraper.format_prompt(data, symbol)
        return prompt
    
    def search_google_function_call(self, query):
        try:
            # Initialize html2text
            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            h.ignore_emphasis = True
            h.ignore_tables = True
            h.single_line_break = True
            
            results = []
            # Search for 3 URLs
            query = f"Tình hình thị trường {query}"
            search_results = search(query, num_results=3)
            content = ""
            for url in search_results:
                try:
                    # Get webpage content
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    
                    # Parse HTML
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Remove unwanted elements
                    for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
                        element.decompose()
                    
                    # Remove all class and id attributes
                    for tag in soup():
                        tag.attrs = {}
                    
                    # Convert HTML to text
                    text = h.handle(str(soup))
                    
                    # Clean up the text
                    text = ' '.join(line.strip() for line in text.splitlines() if line.strip())
                    text = ' '.join(text.split())
                    
                    content += f"{text[:2000]}\n"
                    
                except Exception as e:
                    print(f"Error processing URL {url}: {str(e)}")
                    continue
            
            # Save results to JSON file
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            os.makedirs(output_dir, exist_ok=True)
            
            output_file = os.path.join(output_dir, f'{query}_search_results.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({"content": content}, f, ensure_ascii=False, indent=2)
            
            print(f"Results saved to: {output_file}")
            return content
            
        except Exception as e:
            print(f"Error in search_google: {str(e)}")
            return []

    # Send request with function declarations
    def chat_with_google(self, prompt):
        contents = f"""Bạn là một chuyên gia về tiền điện tử. Hãy dự đoán xu thế của thị trường tiền điện tử trong tương lai.
        Cuối cùng phải có câu trả lời dự đoán xu thế của thị trường tiền điện tử trong tương lai.
        Câu hỏi:
        {prompt}"""
        response = self.client.models.generate_content(
            model=model,
            contents=contents,
            config=config_1,
        )
        # Check for a function call
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            # print(f"Function to call: {function_call.name}")
            # print(f"Arguments: {function_call.args}")
            google_info = self.search_google_function_call(function_call.args["query"])
            crypto_history_prompt = self.load_crypto_history_prompt(f"{function_call.args['query']}")
            content_with_google_info = f"""Bạn là một chuyên gia về tiền điện tử. Hãy dự đoán xu thế của thị trường tiền điện tử trong tương lai.
            Câu hỏi:
            {prompt}
            Lịch sử giá gần nhất của {function_call.args["query"]}:
            {crypto_history_prompt}
            Thông tin tìm kiếm trên google:
            {google_info}"""
            contents = content_with_google_info
            response = self.client.models.generate_content(
                model=model,
                contents=contents
            )
            return response
        else:
            print("No function call found in the response.")
            print(response.text)
        return response

def main():
    classification = Classification(client)
    res = classification.chat_with_google("Tình hình thị trường BTC")
    print(res)
    

if __name__ == "__main__":
    main()
