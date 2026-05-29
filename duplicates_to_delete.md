# Duplicate Files — Deletion Log

Generated: 2026-05-29
Scope: `newrun/crisis/` and `newrun/non_crisis/`
Method: MD5 exact match + 4-gram Jaccard + speaker-stripped fingerprint

---

## BATCH 1 — 13 files deleted 2026-05-29

### TRUNCATION (2 files)
| Deleted | Kept | Reason |
|---------|------|--------|
| `newrun/crisis/7/conversation_1552785a.json` | `newrun/crisis/7/conversation_1552785b.json` | `a` is a cut-off prefix of `b` (140w vs 577w) |
| `newrun/crisis/8/conversation_1553044.json` | `newrun/crisis/8/conversation_1552384.json` | Near-identical (94%), "every one" vs "everyone" |

### FOOTNOTES / DASH ENCODING (5 files)
`22xxx` versions had superscript footnote numbers (`hearings3`, `cambodia.3`) and/or dash encoding noise baked into text.
| Deleted | Kept | Reason |
|---------|------|--------|
| `newrun/crisis/5/conversation_22410.json` | `newrun/crisis/5/conversation_1552906.json` | Footnotes embedded |
| `newrun/crisis/7/conversation_22306.json` | `newrun/crisis/7/conversation_1552667.json` | Footnotes + dash noise |
| `newrun/crisis/7/conversation_22420.json` | `newrun/crisis/7/conversation_1552931.json` | Footnotes + dash noise |
| `newrun/crisis/5/conversation_22599.json` | `newrun/crisis/5/conversation_1553405.json` | Dash encoding noise |
| `newrun/crisis/6/conversation_22534.json` | `newrun/crisis/6/conversation_1553212.json` | Dash encoding noise |

### OMISSION MARKERS (6 files)
`22xxx` versions had `[omitted here is discussion of X]` markers, making them incomplete.
| Deleted | Kept | Reason |
|---------|------|--------|
| `newrun/crisis/5/conversation_22551.json` ⚠️ | `newrun/crisis/6/conversation_1553259.json` | Had `[omitted]` markers (cross-folder) |
| `newrun/crisis/6/conversation_22391.json` ⚠️ | `newrun/crisis/6/conversation_1552865.json` | Had `[omitted]` markers |
| `newrun/crisis/6/conversation_22586.json` | `newrun/crisis/6/conversation_1553370.json` | Had `[omitted]` markers |
| `newrun/crisis/7/conversation_22358.json` | `newrun/crisis/7/conversation_1552782.json` | Had `[omitted]` markers |
| `newrun/crisis/7/conversation_22601.json` | `newrun/crisis/7/conversation_1553404.json` | Had `[omitted]` markers |
| `newrun/crisis/7/conversation_22603.json` | `newrun/crisis/7/conversation_1553410.json` | Had `[omitted]` markers |

⚠️ = was in Label Studio queue (0 annotations) → swapped to full version before deletion.

---

## BATCH 2 — 4 files deleted 2026-05-29

### FOOTNOTES (2 files)
| Deleted | Kept | Reason |
|---------|------|--------|
| `newrun/crisis/5/conversation_22454.json` | `newrun/crisis/5/conversation_1553011.json` | Footnotes (`directive.2`, `mi6.3`) in `22454` |
| `newrun/crisis/7/conversation_22451.json` | `newrun/crisis/7/conversation_1553006.json` | Footnotes + dash noise in `22451`; same ending |

### ENCODING ARTIFACT + OMISSION (2 files)
| Deleted | Kept | Reason |
|---------|------|--------|
| `newrun/non_crisis/conversation_1553233.json` | `newrun/non_crisis/conversation_22539.json` | `1553233` has garbled unicode (`land\x84scape`) |
| `newrun/non_crisis/conversation_22633.json` ⚠️ | `newrun/non_crisis/conversation_1553554.json` | `22633` has `[omitted]` markers |

⚠️ = was in Label Studio queue (0 annotations) → swapped to full version before deletion.

---

## Kept — Pending Your Decision

| Pair | Issue |
|------|-------|
| `crisis/5/conversation_22383.json` vs `non_crisis/conversation_1552841.json` | Same conversation with **conflicting labels** (one crisis, one non_crisis) — same ending, minor dash diff. Decide which label is correct and delete the other. |
| `crisis/6/conversation_1553260.json` vs `crisis/6/conversation_22549.json` | Identical opening 347 words, then completely different second half — likely different conversations, keeping both. |
