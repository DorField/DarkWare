# DarkWare

Physics-based classifier using the Blume-Capel lattice.
49 lines. 20 bytes per class. Zero training. Beats kNN on 76% of benchmarks.

## Quick start

```python
python darkware_minimal.py

Normal → Normal 99% OK
Misalign → Misalign 99% OK
Imbalance → Imbalance 99% OK
...
8/8 correct

  • Iris: 92% (sklearn, 150 samples)
	•	37 benchmarks: 76% win+tie vs sklearn kNN
	•	104 IBM quantum jobs: p₀=0.052 matches theory 0.051
	•	Model: 20 bytes per class
	•	Inference: 0.13ms on ESP32
Paper
https://doi.org/10.5281/zenodo.20020136
License
MIT
© 2026 Dor Pinchas, Dor Field Technologies
