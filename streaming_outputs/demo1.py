# 1. 影像生成串流 (Image Diffusion Streaming) 範例
import gradio as gr
import numpy as np
import time

def fake_diffusion(steps):
    rng = np.random.default_rng()
    for i in range(steps):
        time.sleep(0.5) # 模擬影像渲染時間
        image = rng.random(size=(600, 600, 3))
        yield image # 利用 yield 連續回傳生成中的畫面
        
    # 最終產生的實體影像
    image = np.ones((1000, 1000, 3), np.uint8)
    image[:] = [255, 124, 0] # 純橘色
    yield image

# 建立介面
demo = gr.Interface(
    fn=fake_diffusion,
    inputs=gr.Slider(1, 10, value=3, step=1, label="擴散模擬步數 (Steps)"),
    outputs=gr.Image(label="即時渲染結果"),
    title="🎨 模擬擴散影像生成器 (Streaming)"
)

if __name__ == "__main__":
    demo.launch()