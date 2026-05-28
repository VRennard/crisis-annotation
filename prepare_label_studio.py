"""
Prepares Label Studio import files for 3 annotators.

Target: 200 conversations per annotator, 50/50 crisis/non_crisis split.
Crisis conversations are oversampled toward severity >= 6.

Shared batch (80 conversations, everyone sees these):
  - 40 from non_crisis
  - 40 from crisis, all sev>=6:
      10 sev9 + 10 sev8 + 12 sev7 + 8 sev6

Unique batch (120 per annotator = 60 non_crisis + 60 crisis):
  - 60 non_crisis
  - 54 from crisis sev>=6 (remaining pool)
  -  6 from crisis sev5

Total non_crisis used: 40 + 3*60 = 220 (pool: 222)
Total crisis used:     40 + 3*60 = 220 (pool: 1808)
"""

import json
import os
import random
from pathlib import Path

SEED = 42
SHARED        = 80
UNIQUE        = 120         # per annotator  (total = 200)
N_ANNOTATORS  = 3
NC_UNIQUE     = 60          # non_crisis per annotator unique batch
CR_UNIQUE     = 60          # crisis per annotator unique batch
CR_HIGH_FRAC  = 0.90        # fraction of unique crisis from sev>=6

# Shared crisis breakdown (all sev>=6)
SHARED_SEV9 = 10
SHARED_SEV8 = 10
SHARED_SEV7 = 12
SHARED_SEV6 = 8
SHARED_NC   = 40

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
    sev7       = [r for r in records if r["folder"] == "crisis" and r["severity"] == 7]
    sev6       = [r for r in records if r["folder"] == "crisis" and r["severity"] == 6]
    sev5       = [r for r in records if r["folder"] == "crisis" and r["severity"] == 5]

    print(f"  non_crisis: {len(non_crisis)}  |  sev9: {len(sev9)}  |  sev8: {len(sev8)}  "
          f"|  sev7: {len(sev7)}  |  sev6: {len(sev6)}  |  sev5: {len(sev5)}")

    for pool in (non_crisis, sev9, sev8, sev7, sev6, sev5):
        random.shuffle(pool)

    # ── Build shared batch (80 = 40 NC + 40 crisis sev>=6) ────────────────────
    shared_nc  = non_crisis[:SHARED_NC];   non_crisis = non_crisis[SHARED_NC:]
    shared_s9  = sev9[:SHARED_SEV9];       sev9       = sev9[SHARED_SEV9:]
    shared_s8  = sev8[:SHARED_SEV8];       sev8       = sev8[SHARED_SEV8:]
    shared_s7  = sev7[:SHARED_SEV7];       sev7       = sev7[SHARED_SEV7:]
    shared_s6  = sev6[:SHARED_SEV6];       sev6       = sev6[SHARED_SEV6:]

    shared = shared_nc + shared_s9 + shared_s8 + shared_s7 + shared_s6
    assert len(shared) == SHARED, f"Expected {SHARED} shared, got {len(shared)}"
    random.shuffle(shared)

    # ── Build unique batches ──────────────────────────────────────────────────
    # Crisis pool: sev>=6 first, then sev5 as low-severity filler
    cr_high_pool = sev9 + sev8 + sev7 + sev6   # all remaining sev>=6
    random.shuffle(cr_high_pool)

    n_high = round(CR_UNIQUE * CR_HIGH_FRAC)    # 54
    n_low  = CR_UNIQUE - n_high                  # 6

    batches = []
    for i in range(N_ANNOTATORS):
        nc_slice   = non_crisis[i * NC_UNIQUE : (i + 1) * NC_UNIQUE]
        cr_hi      = cr_high_pool[i * n_high  : (i + 1) * n_high]
        cr_lo      = sev5[i * n_low           : (i + 1) * n_low]
        unique     = nc_slice + cr_hi + cr_lo
        random.shuffle(unique)
        batch = shared + unique
        random.shuffle(batch)
        batches.append(batch)

    # ── Write output ──────────────────────────────────────────────────────────
    names = ["Virgile", "Lula", "Yana"]
    for i, (batch, name) in enumerate(zip(batches, names), 1):
        tasks    = [to_ls_task(r) for r in batch]
        out_path = OUT_DIR / f"annotator_{i}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

        nc_count = sum(1 for r in batch if r["folder"] == "non_crisis")
        cr_count = len(batch) - nc_count
        hi_count = sum(1 for r in batch if r["folder"] == "crisis" and r["severity"] >= 6)
        print(f"  {name} (annotator_{i}.json): {len(tasks)} tasks  |  "
              f"{nc_count} non_crisis / {cr_count} crisis  |  {hi_count} crisis sev>=6")

    print(f"\nShared batch breakdown:")
    print(f"  non_crisis : {len(shared_nc)}")
    print(f"  severity 9 : {len(shared_s9)}")
    print(f"  severity 8 : {len(shared_s8)}")
    print(f"  severity 7 : {len(shared_s7)}")
    print(f"  severity 6 : {len(shared_s6)}")
    print(f"\nDone. Files in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
