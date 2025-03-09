import gradio as gr
from bedrock import get_bedrock_response
from dotenv import load_dotenv

def submit_text(input_text):
    # Call the bedrock API and get the response
    response = get_bedrock_response(input_text)
    return response

def chat_interface(user_message, history,state):
    if history is None:
        history = []
    if state is None:
        state = []
    response,new_state = get_bedrock_response(user_message, history,state)
    return response,new_state

chat_state_component = gr.State(value = None)

demo = gr.ChatInterface(
    fn=chat_interface,
    title="Amazon Bedrock Chat",
    additional_inputs=[chat_state_component],
    additional_outputs=[chat_state_component],
    description="チャット形式でAmazon Bedrockとの連携を行うインターフェースです。"
)

if __name__ == "__main__":
    load_dotenv()
    demo.launch()
