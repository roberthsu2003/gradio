## 版面控制(Controlling Layout)

### 列(Rows)
- with gr.Row()

**顯示2欄**

```python
with gr.Blocks() as demo:
		with gr.Row():
				btn1 = gr.Button("Button 1")
				btn2 = gr.Button("Button 2")
```

```python
with gr.Blocks() as demo:
		with gr.Row(equal_height=True):
			textbox = gr.Textbox()
			btn2 = gr.Button("Button 2")
```

**欄位的寬度**
- scale=0,不會擴充
- scale=1,擴充一點
- scale=2,擴充多一點
- min_width

```python
with gr.Blocks() as demo:
		with gr.Row():
				btn0 = gr.Button("Button 0", scale=0)
				btn1 = gr.Button("Button 1", scale=1)
				btn2 = gr.Button("Button 2", scale=2)
```

**巢狀欄位**

```python
```

