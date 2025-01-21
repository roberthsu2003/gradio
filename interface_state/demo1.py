#Global State example
import gradio as gr

scores = []

def track_score(score):
    scores.append(score)
    top_scores = sorted(scores,reverse=True)[:3]
    return top_scores

demo = gr.Interface(
    fn=track_score,
    inputs=gr.Number(label="分數"),
    outputs=gr.JSON(label="前3個最高的分數"),
    title="前3個最高的分數",
    description="請輸入您的分數,我們將追蹤前3個最高的分數,請同時開啟兩個以上的分頁測試",
)

demo.launch()