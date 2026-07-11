# 8. 連續執行事件 (Running Events Consecutively)
import gradio as gr
import random
import time

with gr.Blocks() as demo:
    # 建立聊天機器人，指定使用 Gradio 5 推薦的 OpenAI 訊息格式 (type="messages")
    chatbot = gr.Chatbot(label="對話視窗", type="messages")
    msg = gr.Textbox(label="請輸入您的訊息（按 Enter 發送）")
    clear = gr.Button("🧹 清空對話記錄")

    def user_action(user_message, history):
        # 先將使用者的對話以字典格式加入歷史紀錄，並回傳空字串以清空文字框
        print("當前歷史對話：", history)
        return "", history + [{"role": "user", "content": user_message}]
    
    def bot_action(history):
        bot_message = random.choice(["你好！有什麼我可以幫忙的？", "這是一個 Blocks 範例。", "很高興為您服務。"])
        time.sleep(1) # 模擬思考時間
        # 將機器人的回答加入歷史紀錄
        return history + [{"role": "assistant", "content": bot_message}]
    
    # 點擊送出或按下 Enter 後：
    # 1. 執行 user_action (清空輸入框，將使用者對話加入歷史紀錄)
    # 2. 緊接著執行 bot_action (模擬機器人思考並回覆)
    msg.submit(fn=user_action, inputs=[msg, chatbot], outputs=[msg, chatbot], queue=False).then(
        fn=bot_action,
        inputs=chatbot,
        outputs=chatbot
    )
    # 點擊清除按鈕時，將 chatbot 清空 (回傳空列表)
    clear.click(lambda: [], None, outputs=chatbot, queue=False)

if __name__ == "__main__":
    demo.launch()