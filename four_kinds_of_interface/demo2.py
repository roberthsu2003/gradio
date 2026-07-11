# 2. 僅有輸出型 (Output-Only Layout) 範例
import time
import gradio as gr

def fake_gan():
    time.sleep(1) # 模擬生成延遲
    images = [
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&w=387&q=80",
        "https://images.unsplash.com/photo-1554151228-14d9def656e4?ixlib=rb-1.2.1&w=386&q=80",
        "https://images.unsplash.com/photo-1542909168-82c3e7fdca5c?ixlib=rb-1.2.1&w=1000&q=80",
    ]
    return images

# inputs 設為 None 可隱藏左側的輸入面板
demo = gr.Interface(
    fn=fake_gan,
    inputs=None,
    outputs=gr.Gallery(label="產生的臉部影像", columns=3),
    title="👤 隨機人臉產生器 (Fake GAN)",
    description="本展示不需要任何輸入，點擊「Generate」即可隨機獲取臉部影像。"
)

if __name__ == "__main__":
    demo.launch()