import sys
from pathlib import Path

import streamlit as st


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.rag_chain import ask_aerocopilot


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AeroCopilot",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------
       GLOBAL
    ------------------------------------------------- */

    .stApp {
        background: #FFFFFF;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 3.5rem;
        padding-bottom: 6rem;
    }

    /* Hide Streamlit's default top decoration */
    [data-testid="stDecoration"] {
        display: none;
    }

    /* -------------------------------------------------
       SIDEBAR
    ------------------------------------------------- */

    [data-testid="stSidebar"] {
        background: #F7F6F2;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    .sidebar-brand {
        font-size: 1.25rem;
        font-weight: 800;
        color: #171717;
        margin-bottom: 0.2rem;
    }

    .sidebar-description {
        color: #777;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    .sidebar-section {
        margin-top: 1.8rem;
        margin-bottom: 0.7rem;
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #777;
    }

    .document-item {
        font-size: 0.82rem;
        color: #555;
        padding: 0.35rem 0;
        line-height: 1.35;
    }

    .system-online {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: #333;
    }

    .online-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #38b87c;
        display: inline-block;
    }

    /* -------------------------------------------------
       HERO
    ------------------------------------------------- */

    .eyebrow {
        color: #7c4dff;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .hero-title {
        color: #171717;
        font-size: 3.4rem;
        font-weight: 800;
        line-height: 1;
        letter-spacing: -0.04em;
        margin: 0;
    }

    .hero-description {
        color: #6c6c6c;
        font-size: 1rem;
        line-height: 1.6;
        max-width: 720px;
        margin-top: 0.9rem;
        margin-bottom: 2rem;
    }


    

    /* -------------------------------------------------
       CHAT
    ------------------------------------------------- */

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        margin-bottom: 1rem;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 0.95rem;
        line-height: 1.65;
    }

    /* -------------------------------------------------
       CITATIONS
    ------------------------------------------------- */

    .sources-label {
        color: #7c4dff;
        font-size: 0.68rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    .source-item {
        background: #FFFFFF;
        border: 1px solid #e1e1dc;
        border-radius: 9px;
        padding: 0.65rem 0.8rem;
        margin-bottom: 0.4rem;
        font-size: 0.78rem;
        color: #555;
    }

    .source-name {
        font-weight: 700;
        color: #333;
    }

    /* -------------------------------------------------
       EVIDENCE
    ------------------------------------------------- */

    .evidence-text {
        font-size: 0.82rem;
        line-height: 1.6;
        color: #555;
    }

    /* -------------------------------------------------
       EXAMPLE QUESTIONS
    ------------------------------------------------- */

    .examples-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #777;
        margin-bottom: 0.4rem;
    }

    /* -------------------------------------------------
       FOOTER
    ------------------------------------------------- */

    .footer {
        text-align: center;
        color: #888;
        font-size: 0.72rem;
        padding: 2rem 0 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            ✈️ AeroCopilot
        </div>

        <div class="sidebar-description">
            Aviation knowledge assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-section">Knowledge Base</div>',
        unsafe_allow_html=True,
    )

    documents_path = BASE_DIR / "data" / "documents"

    documents = []

    if documents_path.exists():
        documents = sorted(documents_path.glob("*.pdf"))

    st.metric(
        "Documents",
        len(documents),
    )

    for document in documents:
        st.markdown(
            f"""
            <div class="document-item">
                📄 {document.name}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="sidebar-section">System</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="system-online">
            <span class="online-dot"></span>
            RAG engine online
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Semantic retrieval")
    st.caption("Grounded generation")
    st.caption("Source citations")
    st.caption("Abstention enabled")

    st.markdown(
        '<div class="sidebar-section">Conversation</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "＋ New conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption(
        "A research prototype from the "
        "Olive Aviation Innovation Lab."
    )

    st.caption(
        "AeroCopilot does not replace approved "
        "aviation documentation or professional judgment."
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="eyebrow">
        OLIVE AVIATION INNOVATION LAB
    </div>

    <div class="hero-title">
        AeroCopilot
    </div>

    <div class="hero-description">
        Ask questions about aviation technical documentation.
        AeroCopilot retrieves relevant evidence and generates
        grounded answers with source citations.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# EMPTY STATE
# =========================================================

# =========================================================
# EMPTY STATE
# =========================================================

if not st.session_state.messages:

    empty_state = st.container(
        border=True
    )

    with empty_state:

        st.markdown(
            "### ✈️ What would you like to know?"
        )

        st.caption(
            "Ask about maintenance, inspections, "
            "safety procedures, or aircraft operations."
        )

    st.write("")

    st.caption("Try asking")

    example_col1, example_col2, example_col3 = st.columns(3)

    examples = [
        "Hydraulic system inspection",
        "Maintenance PPE requirements",
        "Hydraulic leakage procedure",
    ]

    for column, example in zip(
        [example_col1, example_col2, example_col3],
        examples,
    ):

        with column:

            if st.button(
                example,
                use_container_width=True,
            ):

                st.session_state.pending_question = example
                st.rerun()

# =========================================================
# DISPLAY CONVERSATION
# =========================================================

for message in st.session_state.messages:

    role = message["role"]

    with st.chat_message(
        role,
        avatar="✈️" if role == "assistant" else "👤",
    ):

        st.markdown(message["content"])

        # ---------------------------------------------
        # SOURCES
        # ---------------------------------------------

        if role == "assistant":

            citations = message.get(
                "citations",
                [],
            )

            if citations:

                st.markdown(
                    '<div class="sources-label">Sources</div>',
                    unsafe_allow_html=True,
                )

                for citation in citations:

                    source = citation.get(
                        "source",
                        "Unknown source",
                    )

                    page = citation.get(
                        "page",
                        "Unknown page",
                    )

                    score = citation.get(
                        "score",
                        None,
                    )

                    score_text = ""

                    if score is not None:
                        score_text = (
                            f" · score {score}"
                        )

                    st.markdown(
                        f"""
                        <div class="source-item">
                            📄
                            <span class="source-name">
                                {source}
                            </span>
                            · Page {page}
                            {score_text}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            retrieved = message.get(
                "retrieved_documents",
                [],
            )

            if retrieved:

                with st.expander(
                    "View retrieved evidence"
                ):

                    for index, evidence in enumerate(
                        retrieved,
                        start=1,
                    ):

                        st.markdown(
                            f"**Evidence {index}**"
                        )

                        st.markdown(
                            f"""
                            <div class="evidence-text">
                                {evidence}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )


# =========================================================
# PENDING EXAMPLE QUESTION
# =========================================================

pending_question = st.session_state.pop(
    "pending_question",
    None,
)


# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "Ask a follow-up question..."
)

if pending_question:
    prompt = pending_question


# =========================================================
# PROCESS QUESTION
# =========================================================

if prompt:

    prompt = prompt.strip()

    if prompt:

        # ---------------------------------------------
        # ADD USER MESSAGE
        # ---------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        # ---------------------------------------------
        # SHOW USER MESSAGE IMMEDIATELY
        # ---------------------------------------------

        with st.chat_message(
            "user",
            avatar="👤",
        ):

            st.markdown(prompt)

        # ---------------------------------------------
        # PREPARE CONTEXT FOR FOLLOW-UP
        # ---------------------------------------------

        previous_messages = st.session_state.messages[:-1]

        context = ""

        if previous_messages:

            recent_messages = previous_messages[-6:]

            context_parts = []

            for message in recent_messages:

                context_parts.append(
                    f"{message['role'].upper()}: "
                    f"{message['content']}"
                )

            context = "\n".join(context_parts)

        # ---------------------------------------------
        # CREATE SEARCH QUESTION
        # ---------------------------------------------

        search_question = prompt

        if context:

            search_question = f"""
Conversation history:

{context}

Current user question:

{prompt}

Use the conversation history only to understand
what the user is referring to. Answer the current
question using the retrieved AeroCopilot documents.
""".strip()

        # ---------------------------------------------
        # CALL RAG ENGINE
        # ---------------------------------------------

        with st.chat_message(
            "assistant",
            avatar="✈️",
        ):

            with st.spinner(
                "Searching aviation documentation..."
            ):

                try:

                    result = ask_aerocopilot(
                        search_question,
                        k=4,
                    )

                    answer = result.get(
                        "answer",
                        "No answer returned.",
                    )

                    citations = result.get(
                        "citations",
                        [],
                    )

                    retrieved_documents = result.get(
                        "retrieved_documents",
                        [],
                    )

                    st.markdown(answer)

                    # ---------------------------------
                    # SOURCES
                    # ---------------------------------

                    if citations:

                        st.markdown(
                            '<div class="sources-label">'
                            'Sources'
                            '</div>',
                            unsafe_allow_html=True,
                        )

                        for citation in citations:

                            source = citation.get(
                                "source",
                                "Unknown source",
                            )

                            page = citation.get(
                                "page",
                                "Unknown page",
                            )

                            score = citation.get(
                                "score",
                                None,
                            )

                            score_text = ""

                            if score is not None:
                                score_text = (
                                    f" · score {score}"
                                )

                            st.markdown(
                                f"""
                                <div class="source-item">
                                    📄
                                    <span class="source-name">
                                        {source}
                                    </span>
                                    · Page {page}
                                    {score_text}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    # ---------------------------------
                    # EVIDENCE
                    # ---------------------------------

                    if retrieved_documents:

                        with st.expander(
                            "View retrieved evidence"
                        ):

                            for index, evidence in enumerate(
                                retrieved_documents,
                                start=1,
                            ):

                                st.markdown(
                                    f"**Evidence {index}**"
                                )

                                st.markdown(
                                    f"""
                                    <div class="evidence-text">
                                        {evidence}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                    # ---------------------------------
                    # SAVE ASSISTANT MESSAGE
                    # ---------------------------------

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "citations": citations,
                            "retrieved_documents":
                                retrieved_documents,
                        }
                    )

                except Exception as error:

                    error_message = (
                        "AeroCopilot encountered an error "
                        "while processing your question."
                    )

                    st.error(error_message)
                    st.exception(error)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                        }
                    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        AeroCopilot · Olive Aviation Innovation Lab
        <br>
        AI-assisted aviation information retrieval
        and decision support prototype.
    </div>
    """,
    unsafe_allow_html=True,
)