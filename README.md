# Crisis Project — Conversation Metrics

This file describes every column in `conversation_metrics.csv`.
Each row represents one conversation extracted from the `newrun/` JSON files.

---

## Identification

| Column | Description |
|--------|-------------|
| `conversation_id` | Sequential integer ID assigned to each row (1 to N). |
| `crisis_type` | Category of crisis involved (e.g., `Diplomatic`, `Military/Security`, `Economic/Financial`). Multiple types are comma-separated. Set to `None` for non-crisis conversations. |
| `severity` | Crisis severity level (integer, observed range 3–9). Higher values indicate more severe crises. Empty for conversations with no severity rating. |
| `crisis_validated` | Boolean (`True`/`False`). Whether the conversation was confirmed as a genuine crisis by the primary validation pass. Rows where this is `False` were flagged for a GPT recheck (see `conv_*` columns below). |

---

## Basic Conversation Structure

| Column | Description |
|--------|-------------|
| `median_turns` | Median number of speaking turns per speaker across the conversation. |
| `median_words` | Median number of words per Elementary Discourse Unit (EDU). |
| `n_speakers` | Number of unique speakers in the conversation. |

---

## Turn Complexity

| Column | Description |
|--------|-------------|
| `words_per_turn_median` | Median word count per speaking turn (a turn groups consecutive EDUs from the same speaker). |
| `type_token_ratio` | Lexical diversity: number of unique words divided by total words. Higher = more varied vocabulary. Range: 0–1. |
| `sentence_length_stdev` | Standard deviation of sentence lengths (in words) across all EDUs. Higher = more variable sentence structure. |

---

## Speaker Dominance

These metrics measure how evenly distributed speaking turns are across participants.

| Column | Description |
|--------|-------------|
| `dominance_pct` | Percentage of total turns taken by the most active speaker. |
| `fair_share_pct` | Expected turn percentage if all speakers participated equally (= 100 / n_speakers). |
| `dominance_ratio` | `dominance_pct / fair_share_pct`. A value of 1.0 means perfectly equal participation; higher values indicate one speaker dominating. |
| `dominance_ratio_first_third` | Dominance ratio computed over only the first third of turns. |
| `dominance_ratio_last_third` | Dominance ratio computed over only the last third of turns. |
| `dominance_ratio_delta` | Change in dominance ratio from first to last third (`last − first`). Positive = increasing dominance over time; negative = more balanced toward the end. |

---

## Discourse Patterns

| Column | Description |
|--------|-------------|
| `questions_per_turn` | Average number of question marks per speaking turn. |
| `imperatives_per_100w` | Frequency of imperative sentences (commands/directives) per 100 words. Detected by sentence-initial imperative verbs (e.g., *Tell*, *Consider*, *Stop*). |

---

## Linguistic Indicators (per 100 words)

All values are counts of matching words or phrases normalized to a rate per 100 words.

| Column | Keywords / Patterns | Description |
|--------|---------------------|-------------|
| `hedging_per_100w` | *perhaps, maybe, possibly, probably, somewhat, rather, quite, fairly, slightly* | Frequency of hedging language — expressions of uncertainty or tentativeness. |
| `certainty_per_100w` | *definitely, certainly, clearly, obviously, absolutely, surely, undoubtedly* | Frequency of certainty markers — expressions of confidence or assertion. |
| `crisis_kw_per_100w` | *crisis, emergency, urgent, immediate, critical, threat, attack, war, conflict, violence, disaster, catastrophe, danger, risk, terror, deadline, pressure, escalate, deteriorate* | Frequency of crisis-related vocabulary. |
| `first_person_per_100w` | *I, me, my, mine, we, us, our, ours* | Frequency of first-person pronouns, indicating self-reference or group identity. |
| `modals_per_100w` | *could, should, would, might, may, can, will, must, shall* | Frequency of modal verbs, associated with possibility, obligation, and conditionality. |

---

## Discourse Graph Relations

Computed from RST (Rhetorical Structure Theory) relation graphs stored in `Crisis_graphs/`. Empty if no graph file was available for a conversation.

| Column | Description |
|--------|-------------|
| `elaboration_prop` | Proportion of relations labelled `Elaboration` (adding detail to a prior unit). |
| `contrast_prop` | Proportion of relations labelled `Contrast` (opposing or comparing units). |
| `qap_clarification_prop` | Combined proportion of `Question-answer_pair` and `Clarification_question` relations. |
| `relation_entropy` | Shannon entropy over all relation type counts. Higher = more diverse mix of discourse relations; lower = dominated by one relation type. |
| `elab_chain_diameter` | Length of the longest chain of consecutive `Elaboration` edges in the discourse graph (DAG longest path). Reflects how deeply an idea is developed. |

---

## Discourse Trajectory (First vs. Last Third)

These metrics capture how the discourse structure *changes* over the course of the conversation by comparing the first third of EDUs to the last third.

| Column | Description |
|--------|-------------|
| `traj_elaboration_delta` | Change in `Elaboration` relation proportion from first to last third. Positive = more elaboration toward the end. |
| `traj_continuation_delta` | Change in `Continuation` relation proportion from first to last third. |
| `traj_acknowledgement_delta` | Change in `Acknowledgement` relation proportion from first to last third. |
| `traj_comment_delta` | Change in `Comment` relation proportion from first to last third. |

---

## GPT Recheck Fields

These columns are populated only for conversations where `crisis_validated = False` (approximately 260 rows). A secondary GPT pass re-examined those conversations to catch false negatives — cases initially flagged as non-crisis that might still warrant a crisis label.

| Column | Description |
|--------|-------------|
| `conv_is_crisis_recheck` | Boolean (`True`/`False`). GPT's re-assessment of whether the conversation qualifies as a crisis. `True` means the recheck overturns the initial non-crisis verdict. Most `crisis_validated = True` rows leave this empty; a small number (~34) were rechecked regardless and confirmed. |
| `conv_crisis_type` | Crisis category assigned by the recheck GPT pass. Uses the same taxonomy as `crisis_type` (e.g., `Diplomatic`, `Military`, `Economic / Diplomatic`). Set to `Routine` for conversations the recheck also confirms as non-crisis. |
| `conv_confidence` | GPT's stated confidence in the recheck judgment. Observed value is always `high`; the field is reserved for future multi-level confidence scoring. |
| `conv_reason` | Free-text explanation produced by the GPT recheck, summarising why the conversation was or was not classified as a crisis. Describes urgency signals, topic, and geopolitical context. Rare `ERROR: ...` values indicate a failed API call for that row. |

---

## Notes

- **EDU**: Elementary Discourse Unit — the basic segment of text used for discourse analysis (roughly a clause or short sentence).
- **Graph metrics** are empty (`""`) for conversations where no matching `.txt` graph file exists in `Crisis_graphs/`.
- The original conversation IDs (before sequential renaming) are preserved in `conversation_metrics_backup.csv`.
