## Blocks類別和事件監聽者

**Blocks的使用結構**

```python
import gradio as gr

def greet(name):
    return "Hello " + name + "!"

with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output")
    greet_btn = gr.Button("Greet")
    greet_btn.click(fn=greet,inputs=name,outputs=output,api_name="greet")

demo.launch()
```

![](./images/pic1.png)



