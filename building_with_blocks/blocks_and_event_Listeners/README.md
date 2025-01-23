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

## 事件監聽函式inputs的值是List vs Set(Function Input List vs Dict)
- 如何輸入的組件有2個以上,則監聽函式inputs需要多個
- 如果inputs使用的是list,代表function內的參數必需建立多個(依順序並數量必需和list的元素數量相常)
- 如果inputs使用的是set,代表function內的參數只要一個,因為傳給參數是dict,dict的key值是依據set值的名稱

```python
# Function Input List vs Dict

import gradio as gr

with gr.Blocks() as demo:
    a = gr.Number(label='a')
    b = gr.Number(label='b')
    with gr.Row():
        add_btn = gr.Button('Add')
        sub_btn = gr.Button('Subtract')
    c = gr.Number(label='sum')

    def add(num1, num2):
        return num1 + num2
    add_btn.click(add, inputs=[a, b], outputs=c)

    def sub(data):
        return data[a] - data[b]
    sub_btn.click(sub, inputs={a, b}, outputs=c)

demo.launch()

```

![](./images/pic5.png)

## 事件監聽函式outputs的值是list,代表輸出至多個組件
- function也值需傳出多個值(tuple)

```python
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
```

![](./images/pic6.png)

## 動態更新組件的配置

```pytnon
#Updating Component Configurations

import gradio as gr

def change_textbox(choice):
    if choice == "short":
        return gr.Textbox(lines=2, visible=True)
    elif choice == "long":
        return gr.Textbox(lines=8, visible=True, value="Lorem ipsum dolor sit amet")
    else:
        return gr.Textbox(visible=False)
    
with gr.Blocks() as demo:
    radio = gr.Radio(
        ["short", "long", "hidden"],
        label="What kind of essay would you like to write?"
    )
    text = gr.Textbox(lines=2, interactive=True, show_copy_button=True)
    radio.change(
        fn = change_textbox,
        inputs = radio,
        outputs = text
    )

demo.launch()
```

![](./images/pic7.png)

## 不改變Component的值

```python
#Not Changing a Component's Value

import random
import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        clear_button = gr.Button("Clear")
        skip_button = gr.Button("Skip")
        random_button = gr.Button("Random")
    numbers = [gr.Number(), gr.Number()]

    clear_button.click(lambda: (None, None),outputs=numbers)
    skip_button.click(lambda: [gr.skip(), gr.skip()], outputs=numbers)
    random_button.click(lambda: (random.randint(0,100),random.randint(0,100)), outputs=numbers)

demo.launch()
```

![](./images/pic8.png)

## 連續執行事件
- 執行完事件後,接續執行下一個事件
- 使用then()

```python
#Running Events Consecutively

import gradio as gr
import random
import time

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        print(history)
        return "", history + [[user_message, None]]
    
    def bot(history):
        bot_message = random.choice(["I'm sorry, I don't understand.", "I'm a chatbot.", "I'm here to help you."])
        time.sleep(2)
        history[-1][1] = bot_message
        return history
    
    msg.submit(fn=user, inputs=[msg, chatbot], outputs=[msg, chatbot], queue=False).then(
        fn=bot,
        inputs=chatbot,
        outputs=chatbot
    )
    clear.click(lambda: None, None, outputs=chatbot, queue=False)

demo.launch()
```

![](./images/pic9.png)

## 鍊結多到觸發到一個function

```python
import gradio as gr

with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output Box")
    greet_btn = gr.Button("Greet")
    trigger = gr.Textbox(label="Trigger Box")

    def greet(name, evt_data:gr.EventData):
        return "Hello " + name + "!", evt_data.target.__class__.__name__
    
    def clear_name(evt_data: gr.EventData):
        return ""
    
    gr.on(
        triggers=[name.submit, greet_btn.click],
        fn = greet,
        inputs = name,
        outputs = [output, trigger]
    ).then(clear_name, outputs=[name])

demo.launch()
```

![](./images/pic10.png)


```python
import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        num1 = gr.Slider(1, 10)
        num2 = gr.Slider(1, 10)
        num3 = gr.Slider(1, 10)
    output = gr.Number(label="Sum")

    @gr.on(inputs=[num1, num2, num3], outputs=output)
    def sum(a, b, c):
        return a + b + c

demo.launch()
```

![](./images/pic11.png)













