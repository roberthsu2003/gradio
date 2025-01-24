import gradio as gr

with gr.Blocks() as demo:
    text_count = gr.State(1)
    add_btn = gr.Button("Add Box")
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
            box = gr.Textbox(key=i, label=f"Box {i}")
            boxes.append(box)

        def merge(*args):
            return " ".join(args)
        
        merge_btn.click(merge, boxes, output)
    
    merge_btn = gr.Button("Merge")
    output = gr.Textbox(label="Merged Output")

demo.launch()
