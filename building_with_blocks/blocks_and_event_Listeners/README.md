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

**事件監聽者,Textbox和使用者的互動**
- click
- inputs內的Textbox,預設可以和使用者互動
- outpus內的Textbox,預設不可以和使用者互動
- 自訂互動-`output = gr.Textbox(label="Output", interactive=True)`







