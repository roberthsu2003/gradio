import gradio as gr
import random

def random_message(message, history):
    return random.choice(['Yes','No'])

gr.ChatInterface(
    fn = random_message,
    type = "messages"
).launch()