"""Gradio frontend for the Semantic Search Engine API.

Run with:
    python app.py                         # defaults to http://localhost:3000
    SEARCH_API_URL=http://myhost:3000 python app.py
"""

import os
import gradio as gr
import pandas as pd

from client import SearchEngineClient

API_URL = os.getenv("SEARCH_API_URL", "http://localhost:3000")
client = SearchEngineClient(base_url=API_URL)


# ── Helpers ───────────────────────────────────────────────────────────────────


def _status_badge(ok: bool) -> str:
    return "🟢 Connected" if ok else "🔴 Disconnected"


def check_health():
    """Return a markdown string with API health info."""
    try:
        data = client.health()
        return (
            f"**Status:** {_status_badge(True)}\n\n"
            f"**Model:** `{data['model_name']}`\n\n"
            f"**Corpus size:** {data['corpus_size']} sentences"
        )
    except Exception as exc:
        return f"**Status:** {_status_badge(False)}\n\n**Error:** {exc}"


# ── Tab 1: Similarity ────────────────────────────────────────────────────────


def compute_similarity(sentence1: str, sentence2: str):
    if not sentence1.strip() or not sentence2.strip():
        return "⚠️ Please enter both sentences."
    try:
        result = client.similarity(sentence1, sentence2)
        score = result["score"]
        bar = "█" * int(abs(score) * 20) + "░" * (20 - int(abs(score) * 20))
        return (
            f"### Similarity Score: **{score:.4f}**\n\n"
            f"`[{bar}]`\n\n"
            f"- **Sentence 1:** {result['sentence1']}\n"
            f"- **Sentence 2:** {result['sentence2']}"
        )
    except Exception as exc:
        return f"❌ Error: {exc}"


# ── Tab 2: Corpus Status ──────────────────────────────────────────────────────


def get_corpus_status():
    try:
        result = client.get_corpus()
        return f"📦 **Corpus size:** {result['size']} sentences  |  **Model:** `{result['model_name']}`"
    except Exception as exc:
        return f"❌ Error: {exc}"


def clear_corpus():
    try:
        result = client.clear_corpus()
        return f"🗑️ Corpus cleared. Size: **{result['size']}**"
    except Exception as exc:
        return f"❌ Error: {exc}"


def browse_corpus(page: int):
    """Fetch a page of corpus sentences and return a summary + DataFrame."""
    page = max(int(page), 1)
    page_size = 20
    offset = (page - 1) * page_size
    try:
        result = client.browse_corpus(offset=offset, limit=page_size)
        sentences = result["sentences"]
        total = result["total"]
        total_pages = max(1, (total + page_size - 1) // page_size)

        if not sentences:
            return f"Page {page} is empty (corpus has {total} sentences).", None, page

        summary = (
            f"📦 **Corpus size:** {total} sentences  |  "
            f"**Page:** {page} / {total_pages}  |  "
            f"**Showing:** {offset + 1}–{offset + len(sentences)}"
        )

        df = pd.DataFrame(
            {"#": range(offset + 1, offset + len(sentences) + 1), "Sentence": sentences}
        )
        return summary, df, page
    except Exception as exc:
        return f"❌ Error: {exc}", None, page


def browse_next(page: int):
    return browse_corpus(page + 1)


def browse_prev(page: int):
    return browse_corpus(max(page - 1, 1))


# ── Tab 3: Search ────────────────────────────────────────────────────────────


def run_search(query: str, top_k: int):
    if not query.strip():
        return "⚠️ Enter a search query.", None
    try:
        result = client.search(query, top_k=int(top_k))
        hits = result["results"]
        if not hits:
            return "No results found.", None

        summary = (
            f"**Query:** {result['query']}\n\n"
            f"**Corpus size:** {result['total_corpus_size']}  |  "
            f"**Results:** {len(hits)}"
        )

        df = pd.DataFrame(hits)
        df.columns = ["Rank", "Sentence", "Score"]
        df["Score"] = df["Score"].apply(lambda s: f"{s:.4f}")
        return summary, df
    except Exception as exc:
        return f"❌ Error: {exc}", None


# ── Build UI ──────────────────────────────────────────────────────────────────

with gr.Blocks(
    title="Semantic Search Engine",
    theme=gr.themes.Soft(),
) as demo:
    gr.Markdown(
        "# 🔍 Semantic Search Engine\n"
        "A frontend for the sentence-transformers powered search API."
    )

    with gr.Row():
        health_box = gr.Markdown(value="Click **Refresh** to check API status.")
        health_btn = gr.Button("🔄 Refresh", scale=0)
    health_btn.click(fn=check_health, outputs=health_box)

    # ── Similarity tab ────────────────────────────────────────────────────
    with gr.Tab("🔗 Similarity"):
        gr.Markdown("Compare two sentences and get their cosine similarity score.")
        with gr.Row():
            sim_s1 = gr.Textbox(label="Sentence 1", placeholder="The cat sat on the mat.")
            sim_s2 = gr.Textbox(label="Sentence 2", placeholder="A kitten rested on the rug.")
        sim_btn = gr.Button("Compute Similarity", variant="primary")
        sim_out = gr.Markdown()
        sim_btn.click(fn=compute_similarity, inputs=[sim_s1, sim_s2], outputs=sim_out)

    # ── Corpus tab ────────────────────────────────────────────────────────
    with gr.Tab("📚 Corpus"):
        gr.Markdown("The corpus is pre-populated with AG News headlines at API startup.")
        with gr.Row():
            corpus_status_btn = gr.Button("📊 Status", variant="primary")
            corpus_clear_btn = gr.Button("🗑️ Clear", variant="stop")
        corpus_out = gr.Markdown()
        corpus_status_btn.click(fn=get_corpus_status, outputs=corpus_out)
        corpus_clear_btn.click(fn=clear_corpus, outputs=corpus_out)

        gr.Markdown("---")
        gr.Markdown("### Browse Corpus")
        browse_page = gr.State(value=1)
        browse_summary = gr.Markdown(value="Click **Load** to browse corpus sentences.")
        browse_table = gr.Dataframe(
            headers=["#", "Sentence"],
            interactive=False,
        )
        with gr.Row():
            browse_prev_btn = gr.Button("⬅️ Previous", scale=1)
            browse_load_btn = gr.Button("Load", variant="primary", scale=1)
            browse_next_btn = gr.Button("Next ➡️", scale=1)
        browse_load_btn.click(
            fn=browse_corpus,
            inputs=[browse_page],
            outputs=[browse_summary, browse_table, browse_page],
        )
        browse_next_btn.click(
            fn=browse_next,
            inputs=[browse_page],
            outputs=[browse_summary, browse_table, browse_page],
        )
        browse_prev_btn.click(
            fn=browse_prev,
            inputs=[browse_page],
            outputs=[browse_summary, browse_table, browse_page],
        )

    # ── Search tab ────────────────────────────────────────────────────────
    with gr.Tab("🔍 Search"):
        gr.Markdown("Search the indexed corpus for semantically similar sentences.")
        with gr.Row():
            search_query = gr.Textbox(label="Search Query", placeholder="How does artificial intelligence work?", scale=3)
            search_k = gr.Slider(label="Top K", minimum=1, maximum=50, value=5, step=1, scale=1)
        search_btn = gr.Button("Search", variant="primary")
        search_summary = gr.Markdown()
        search_table = gr.Dataframe(
            headers=["Rank", "Sentence", "Score"],
            interactive=False,
        )
        search_btn.click(fn=run_search, inputs=[search_query, search_k], outputs=[search_summary, search_table])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
