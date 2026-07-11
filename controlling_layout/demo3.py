# 3. 動態可見度 (Visibility) 範例
import gradio as gr

with gr.Blocks() as demo:
    name_box = gr.Textbox(label="病人姓名")
    age_box = gr.Number(label="年齡", minimum=0, maximum=100, value=25)
    symptoms_box = gr.CheckboxGroup(
        ["咳嗽 (Cough)", "發燒 (Fever)", "流鼻水 (Runny Nose)"], 
        label="症狀描述"
    )
    submit_btn = gr.Button("送出診斷結果")

    # 預設隱藏此輸出欄位 (visible=False)
    with gr.Column(visible=False) as output_col:
        diagnosis_box = gr.Textbox(label="診斷結果")
        patient_summary_box = gr.Textbox(label="病人摘要")
    
    def submit(name, age, symptoms):
        diagnosis = '疑似新冠 (COVID-19)' if '咳嗽 (Cough)' in symptoms else '一般流感 (Flu)'
        return {
            submit_btn: gr.Button(visible=False), # 隱藏送出按鈕
            diagnosis_box: diagnosis,
            patient_summary_box: f"患者：{name}，年齡：{age} 歲",
            output_col: gr.Column(visible=True) # 顯示原本隱藏的輸出欄位
        }
    
    submit_btn.click(
        submit,
        inputs=[name_box, age_box, symptoms_box],
        outputs=[submit_btn, diagnosis_box, patient_summary_box, output_col]
    )

if __name__ == "__main__":
    demo.launch()

