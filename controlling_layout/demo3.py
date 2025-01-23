import gradio as gr

with gr.Blocks() as demo:
    name_box = gr.Textbox(label="Name")
    age_box = gr.Number(label="Age",minimum=0, maximum=100)
    symptoms_box = gr.CheckboxGroup(["Cough", "Fever", "Runny Nose"])
    submit_btn = gr.Button("Submit")

    with gr.Column(visible=False) as output_col:
        diagnosis_box = gr.Textbox(label="Diagnosis")
        patient_summary_box = gr.Textbox(label="Patient Summary")
    
    def submit(name, age, symptoms):
        return {
            submit_btn: gr.Button(visible=False),            
            diagnosis_box: 'covid' if 'Cough' in symptoms else 'flu',
            patient_summary_box: f"{name}, {age} y/o",
            output_col:gr.Column(visible=True)
        }
    
    submit_btn.click(
        submit,
        inputs = [name_box, age_box, symptoms_box],
        outputs = [submit_btn, diagnosis_box, patient_summary_box, output_col]
    )

demo.launch()
