# Decision log

- Switched brand from sprintcare to AppleSupport after checking the uploaded file:
  sprintcare had exactly 1 usable row, AppleSupport had 13, the most of any brand in the
  93-row sample.

- Kept the raw uploaded file (`data/twcs_sample_raw.csv`) in the repo unmodified and
  built every downstream file from it.

- Noticed the 13 real AppleSupport rows are almost entirely about one real event (the
  2017 iOS 11.0.2 battery drain complaints), so 12 of them get the same intent label
  (`software_update_device_issue`) and only 1 covers a different intent (Apple ID / App
  Store code issue). Didn't force artificial diversity into the real data's labels —
  reported the imbalance honestly instead of hiding it.

- Split the 13 real rows 8-train / 5-golden rather than putting all 13 in training or all
  13 in eval. Putting all of them in training would mean the golden set has zero real
  examples; putting all of them in eval would mean the retrieval index (which is supposed
  to ground replies in real historical resolutions) has no real examples to draw from.
  8/5 keeps both goals partially served, and is disclosed as a trade-off in the README
  since with only 13 total real rows.

- The one real `apple_id_account_access` example went into the golden set, not training,
  even though this means that intent's retrieval grounding is 100% synthetic. Chose this
  because the golden set having zero real examples for an entire intent felt like a worse
  gap than the retrieval index missing one real template.

- Added a small similarity bonus (+0.05) for real rows in the retrieval ranking
  (`src/retrieve.py`), so that when a real and a synthetic template are close matches,
  the real one wins — retrieval-grounding should prefer actual historical brand behavior
  when available.

- Tuned the classifier's `min_df` and `class_weight` via 4-fold cross-validation on
  `train_pool.csv` only, before ever touching the golden set, and then evaluated exactly
  once on the golden set. The tuned config scored slightly worse on golden (77.3%) than
  an earlier untuned version (79.3%) despite scoring better in CV. Kept the CV-selected
  config anyway rather than reverting, because re-picking based on the golden-set number
  would be tuning on the test set, which defeats the point of having a held-out set at
  all. Documented the discrepancy instead of hiding it.

- Reported that the simple keyword-rule baseline (80.0%) narrowly beats the ML classifier
  (77.3%) on this golden set, rather than adjusting the taxonomy or golden set until the
  ML model won. At this data scale (88 training rows, 6 overlapping-vocabulary intents),
  this is a real and informative result, not a bug to be hidden.

- Broke out intent accuracy by data source (real / held-out synthetic / edge case)
  as a first-class metric in `eval/run_metrics.py`, not just an appendix note, because a
  single blended accuracy number would hugely overstate performance on the hard cases
  that matter most (edge cases score 55.6% vs 100% on the tiny real sample).

- Built the golden eval set out of three explicitly tagged sources (held-out synthetic,
  edge cases, real) instead of one undifferentiated pool, specifically so source-level
  breakdowns would be possible later without re-labeling anything.

- Deliberately wrote edge cases that could trip up the escalation policy in both
  directions: false negatives (account takeover phrased as "someone changed my password"
  without the word "hack", which the keyword-based risk check misses) and false positives
  (a compliment or routine how-to question the classifier is uncertain about, which
  triggers the low-confidence auto-escalation rule). Both show up in the human-scored
  sample and are called out honestly rather than cherry-picking cases that flatter the
  policy.