import gradio as gr
from bedrock import get_bedrock_response

def submit_text(input_text):
    # Call the bedrock API and get the response
    response = get_bedrock_response(input_text)
    return response


def alternatingly_agree(message, history):
    if len([h for h in history if h['role'] == "assistant"]) % 2 == 0:
        return f"Yes, I do think that: {message}"
    else:
        return "I don't think so"



demo = gr.ChatInterface(
    fn=alternatingly_agree,
    type="messages",
    title="Amazon Bedrock Interface",
    description="Enter text to query the model via Amazon Bedrock."
)

if __name__ == "__main__":
    demo.launch()
