## 快速上手

### 安裝

```
pip install --upgrade gradio
```

### Gradio可在jupyter notebook上安裝

### 建立第一個範例


```python
import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)

demo.launch()

```

### 執行檔案

```python
python xxx.py
```

### 開發模式執行檔案(Hot Reload mode)

```python
gradio xxx.py
```

![](./images/pic1.png)

### 程式觀念說明