# 2. 分頁與摺疊面板 (Tabs and Accordions) 範例
import numpy as np
import gradio as gr

def flip_text(x):
    return x[::-1] if x else ""

def flip_image(x):
    return np.fliplr(x) if x is not None else None

with gr.Blocks() as demo:
    gr.Markdown("## 🔄 文本與影像反轉處理工具")
    
    # 分頁 A：文本反轉
    with gr.Tab("📝 文本反轉"):
        text_input = gr.Textbox(label="輸入文字")
        text_output = gr.Textbox(label="反轉結果")
        text_button = gr.Button("執行文字反轉")
    
    # 分頁 B：影像反轉
    with gr.Tab("🖼️ 影像反轉"):
        with gr.Row():
            image_input = gr.Image(label="上傳圖片")
            image_output = gr.Image(label="水平翻轉後圖片")
        image_button = gr.Button("執行影像反轉")

    # 摺疊面板：進階控制參數，預設收合 (open=False)
    with gr.Accordion("⚙️ 進階控制參數", open=False):
        gr.Markdown("此處可微調進階演算法選項：")
        temp_slider = gr.Slider(
            minimum=0, 
            maximum=1, 
            value=0.1,
            step=0.1,
            interactive=True,
            label="強度閥值 (Threshold)"
        )

    text_button.click(flip_text, inputs=text_input, outputs=text_output)
    image_button.click(flip_image, inputs=image_input, outputs=image_output)

if __name__ == "__main__":
    demo.launch()