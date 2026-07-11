# 1. Blocks 會話狀態 (Session State) 範例
import gradio as gr

with gr.Blocks() as demo:
    # 建立一個 Session 狀態變數，用來存放購物車商品清單 (預設為空清單)
    cart = gr.State([])
    
    items_to_add = gr.CheckboxGroup(
        ["麥片 (Cereal)", "牛奶 (Milk)", "柳橙汁 (Orange Juice)", "礦泉水 (Water)"],
        label="選擇欲加入購物車的商品"
    )
    add_btn = gr.Button("🛒 加入購物車")

    def add_item(new_items, previous_cart):
        # 將新選取的商品合併到先前的購物車中
        updated_cart = previous_cart + new_items
        return updated_cart
    
    add_btn.click(
        fn=add_item,
        inputs=[items_to_add, cart],
        outputs=cart
    )

    cart_size = gr.Number(label="目前購物車商品總數", value=0)
    # 當狀態 cart 改變時，動態更新數量顯示
    cart.change(lambda current_cart: len(current_cart), inputs=cart, outputs=cart_size)

if __name__ == "__main__":
    demo.launch()