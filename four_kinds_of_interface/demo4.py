from huggingface_hub import InferenceClient
import gradio as gr


client = InferenceClient(api_key="xxxxxxxxxxxxxxxxxxxxxxxx")

def generate_text(text_prompt):
    messages = [
        {
            "role": "user",
            "content": text_prompt
        }
    ]

    completion = client.chat.completions.create(
        model="mistralai/Mistral-Nemo-Instruct-2407", 
        messages=messages, 
        max_tokens=500,
    )

    return completion.choices[0].message
    
textbox = gr.Textbox()

demo = gr.Interface(
    fn = generate_text,
    inputs = textbox,
    outputs = textbox)
    
demo.launch()
