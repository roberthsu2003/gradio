# 🚀 機器學習模型部署：FastAPI + Gradio 漸進式融合與子資料夾 Space 部署

當我們將訓練好的機器學習或深度學習模型準備上線時，通常有兩個開發目標：

1.  **建立 Web API (FastAPI)**：提供規格嚴謹的 `/predict` 等 API 端點，方便外部 App、網頁前端或其他微服務發送 JSON 請求來獲取即時預測。
2.  **建立 網頁 UI (Gradio)**：提供精美、直觀的網頁介面，讓非程式背景的團隊成員或客戶能直接用滑桿、上傳按鈕進行操作。

本章節將引導您**由淺入深、循序漸進地**將這兩者無縫結合。最後，我們將說明如何**免寫 Dockerfile**，並以**子資料夾 Git Subtree 部署**的進階方式，將您的專案打包上傳至 Hugging Face Spaces 雲端。

---

## 🧭 目錄
1. [基本觀念：模型序列化](#-1-基本觀念模型序列化)
2. [技術架構：Gradio 與 FastAPI 的融合](#-2-技術架構gradio-與-fastapi-的融合)
3. [漸進式教學小章節](#-3-漸進式教學小章節)
    * [範例 1：最基礎的掛載融合 (`demo1.py`)](#範例-1最基礎的掛載融合-demo1py)
    * [範例 2：模型推理與 Pydantic 驗證 (`demo2.py`)](#範例-2模型推理與-pydantic-驗證-demo2py)
    * [範例 3：完整生產級全生命週期平台 (`app.py`)](#範例-3完整生產級全生命週期平台-apppy)
4. [本地測試步驟](#-4-本地測試步驟)
5. [Hugging Face Spaces 子資料夾 Git Subtree 部署指南](#-5-hugging-face-spaces-子資料夾-git-subtree-部署指南)

---

## 💾 1. 基本觀念：模型序列化

### 什麼是模型部署 (Model Deployment)？
在開發環境（如 Jupyter Notebook）中訓練好的模型僅存在於記憶體中。一旦關閉程式，模型就會消失。**模型部署**就是將模型檔案持久化，並在 Web 伺服器上長期運行。我們不能在每次用戶要預測時都重跑一遍訓練程式，這會造成嚴重的延遲。

### 什麼是序列化 (Serialization)？
- **序列化**：將記憶體中的模型物件，儲存為硬碟中的二進位檔案（例如 `iris_model.joblib`）。
- **反序列化**：Web 伺服器啟動時，直接讀取此二進位檔案，還原成模型物件，即可在毫秒內進行「即時預測 (Inference)」。
- 我們推薦使用 **`joblib`**，因為它對包含大量 NumPy 陣列的機器學習模型有極佳的讀寫效能。

> [!CAUTION]
> **安全性警告**：`joblib` 或 `pickle` 在反序列化時會執行任意程式碼。**千萬不要載入來源不明或未受信任的模型檔案**，否則會使伺服器面臨嚴重的安全威脅！

---

## 🔌 2. 技術架構：Gradio 與 FastAPI 的融合

Gradio 套件底層其實是用 **FastAPI** 框架寫成的。Gradio 提供了 `gr.mount_gradio_app()` 函數，這能讓我們做兩件事：
1.  建立一個標準的 FastAPI App，並在上面撰寫 Pydantic 的資料校驗與 `/predict` API 端點。
2.  建立 Gradio 的網頁介面。
3.  將 Gradio 網頁介面掛載到 FastAPI 的根路徑 `/` 下。

這樣一來，造訪首頁 `/` 時會顯示 Gradio 網頁，而發送請求到 `/predict` 時則是標準的 API 服務！

---

## 🛠️ 3. 漸進式教學小章節

為了讓您能一步步掌握融合技術，我們將專案拆解為以下三個層級的範例：

### 📁 檔案清單
```text
model_deployment_fastapi_hf/
├── train_save.py      # 訓練並序列化模型
├── demo1.py           # 範例 1：最基礎的掛載融合 (Greet 範例)
├── demo2.py           # 範例 2：加入 Iris 模型預測與 Pydantic 驗證
├── app.py             # 範例 3：全功能生產級平台 (重訓、Monkey-Patch、ZeroGPU)
└── requirements.txt   # 套件依賴清單
```

---

### 範例 1：最基礎的掛載融合 (`demo1.py`)
這是一個最精簡的入門範例。我們只建立一個簡單的 `greet` 函數，學習如何使用 `gr.mount_gradio_app` 將 Gradio 介面掛載到 FastAPI App 上，而沒有牽涉複雜的模型與參數。

👉 [開啟 demo1.py 查看原始碼](./demo1.py)

---

### 範例 2：模型推理與 Pydantic 驗證 (`demo2.py`)
在此小節中，我們引入了機器學習推理：
1. 執行 `train_save.py` 訓練隨機森林分類器，並匯出為 `iris_model.joblib`。
2. 在 FastAPI 中使用 **Pydantic** 定義 `IrisInput` 與 `IrisOutput` 的 JSON 格式規格，限制輸入數據必須在限制區間內（防範髒數據導致模型崩潰）。
3. 建立 `/predict` API 路由。
4. 在 Gradio 中拉出 4 個特徵滑桿作為 UI 輸入，呼叫模型推理並輸出預測結果。

👉 [開啟 demo2.py 查看原始碼](./demo2.py)

---

### 範例 3：完整生產級全生命週期平台 (`app.py`)
這是最完整的實戰專案（也是 Hugging Face Spaces 部署的入口程式，因此命名為 `app.py`）。除了範例 2 的預測功能外，還擴充了以下強大機制：
- **線上超參數重訓**：新增 `/train` API 端點與 Gradio 訓練分頁，使用者能在 UI 上調整隨機森林參數並即時重訓，更新後端模型。
- **Gradio 5 猴子補丁 (Monkey-Patch)**：因為 Hugging Face Spaces 的特殊生命週期，本範例使用 Patch 攔截 Gradio App 建立過程，強制融合自訂路由，開通 `/docs` (Swagger UI) 與 `/openapi.json` 文件路徑。
- **自動化雙保險設計**：啟動時若無檢測到模型，會自動執行訓練，確保雲端啟動永不失敗。
- **ZeroGPU 與本地環境 Mock 相容**：動態 Mock 雲端 `spaces` 模組，使其不論在本地（無 GPU）還是雲端（ZeroGPU 掃描）都能正常啟動。

👉 [開啟 app.py 查看原始碼](./app.py)

---

## 💻 4. 本地測試步驟

請在虛擬環境下安裝套件與執行（推薦使用現代套件管理工具 **`uv`**）：

### 1. 安裝套件
```bash
# 建立並啟用環境
uv venv
source .venv/bin/activate  # Windows 請用 .venv\Scripts\activate

# 安裝相依套件
uv pip install -r requirements.txt
```

### 2. 本地執行服務

**執行範例 1：**
```bash
uv run python demo1.py
```
造訪 `http://127.0.0.1:8000/` 查看基礎掛載網頁。

**執行範例 2：**
```bash
uv run python demo2.py
```
除了造訪 `http://127.0.0.1:8000/` 操作 UI，您也可以測試它的 API：
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

**執行完整範例 3 (app.py)：**
```bash
uv run app.py
```
啟動後，除了網頁 UI，您可直接造訪 `http://127.0.0.1:8000/docs` 打開 FastAPI 自動生成的 Swagger UI 互動式 API 文件！

---

## ☁️ 5. Hugging Face Spaces 子資料夾 Git Subtree 部署指南

> [!IMPORTANT]
> **💡 為什麼要用「子資料夾」部署？**
> 在上課或協作專案時，我們的所有程式碼通常都集中在一個大型 GitHub 儲存庫（例如 `machine_learning/`）。
> 然而，Hugging Face Spaces 要求 `app.py` 必須放置在倉庫的**根目錄**下。
> 為了避免特地為 Hugging Face 建立無數個獨立 GitHub 倉庫，我們可以使用 **`git subtree`** 技術，僅將主專案中的子資料夾（如 `model_deployment_fastapi_hf/`）獨立推送到 Hugging Face Spaces 作為其根目錄！

### 步驟 1：建立並設定 Hugging Face 帳戶
1.  **取得 Write Token**：造訪 Hugging Face 右上角頭像 -> **`Settings`** -> **`Access Tokens`** -> **`Create new token`**。名稱自訂，**類型必須選擇 `Write`**，並複製備用。
2.  **建立 Space**：點擊 **`New Space`**。
    *   **Space name**：例如 `iris-fastapi-service` (自訂)
    *   **SDK**：選擇 **`Gradio`** (注意：**千萬不要**選 Docker，因為 Gradio SDK 會自動幫我們搞定容器化配置！)
    *   **Space hardware**：免費版請選擇 **`ZeroGPU`**。
3.  點擊 **`Create Space`**。

---

### 步驟 2：利用 Git Subtree 推送子資料夾 (推薦 🚀)

請在您的**主專案（包含子資料夾的大 GitHub 倉庫）根目錄**下，開啟終端機執行以下步驟：

#### 1. 將遠端的 Space 臨時克隆至主專案「外部」
```bash
# ⚠️ 請在主專案目錄的「外面」執行 clone，例如 clone 到暫存目錄下
git clone https://huggingface.co/spaces/您的用戶名/您的Space名稱
```

#### 2. 複製設定檔回主專案的子資料夾
將剛才克隆下來的資料夾中的 `README.md`（包含頂部帶有 YAML 中繼資料的 `---` 區塊）和 `.gitattributes` 複製並覆蓋到您主專案的 `model_deployment_fastapi_hf/` 子資料夾下。複製完後，即可將外面克隆的暫存資料夾刪除。

#### 3. 提交變更至您的主專案 Git
```bash
git add model_deployment_fastapi_hf/
git commit -m "Add HF config files to subfolder"
```

#### 4. 使用臨時分支將子資料夾強制推送到 HF Spaces
在主專案根目錄下，執行以下三行指令（將 prefix 指向您的子資料夾路徑，並替換用戶名與 Space 名稱）：
```bash
# (1) 將子資料夾單獨分割成一個本地臨時分支 temp-deploy
git subtree split --prefix=model_deployment_fastapi_hf -b temp-deploy

# (2) 將此臨時分支強制推送到 Hugging Face 的 main 分支 (會要求輸入密碼，請填入第一步複製的 Access Token)
git push https://huggingface.co/spaces/您的用戶名/您的Space名稱 temp-deploy:main --force

# (3) 刪除本地臨時分支保持環境乾淨
git branch -D temp-deploy
```

---

> [!IMPORTANT]
> **💥 Gradio 5 版本雲端部署的「重大避坑點」：**
> 在 `app.py` 啟動參數中，**必須指定 `ssr_mode=False`**：
> ```python
> demo.launch(
>     server_name="0.0.0.0",
>     server_port=7860,
>     prevent_thread_lock=False,
>     ssr_mode=False  # ⚠️ 關閉 SSR 代理，防止自訂的 API 與 /docs 路由被劫持
> )
> ```
> 在 Gradio 5 中，預設啟用的 SSR (伺服器端渲染) 會由 Node.js 代理攔截 7860 Port。若不關閉 `ssr_mode`，Gradio SSR 代理會阻斷所有自訂 FastAPI 路由，導致您的 `/predict` 與 `/docs` 拋出 404 錯誤！關閉後，流量將由 Python 後端直接接管，使 UI 與 API 在雲端完美共存！
