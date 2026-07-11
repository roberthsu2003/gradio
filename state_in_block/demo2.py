# 2. 瀏覽器本地狀態 (Local Storage State) 範例
import random
import string
import gradio as gr
import time

with gr.Blocks() as demo:
    gr.Markdown("### 🔒 本地帳密儲存器\n您的帳號和密碼將會自動儲存於瀏覽器的本地儲存空間 (Local Storage)。重新整理頁面後，欄位內容依然會被保留。")
    
    username = gr.Textbox(label="帳號名稱")
    password = gr.Textbox(label="密碼密鑰", type="password")
    btn = gr.Button("🎲 隨機產生帳密")
    
    # 建立 BrowserState，用來持久化儲存帳號與密碼 (格式為 [帳號, 密碼])
    local_storage = gr.BrowserState(["", ""])
    saved_message = gr.Markdown("✅ 已儲存至本地瀏覽器", visible=False)

    # 1. 隨機產生測試帳密
    @btn.click(outputs=[username, password])
    def generate_randomly():
        u = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        p = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        return u, p
    
    # 2. 當頁面載入 (demo.load) 時，自動從 local storage 讀取舊資料並填入
    @demo.load(inputs=[local_storage], outputs=[username, password])
    def load_from_local_storage(saved_values):
        print("正在從瀏覽器 Local Storage 載入：", saved_values)
        return saved_values[0], saved_values[1]
    
    # 3. 當帳號或密碼欄位值改變時，自動更新並保存至 local storage
    @gr.on([username.change, password.change],
            inputs=[username, password],
            outputs=[local_storage])
    def save_to_local_storage(u, p):
        return [u, p]
    
    # 4. 當儲存狀態改變時，顯示帶有時間戳記的保存提示訊息
    @gr.on(local_storage.change, outputs=[saved_message])
    def show_saved_message():
        timestamp = time.strftime("%H:%M:%S")
        return gr.Markdown(
            f"✅ 已於 {timestamp} 成功自動保存至本地儲存區",
            visible=True
        )

if __name__ == "__main__":
    demo.launch()