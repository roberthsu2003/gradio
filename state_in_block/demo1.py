# Session State in block

import gradio as gr

with gr.Blocks() as demo:
    cart = gr.State([])
    items_to_add = gr.CheckboxGroup(["Cereal", "Milk", "Orange Juice", "Water"])

    def add_item(new_items, previous_cart):
        cart = previous_cart + new_items
        return cart
    
    gr.Button("Add Items").click(
        fn = add_item,
        inputs = [items_to_add, cart],
        outputs = cart
    )

    cart_size = gr.Number(label="Cart Size")
    cart.change(lambda cart: len(cart), inputs=cart, outputs=cart_size)

demo.launch()