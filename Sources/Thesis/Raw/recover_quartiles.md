---
created: 2026-04-20
source_filename: "recover_quartiles.py"
file_type: py
tags: [thesis-code, event-study, quartiles, recovery, pipeline-crash, duplicate]
---

# recover_quartiles.py — Re-run Quartile Assignment (Raw/ copy)

*Duplicate of [[recover_quartiles]] in Sources/Thesis/Notes/.*

Re-runs only the earnings surprise and velocity quartile assignment step of the event study pipeline after a crash. Avoids re-processing the full build_event_study.py pipeline.

See [[recover_quartiles]] for full annotation.

## Key Concepts
- [[Post-Earnings Announcement Drift]]
- [[Sentiment Velocity]]
