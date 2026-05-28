"""
Extends all annotator files to 200 conversations, identical across all annotators.

Rule:
  - First 40 tasks are KEPT exactly as-is (already annotated, shared IAA batch).
  - Tasks 41-200 are regenerated: same 160 conversations for all 3 annotators.
  - Full 200 = 50/50 split: 100 non_crisis + 100 crisis.
  - Crisis is oversampled toward sev>=6 (~90% of crisis slots).

First 40 (fixed): 20 non_crisis + 20 crisis
Remaining 160:    80 non_crisis + 80 crisis
  crisis breakdown: 72 sev>=6  +  8 sev5
"""

import json
import random
from pathlib import Path

SEED    = 99
NEWRUN  = Path("newrun")
OUT_DIR = Path("label_studio")

NC_NEEDED   = 80
CR_NEEDED   = 80
CR_HIGH     = 72   # sev >= 6
CR_LOW      = 8    # sev 5

random.seed(SEED)


def load_conversations(exclude_ids):
    records = []
    for json_path in NEWRUN.rglob("*.json"):
        conv_id = json_path.stem
        if conv_id in exclude_ids:
            continue
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
        folder = json_path.parent.relative_to(NEWRUN).parts[0]
        cls    = data.get("classification", {})
        turns  = data.get("conversation", [])

        text_lines, current_spk, current_edus = [], None, []
        for turn in turns:
            for edu in turn.get("edus", []):
                spk = edu.get("speaker", "?")
                txt = edu.get("text", "").strip()
                if spk != current_spk:
                    if current_edus:
                        text_lines.append(f"[{current_spk}] " + " ".join(current_edus))
                    current_spk, current_edus = spk, [txt]
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


def main():
    # Load the fixed first-40 from annotator_1 (same across all annotators)
    with open(OUT_DIR / "annotator_1.json", encoding="utf-8") as f:
        existing = json.load(f)

    first40   = existing[:40]
    fixed_ids = {t["data"]["conversation_id"] for t in first40}
    print(f"Fixed first-40 IDs loaded: {len(fixed_ids)}")

    # Load remaining corpus, excluding the fixed 40
    print("Loading available conversations...")
    records = load_conversations(exclude_ids=fixed_ids)

    non_crisis = [r for r in records if r["folder"] == "non_crisis"]
    sev_high   = [r for r in records if r["folder"] == "crisis" and r["severity"] >= 6]
    sev5       = [r for r in records if r["folder"] == "crisis" and r["severity"] == 5]

    print(f"  non_crisis: {len(non_crisis)}  |  crisis sev>=6: {len(sev_high)}  |  sev5: {len(sev5)}")
    assert len(non_crisis) >= NC_NEEDED, f"Not enough non_crisis: {len(non_crisis)} < {NC_NEEDED}"
    assert len(sev_high)   >= CR_HIGH,   f"Not enough sev>=6 crisis: {len(sev_high)} < {CR_HIGH}"
    assert len(sev5)       >= CR_LOW,    f"Not enough sev5 crisis: {len(sev5)} < {CR_LOW}"

    for pool in (non_crisis, sev_high, sev5):
        random.shuffle(pool)

    # Sample the 160 new conversations
    new_nc  = non_crisis[:NC_NEEDED]
    new_chi = sev_high[:CR_HIGH]
    new_clo = sev5[:CR_LOW]
    extension = new_nc + new_chi + new_clo
    random.shuffle(extension)
    assert len(extension) == 160

    new_tasks = [to_ls_task(r) for r in extension]
    full_batch = first40 + new_tasks   # first 40 fixed, then 160 new

    # Write identical file for all 3 annotators
    names = ["Virgile", "Lula", "Yana"]
    for i, name in enumerate(names, 1):
        out_path = OUT_DIR / f"annotator_{i}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(full_batch, f, ensure_ascii=False, indent=2)

    nc_total = sum(1 for t in full_batch if t["data"]["source"] == "non_crisis")
    cr_total = 200 - nc_total
    hi_total = sum(1 for r in new_chi + list({t["data"]["conversation_id"] for t in first40
                   if t["data"]["source"] == "crisis"}) if True)  # approx
    hi_exact = sum(1 for r in (new_chi) ) + sum(
        1 for t in first40 if t["data"]["source"] == "crisis"
    )
    print(f"\nAll 3 annotators now have identical 200-task files:")
    print(f"  Total: {len(full_batch)}  |  {nc_total} non_crisis / {cr_total} crisis")
    print(f"  New 160 breakdown: {len(new_nc)} NC  +  {len(new_chi)} crisis sev>=6  +  {len(new_clo)} crisis sev5")
    print(f"\nDone. Files written to: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
