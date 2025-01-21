#session state example

import gradio as gr

def store_message(message:str, history:list[str]):
    output = {
        "目前訊息":message,
        "歷史訊息":history[::-1]
    }
    history.append(message)
    return output, history

demo = gr.Interface(
    fn = store_message,
    inputs = ["textbox", gr.State(value=[])],
    outputs = ["json", gr.State()]
)

demo.launch()