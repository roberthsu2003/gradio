import random
import string
import gradio as gr

def save_image_random_name(image):
    random_name = ''.join(random.choices(string.ascii_letters, k=10)) + '.png'
    image.save(random_name)
    print(f"儲存:{random_name}影像")

demo = gr.Interface(
    fn = save_image_random_name,
    inputs = gr.Image(type='pil'), 
    outputs = None)

demo.launch()