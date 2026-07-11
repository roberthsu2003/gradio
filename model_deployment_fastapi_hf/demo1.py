# 範例 1：最基礎的 FastAPI 與 Gradio 融合掛載
import os
import sys
import uvicorn
from fastapi import FastAPI
import gradio as gr

# 1. 建立 FastAPI 實例
app = FastAPI(title="基礎融合服務")

# 2. 定義簡單的業務函數與 Gradio UI
def greet(name):
    return f"哈囉，{name}！這是由 FastAPI 後端與 Gradio 前端融合的服務。"

demo = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(label="您的名字", placeholder="請輸入名字..."),
    outputs=gr.Textbox(label="回傳訊息"),
    title="🚀 基礎 FastAPI + Gradio 掛載示範"
)

# 3. 將 Gradio 掛載到 FastAPI 的根路徑 "/"
# 注意：這會將 Gradio 網頁作為首頁展示，其他 FastAPI 自訂 API 可以掛在別的路由下
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    print("服務啟動中，請造訪 http://127.0.0.1:8000/")
    uvicorn.run("demo1:app", host="127.0.0.1", port=8000, reload=True)
