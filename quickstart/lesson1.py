import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)
    

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
    examples = [["徐國堂","2"],["徐瑞彤","1"]],
    title="Greeting and example",
    flagging_options=None
)

demo.launch()
