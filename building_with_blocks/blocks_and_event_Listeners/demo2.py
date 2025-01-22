#使用decorator的寫法

import gradio as gr

with gr.Blcoks() as demo:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output box")
    greet_btn = gr.Button("Greet")

    @greet_btn.click(inputs=name, outputs=output)
    def greet(name):
        return "Hello " + name + "!"
demo.launch()
    