# Duplicate Files to Delete

Generated: 2026-05-29
Scope: `newrun/crisis/` and `newrun/non_crisis/`
Method: MD5 exact match + 4-gram Jaccard + speaker-stripped fingerprint

---

## 13 Confirmed Deletions

For each pair, the file to DELETE is listed with the reason.

### TRUNCATION (2 files)

| Delete | Keep | Reason |
|--------|------|--------|
| `newrun/crisis/7/conversation_1552785a.json` | `newrun/crisis/7/conversation_1552785b.json` | `a` is a cut-off prefix of `b` (140w vs 577w, identical opening) |
| `newrun/crisis/8/conversation_1553044.json` | `newrun/crisis/8/conversation_1552384.json` | Near-identical (94%), only "every one" vs "everyone" — keep longer |

### FOOTNOTES / DASH ENCODING (5 files)
The `22xxx` versions have superscript footnote numbers baked into text (`hearings3`, `cambodia.3`, etc.) and/or dash encoding noise (`--` vs em-dash). The `155xxxx` versions are the clean source.

| Delete | Keep | Reason |
|--------|------|--------|
| `newrun/crisis/5/conversation_22410.json` | `newrun/crisis/5/conversation_1552906.json` | Footnotes embedded in B (`hearings3`, `bill,4`) |
| `newrun/crisis/7/conversation_22306.json` | `newrun/crisis/7/conversation_1552667.json` | Footnotes + dash encoding noise; same ending |
| `newrun/crisis/7/conversation_22420.json` | `newrun/crisis/7/conversation_1552931.json` | Footnotes (`cambodia.3`) + dash noise; same ending |
| `newrun/crisis/5/conversation_22599.json` | `newrun/crisis/5/conversation_1553405.json` | Dash encoding noise only; same ending |
| `newrun/crisis/6/conversation_22534.json` | `newrun/crisis/6/conversation_1553212.json` | Dash encoding noise only; same ending |

### OMISSION MARKERS (6 files)
These `22xxx` files contain `[omitted here is discussion of X]` redaction markers, making them shorter/incomplete versions. The `155xxxx` counterpart has the full text.

| Delete | Keep | Reason |
|--------|------|--------|
| `newrun/crisis/5/conversation_22551.json` ⚠️ | `newrun/crisis/6/conversation_1553259.json` | A has `[omitted]` markers; B is the full version (cross-folder) |
| `newrun/crisis/6/conversation_22391.json` ⚠️ | `newrun/crisis/6/conversation_1552865.json` | B has `[omitted]` markers; A is the full version |
| `newrun/crisis/6/conversation_22586.json` | `newrun/crisis/6/conversation_1553370.json` | B has `[omitted]` markers; A is the full version |
| `newrun/crisis/7/conversation_22358.json` | `newrun/crisis/7/conversation_1552782.json` | B has `[omitted]` markers; A is the full version |
| `newrun/crisis/7/conversation_22601.json` | `newrun/crisis/7/conversation_1553404.json` | B has `[omitted]` markers; A is the full version |
| `newrun/crisis/7/conversation_22603.json` | `newrun/crisis/7/conversation_1553410.json` | B has `[omitted]` markers; A is the full version |

⚠️ = loaded in Label Studio but **not yet annotated** — safe to replace/remove from task queue.

---

## 3 Pairs Requiring Manual Review

| Pair | Issue |
|------|-------|
| `crisis/5/conversation_1553011.json` vs `crisis/5/conversation_22454.json` | Same convo, different redaction style: `[redacted]` vs `[1? lines not declassified]` |
| `crisis/7/conversation_1553006.json` vs `crisis/7/conversation_22451.json` | Footnotes + dash noise throughout, but different ending — verify same convo |
| `crisis/6/conversation_1553260.json` vs `crisis/6/conversation_22549.json` | Identical opening 347 words, then completely different second half — may be legitimately different conversations |

---

## Label Studio Status

- `conversation_1552785a` — in Label Studio (all 3 annotators), **0 annotations done**
- `conversation_22391` — in Label Studio (all 3 annotators), **0 annotations done**
- All other 11 files to delete: not in Label Studio

Action needed: replace `1552785a` → `1552785b` and `22391` → `1552865` in Label Studio task queues before deleting.
