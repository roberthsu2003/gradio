import gradio as gr
import random

def random_message(message, history):
    return random.choice(['是的 (Yes)', '不對 (No)'])

gr.ChatInterface(
    fn = random_message,
    type = "messages"
).launch()