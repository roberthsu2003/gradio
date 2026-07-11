import gradio as gr

def yes_man(message, history):
    if message.endswith("?"):
        return "是的！"
    else:
        return "請儘管問我任何問題！"

demo = gr.ChatInterface(
    fn = yes_man,
    type= "messages",
    chatbot = gr.Chatbot(height=300),
    textbox = gr.Textbox(placeholder="請輸入一個是非題（以問號 ? 結尾）...", container=False, scale=7),
    title = "👍 是是先生 (Yes Man)",
    description = "問『是是先生』任何問題，他都會欣然同意！",
    theme = "ocean",
    examples = ["你好", "我很酷嗎？", "番茄是蔬菜嗎？"]
)

demo.launch()