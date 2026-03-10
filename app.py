import json
import streamlit as st
import pandas as pd
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Crisis Annotation", layout="wide")

DATA_FILES = {
    "Virgile":  "label_studio/annotator_1.json",
    "Lula":     "label_studio/annotator_2.json",
    "Yana":     "label_studio/annotator_3.json",
}

SHEET_ID = "1a2hf6GuBozc-mpdkTWaObTj2XlYrvN7KZ1ibc8ZqZpw"
SCOPES   = ["https://www.googleapis.com/auth/spreadsheets"]
ACCENT   = "#c0392b"

st.markdown(f"""
<style>
    .stApp {{ background-color: #1a1a2e; }}
    section[data-testid="stMain"] > div {{ background-color: #1a1a2e; }}
    html, body, [class*="css"], p, label, span, div {{ color: #f0f0f0 !important; }}
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
    .form-panel {{
        background: #16213e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 20px;
    }}
    hr {{ border-color: #333 !important; }}
    .stProgress > div > div {{ background-color: {ACCENT} !important; }}
    .stButton > button[kind="primary"] {{
        background-color: {ACCENT} !important;
        border: none !important;
        color: white !important;
        font-weight: 600;
    }}
    .stButton > button[kind="primary"]:hover {{ background-color: #a93226 !important; }}
    .stButton > button {{
        background-color: #2c2c54 !important;
        border: 1px solid #444 !important;
        color: #f0f0f0 !important;
    }}
    .stRadio label {{ color: #f0f0f0 !important; }}
    .stSlider label {{ color: #f0f0f0 !important; }}
    .stSelectbox label {{ color: #f0f0f0 !important; }}
    .stSelectbox div[data-baseweb="select"] {{
        background-color: #16213e !important;
        border-color: #444 !important;
    }}
    .stDownloadButton > button {{
        background-color: #27ae60 !important;
        border: none !important;
        color: white !important;
        font-weight: 600;
        width: 100%;
    }}
    h1 {{ color: {ACCENT} !important; letter-spacing: 1px; }}
    h2, h3 {{ color: #e0e0e0 !important; }}
</style>
""", unsafe_allow_html=True)


# ── Google Sheets connection ──────────────────────────────────────────────────

@st.cache_resource
def get_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES,
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    # Create header row if sheet is empty
    if sheet.row_count == 0 or sheet.cell(1, 1).value != "annotator":
        sheet.append_row(["annotator", "conversation_id", "is_crisis", "rating", "timestamp"])
    return sheet


def load_annotations_from_sheet(annotator: str) -> dict:
    """Load all saved annotations for this annotator from the sheet."""
    sheet = get_sheet()
    records = sheet.get_all_records()
    annotations = {}
    for r in records:
        if str(r.get("annotator")) == annotator:
            # Later rows overwrite earlier ones (handles re-annotations)
            annotations[str(r["conversation_id"])] = {
                "is_crisis": r["is_crisis"],
                "rating": int(r["rating"]),
            }
    return annotations


def save_annotation_to_sheet(annotator: str, conv_id: str, is_crisis: str, rating: int):
    """Update existing row if present, otherwise append."""
    sheet = get_sheet()
    all_values = sheet.get_all_values()  # [[col1, col2, ...], ...]
    new_row = [annotator, conv_id, is_crisis, rating, datetime.utcnow().isoformat()]
    for i, row in enumerate(all_values[1:], start=2):  # skip header, 1-indexed
        if row[0] == annotator and row[1] == conv_id:
            sheet.update(f"A{i}:E{i}", [new_row])
            return
    sheet.append_row(new_row)


# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_data
def load_tasks(annotator: str):
    with open(DATA_FILES[annotator], encoding="utf-8") as f:
        return json.load(f)


def get_csv(annotations: dict) -> str:
    rows = [{"conversation_id": k, **v} for k, v in annotations.items()]
    return pd.DataFrame(rows).to_csv(index=False)


# ── Login screen ──────────────────────────────────────────────────────────────

def login():
    st.title("Crisis Annotation")
    st.markdown(
        "<p style='color:#aaa; margin-top:-12px;'>Diplomatic conversations · 100 tasks per annotator</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    col, _ = st.columns([1, 2])
    with col:
        st.subheader("Who are you?")
        annotator = st.selectbox("Select your name", list(DATA_FILES.keys()))

        if st.button("Start annotating", type="primary"):
            with st.spinner("Loading your saved progress…"):
                annotations = load_annotations_from_sheet(annotator)

            n = len(annotations)
            if n > 0:
                st.success(f"Found {n} saved annotations — resuming where you left off.")

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
            f"{status} Task {idx + 1} of {total} &nbsp;·&nbsp; "
            f"<code style='color:#aaa'>{conv_id}</code></p>",
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
        st.markdown(f"<div class='conv-box'>{text}</div>", unsafe_allow_html=True)

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
            save_annotation_to_sheet(annotator, conv_id, is_crisis, rating)
            if idx < total - 1:
                st.session_state.idx += 1
            st.rerun()

        st.divider()
        st.caption(f"✅ {len(annotations)} / {total} saved to Google Sheets")
        st.download_button(
            "💾 Download CSV",
            data=get_csv(annotations),
            file_name=f"{annotator}_annotations.csv",
            mime="text/csv",
            disabled=(len(annotations) == 0),
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if len(annotations) == total:
        st.success("All done! You can now download your CSV or just close the tab.")


# ── Router ────────────────────────────────────────────────────────────────────

if "annotator" not in st.session_state:
    login()
else:
    annotate()
