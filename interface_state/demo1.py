# 全域狀態 (Global State) 範例
import gradio as gr

# 全域變數，供所有使用者連線共享
scores = []

def track_score(score):
    scores.append(score)
    # 取出前 3 個最高的分數
    top_scores = sorted(scores, reverse=True)[:3]
    return top_scores

# 建立介面
demo = gr.Interface(
    fn=track_score,
    inputs=gr.Number(label="您的得分 (請輸入數值)"),
    outputs=gr.JSON(label="目前前 3 名最高分數排行榜"),
    title="🏆 全域分數排行榜系統",
    description="本系統展示全域狀態的運作。請輸入分數，系統將追蹤所有使用者的最高紀錄。您可以同時開啟多個瀏覽器分頁進行交叉測試！",
)

if __name__ == "__main__":
    demo.launch()