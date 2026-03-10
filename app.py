import json
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Crisis Annotation", layout="wide")

DATA_FILES = {
    "Virgile":  "label_studio/annotator_1.json",
    "Lula":     "label_studio/annotator_2.json",
    "Yana":     "label_studio/annotator_3.json",
}

ACCENT = "#c0392b"  # deep red — fitting for a crisis project

st.markdown(f"""
<style>
    /* Page background */
    .stApp {{ background-color: #1a1a2e; }}

    /* Main content area */
    section[data-testid="stMain"] > div {{
        background-color: #1a1a2e;
    }}

    /* Sidebar (unused but just in case) */
    section[data-testid="stSidebar"] {{ background-color: #16213e; }}

    /* All text white by default */
    html, body, [class*="css"], p, label, span, div {{
        color: #f0f0f0 !important;
    }}

    /* Conversation box */
    .conv-box {{
        background: #16213e;
        border: 1px solid #c0392b55;
        border-radius: 8px;
        padding: 20px;
        font-family: Georgia, serif;
        font-size: 14px;
        line-height: 1.9;
        white-space: pre-wrap;
        max-height: 540px;
        overflow-y: auto;
        color: #e8e8e8 !important;
    }}

    /* Form panel */
    .form-panel {{
        background: #16213e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 20px;
    }}

    /* Dividers */
    hr {{ border-color: #333 !important; }}

    /* Progress bar colour */
    .stProgress > div > div {{ background-color: {ACCENT} !important; }}

    /* Primary buttons */
    .stButton > button[kind="primary"] {{
        background-color: {ACCENT} !important;
        border: none !important;
        color: white !important;
        font-weight: 600;
    }}
    .stButton > button[kind="primary"]:hover {{
        background-color: #a93226 !important;
    }}

    /* Secondary buttons */
    .stButton > button {{
        background-color: #2c2c54 !important;
        border: 1px solid #444 !important;
        color: #f0f0f0 !important;
    }}

    /* Radio buttons */
    .stRadio label {{ color: #f0f0f0 !important; }}

    /* Slider */
    .stSlider label {{ color: #f0f0f0 !important; }}

    /* Select box */
    .stSelectbox label {{ color: #f0f0f0 !important; }}
    .stSelectbox div[data-baseweb="select"] {{
        background-color: #16213e !important;
        border-color: #444 !important;
    }}

    /* Download button */
    .stDownloadButton > button {{
        background-color: #27ae60 !important;
        border: none !important;
        color: white !important;
        font-weight: 600;
        width: 100%;
    }}

    /* Title */
    h1 {{ color: {ACCENT} !important; letter-spacing: 1px; }}
    h2, h3 {{ color: #e0e0e0 !important; }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_tasks(annotator: str):
    with open(DATA_FILES[annotator], encoding="utf-8") as f:
        return json.load(f)


def get_csv(annotations: dict) -> str:
    rows = [{"conversation_id": k, **v} for k, v in annotations.items()]
    return pd.DataFrame(rows).to_csv(index=False)


# ── Login screen ─────────────────────────────────────────────────────────────

def login():
    st.title("Crisis Annotation")
    st.markdown("<p style='color:#aaa; margin-top:-12px;'>Diplomatic conversations · 100 tasks per annotator</p>", unsafe_allow_html=True)
    st.divider()

    col, _ = st.columns([1, 2])
    with col:
        st.subheader("Who are you?")
        annotator = st.selectbox("Select your name", list(DATA_FILES.keys()))
        resume_file = st.file_uploader("Resume from a previous session (optional)", type="csv")

        if st.button("Start annotating", type="primary"):
            annotations = {}
            if resume_file:
                df = pd.read_csv(resume_file)
                for _, row in df.iterrows():
                    annotations[str(row["conversation_id"])] = {
                        "is_crisis": row["is_crisis"],
                        "rating": int(row["rating"]),
                    }

            st.session_state.annotator = annotator
            st.session_state.annotations = annotations

            tasks = load_tasks(annotator)
            annotated_ids = set(annotations.keys())
            first_unannotated = next(
                (i for i, t in enumerate(tasks)
                 if str(t["data"]["conversation_id"]) not in annotated_ids),
                0,
            )
            st.session_state.idx = first_unannotated
            st.rerun()


# ── Annotation screen ─────────────────────────────────────────────────────────

def annotate():
    annotator = st.session_state.annotator
    annotations = st.session_state.annotations
    tasks = load_tasks(annotator)
    total = len(tasks)
    idx = st.session_state.idx
    task = tasks[idx]
    conv_id = str(task["data"]["conversation_id"])
    text = task["data"]["text"]
    existing = annotations.get(conv_id)

    # ── Header ──
    h1, h2 = st.columns([6, 2])
    with h1:
        done = len(annotations)
        st.progress(done / total, text=f"{done} / {total} annotated  —  annotating as **{annotator}**")
    with h2:
        if st.button("Change annotator"):
            for key in ("annotator", "annotations", "idx"):
                st.session_state.pop(key, None)
            st.rerun()

    # ── Navigation ──
    nav_l, nav_c, nav_r = st.columns([1, 8, 1])
    with nav_l:
        if st.button("← Prev", disabled=(idx == 0)):
            st.session_state.idx -= 1
            st.rerun()
    with nav_c:
        status = "✅" if existing else "○"
        st.markdown(
            f"<p style='text-align:center; color:#888;'>"
            f"{status} Task {idx + 1} of {total} &nbsp;·&nbsp; <code style='color:#aaa'>{conv_id}</code>"
            f"</p>",
            unsafe_allow_html=True,
        )
    with nav_r:
        if st.button("Next →", disabled=(idx == total - 1)):
            st.session_state.idx += 1
            st.rerun()

    st.divider()

    # ── Main columns ──
    col_text, col_form = st.columns([3, 1])

    with col_text:
        st.markdown("**Conversation**")
        st.markdown(
            f"<div class='conv-box'>{text}</div>",
            unsafe_allow_html=True,
        )

    with col_form:
        st.markdown("<div class='form-panel'>", unsafe_allow_html=True)
        st.markdown("**Your annotation**")

        is_crisis_options = ["Yes", "No"]
        is_crisis_default = (
            is_crisis_options.index(existing["is_crisis"]) if existing else None
        )
        is_crisis = st.radio(
            "Is this a crisis-time conversation?",
            is_crisis_options,
            index=is_crisis_default,
            key=f"ic_{idx}",
        )

        rating_default = existing["rating"] if existing else 5
        rating = st.slider(
            "Severity (1 = no crisis · 10 = acute crisis)",
            min_value=1, max_value=10,
            value=rating_default,
            key=f"r_{idx}",
        )

        st.markdown("")
        save_label = "Save & Next →" if idx < total - 1 else "Save"
        if st.button(save_label, type="primary", disabled=(is_crisis is None)):
            annotations[conv_id] = {"is_crisis": is_crisis, "rating": rating}
            st.session_state.annotations = annotations
            if idx < total - 1:
                st.session_state.idx += 1
            st.rerun()

        st.divider()
        st.download_button(
            "💾 Download progress",
            data=get_csv(annotations),
            file_name=f"{annotator}_annotations.csv",
            mime="text/csv",
            disabled=(len(annotations) == 0),
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if len(annotations) == total:
        st.success("All done! Download your CSV above and send it back.")


# ── Router ────────────────────────────────────────────────────────────────────

if "annotator" not in st.session_state:
    login()
else:
    annotate()
