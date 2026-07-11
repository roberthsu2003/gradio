# 3. 僅有輸入型 (Input-Only Layout) 範例
import random
import string
import gradio as gr

def save_image_random_name(image):
    if image is not None:
        # 隨機產生檔名並將上傳的圖片存到本地硬碟
        random_name = ''.join(random.choices(string.ascii_letters, k=10)) + '.png'
        image.save(random_name)
        print(f"成功儲存影像至本地：{random_name}")

# outputs 設為 None 可隱藏右側的輸出面板
demo = gr.Interface(
    fn=save_image_random_name,
    inputs=gr.Image(type='pil', label="請上傳要保存的圖片"), 
    outputs=None,
    title="💾 圖片收集系統 (僅有輸入)",
    description="本介面只接收您的圖片輸入並儲存至伺服器硬碟，不會向介面回傳任何資料。"
)

if __name__ == "__main__":
    demo.launch()