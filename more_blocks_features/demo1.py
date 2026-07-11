import gradio as gr

def calculator(num1, operation, num2):
    if operation == "加法 (add)":
        return num1 + num2
    elif operation == "減法 (subtract)":
        return num1 - num2
    elif operation == "乘法 (multiply)":
        return num1 * num2
    elif operation == "除法 (divide)":
        return num1 / num2

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            num_1 = gr.Number(value=4)
            operation = gr.Radio(["加法 (add)", "減法 (subtract)", "乘法 (multiply)", "除法 (divide)"])
            num_2 = gr.Number(value=0)
            submit_btn = gr.Button(value="⚡ 進行計算")
        with gr.Column():
            result = gr.Number()
    
    submit_btn.click(
        calculator, inputs=[num_1, operation, num_2], outputs=[result], api_name=False
    )
    examples = gr.Examples(
        examples = [
            [5, "加法 (add)", 3],
            [4, "除法 (divide)", 2],
            [-4, "乘法 (multiply)", 2.5],
            [0, "減法 (subtract)", 1.2]
        ],
        inputs=[num_1, operation, num_2]
    )

demo.launch(show_api=False)