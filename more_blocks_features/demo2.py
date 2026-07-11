import gradio as gr
import random
import time

with gr.Blocks() as demo:
    timer = gr.Timer(1)
    timestamp = gr.Number(label="⏱️ 當前系統時間戳記")
    timer.tick(lambda: round(time.time()),outputs=timestamp)

    number = gr.Number(lambda: random.randint(1, 10), every=timer, label="🎲 每秒隨機數 (1-10)")

    with gr.Row():
        gr.Button("▶️ 啟動定時器").click(lambda:gr.Timer(active=True),None,timer)
        gr.Button("⏸️ 停止定時器").click(lambda: gr.Timer(active=False), None, timer)
        gr.Button("⚡ 加速定時器 (0.2s)").click(lambda:0.2, None, timer)

demo.launch()