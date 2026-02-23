import gradio as gr
from sentiment_analysis_app.sentiment_analysis_app import demo as sentiment_demo
from translation_app.translation_app import demo as translation_demo

app = gr.TabbedInterface(
    interface_list=[sentiment_demo, translation_demo],
    tab_names=["Sentiment Analysis", "Translation"],
    title="Azure AI Foundry Tools",
)

if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft())
