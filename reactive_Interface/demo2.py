# 串流影像處理介面 (Streaming Interface) 範例
import gradio as gr
import numpy as np

def flip(im):
    # 接收 Webcam 影像資料塊 (Data Frame) 並對其進行上下反轉
    return np.flipud(im) if im is not None else None

demo = gr.Interface(
    fn=flip,
    # sources=["webcam"] 為 Webcam 視訊輸入，streaming=True 啟用連續幀串流傳輸
    inputs=gr.Image(sources=["webcam"], streaming=True),
    outputs=gr.Image(label="即時反轉影像"),
    live=True
)

if __name__ == "__main__":
    demo.launch()