import gradio as gr

def alternatingly_agree(message, history):
    if len([h for h in history if h['role']=='assistant']) % 2 == 0:
        return f"沒錯，我也這麼認為：{message}"
    else:
        return "我不這麼認為"

gr.ChatInterface(
    fn = alternatingly_agree,
    type = "messages"
).launch()