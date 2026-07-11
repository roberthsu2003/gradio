import gradio as gr

# 定義核心功能函數
def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

# 使用顯式實例化組件來獲得更精緻的 UI 控制與文字描述
demo = gr.Interface(
    fn=greet,
    inputs=[
        gr.Textbox(
            label="請輸入您的姓名", 
            placeholder="例如：徐國堂", 
            info="這將作為問候對象"
        ),
        gr.Slider(
            minimum=1, 
            maximum=10, 
            step=1, 
            value=2, 
            label="驚嘆號強度", 
            info="控制問候語結尾驚嘆號的個數"
        )
    ],
    outputs=[
        gr.Textbox(label="問候結果")
    ],
    examples=[
        ["徐國堂", 2], 
        ["徐瑞彤", 1]
    ],
    title="🌟 互動問候產生器",
    description="輸入名字並調整滑桿，系統將根據設定生成帶有不同強度的問候語。",
    flagging_options=None # 關閉資料標記功能
)

if __name__ == "__main__":
    demo.launch()

