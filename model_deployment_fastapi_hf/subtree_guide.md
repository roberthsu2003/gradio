# Git Subtree 子資料夾部署說明

這份文件用最實務的方式，說明什麼是 Git subtree，以及為什麼它很適合把大型專案中的某個子資料夾，獨立推送到 Hugging Face Spaces 之類的外部 Git 倉庫。

## 什麼是 subtree

Git subtree 的核心想法是：

1. 主專案仍然維持原本的結構。
2. 某個子資料夾可以被「切出來」當成另一個倉庫的內容。
3. 之後你可以只把這個子資料夾的變更推送到外部專案，例如 Hugging Face Spaces。

對這個教學來說，`model_deployment_fastapi_hf/` 就是要被切出去的子資料夾。外部的 Hugging Face Space 只需要看到這個資料夾裡的檔案，不需要知道整個大倉庫的其他內容。

## 為什麼要用 subtree

如果不用 subtree，常見做法有兩種：

1. 另外建立一個獨立倉庫，只放 Space 需要的檔案。
2. 手動複製檔案到另一個專案，再分別維護。

這兩種方式都容易造成重複維護。subtree 的好處是：

1. 主專案只維護一份原始碼。
2. 子資料夾可以獨立部署。
3. 需要更新 Space 時，只要重新 split 再 push 即可。

## 這個章節的部署目標

本章要做的是：把主專案中的 `model_deployment_fastapi_hf/` 子資料夾，推送成 Hugging Face Space 的根目錄。

這代表 Space 上看到的結構會像這樣：

```text
README.md
.gitattributes
app.py
demo1.py
demo2.py
requirements.txt
train_save.py
```

但在你的主專案裡，這些檔案仍然只是 `model_deployment_fastapi_hf/` 底下的一部分。

## 實際流程

### 1. 先準備 Space

先在 Hugging Face 建立一個 Space，並準備好 Write Token。這一步的目的，是讓之後的 `git push` 可以直接寫入遠端 Space。

### 2. 把 Space 設定檔放回子資料夾

從 Space clone 下來後，通常會看到它自己的 `README.md` 和 `.gitattributes`。

你要把這兩個檔案放回主專案的 `model_deployment_fastapi_hf/` 子資料夾，因為：

1. `README.md` 需要包含 Hugging Face Space 的前置 YAML 設定。
2. `.gitattributes` 可以幫助 Hugging Face 正確辨識檔案行為。

### 3. 先提交主專案變更

這樣做的好處是，主專案會留下完整歷史，之後如果要回頭追查 Space 的內容是怎麼來的，也會比較清楚。

### 4. 用 subtree split 切出子資料夾

`git subtree split` 會把指定子資料夾的歷史獨立整理成一條新分支。

對應到本章，就是把 `model_deployment_fastapi_hf/` 切成可推送的內容。

### 5. 把臨時分支推到 Space

最後把剛剛切出來的臨時分支推送到 Hugging Face Space 的 `main` 分支，Space 就會把這個子資料夾當成自己的根目錄。

## 範例指令

以下是一組完整流程範例，假設：

1. 主專案在本機。
2. 子資料夾名稱是 `model_deployment_fastapi_hf/`。
3. Hugging Face Space 名稱是 `your-name/iris-fastapi-service`。

```bash
# 1. 在主專案外部 clone Space
git clone https://huggingface.co/spaces/your-name/iris-fastapi-service

# 2. 把 Space 的 README.md 和 .gitattributes 複製回主專案子資料夾

# 3. 在主專案提交變更
git add model_deployment_fastapi_hf/
git commit -m "Add HF config files to subfolder"

# 4. 切出子資料夾內容成臨時分支
git subtree split --prefix=model_deployment_fastapi_hf -b temp-deploy

# 5. 推送到 Hugging Face Space
git push https://huggingface.co/spaces/your-name/iris-fastapi-service temp-deploy:main --force

# 6. 刪除臨時分支
git branch -D temp-deploy
```

## 你可以把它想成什麼

如果把主專案比喻成一棟大樓，那 subtree 就像是：

1. 先把其中一個樓層整理成獨立可運作的單位。
2. 對外出租或交付時，只交付這一層。
3. 內部維護時，仍然回到整棟大樓的原始結構管理。

這就是它比「手動複製資料夾」更穩定的原因。

## 常見錯誤

### prefix 寫錯

如果 `git subtree split` 的 `--prefix` 寫錯，切出來的內容會不是你要的子資料夾。

### 在主專案內部 clone Space

Space 的暫存 clone 最好放在主專案外面，避免把外部倉庫誤放進主專案歷史裡。

### 忘記推送 README 與 .gitattributes

如果 Space 上看不到正確設定，通常是因為子資料夾裡缺少 Hugging Face 需要的設定檔。

### 忘記關閉 ssr_mode

如果你的 App 需要同時提供 UI 與 API，記得在 `app.py` 中使用 `ssr_mode=False`，否則有可能影響自訂路由。

## 建議的使用方式

當你之後更新了 `model_deployment_fastapi_hf/`，可以重複以下做法：

1. 更新主專案內容。
2. 提交主專案變更。
3. 再做一次 subtree split。
4. 強制推送到 Space。

這樣可以維持主專案與 Space 內容一致。