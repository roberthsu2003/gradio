## 保存Blocks State

### Global State
- 就是python文件變數
- 分享給所有的使用者和function

### Session State
Gradio 支援會話狀態，其中資料在頁面會話中的多次提交中仍然存在，在 Blocks 應用程式中也是如此,session state不會分享給其它使用者, 儲存資料在session state,必需做3件事

- 建立gr.State()實體, 如果這實體需要有default值,建立時就將default值加入
- 在事件監聽器內,依據需要,將它放在inputs或outputs
- 在事件監聽器函式內,接收或傳遞


```python

```