import json
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Crisis Annotation", layout="wide")

DATA_FILES = {
    "Annotator 1": "label_studio/annotator_1.json",
    "Annotator 2": "label_studio/annotator_2.json",
    "Annotator 3": "label_studio/annotator_3.json",
}


@st.cache_data
def load_tasks(annotator: str):
    with open(DATA_FILES[annotator], encoding="utf-8") as f:
        return json.load(f)


def get_csv(annotations: dict) -> str:
    rows = [{"conversation_id": k, **v} for k, v in annotations.items()]
    return pd.DataFrame(rows).to_csv(index=False)


# ── Login screen ────────────────────────────────────────────────────────────

def login():
    st.title("Crisis Annotation")
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

        # Jump to first unannotated task
        tasks = load_tasks(annotator)
        annotated_ids = set(annotations.keys())
        first_unannotated = next(
            (i for i, t in enumerate(tasks)
             if str(t["data"]["conversation_id"]) not in annotated_ids),
            0,
        )
        st.session_state.idx = first_unannotated
        st.rerun()


# ── Annotation screen ────────────────────────────────────────────────────────

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

    # ── Header row ──
    header_left, header_right = st.columns([6, 2])
    with header_left:
        done = len(annotations)
        st.progress(done / total, text=f"{done} / {total} annotated")
    with header_right:
        if st.button("Change annotator"):
            for key in ("annotator", "annotations", "idx"):
                st.session_state.pop(key, None)
            st.rerun()

    # ── Navigation ──
    nav_left, nav_center, nav_right = st.columns([1, 8, 1])
    with nav_left:
        if st.button("← Prev", disabled=(idx == 0)):
            st.session_state.idx -= 1
            st.rerun()
    with nav_center:
        status = "✅" if existing else "○"
        st.markdown(
            f"<p style='text-align:center; color:grey;'>"
            f"{status} Task {idx + 1} of {total} — <code>{conv_id}</code>"
            f"</p>",
            unsafe_allow_html=True,
        )
    with nav_right:
        if st.button("Next →", disabled=(idx == total - 1)):
            st.session_state.idx += 1
            st.rerun()

    st.divider()

    # ── Conversation text ──
    col_text, col_form = st.columns([3, 1])

    with col_text:
        st.markdown("**Conversation**")
        st.markdown(
            f"<div style='"
            f"background:#f8f8f8; border:1px solid #ddd; border-radius:6px;"
            f"padding:16px; font-family:serif; font-size:14px; line-height:1.8;"
            f"white-space:pre-wrap; max-height:520px; overflow-y:auto;'>"
            f"{text}"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── Annotation form ──
    with col_form:
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
            "Severity (1 = no crisis, 10 = acute crisis)",
            min_value=1,
            max_value=10,
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
            file_name=f"{annotator.replace(' ', '_')}_annotations.csv",
            mime="text/csv",
            disabled=(len(annotations) == 0),
        )

    # ── Done banner ──
    if len(annotations) == total:
        st.success("All done! Download your CSV above and send it back.")


# ── Router ──────────────────────────────────────────────────────────────────

if "annotator" not in st.session_state:
    login()
else:
    annotate()
