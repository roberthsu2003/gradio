# 🚀 機器學習模型部署：免 Dockerfile 的 FastAPI + Gradio 混合服務部署教學

當我們訓練好一個機器學習或深度學習模型後，通常會面臨兩大核心開發需求：

1.  **建立 Web API (例如 FastAPI)**：提供高效、格式與規範定義完整的預測端點，供外部系統（如 App、Web 前端或其他微服務）透過 JSON 格式請求進行「即時推理 (Inference)」。
2.  **建立 網頁 UI 介面 (例如 Gradio)**：提供直觀、美觀的互動式網頁，讓非程式背景的客戶或團隊成員在瀏覽器上操作（如調整滑桿、輸入文字）並立即獲得結果。

以往要同時部署 Web API 與 UI，通常需要編寫複雜的 **Dockerfile** 將兩個服務容器化。**本教學將介紹一個極為巧妙的「免 Dockerfile」方案**：利用 Gradio 底層本就是 FastAPI 的特性，直接將自訂的 FastAPI API 路由掛載至 Gradio App 中，並輕鬆部署至 Hugging Face Spaces。

---

## 🧭 目錄
1. [基本觀念：模型序列化](#-1-基本觀念模型序列化)
2. [技術架構：Gradio 結合 FastAPI 的巧妙之處](#-2-技術架構gradio-結合-fastapi-的巧妙之處)
3. [專案架構與程式碼說明](#-3-專案架構與程式碼說明)
4. [本地測試步驟](#-4-本地測試步驟)
5. [部署至 Hugging Face Spaces 步驟](#-5-部署至-hugging-face-spaces-步驟)

---

## 💾 1. 基本觀念：模型序列化

### 什麼是模型部署 (Model Deployment)？
當您在 Jupyter Notebook 中完成模型訓練後，該模型只暫存於記憶體中。一旦結束執行，模型便會消失。為了提供長期預測服務，我們不能在每次用戶呼叫時都重新訓練，這會造成不可接受的延遲。**模型部署**就是將訓練好的模型持久化儲存，並移至伺服器上持續執行。

### 什麼是序列化 (Serialization)？
- **序列化**：將記憶體中的模型物件，儲存為硬碟中的二進位檔案（例如 `iris_model.joblib`）。
- **反序列化**：當服務啟動時，直接將該二進位檔案還原為記憶體中的模型物件，即可在毫秒內完成單次「即時預測」。
- 本專案採用 **`joblib`**，它非常適合儲存包含大量 NumPy 大型陣列的機器學習模型。

> [!CAUTION]
> **安全性警示**：`joblib` 或 `pickle` 在反序列化時會執行任意程式碼。**千萬不要載入來源不明或未受信任的模型檔案**，否則會使伺服器面臨惡意代碼執行的安全威脅！

---

## 🔌 2. 技術架構：Gradio 結合 FastAPI 的巧妙之處

### 為什麼可以不用寫 Dockerfile？
若要在 Hugging Face Spaces 上使用 **Docker SDK**，您必須編寫 `Dockerfile` 自行設定操作系統、Python 環境、開放埠（Port）等。

但若您選擇 **Gradio SDK**，Hugging Face 會在雲端**自動完成所有 Docker 容器化配置**。您只需提交 Python 程式碼，平台即能自動啟動。

### 融合掛載機制 (Monkey-Patching)
由於 Gradio 本身就是基於 **FastAPI** 框架開發的，它提供了 `gr.mount_gradio_app()` 函數。
本專案採用了更進階的 **Monkey-Patch (猴子補丁)** 技術來攔截並重組 FastAPI 實例：
1. 建立一個標準的 FastAPI App，並宣告 Pydantic Schema 來進行輸入數值校驗與 API 文件宣告。
2. 建立 Gradio UI 介面，規劃「即時模型預測」與「線上超參數重訓」雙分頁。
3. 使用猴子補丁將自訂的 API 路由和 Swagger UI (`/docs`) 直接合併入 Gradio 的底層 Uvicorn 應用中。

---

## 🗂️ 3. 專案架構與程式碼說明

本章節包含以下三個核心檔案：

```text
模型部署/
├── train_save.py      # 訓練並序列化模型
├── app.py             # 結合 FastAPI 與 Gradio 的服務主程式
└── requirements.txt   # 套件依賴清單
```

### 1. 訓練模型：`train_save.py`
使用 Scikit-Learn 訓練一個鳶尾花隨機森林分類器，並使用 `joblib.dump` 將模型與類別標籤、特徵重要性、準確度指標一同打包儲存為 `iris_model.joblib`。

### 2. 服務主程式：`app.py`
該檔案展示了 API 與 UI 的深度整合：
- **自動初始化雙保險**：啟動時檢查是否存在 `iris_model.joblib`，若無，會**自動呼叫 `train_save.py` 進行線上訓練**，保證服務永不因缺少模型檔而啟動失敗。
- **FastAPI API 區塊**：定義 Pydantic 規格（`IrisInput` 與 `IrisOutput`），限制特徵必須在 `0.1` 與 `10.0` 之間。
- **Gradio UI 區塊**：使用 `gr.Slider` 提供特徵輸入，並透過 `gr.HTML` 即時渲染帶有背景色彩的品種卡片與機率長條圖。
- **Monkey-Patch 融合與 ZeroGPU 相容**：動態 mock `spaces` 模組，使得程式既能在本地執行（無 GPU），亦能部署至 Hugging Face ZeroGPU 空間中。

---

## 💻 4. 本地測試步驟

### 1. 安裝套件

建議建立虛擬環境進行安裝：

**使用 `uv` (推薦，速度極快)：**
```bash
uv venv
source .venv/bin/activate  # Windows 請用 .venv\Scripts\activate
uv pip install -r requirements.txt
```

**使用傳統 `pip`：**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. 執行服務
在本地不需要手動跑 `train_save.py`，請直接啟動 `app.py`：

**使用 `uv` 執行 (免啟用虛擬環境)：**
```bash
uv run app.py
```

**啟用虛擬環境下執行：**
```bash
python app.py
```
看見 `INFO: Uvicorn running on http://127.0.0.1:8000` 後，代表服務啟動成功。

### 3. 本地測試方式
*   **測試網頁 UI**：打開瀏覽器，造訪 `http://127.0.0.1:8000/`：
    1.  **🔮 即時模型預測**：滑動特徵滑桿，即時預測品種與機率。
    2.  **⚙️ 線上模型訓練與評估**：設定決策樹數量、測試分割比與隨機種子，點擊「開始訓練模型」即可線上重訓，並即時更新 UI 中的評估指標與特徵重要性長條圖。
*   **測試 FastAPI API (即時預測)**：
    ```bash
    curl -X POST http://127.0.0.1:8000/predict \
      -H "Content-Type: application/json" \
      -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
    ```
*   **測試 FastAPI API (線上重新訓練)**：
    ```bash
    curl -X POST http://127.0.0.1:8000/train \
      -H "Content-Type: application/json" \
      -d '{"n_estimators": 50, "max_depth": 3, "test_size": 0.3, "random_state": 100}'
    ```
*   **測試 Swagger API 文件**：直接存取 `http://127.0.0.1:8000/docs` 即可打開互動式 API 文件。

---

## ☁️ 5. 部署至 Hugging Face Spaces 步驟

### 步驟 A：建立 Space
1. 登入 Hugging Face，點選 **New Space**。
2. 輸入 Space 名稱，並將 **SDK** 選擇為 **Gradio**。
3. 隱私權設定為 **Public**，點選 Create Space。

### 步驟 B：推送專案檔案
將專案目錄下的這三個關鍵檔案推送到 Hugging Face Git 倉庫中：
- `app.py`
- `train_save.py`
- `requirements.txt`

> [!IMPORTANT]
> **Gradio 5/6 新版本部署的「大踩坑點」避坑指南：**
> - **問題背景**：Gradio 5.x 預設啟用了 **伺服器端渲染 (SSR, Server-Side Rendering) 代理**。該代理會攔截並劫持 7860 Port 的流量。當我們掛載 FastAPI 路由後，SSR 代理會阻擋我們自訂的 `/predict`、`/train` 端點與 `/docs`，造成點擊 API 時出現 404 或連線失敗。
> - **解決方案**：在 `app.py` 的 `demo.launch()` 啟動參數中，**必須將 `ssr_mode` 設為 `False`**！
>   ```python
>   demo.launch(
>       server_name="0.0.0.0",
>       server_port=7860,
>       prevent_thread_lock=False,
>       ssr_mode=False # ⚠️ 關閉 SSR 代理以防止自訂 API 路徑被劫持
>   )
>   ```
> - 關閉 SSR 後，Gradio 空間會直接將 7860 流量交由 Python 後端處理，如此一來 API 預測端點與 `/docs` (Swagger API) 便能在雲端完美通車！
