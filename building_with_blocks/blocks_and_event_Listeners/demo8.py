# Function Return List

import gradio as gr

with gr.Blocks() as demo:
    food_box = gr.Number(value=10, label="Food Count")
    status_box = gr.Textbox()

    def eat(food):
        if food > 0:
            return food-1, "full"
        else:
            return 0, "hungry"
        
    gr.Button("Eat").click(
        fn = eat,
        inputs = food_box,
        outputs = [food_box, status_box]
    )

demo.launch()