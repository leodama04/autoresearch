A zero-shot language model evaluation using BPB (Batch Processing Benchmark) metric.

## How to run

```bash
uv run prepare.py
# Data and tokenizer are already set up
# Then run training:
uv run train.py
```

## Results

Results are saved to `results.tsv`:
- val_bpb: The batch processing benchmark score
- memory_gb: Peak memory usage in GB
- status: keep, discard, or crash

## Training hyperparameters

- Time budget: 5 minutes
- Sequence length: Configured in train.py
- Batch size: Configured in train.py

## License

See LICENSE file.