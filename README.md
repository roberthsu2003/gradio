# Gradio UI 介面開發指南 🚀

本專案是用於學習與開發 Gradio 應用程式的完整指南，包含實用的範例程式碼與核心概念說明，非常適合機器學習、深度學習及自然語言處理（NLP）領域的工程師快速建立展示原型。

> [!NOTE]
> **Gradio** 是由 Hugging Face 團隊維護的開源工具，能讓您在幾行 Python 程式碼內，快速為機器學習模型構建美觀且互動性強的 Web 介面。

---

## 🧭 學習導覽

### 🏁 快速入門
*   **[安裝與建立第一個範例](./quickstart)**：快速配置 Gradio 開發環境，並啟動您的首個應用程式。
*   **[Gradio Playground 線上編輯器](https://www.gradio.app/playground)**：
    *   在瀏覽器中直接撰寫與測試 Gradio 應用。
    *   透過左側邊欄快速檢索各類常用組件與程式碼範例。

---

## 📦 Interface 類別
`gr.Interface` 是 Gradio 最核心且最易於使用的 API，專為「輸入 ➡️ 輸出」模式的模型展示而設計。

1.  **[Gradio 基本組件說明官方文件](https://www.gradio.app/docs/gradio/interface)**
2.  **[保存使用者狀態](./interface_state)**：了解如何區分**全域狀態**（所有使用者共享）與 **Session 狀態**（個別使用者獨立保存）。
3.  **[即時與串流回應介面](./reactive_Interface)**：
    *   **即時回應 (Live Interface)**：數值改變時即時更新。
    *   **串流回應 (Stream Interface)**：持續、分段輸出結果。
4.  **[四種版面配置型態](./four_kinds_of_interface)**：認識「輸入-輸出」、「僅輸出」、「僅輸入」以及「同介面輸入輸出」的版面設計。

---

## 🛠️ Blocks 類別
當您需要比 `gr.Interface` 更彈性、更複雜的 UI 配置（例如自訂排版、多重事件監聽）時，應使用 `gr.Blocks`。

1.  **[Blocks 基礎與事件監聽](./building_with_blocks/blocks_and_event_Listeners)**：掌握 `with gr.Blocks()` 的基本結構與事件綁定。
2.  **[版面控制 (Controlling Layout)](./controlling_layout)**：學習如何使用 `gr.Row`、`gr.Column` 與 `gr.Tab` 規劃精緻的 UI。
3.  **[保存 Blocks 內的狀態](./state_in_block)**：在 Blocks 架構下使用 `gr.State` 儲存會話資訊。
4.  **[動態組件渲染 (gr.render)](./dynamic_number_of_components)**：使用 `@gr.render` 裝飾器根據使用者輸入動態增刪 UI 組件。
5.  **[更多 Blocks 進階功能](./more_blocks_features)**：如定時器 (`gr.Timer`)、收集事件資料 (`gr.SelectData`) 等。

---

## 🚀 進階與實戰

### ⚙️ 系統效能
*   **[佇列機制 (Queuing)](./queuing)**：深入了解 Gradio 的背景事件佇列，掌握並行限制與效能優化。
*   **[串流輸出 (Streaming Outputs)](./streaming_outputs)**：使用 Generator 與 `yield` 實現字詞或圖像的即時串流渲染。

### 💬 聊天機器人 (Chatbots)
*   **[快速構建 Chatbot 應用](./creating_a_chatbot_fast)**：結合 `gr.ChatInterface` 與本地/線上大語言模型（如 Ollama）快速搭建對話介面。

### 🔌 模型部署與 API 整合
*   **[FastAPI 整合與 HF Spaces 部署](./model_deployment_fastapi_hf)**：利用猴子補丁與掛載技術，在同一個 Hugging Face Space 中同時提供 Web API 端點與 Gradio UI，無須撰寫 Dockerfile。
