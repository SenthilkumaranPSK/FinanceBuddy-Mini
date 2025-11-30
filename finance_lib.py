import boto3
import json
import requests
from botocore.exceptions import NoCredentialsError, NoRegionError, ClientError

# Model ID
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
GEMINI_API_KEY = "AIzaSyCPZ5bf1N0Tq7LO-n7QjhnsY6TpxeAd1VQ" # From user memory

def get_bedrock_client(region=None, profile_name=None, aws_access_key_id=None, aws_secret_access_key=None):
    session_kwargs = {}
    if profile_name:
        session_kwargs['profile_name'] = profile_name
    if region:
        session_kwargs['region_name'] = region
    if aws_access_key_id and aws_secret_access_key:
        session_kwargs['aws_access_key_id'] = aws_access_key_id
        session_kwargs['aws_secret_access_key'] = aws_secret_access_key
        
    session = boto3.Session(**session_kwargs)
    return session.client(service_name='bedrock-runtime', region_name=region or "us-east-1")

def call_gemini(prompt, system_prompt=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    contents = [{"role": "user", "parts": [{"text": prompt}]}]
    
    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 4096
        }
    }
    
    if system_prompt:
        payload["systemInstruction"] = {
            "parts": [{"text": system_prompt}]
        }
        
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        raise Exception(f"Gemini API Error: {str(e)}")

def call_bedrock(prompt, system_prompt=None, credentials=None):
    if credentials is None:
        credentials = {}
        
    try:
        bedrock = get_bedrock_client(
            region=credentials.get('region'),
            profile_name=credentials.get('profile_name'),
            aws_access_key_id=credentials.get('aws_access_key_id'),
            aws_secret_access_key=credentials.get('aws_secret_access_key')
        )
        
        messages = [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]
        
        inference_config = {
            "maxTokens": 4096,
            "temperature": 0,
            "topP": 0.9
        }
        
        args = {
            "modelId": MODEL_ID,
            "messages": messages,
            "inferenceConfig": inference_config
        }
        
        if system_prompt:
            args["system"] = [{"text": system_prompt}]

        response = bedrock.converse(**args)
        
        return response['output']['message']['content'][0]['text']
        
    except (NoCredentialsError, NoRegionError, ClientError) as e:
        print(f"AWS Error: {e}. Falling back to Gemini...")
        return call_gemini(prompt, system_prompt)
    except Exception as e:
        if "credentials" in str(e).lower() or "region" in str(e).lower():
             print(f"AWS Error: {e}. Falling back to Gemini...")
             return call_gemini(prompt, system_prompt)
        raise e

# --- Agents ---

def parse_file(csv_content):
    system_prompt = """You are a Financial File Parser Agent.
    Analyze the CSV content and normalize it into a JSON structure.
    Detect columns for Date, Description, and Amount.
    
    Output JSON format:
    {
        "rows": <count>,
        "currency": "INR",
        "fields_detected": ["date", "description", "amount"],
        "normalized_data": [
            {"date": "YYYY-MM-DD", "description": "...", "amount": 123.45},
            ...
        ]
    }
    """
    prompt = f"CSV Content:\n{csv_content}"
    response = call_bedrock(prompt, system_prompt)
    return _clean_json(response)

def categorize_transactions(transactions):
    system_prompt = """You are a Transaction Categorizer Agent.
    Assign categories to each transaction.
    Categories: Food, Transport, Bills, Shopping, Subscriptions, Salary, Rent, Entertainment, Unknown.
    
    Output JSON list:
    [
        {"description": "...", "amount": ..., "category": "..."}
    ]
    """
    prompt = f"Transactions:\n{json.dumps(transactions)}"
    response = call_bedrock(prompt, system_prompt)
    return _clean_json(response)

def detect_anomalies(transactions):
    system_prompt = """You are a Financial Anomaly Detection Agent.
    Detect suspicious or abnormal transactions (sudden spikes, recurring duplicates, unknown merchants).
    
    Output JSON:
    {
        "anomalies_detected": <count>,
        "items": [
            {"description": "...", "amount": ..., "reason": "..."}
        ]
    }
    """
    prompt = f"Transactions:\n{json.dumps(transactions)}"
    response = call_bedrock(prompt, system_prompt)
    return _clean_json(response)

def forecast_and_plan(transactions):
    system_prompt = """You are a Financial Forecasting & Planning Agent.
    Analyze spending patterns to predict next month's expenses and suggest a plan.
    
    Output JSON:
    {
        "predicted_spending": <amount>,
        "suggested_plan": [
            "Reduce X by ...",
            "Cap Y at ...",
            "..."
        ],
        "savings_target": <amount>,
        "explanation": "..."
    }
    """
    prompt = f"Transactions:\n{json.dumps(transactions)}"
    response = call_bedrock(prompt, system_prompt)
    return _clean_json(response)

def _clean_json(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    try:
        return json.loads(text)
    except:
        return {}
