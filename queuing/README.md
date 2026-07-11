# ⚙️ 佇列機制 (Queuing)

當有多位使用者同時使用同一個 Gradio 應用程式時，若背後運行的模型推理或資料處理量非常龐大，可能會導致伺服器過載或回應逾時。為了解決此問題，Gradio 內建了高效的**佇列 (Queue) 系統**。

> [!NOTE]
> **佇列的運作原則：**
> Gradio 會在背景為事件建立排隊佇列，遵循 **先進先出 (FIFO, First In First Out)** 的原則。當有大量請求湧入時，使用者會看見自己當前的排隊名次，系統會依序處理，處理完畢後自動將該任務從佇列中移除。

---

## 🛠️ 配置佇列參數

預設情況下，Gradio 會為每個事件監聽器啟用佇列，並限制每次只處理一個任務。您可以透過以下兩個核心參數來調整佇列的並行處理策略：

### 1. `concurrency_limit` (並行限制)
控制此事件監聽器**同一時間最大允許的並行執行任務數**。
- `concurrency_limit=1`（預設值）：一次只處理一個請求，其餘排隊。
- `concurrency_limit=5`：允許最多 5 個任務同時並行運算。
- `concurrency_limit=None`：不設限制，所有進來的任務均會立即並行處理（需注意伺服器負載）。

```python
import gradio as gr

with gr.Blocks() as demo:
    prompt = gr.Textbox(label="請輸入提示詞")
    image = gr.Image(label="生成的圖片")
    generate_btn = gr.Button("🎨 生成圖片")
    
    # 限制該點擊事件最多允許 5 個任務同時生成
    generate_btn.click(image_gen, inputs=prompt, outputs=image, concurrency_limit=5)
```

---

### 2. `concurrency_id` (共用佇列識別碼)
當您的應用中有多個不同的按鈕事件，但它們背後都共用同一個受限資源（例如只有一張顯卡，或只有一個外部 API Key）時，您可以使用 `concurrency_id` 將多個事件監聽器**綁定在同一個共用佇列**中，並限制該佇列整體的總並行數。

```python
import gradio as gr

with gr.Blocks() as demo:
    prompt = gr.Textbox(label="請輸入提示詞")
    image = gr.Image(label="生成的圖片")
    
    generate_btn_1 = gr.Button("🎨 使用模型 A 生成")
    generate_btn_2 = gr.Button("🎨 使用模型 B 生成")
    generate_btn_3 = gr.Button("🎨 使用模型 C 生成")
    
    # 藉由指定相同的 concurrency_id="gpu_queue"
    # 這三個按鈕所觸發的事件將會共用同一個 GPU 資源佇列，且總並行上限為 2
    generate_btn_1.click(image_gen_1, prompt, image, concurrency_limit=2, concurrency_id="gpu_queue")
    generate_btn_2.click(image_gen_2, prompt, image, concurrency_limit=2, concurrency_id="gpu_queue")
    generate_btn_3.click(image_gen_3, prompt, image, concurrency_limit=2, concurrency_id="gpu_queue")
```