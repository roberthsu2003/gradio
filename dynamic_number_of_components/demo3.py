import gradio as gr

with gr.Blocks() as demo:
    text_count = gr.State(1)
    add_btn = gr.Button("➕ 新增文字框")
    add_btn.click(
        fn = lambda x: x+1,
        inputs = text_count,
        outputs = text_count
    )

    @gr.render(inputs=text_count)
    def render_count(count):
        print(count)
        boxes = []
        for i in range(count):
            box = gr.Textbox(key=i, label=f"輸入框 {i}")
            boxes.append(box)

        def merge(*args):
            return " ".join(args)
        
        merge_btn.click(merge, boxes, output)
    
    merge_btn = gr.Button("🔗 合併文字")
    output = gr.Textbox(label="合併後的輸出結果")

demo.launch()
