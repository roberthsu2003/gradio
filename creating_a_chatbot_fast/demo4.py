import gradio as gr

def yes_man(message, history):
    if message.endswith("?"):
        return "Yes"
    else:
        return "Ask me anything!"

demo = gr.ChatInterface(
    fn = yes_man,
    type= "messages",
    chatbot = gr.Chatbot(height=300),
    textbox = gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=7),
    title = "Yes Man",
    description = "Ask Yes Man any question",
    theme = "ocean",
    examples = ["Hello", "Am I cool?", "Are tomatoes vegetables?"]
)

demo.launch()