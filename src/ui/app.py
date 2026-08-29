import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/ask"


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="VectorDNA",
    page_icon="🧬",
    layout="centered",
)


# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main container */
    .block-container {
        max-width: 900px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 0.2rem;
    }

    .brand-icon {
        font-size: 2.8rem;
    }

    .brand-name {
        font-size: 2.8rem;
        font-weight: 750;
        letter-spacing: -1px;
    }

    .subtitle {
        color: #6b7280;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    /* Ask section */
    .ask-label {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    /* Answer */
    .answer-card {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.4rem 1.5rem;
        margin-top: 0.5rem;
        line-height: 1.7;
    }

    /* Source cards */
    .source-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }

    .source-title {
        font-weight: 650;
        font-size: 1rem;
        margin-bottom: 0.35rem;
    }

    .source-file {
        color: #047857;
        font-family: monospace;
        font-size: 0.85rem;
        background: #f0fdf4;
        padding: 0.2rem 0.4rem;
        border-radius: 5px;
    }

    .score {
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: 0.6rem;
    }

    /* Section headings */
    .section-heading {
        font-size: 1.55rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 0.8rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.8rem;
        margin-top: 3rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">🧬</div>
        <div class="brand-name">VectorDNA</div>
    </div>

    <div class="subtitle">
        Ask questions about Python documentation using local RAG.
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Question input
# --------------------------------------------------

st.markdown(
    '<div class="ask-label">Ask a question</div>',
    unsafe_allow_html=True,
)

question = st.text_area(
    label="Question",
    placeholder="e.g. What is the asyncio event loop?",
    height=100,
    label_visibility="collapsed",
)


ask = st.button(
    "Ask VectorDNA →",
    type="primary",
    use_container_width=False,
)


# --------------------------------------------------
# Ask API
# --------------------------------------------------

if ask:

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Searching documentation and generating an answer..."):

        try:
            response = requests.post(
                API_URL,
                json={"question": question.strip()},
                timeout=60,
            )

            response.raise_for_status()

            data = response.json()

        except requests.RequestException:
            st.error(
                "Unable to connect to the VectorDNA API. "
                "Make sure FastAPI is running."
            )
            st.stop()

    # --------------------------------------------------
    # Answer
    # --------------------------------------------------

    st.markdown(
        '<div class="section-heading">Answer</div>',
        unsafe_allow_html=True,
    )

    st.html(
        f"""
        <div class="answer-card">
            {data["answer"]}
        </div>
        """
    )

    # --------------------------------------------------
    # Sources
    # --------------------------------------------------

    st.markdown(
        '<div class="section-heading">Sources</div>',
        unsafe_allow_html=True,
    )

    for source in data["sources"]:

        score = source["score"]

        st.html(
            f"""
            <div class="source-card">
                <div class="source-title">
                    {source["section"]}
                </div>

                <div>
                    <span class="source-file">
                        {source["source"]}
                    </span>
                </div>

                <div class="score">
                    Similarity score: <strong>{score:.3f}</strong>
                </div>
            </div>
            """
        )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        VectorDNA · Local RAG · Qdrant + Ollama
    </div>
    """,
    unsafe_allow_html=True,
)