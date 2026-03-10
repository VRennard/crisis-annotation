"""
Prepares Label Studio import files for 3 annotators.

Output:
  label_studio/annotator_1.json  -- 100 tasks (80 unique + 20 shared)
  label_studio/annotator_2.json  -- 100 tasks (80 unique + 20 shared)
  label_studio/annotator_3.json  -- 100 tasks (80 unique + 20 shared)
  label_studio/labeling_config.xml  -- paste this into Label Studio project settings

The 20 shared tasks let you compute inter-annotator agreement later.
"""

import json
import os
import random
from pathlib import Path

SEED = 42
UNIQUE_PER_ANNOTATOR = 60
SHARED = 40  # all 3 annotators see these
N_ANNOTATORS = 3
NEWRUN = Path("newrun")
OUT_DIR = Path("label_studio")

random.seed(SEED)


def load_conversations():
    records = []
    for json_path in NEWRUN.rglob("*.json"):
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        conv_id = json_path.stem  # e.g. conversation_1552551
        folder = json_path.parent.relative_to(NEWRUN).parts[0]  # crisis / non_crisis
        classification = data.get("classification", {})
        turns = data.get("conversation", [])

        # Flatten EDUs into readable text grouped by speaker turn
        text_lines = []
        current_speaker = None
        current_edus = []
        for turn in turns:
            for edu in turn.get("edus", []):
                spk = edu.get("speaker", "?")
                txt = edu.get("text", "").strip()
                if spk != current_speaker:
                    if current_edus:
                        text_lines.append(f"[{current_speaker}] " + " ".join(current_edus))
                    current_speaker = spk
                    current_edus = [txt]
                else:
                    current_edus.append(txt)
        if current_edus:
            text_lines.append(f"[{current_speaker}] " + " ".join(current_edus))

        conversation_text = "\n\n".join(text_lines)

        records.append({
            "id": conv_id,
            "folder": folder,
            "is_crisis_gt": classification.get("is_crisis"),
            "text": conversation_text,
        })

    return records


def to_ls_task(record):
    return {
        "data": {
            "conversation_id": record["id"],
            "source": record["folder"],
            "text": record["text"],
        }
    }


def main():
    OUT_DIR.mkdir(exist_ok=True)

    print("Loading conversations...")
    records = load_conversations()
    print(f"  Loaded {len(records)} conversations")

    # Shuffle and split
    random.shuffle(records)
    shared = records[:SHARED]
    remaining = records[SHARED:]

    batches = []
    for i in range(N_ANNOTATORS):
        start = i * UNIQUE_PER_ANNOTATOR
        unique = remaining[start: start + UNIQUE_PER_ANNOTATOR]
        batch = shared + unique
        random.shuffle(batch)
        batches.append(batch)

    for i, batch in enumerate(batches, 1):
        tasks = [to_ls_task(r) for r in batch]
        out_path = OUT_DIR / f"annotator_{i}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        print(f"  annotator_{i}.json — {len(tasks)} tasks")

    # Write labeling config
    config = """<View>
  <Style>
    .conversation-box {
      background: #f9f9f9;
      border: 1px solid #ddd;
      border-radius: 6px;
      padding: 16px;
      font-family: serif;
      font-size: 14px;
      line-height: 1.7;
      white-space: pre-wrap;
      max-height: 500px;
      overflow-y: auto;
    }
  </Style>

  <Text name="text" value="$text" className="conversation-box"/>

  <Header value="Is this a crisis-time conversation?"/>
  <Choices name="is_crisis" toName="text" choice="single" showInline="true" required="true">
    <Choice value="Yes"/>
    <Choice value="No"/>
  </Choices>

  <Header value="Severity / intensity (1 = no crisis at all, 10 = acute crisis)"/>
  <Rating name="rating" toName="text" maxRating="10" icon="star" size="medium" required="true"/>
</View>"""

    config_path = OUT_DIR / "labeling_config.xml"
    config_path.write_text(config, encoding="utf-8")
    print(f"  labeling_config.xml written")
    print(f"\nDone. Files are in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
