import gradio as gr

def select_cell(evt: gr.SelectData):
    return f"Selected cell at row: {evt.index[0]}, column: {evt.index[1]}"

with gr.Blocks() as demo:
    turn = gr.Textbox("X", interactive=False, label="Turn")
    board = gr.Dataframe(value=[["","",""]]*3, interactive=False, type="array")
    selected_cell_output = gr.Textbox(label="Selected Cell")

    board.select(select_cell, None, selected_cell_output)

demo.launch()
