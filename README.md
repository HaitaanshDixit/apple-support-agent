# AppleSupport AI Agent

An intent classifier + grounded reply drafter + escalation policy for the `@AppleSupport`
brand, built from a real (if small) slice of the Customer Support on Twitter dataset.

## About the data (read this first)

Given the dataset `data/twcs_sample_raw.csv`, a 93-row slice of the real
`thoughtvector/customer-support-on-twitter` dataset (correct schema, real tweets).
The `AppleSupport`, slice of dataset which has the most coverage in this file: **13 real reply pairs**, almost all from the well-documented 2017 iOS 11.0.2 battery-drain backlash, plus one real "App Store verification code never arrives" case.

13 real examples is not enough on its own to train a classifier or fill a 150-example
golden set, so this repo is built in three honest layers:

1. **Real data** (`data/twcs_sample_raw.csv` -> `data/apple_support_real_pairs.csv` ->
   `data/apple_real_labeled.csv`): all 13 real AppleSupport reply pairs, hand-labeled by
   me with intent. 8 go into the training/retrieval pool (so the agent's replies for
   software-update and Apple ID issues are grounded in genuine historical AppleSupport
   phrasing), 5 are held out into the golden eval set untouched by training.
2. **Synthetic data** (`data/make_synthetic_corpus.py`): 180 constructed examples across
   6 intents, written in the same style as the real data (informal tweet, diagnostic
   question + "DM us" reply), needed for training volume and for 2 intents the real
   sample has zero examples of (billing disputes, hardware damage, how-to questions,
   compliments). This is disclosed, not hidden.
3. **Hand-written edge cases** (`data/edge_cases.csv`): 45 harder cases targeting the
   escalation policy specifically (fraud, account takeover, safety hazards, compound
   intents, compliments that could be misread as complaints).

The golden eval set is real + synthetic-held-out + edge cases, **with the source of each
row tagged** in `eval/golden_eval.csv` and metrics broken out by source in
`eval/run_metrics.py`, so you can always see how much of any headline number rests on the
5 genuinely real examples vs. constructed ones.

## What's in the box

- `data/twcs_sample_raw.csv` — the raw file you uploaded, kept as-is
- `data/extract_real_pairs.py` — pulls the 13 real AppleSupport reply pairs out of it
- `data/label_real_pairs.py` — hand-assigns intent + train/golden split to those 13
- `data/make_synthetic_corpus.py` — builds the 180-row synthetic corpus (6 intents)
- `data/edge_cases.csv` — 45 hand-written hard/ambiguous/risk cases
- `data/make_split.py` — combines real + synthetic into `train_pool.csv` (88 rows: 8 real
  + 80 synthetic) and `held_out_pool.csv` (100 synthetic rows never seen by the model)
- `eval/build_golden.py` — builds `eval/golden_eval.csv` (150 rows: 100 held-out
  synthetic + 45 edge cases + 5 real), each with a hand-reviewed gold intent and gold
  escalation label
- `src/classify.py` — TF-IDF + logistic regression intent classifier (hyperparameters
  chosen via cross-validation on `train_pool.csv` only, never on the golden set)
- `src/retrieve.py` — TF-IDF nearest-neighbor retrieval over the training pool, with a
  small similarity bonus for real rows so genuine historical resolutions are preferred
  when relevant
- `src/escalate.py` — rule-based escalation policy
- `src/draft_reply.py` — drafts a reply from the retrieved historical resolution;
  optionally rewrites it with Claude if `ANTHROPIC_API_KEY` is set (headline numbers do
  NOT depend on having a key)
- `src/pipeline.py` — glues classify -> escalate -> draft together, CLI entry point
- `eval/baselines.py` — trivial (majority class) and simple (keyword rules) baselines
- `eval/run_metrics.py` — intent + escalation metrics vs baselines, broken out by data
  source
- `eval/judge.py` — reply-quality rubric judge (LLM-backed if key present, heuristic
  fallback otherwise)
- `eval/run_replies.py` — runs the pipeline over the golden set and scores replies
- `eval/sample_for_judge.py` — deterministically samples 30 pipeline outputs
- `eval/human_scores.csv`, `eval/judge_agreement.py` — my own manual 0-5 ratings on that
  30-example subsample, read for actual semantic correctness, and the agreement
  calculation against the judge
- `DECISION_LOG.md` — the non-obvious calls made along the way

## Reproduce in under 15 minutes

```bash
pip install -r requirements.txt --break-system-packages
bash run_all.sh
```

This re-extracts the real pairs, rebuilds the synthetic corpus and splits, rebuilds the
golden set, trains the classifier, builds the retrieval index, and prints/saves every
metric. Takes well under a minute on a laptop. No API key required.

Try a single message through the pipeline:

```bash
python3 -m src.pipeline --text "@AppleSupport my battery drains so fast since the new update, its unusable"
```

Turn on LLM-drafted replies and an LLM judge (optional, requires `ANTHROPIC_API_KEY`):

```bash
python3 -m src.pipeline --text "..." --use_llm
```

## Headline numbers (all with the honest caveats above)

- Intent accuracy on golden set (150 examples): 77.3%, vs 17.3% trivial baseline. The
  simple keyword-rule baseline actually edges it out slightly (80.0%) — see
  `DECISION_LOG.md` for why I kept the ML model anyway and didn't p-hack the eval set.
- Intent accuracy by source: **100% on the 5 real examples**, 86.0% on held-out
  synthetic, 55.6% on hand-written edge cases — a big spread that a single blended number
  hides.
- Escalation policy: 86.4% recall, 28.8% precision, 66.7% accuracy — tuned for recall on
  risk cases at the cost of over-escalating.
- Average heuristic reply-quality judge score: 4.28 / 5 — but see below.
- Judge-vs-human agreement on a 30-example subsample I hand-scored: **weak** (Cohen's
  kappa = 0.0, Pearson r = 0.06, not significant). The judge is fooled by surface
  features like the presence of the word "DM"; it does not catch cases where the reply
  is confidently on-brand but about the wrong topic (e.g. a compliment tweet gets
  answered with a battery-troubleshooting question). This is the single biggest thing to
  fix next, and it's why the 4.28/5 number should not be read as "the replies are good."
