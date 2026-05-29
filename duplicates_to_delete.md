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

---

## BATCH 3 — 127 files deleted 2026-05-29


### ENCODING (24 files)
| Deleted | Kept | Folder |
|---------|------|--------|
| `conversation_22381` | `conversation_1552839` | `crisis/5` |
| `conversation_22567` | `conversation_1553300` | `crisis/6` |
| `conversation_22400` | `conversation_1552899` | `crisis/6` |
| `conversation_22573` | `conversation_1553324` | `crisis/5` |
| `conversation_22488` | `conversation_1553121` | `crisis/6` |
| `conversation_22428` | `conversation_1552953` | `crisis/7` |
| `conversation_22496` | `conversation_1553134` | `crisis/6` |
| `conversation_22598` | `conversation_1553402` | `non_crisis` |
| `conversation_22560` | `conversation_1553275` | `crisis/6` |
| `conversation_22566` | `conversation_1553295` | `crisis/5` |
| `conversation_22352` | `conversation_1552756` | `non_crisis` |
| `conversation_22457` | `conversation_1553020` | `crisis/7` |
| `conversation_1553022a` | `conversation_22458` | `crisis/5` |
| `conversation_22498` | `conversation_1553138` | `crisis/7` |
| `conversation_22582` | `conversation_1553347` | `crisis/5` |
| `conversation_22583` | `conversation_1553348` | `crisis/7` |
| `conversation_22328` | `conversation_1552733` | `crisis/5` |
| `conversation_22404` | `conversation_1552905` | `crisis/7` |
| `conversation_22550` | `conversation_1553258` | `crisis/5` |
| `conversation_691` | `conversation_1552384` | `crisis/8` |
| `conversation_22403` | `conversation_1552901` | `crisis/6` |
| `conversation_718` | `conversation_1552411` | `crisis/5` |
| `conversation_22503` | `conversation_1553148` | `crisis/6` |
| `conversation_22494` | `conversation_1553131` | `crisis/7` |

### FOOTNOTES (66 files)
| Deleted | Kept | Folder |
|---------|------|--------|
| `conversation_22620` | `conversation_1553476` | `crisis/8` |
| `conversation_22615` | `conversation_1553442` | `crisis/5` |
| `conversation_22461` | `conversation_1553029` | `crisis/8` |
| `conversation_22497` | `conversation_1553133` | `crisis/7` |
| `conversation_22362` | `conversation_1552792` | `crisis/5` |
| `conversation_22474` | `conversation_1553078` | `crisis/6` |
| `conversation_22345` | `conversation_1552751` | `crisis/5` |
| `conversation_22572` | `conversation_1553323` | `crisis/6` |
| `conversation_22439` | `conversation_1552979` | `crisis/5` |
| `conversation_22460` | `conversation_1553027` | `crisis/7` |
| `conversation_22459` | `conversation_1553026` | `crisis/8` |
| `conversation_22555` | `conversation_1553273` | `crisis/5` |
| `conversation_22441` | `conversation_1552984` | `non_crisis` |
| `conversation_22447` | `conversation_1552995` | `crisis/7` |
| `conversation_22584` | `conversation_1553350` | `crisis/6` |
| `conversation_22329` | `conversation_1552732` | `crisis/7` |
| `conversation_22363` | `conversation_1552796` | `crisis/6` |
| `conversation_22349` | `conversation_1552754` | `crisis/7` |
| `conversation_22636` | `conversation_1553567` | `crisis/6` |
| `conversation_22485` | `conversation_1553118` | `crisis/6` |
| `conversation_22398` | `conversation_1552896` | `crisis/7` |
| `conversation_22587` | `conversation_1553371` | `crisis/5` |
| `conversation_22578` | `conversation_1553334` | `crisis/6` |
| `conversation_22373` | `conversation_1552816` | `crisis/6` |
| `conversation_22424` | `conversation_1552941` | `crisis/6` |
| `conversation_22475` | `conversation_1553082` | `crisis/6` |
| `conversation_22525` | `conversation_1553201` | `crisis/7` |
| `conversation_22581` | `conversation_1553346` | `crisis/6` |
| `conversation_22359` | `conversation_1552785b` | `crisis/7` |
| `conversation_22322` | `conversation_1552715` | `crisis/7` |
| `conversation_22297` | `conversation_1552646` | `crisis/7` |
| `conversation_22377` | `conversation_1552831` | `non_crisis` |
| `conversation_22608` | `conversation_1553423` | `crisis/6` |
| `conversation_22269` | `conversation_1552617` | `crisis/8` |
| `conversation_22399` | `conversation_1552897` | `crisis/6` |
| `conversation_22387` | `conversation_1552856` | `crisis/7` |
| `conversation_1552394` | `conversation_701` | `crisis/7` |
| `conversation_22469` | `conversation_1553050` | `crisis/8` |
| `conversation_22493` | `conversation_1553129` | `crisis/7` |
| `conversation_22580` | `conversation_1553340` | `crisis/7` |
| `conversation_22301` | `conversation_1552661` | `crisis/6` |
| `conversation_22425` | `conversation_1552946` | `crisis/7` |
| `conversation_1552373` | `conversation_680` | `crisis/6` |
| `conversation_22487` | `conversation_1553122` | `crisis/7` |
| `conversation_700` | `conversation_1552393` | `crisis/7` |
| `conversation_22500` | `conversation_1553140` | `crisis/6` |
| `conversation_1552376` | `conversation_683` | `crisis/7` |
| `conversation_22331` | `conversation_1552734` | `crisis/7` |
| `conversation_1552408` | `conversation_715` | `crisis/6` |
| `conversation_22299` | `conversation_1552653` | `crisis/7` |
| `conversation_22597` | `conversation_1553403` | `crisis/5` |
| `conversation_22291` | `conversation_1552635` | `crisis/7` |
| `conversation_22523` | `conversation_1553198` | `crisis/7` |
| `conversation_22385` | `conversation_1552845` | `non_crisis` |
| `conversation_22211` | `conversation_1552561` | `crisis/6` |
| `conversation_22543` | `conversation_1553241` | `crisis/7` |
| `conversation_22339` | `conversation_1552747` | `crisis/6` |
| `conversation_22263` | `conversation_1552616` | `crisis/7` |
| `conversation_1552383` | `conversation_690` | `crisis/9` |
| `conversation_22004` | `conversation_22007` | `crisis/7` |
| `conversation_22261` | `conversation_1552612` | `crisis/7` |
| `conversation_22484` | `conversation_1553114` | `crisis/6` |
| `conversation_22512` | `conversation_1553168` | `crisis/7` |
| `conversation_22509` | `conversation_1553155` | `crisis/7` |
| `conversation_1553422` | `conversation_22606` | `crisis/8` |
| `conversation_22517` | `conversation_1553182` | `crisis/5` |

### OMISSION (37 files)
| Deleted | Kept | Folder |
|---------|------|--------|
| `conversation_22317` | `conversation_1552699` | `crisis/7` |
| `conversation_22516` | `conversation_1553173` | `crisis/6` |
| `conversation_22501` | `conversation_1553142` | `crisis/5` |
| `conversation_22397` | `conversation_1552893` | `crisis/6` |
| `conversation_22427` | `conversation_1552949` | `crisis/7` |
| `conversation_22449` | `conversation_1552996` | `crisis/7` |
| `conversation_22575` | `conversation_1553325` | `crisis/7` |
| `conversation_22506` | `conversation_1553152 (2)` | `crisis/7` |
| `conversation_22417` | `conversation_1552923` | `crisis/7` |
| `conversation_22337` | `conversation_1552746` | `crisis/7` |
| `conversation_22396` | `conversation_1552892a` | `crisis/7` |
| `conversation_22426` | `conversation_1552947` | `crisis/5` |
| `conversation_22390` | `conversation_1552864` | `crisis/7` |
| `conversation_22354` | `conversation_1552768b` | `crisis/5` |
| `conversation_22595` | `conversation_1553400` | `crisis/5` |
| `conversation_22473` | `conversation_1553076a` | `crisis/5` |
| `conversation_22579` | `conversation_1553335` | `crisis/6` |
| `conversation_22452` | `conversation_1553004` | `crisis/7` |
| `conversation_22450` | `conversation_1553003` | `crisis/7` |
| `conversation_22537` | `conversation_1553223` | `crisis/5` |
| `conversation_22533` | `conversation_1553211b` | `crisis/7` |
| `conversation_22412` | `conversation_1552912` | `crisis/5` |
| `conversation_22556` | `conversation_1553274` | `crisis/5` |
| `conversation_22448` | `conversation_1552998` | `crisis/7` |
| `conversation_22552` | `conversation_1553263` | `crisis/5` |
| `conversation_22482` | `conversation_1553109` | `crisis/7` |
| `conversation_22342` | `conversation_1552749` | `crisis/7` |
| `conversation_22542` | `conversation_1553241` | `crisis/7` |
| `conversation_22559` | `conversation_1553276` | `crisis/5` |
| `conversation_22444` | `conversation_1552988` | `crisis/7` |
| `conversation_22384` | `conversation_1552844` | `crisis/7` |
| `conversation_22370` | `conversation_1552805` | `crisis/7` |
| `conversation_22365` | `conversation_1552798` | `crisis/5` |
| `conversation_22462` | `conversation_1553033 (2)` | `crisis/7` |
| `conversation_22548` | `conversation_1553259` | `crisis/5` |
| `conversation_22374` | `conversation_1552822` | `crisis/6` |
| `conversation_22408` | `conversation_1552907` | `crisis/6` |