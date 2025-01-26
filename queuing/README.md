## 佇例Queuing
- 佇列內可以依順序放置事件任務,並可以依序執行工作.
- 先進先處理,直到處理完畢,完畢後,從佇列移除任務

每一個Gradio App都有佇列系統,佇列可擴展到數千人同時使用。因為每個app都存在許多事件監聽器可能涉及大量的處理工作,因此Gradio會自動在應用程式背景為每一個事件監聽器建立一個佇列以便於處理事件監聽器的事件任務

### 設定Queue
預設的情況下,每一個事件監聽器會有一個專用的queue,一次處理一個事件任務。如果要修改這個設定可以透過2個引數來修改。

- concurrency_limit:可以設定一次可以同時處理事件任務的數量,預設為1,也可以透過Blocks.queue()的方式更改預設值,如果不要有限制可以設成None,就是沒有限制同時執行多少個數量的事件需求。

```
import gradio as gr

with gr.Blocks() as demo:
	prompt = gr.Textbox()
	image = gr.Image()
	generate_btn = gr.Button("Generate Image")
	
	generate_btn.click(image_gen, prompt, image, concurrency_limit=5)
```

上面的程式碼,這個click事件監聽器最多一次可以同時處理5個以上的事件需求任務,如果有超過的事件需求任務必需排隊等到其它完成後有才會再處理。

- concurrency_id:這個設定允許多個事件監聽器共同使用同一個queue

```
import gradio as gr
with gr.Blocks() as demo:
	prompt = gr.Textbox()
	image = gr.Image()
	generate_btn_1 = gr.Button("Generate Image via model 1")
	generate_btn_2 = gr.Button("Generate Image via model 2")
	generate_btn_3 = gr.Button("Generate Image via model 3")
	generate_btn_1.click(image_gen_1, prompt, image, concurrency_limit=2, concurrency_id="gpu_queue")
	
	generate_btn_2.click(image_gen_1, prompt, image, concurrency_limit=2, concurrency_id="gpu_queue")
	
	generate_btn_3.click(image_gen_1, prompt, image, concurrency_limit=2, concurrency_id="gpu_queue")
```