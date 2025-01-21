# stream Interface

import gradio as gr
import numpy as np

def flip(im):
    return np.flipud(im)

demo = gr.Interface(
    fn = flip,
    inputs = gr.Image(source=["webcam"],streaming=True),
    outputs = "image",
    live = True
)

demo.launch()