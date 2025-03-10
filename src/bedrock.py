import os
import json
import boto3
import logging
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_tool_format(tools):
    """
    Converts tools into the format required for the Bedrock API.

    Args:
        tools (list): List of tool objects

    Returns:
        dict: Tools in the format required by Bedrock
    """
    converted_tools = []

    for tool in tools:
        converted_tool = {
            "toolSpec": {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": {
                    "json": tool.inputSchema
                }
            }
        }
        converted_tools.append(converted_tool)

    return {"tools": converted_tools}


async def get_bedrock_response(input_text, history,state):
    """
    AWS認証情報を用いてAmazon Bedrock Converse APIを呼び出す。
    """

    async with stdio_client(
        StdioServerParameters(command="uv", args=["run", "mcp-fetch-website"])
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            BEDROCK_MODEL_ID = "us.amazon.nova-pro-v1:0"
            tools_result = await session.list_tools()
            tools_list = [{"name": tool.name, "description": tool.description,
                          "inputSchema": tool.inputSchema} for tool in tools_result.tools]
            logger.info("Available tools: %s", tools_list)

            # Prepare the request for Nova Pro model
            system = [
                {
                    "text": "You are a helpful AI assistant. You have access to the following tools: " +
                    json.dumps(tools_list) + "Speak in Japanese"
                }
            ]
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
                while True:
                    response = client.converse(
                        modelId=BEDROCK_MODEL_ID,
                        messages=messages,
                        system=system,
                        inferenceConfig={
                            "maxTokens": 300,
                            "topP": 0.1,
                            "temperature": 0.3
                        },
                        toolConfig=convert_tool_format(tools_result.tools)
                    )
                    stop_reason = response['stopReason']
                    output_message = response['output']['message']
                    messages.append(output_message)
                    if stop_reason == 'tool_use':
                        # Tool use requested. Call the tool and send the result to the model.
                        tool_requests = response['output']['message']['content']
                        for tool_request in tool_requests:
                            if 'toolUse' in tool_request:
                                tool = tool_request['toolUse']
                                logger.info("Requesting tool %s. Request: %s",
                                            tool['name'], tool['toolUseId'])

                                try:
                                    # Call the tool through the MCP session
                                    tool_response = await session.call_tool(tool['name'], tool['input'])

                                    # Convert tool response to expected format
                                    tool_result = {
                                        "toolUseId": tool['toolUseId'],
                                        "content": [{"text": str(tool_response)}]
                                    }
                                except Exception as err:
                                    logger.error("Tool call failed: %s", str(err))
                                    tool_result = {
                                        "toolUseId": tool['toolUseId'],
                                        "content": [{"text": f"Error: {str(err)}"}],
                                        "status": "error"
                                    }

                                # Add tool result to messages
                                messages.append({
                                    "role": "user",
                                    "content": [{"toolResult": tool_result}]
                                })
                    else:
                        response_text = ""
                        for content in output_message['content']:
                            if 'text' in content:
                                response_text += content['text'] + "\n"
                        return response_text,messages
            except Exception as e:
                return f"Error invoking Bedrock Converse API: {e}",messages
