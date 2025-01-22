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

**使用decorator語法**

```python
#使用decorator的寫法

import gradio as gr

with gr.Blcoks() as demo:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output box")
    greet_btn = gr.Button("Greet")

    @greet_btn.click(inputs=name, outputs=output)
    def greet(name):
        return "Hello " + name + "!"
demo.launch()
    
```


![](./images/pic1.png)



**事件監聽者,Textbox和使用者的互動**
- click
- inputs內的Textbox,預設可以和使用者互動
- outpus內的Textbox,預設不可以和使用者互動
- 自訂互動-`output = gr.Textbox(label="Output", interactive=True)`

## 事件監聽者的狀態

```python
#Types of Event Listeners

import gradio as gr
def welcome(name):
    return f"Welcome to Gradio,{name}"

with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Hello World!
        Start typing below to see the output
        """
    )
    inp = gr.Textbox(placeholder="What is your name?")
    out = gr.Textbox()
    inp.change(welcome, inp, out)

demo.launch()
```

![](./images/pic2.png)

不同的組件支援不同的事件,Textbox支援change

> 官方組件支援的[事件](https://www.gradio.app/docs/gradio/button#event-listeners)

## 多個程式流程

**範例1**

```python
#Multiple Data Flows
import gradio as gr

def increase(num):
    return num + 1

with gr.Blocks() as demo:
    a = gr.Number(label="a")
    b = gr.Number(label="b")
    atob = gr.Button("a > b")
    btoa = gr.Button("b > a")
    atob.click(increase, a, b)
    btoa.click(increase, b, a)

demo.launch()
```

![](./images/pic3.png)

**範例2**

```python
from transformers import pipeline
import gradio as gr
import requests

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    #return_all_scores=True
)

def speech_to_text(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()['text'] 

def text_to_sentiment(text):
    print(text)
    sentiments = distilled_student_sentiment_classifier(text)
    return f"情緒:{sentiments[0]['label']}, 分數:{sentiments[0]['score']}"

demo = gr.Blocks()

with demo:
    audio_file = gr.Audio(type="filepath")
    text = gr.Textbox()
    label = gr.Label()

    b1 = gr.Button("Recognize Speech")
    b2 = gr.Button("Classify Sentiment")

    b1.click(speech_to_text, inputs=audio_file, outputs=text)
    b2.click(text_to_sentiment, inputs=text, outputs=label)

demo.launch()
```

![](./images/pic4.png)






