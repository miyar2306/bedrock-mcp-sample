import os
import json
import boto3
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def get_bedrock_response(input_text, history,state):
    """
    Call Amazon Bedrock Converse API using AWS credentials.
    """

    async with stdio_client(
        StdioServerParameters(command="uv", args=["run", "mcp-fetch-website"])
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

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
                # Add history in tuple format
                # history.append((input_text, response_text))
                return response_text,messages
            except Exception as e:
                return f"Error invoking Bedrock Converse API: {e}",messages
