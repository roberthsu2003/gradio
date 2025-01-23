import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        text1 = gr.Textbox(label="Text 1")
        slider2 = gr.Textbox(label="Slider 2")
        drop3 = gr.Dropdown(label="Drop 3", choices=["a", "b", "c"])
    
    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            text1 = gr.Textbox(label="prompt 1")
            text2 = gr.Textbox(label="prompt 2")
            inbtw = gr.Button("Between")
            text4 = gr.Textbox(label="prompt 1")
            text5 = gr.Textbox(label="prompt 2") 
        
        with gr.Column(scale=2, min_width=300):
            img1 = gr.Image("cheetah.jpg")
            btn = gr.Button("Go")

demo.launch()