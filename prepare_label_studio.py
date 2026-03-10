"""
Prepares Label Studio import files for 3 annotators.

Shared batch (40 conversations, everyone sees these):
  - 20 from non_crisis
  -  8 from crisis severity 9
  -  5 from crisis severity 8
  -  7 from crisis severity 5-7 (filler)

Unique batch (60 per annotator):
  - at least 10 non_crisis  (so total non_crisis >= 30 per annotator)
  - rest from crisis (any severity)
"""

import json
import os
import random
from pathlib import Path

SEED = 42
SHARED        = 40
UNIQUE        = 60          # per annotator
N_ANNOTATORS  = 3
MIN_NON_CRISIS_UNIQUE = 10  # ensures >= 30 non_crisis total per annotator

NEWRUN  = Path("newrun")
OUT_DIR = Path("label_studio")

random.seed(SEED)


# ── Load all conversations ────────────────────────────────────────────────────

def load_conversations():
    records = []
    for json_path in NEWRUN.rglob("*.json"):
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        conv_id = json_path.stem
        folder  = json_path.parent.relative_to(NEWRUN).parts[0]  # crisis / non_crisis
        cls     = data.get("classification", {})
        turns   = data.get("conversation", [])

        # Flatten EDUs into readable text
        text_lines     = []
        current_spk    = None
        current_edus   = []
        for turn in turns:
            for edu in turn.get("edus", []):
                spk = edu.get("speaker", "?")
                txt = edu.get("text", "").strip()
                if spk != current_spk:
                    if current_edus:
                        text_lines.append(f"[{current_spk}] " + " ".join(current_edus))
                    current_spk  = spk
                    current_edus = [txt]
                else:
                    current_edus.append(txt)
        if current_edus:
            text_lines.append(f"[{current_spk}] " + " ".join(current_edus))

        records.append({
            "id":       conv_id,
            "folder":   folder,
            "severity": cls.get("severity", 0),
            "text":     "\n\n".join(text_lines),
        })
    return records


def to_ls_task(r):
    return {"data": {"conversation_id": r["id"], "source": r["folder"], "text": r["text"]}}


# ── Sampling ──────────────────────────────────────────────────────────────────

def main():
    OUT_DIR.mkdir(exist_ok=True)

    print("Loading conversations...")
    records = load_conversations()

    non_crisis = [r for r in records if r["folder"] == "non_crisis"]
    sev9       = [r for r in records if r["folder"] == "crisis" and r["severity"] == 9]
    sev8       = [r for r in records if r["folder"] == "crisis" and r["severity"] == 8]
    sev_other  = [r for r in records if r["folder"] == "crisis" and r["severity"] not in (8, 9)]

    print(f"  non_crisis: {len(non_crisis)}  |  sev9: {len(sev9)}  |  sev8: {len(sev8)}  |  other crisis: {len(sev_other)}")

    random.shuffle(non_crisis)
    random.shuffle(sev9)
    random.shuffle(sev8)
    random.shuffle(sev_other)

    # ── Build shared batch ────────────────────────────────────────────────────
    shared_nc   = non_crisis[:20];        non_crisis = non_crisis[20:]
    shared_s9   = sev9[:8];               sev9       = sev9[8:]
    shared_s8   = sev8[:5];               sev8       = sev8[5:]
    shared_fill = sev_other[:7];          sev_other  = sev_other[7:]

    shared = shared_nc + shared_s9 + shared_s8 + shared_fill
    assert len(shared) == SHARED, f"Expected {SHARED} shared, got {len(shared)}"
    random.shuffle(shared)

    # ── Build unique batches ──────────────────────────────────────────────────
    # Remaining non_crisis pool for unique slots
    crisis_pool = sev9 + sev8 + sev_other
    random.shuffle(crisis_pool)

    batches = []
    for i in range(N_ANNOTATORS):
        nc_slice  = non_crisis[i * MIN_NON_CRISIS_UNIQUE : (i + 1) * MIN_NON_CRISIS_UNIQUE]
        n_crisis  = UNIQUE - len(nc_slice)
        cr_slice  = crisis_pool[i * n_crisis : (i + 1) * n_crisis]
        unique    = nc_slice + cr_slice
        random.shuffle(unique)
        batch = shared + unique
        random.shuffle(batch)
        batches.append(batch)

    # ── Write output ──────────────────────────────────────────────────────────
    names = ["Virgile", "Lula", "Yana"]
    for i, (batch, name) in enumerate(zip(batches, names), 1):
        tasks     = [to_ls_task(r) for r in batch]
        out_path  = OUT_DIR / f"annotator_{i}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

        nc_count  = sum(1 for r in batch if r["folder"] == "non_crisis")
        print(f"  {name} (annotator_{i}.json): {len(tasks)} tasks, {nc_count} non_crisis")

    print(f"\nShared batch breakdown:")
    print(f"  non_crisis : {len(shared_nc)}")
    print(f"  severity 9 : {len(shared_s9)}")
    print(f"  severity 8 : {len(shared_s8)}")
    print(f"  other      : {len(shared_fill)}")
    print(f"\nDone. Files in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
