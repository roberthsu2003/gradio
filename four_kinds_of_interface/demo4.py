# 4. 輸入輸出共用同個介面 (Shared Layout) 範例
from huggingface_hub import InferenceClient
import gradio as gr

# 請將下方 "your_huggingface_api_token_here" 替換為您自己的 Hugging Face Token 
# 可在 https://huggingface.co/settings/tokens 取得
client = InferenceClient(api_key="your_huggingface_api_token_here")

def generate_text(text_prompt):
    if not text_prompt.strip():
        return "請輸入一些文字提示詞..."
        
    messages = [
        {
            "role": "user",
            "content": text_prompt
        }
    ]

    try:
        completion = client.chat.completions.create(
            model="mistralai/Mistral-Nemo-Instruct-2407", 
            messages=messages, 
            max_tokens=500,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"連線錯誤或未配置 API Key。請確認您的 Hugging Face Token 是否正確。\n錯誤詳情：{e}"
    
# 建立一個 Textbox 實例，使其行數較多，適合寫作
textbox = gr.Textbox(
    label="文本編輯與自動生成面板 (輸入提示詞並在此處獲得回覆)", 
    placeholder="在此輸入您的故事大綱或提示詞...",
    lines=8
)

# 透過將 textbox 同時指定給 inputs 與 outputs，實現共用介面版面
demo = gr.Interface(
    fn=generate_text,
    inputs=textbox,
    outputs=textbox,
    title="📝 智能文字共用編輯器 (Shared Input-Output)"
)
    
if __name__ == "__main__":
    demo.launch()
