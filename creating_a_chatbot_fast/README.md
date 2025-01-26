## 如何建立一個Gradio Chatbot

## 整合olloma

```python
import gradio as gr

gr.load_chat("http://localhost:11434/v1/", model="llama3.2", token="ollama").launch()
```


## 定義一個chat 函式

使用gr.ChatInterface()建立一個chatbot應用程式, 第1件事必需定義自已的chat 函式,在最簡單的範例中,你的chat 函式必需接受2個引數:message和history,可以任何的引數名稱,但要依順序

- message: 型別為str,是使用者填寫的資料
- history: 是一個openai樣式的dictionary,包含role和content的key,儲存先前的對話記錄。

**history的格式如下**

```python
[
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Paris"}
]
```

如果下一個message如下:

```
"And what is its largest city?"
```

這是chat 函式必需要傳出字串

- return 值 - 這個值是依據history和message傳出的回答,如這個案例

```
Paris is also the largest city.
```

**範例,亂數傳出Yes或No

```

```