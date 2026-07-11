# 即時回應介面 (Live Interface) 範例
import gradio as gr

def calculator(num1, operation, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        return (num1 / num2) if num2 != 0 else "無法除以零"

demo = gr.Interface(
    fn=calculator,
    inputs=[
        gr.Number(label="輸入數值 1", value=0),
        gr.Radio(["add", "subtract", "multiply", "divide"], label="選擇運算方法"),
        gr.Number(label="輸入數值 2", value=0)
    ],
    outputs=gr.Number(label="運算結果"),
    live=True # 啟用即時運算，數值改變時會立即呼叫 calculator 函數
)

if __name__ == "__main__":
    demo.launch()
