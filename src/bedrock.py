import os
import json
import requests

def get_bedrock_response(input_text):
    """
    Calls the Amazon Bedrock API to get a response for the input_text.
    Loads the configuration from config/config.json.
    If the endpoint is not configured, returns a simulated response.
    """
    # Determine the path for the configuration file
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        return f"Error loading configuration: {e}"

    # Retrieve API endpoint and API key from configuration
    endpoint = config.get('bedrock_endpoint')
    api_key = config.get('api_key')

    # If no endpoint is provided, return a simulated response
    if not endpoint:
        return f"Simulated response from Bedrock for input: {input_text}"

    # Prepare headers and payload for the API request
    headers = {
        'Content-Type': 'application/json'
    }
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    payload = {
        "input": input_text
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get('result', 'No result found in response.')
    except Exception as e:
        return f"Error calling Bedrock API: {e}"
