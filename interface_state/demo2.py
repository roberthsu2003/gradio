# 會話狀態 (Session State) 範例
import gradio as gr

# 核心邏輯函數，第二個參數接收狀態
def store_message(message: str, history: list[str]):
    output = {
        "您剛輸入的訊息": message,
        "歷史訊息紀錄 (新到舊)": history[::-1]
    }
    history.append(message)
    # 同時回傳 UI 顯示內容與更新後的歷史紀錄狀態
    return output, history

# 建立會話狀態介面
demo = gr.Interface(
    fn=store_message,
    # 透過 gr.State 指定狀態的初值為空清單 []
    inputs=[
        gr.Textbox(label="請輸入您的訊息", placeholder="請在此鍵入文字並送出..."), 
        gr.State(value=[])
    ],
    # 輸出中對應包含要更新的狀態元件 gr.State()
    outputs=[
        gr.JSON(label="訊息紀錄面板"), 
        gr.State()
    ],
    title="💬 個人歷史訊息記錄器",
    description="本系統展示會話狀態的運作。您在此輸入的訊息只會暫存在您目前的瀏覽器分頁中，其他連線的使用者不會看到您的資料。",
)

if __name__ == "__main__":
    demo.launch()