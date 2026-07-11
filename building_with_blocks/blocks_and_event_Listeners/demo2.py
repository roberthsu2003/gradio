#使用decorator的寫法

import gradio as gr

with gr.Blocks() as demo:
    name = gr.Textbox(label="您的姓名")
    output = gr.Textbox(label="輸出框")
    greet_btn = gr.Button("送出問候")

    @greet_btn.click(inputs=name, outputs=output)
    def greet(name):
        return "Hello " + name + "!"
demo.launch()
    