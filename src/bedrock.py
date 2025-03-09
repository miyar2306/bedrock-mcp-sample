import os
import json
import boto3

def get_bedrock_response(input_text, history,state):
    """
    AWS認証情報を用いてAmazon Bedrock Converse APIを呼び出す。
    """
    # AWS認証情報のチェック
    if not (os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY")):
        return "Error: AWS認証情報が不足している。", history

    BEDROCK_MODEL_ID = "us.amazon.nova-pro-v1:0"
    system = [{"text": "You are a helpful AI assistant."}]
    state.append({
                "role": "user",
                "content": [{"text": input_text}]
            })
    
    messages = state.copy()

    try:
        client = boto3.client("bedrock-runtime")
    except Exception as e:
        return f"Error creating boto3 client: {e}", history

    try:
        response = client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=messages,
            system=system,
            inferenceConfig={
                "maxTokens": 300,
                "topP": 0.1,
                "temperature": 0.3
            }
        )
        output_message = response['output']['message']
        messages.append(output_message)
        response_text = ""
        for content in output_message['content']:
            if 'text' in content:
                response_text += content['text'] + "\n"
        # 履歴はタプル形式にして追加する
        # history.append((input_text, response_text))
        return response_text,messages
    except Exception as e:
        return f"Error invoking Bedrock Converse API: {e}"
