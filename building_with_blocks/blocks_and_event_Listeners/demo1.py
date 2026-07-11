import gradio as gr

def greet(name):
    return "Hello " + name + "!"

with gr.Blocks() as demo:
    name = gr.Textbox(label="您的姓名")
    output = gr.Textbox(label="輸出結果")
    greet_btn = gr.Button("送出問候")
    greet_btn.click(fn=greet,inputs=name,outputs=output,api_name="greet")

demo.launch()