# 1. 標準版型 (Standard Layout) 範例
import numpy as np
import gradio as gr

def sepia(input_img):
    if input_img is None:
        return None
    # 套用復古濾鏡效果 (Sepia Filter)
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()                          
    return sepia_img

# 建立具有明顯輸入與輸出對比的標準介面
demo = gr.Interface(
    fn=sepia, 
    inputs=gr.Image(label="原始影像"), 
    outputs=gr.Image(label="復古濾鏡效果"),
    title="📸 復古濾鏡產生器 (標準版型)"
)

if __name__ == "__main__":
    demo.launch()