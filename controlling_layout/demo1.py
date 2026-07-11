# 1. 巢狀排版 (Nested Row/Column) 範例
import os
import gradio as gr

with gr.Blocks() as demo:
    # 第一列：水平排列的三個常用組件
    with gr.Row():
        text_input = gr.Textbox(label="文字輸入區")
        slider_input = gr.Slider(0, 100, label="數值滑桿")
        dropdown_input = gr.Dropdown(label="下拉選擇選單", choices=["選項 A", "選項 B", "選項 C"])
    
    # 第二列：左右分割欄位 (左 1 : 右 2)
    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            prompt_1 = gr.Textbox(label="正向提示詞 (Prompt 1)")
            prompt_2 = gr.Textbox(label="負向提示詞 (Prompt 2)")
            inbtw = gr.Button("中間插值按鈕")
            prompt_3 = gr.Textbox(label="插值參數 1")
            prompt_4 = gr.Textbox(label="插值參數 2") 
        
        with gr.Column(scale=2, min_width=300):
            # 載入專案底下的 cheetah.jpg（若有此檔案）
            img_path = "cheetah.jpg" if os.path.exists("cheetah.jpg") else None
            img_display = gr.Image(img_path, label="獵豹影像展示")
            action_btn = gr.Button("🚀 開始執行 (Go)")

if __name__ == "__main__":
    demo.launch()