#Running Events Consecutively

import gradio as gr
import random
import time

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        print(history)
        return "", history + [[user_message, None]]
    
    def bot(history):
        bot_message = random.choice(["I'm sorry, I don't understand.", "I'm a chatbot.", "I'm here to help you."])
        time.sleep(2)
        history[-1][1] = bot_message
        return history
    
    msg.submit(fn=user, inputs=[msg, chatbot], outputs=[msg, chatbot], queue=False).then(
        fn=bot,
        inputs=chatbot,
        outputs=chatbot
    )
    clear.click(lambda: None, None, outputs=chatbot, queue=False)

demo.launch()