#!/bin/bash
set -e
pip install -q -r requirements.txt --break-system-packages
python3 data/extract_real_pairs.py
python3 data/label_real_pairs.py
python3 data/make_synthetic_corpus.py
python3 data/make_split.py
python3 eval/build_golden.py
python3 src/classify.py
python3 src/retrieve.py
python3 -m eval.run_metrics
python3 -m eval.run_replies
python3 -m eval.sample_for_judge
python3 -m eval.judge_agreement
echo "done. see eval/metrics_summary.json and eval/pipeline_outputs.csv"
