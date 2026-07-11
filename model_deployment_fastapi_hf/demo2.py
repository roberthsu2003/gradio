# 範例 2：FastAPI (Pydantic 預測 API) + Gradio (預測 UI) + Iris 模型
import os
import sys
import joblib
import uvicorn
from fastapi import FastAPI, HTTPException
import gradio as gr
from pydantic import BaseModel, Field

# 確保相對導入正常
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 1. 載入模型（防呆設計：若無模型則自動重訓）
model_path = os.path.join(current_dir, "iris_model.joblib")
if not os.path.exists(model_path):
    print("未檢測到模型，正在執行 train_save.py 初始化模型...")
    from train_save import train_and_save_model
    train_and_save_model()

model_data = joblib.load(model_path)
model = model_data["model"]
target_names = model_data["target_names"]

# 2. 建立 FastAPI 實例與 Pydantic 資料結構
app = FastAPI(title="Iris 預測服務 API")

class IrisInput(BaseModel):
    sepal_length: float = Field(..., ge=0.1, le=10.0, description="花萼長度")
    sepal_width: float = Field(..., ge=0.1, le=10.0, description="花萼寬度")
    petal_length: float = Field(..., ge=0.1, le=10.0, description="花瓣長度")
    petal_width: float = Field(..., ge=0.1, le=10.0, description="花瓣寬度")

class IrisOutput(BaseModel):
    prediction: str = Field(..., description="預測品種名稱")
    probabilities: dict[str, float] = Field(..., description="各品種預測機率")

# FastAPI 預測端點
@app.post("/predict", response_model=IrisOutput)
def predict_api(payload: IrisInput):
    features = [[payload.sepal_length, payload.sepal_width, payload.petal_length, payload.petal_width]]
    try:
        pred_id = int(model.predict(features)[0])
        pred_label = target_names[pred_id]
        probs = model.predict_proba(features)[0]
        prob_dict = {target_names[i]: float(p) for i, p in enumerate(probs)}
        return IrisOutput(prediction=pred_label, probabilities=prob_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. 建立 Gradio UI
def predict_ui(sepal_len, sepal_wid, petal_len, petal_wid):
    features = [[sepal_len, sepal_wid, petal_len, petal_wid]]
    pred_id = int(model.predict(features)[0])
    pred_label = target_names[pred_id]
    probs = model.predict_proba(features)[0]
    result_text = f"💡 預測品種：{pred_label}\n"
    for i, p in enumerate(probs):
        result_text += f"- {target_names[i]}: {p*100:.1f}%\n"
    return result_text

demo = gr.Interface(
    fn=predict_ui,
    inputs=[
        gr.Slider(0.1, 10.0, value=5.1, label="花萼長度 Sepal Length (cm)"),
        gr.Slider(0.1, 10.0, value=3.5, label="花萼寬度 Sepal Width (cm)"),
        gr.Slider(0.1, 10.0, value=1.4, label="花瓣長度 Petal Length (cm)"),
        gr.Slider(0.1, 10.0, value=0.2, label="花瓣寬度 Petal Width (cm)"),
    ],
    outputs=gr.Textbox(label="預測結果與機率分佈"),
    title="🌸 Iris 鳶尾花即時預測介面"
)

# 4. 融合掛載
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run("demo2:app", host="127.0.0.1", port=8000, reload=True)
