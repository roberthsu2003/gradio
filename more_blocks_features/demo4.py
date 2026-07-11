import gradio as gr

def select_cell(evt: gr.SelectData):
    return f"您點擊了第 {evt.index[0] + 1} 列、第 {evt.index[1] + 1} 行的儲存格 (索引座標: {evt.index})"

with gr.Blocks() as demo:
    turn = gr.Textbox("X", interactive=False, label="👤 當前玩家回合")
    board = gr.Dataframe(value=[["","",""]]*3, interactive=False, type="array")
    selected_cell_output = gr.Textbox(label="📍 您所點擊的儲存格座標")

    board.select(select_cell, None, selected_cell_output)

demo.launch()
