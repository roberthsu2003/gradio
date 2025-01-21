import numpy as np
import gradio as gr

def sepia(input_img):
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()                          
    return sepia_img

demo = gr.Interface(
    fn=sepia, 
    inputs="image", 
    outputs="image")

demo.launch()