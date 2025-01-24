#Dynamic Apps with the Render Decorator

import gradio as gr

with gr.Blocks() as demo:
    input_text = gr.Textbox(label='input')

    @gr.render(inputs=input_text)
    def show_split(text):
        if len(text) == 0:
            gr.Markdown("## No Input Provided")
        else:
            for letter in text:
                gr.Textbox(letter)

demo.launch()
