# iba-blindsight-guard

**BlindSight-ready. Vision restored. Intent enforced.**

Neuralink’s Blindsight (and competing vision-restoration BCI systems) can decode camera input, stimulate the visual cortex, and generate phosphenes for sight restoration — even in people born blind.

This tool adds real cryptographic governance at the neural layer.

Every vision-related neural command (decode → stimulate → phosphene navigation) must respect a signed **IBA Intent Certificate** from a licensed clinician.

## Features
- Vision-specific IBA scopes (decode/stimulate/phosphene/nav only)
- Hard-denied exports, streams, and overrides
- Clinician-interval + kill_threshold enforcement (patient-first boundary)
- Optional safe hollowing of sensitive neural patterns
- Works with any vision-restoration BCI (Neuralink Blindsight, Science Corp PRIMA, cortical implants, etc.)

## Patent & Filings
- **Patent Pending**: GB2603013.0 (filed 5 Feb 2026, PCT route open — 150+ countries)
- **NIST Docket**: NIST-2025-0035 (13 IBA filings)
- **NCCoE Filings**: 10 submissions on AI agent authorization

## Quick Start
```bash
git clone https://github.com/Grokipaedia/iba-blindsight-guard.git
cd iba-blindsight-guard
pip install -r requirements.txt
python guard.py "decode-camera-stimulate-phosphene-navigate" --hollow medium
