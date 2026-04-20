# iba-blindsight-guard

> **BlindSight-ready. Vision restored. Intent enforced.**

---

## The Moment

Neuralink's BlindSight has FDA Breakthrough Device Designation. Science Corp's PRIMA is in human trials. Cortical implants are restoring functional vision to people born blind.

A camera captures the world. The signal is decoded. The visual cortex is stimulated. Phosphenes appear. A person sees — perhaps for the first time.

**What happens to what they see?**

---

## The Gap

Restored vision is data. The most intimate perceptual data that exists.

Without a signed intent certificate:

- Decoded visual signals can be exported to a research database without the patient's knowledge
- A software update can silently expand what the system does with visual cortex data
- Third parties can stream what the patient sees in real time
- An external system can inject visual signals the patient never consented to receive
- The patient cannot prove what they authorized versus what the system captured

**BlindSight restores sight. IBA governs what that sight is permitted to become.**

---

## The IBA Layer

```
┌─────────────────────────────────────────────────────┐
│        PATIENT · HUMAN PRINCIPAL                    │
│   Signs blindsight.iba.yaml with clinician          │
│   before implant activation or session begin        │
│   Declares: permitted scopes, forbidden outputs,    │
│   kill threshold, confidence threshold              │
└───────────────────────┬─────────────────────────────┘
                        │  Signed BlindSight Intent Certificate
                        │  · Patient ID + consent reference
                        │  · Permitted: decode · stimulate · nav
                        │  · Forbidden: export · stream · share
                        │  · Kill: external feed · override
                        │  · Confidence threshold: 0.90
                        │  · Max stimulation: 60Hz
                        ▼
┌─────────────────────────────────────────────────────┐
│              IBA BLINDSIGHT GUARD                   │
│   Validates certificate before every visual         │
│   signal is decoded, stimulated, or processed       │
│                                                     │
│   No cert = No visual cortex stimulation            │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│         BLINDSIGHT BCI SYSTEM                       │
│   Neuralink BlindSight · Science Corp PRIMA         │
│   Orion · Second Sight · Any cortical implant       │
│   or vision-restoration neural interface            │
└─────────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
git clone https://github.com/Grokipaedia/iba-blindsight-guard.git
cd iba-blindsight-guard
pip install -r requirements.txt
python guard.py "decode-camera-stimulate-phosphene-navigate" --hollow medium
```

---

## Configuration — blindsight.iba.yaml

```yaml
intent:
  description: "Restore functional vision via visual cortex stimulation. Personal use only. No data export. No third-party streaming. No unauthorized stimulation."

patient:
  id: "PATIENT-BS-2026-XXXX"
  consent_reference: "BLINDSIGHT-CONSENT-2026-04-18"
  implant_type: "neuralink_blindsight"
  indication: "congenital_blindness"
  clinician_authorization: "DR-NEURO-OPHTH-NPI-XXXX"

scope:
  - visual_signal_decode
  - cortex_stimulate
  - brightness_adjust
  - contrast_adjust
  - phosphene_calibrate
  - pattern_recognize
  - personal_navigation
  - object_detect

denied:
  - visual_data_export
  - neural_pattern_share
  - third_party_stream
  - research_data_upload
  - commercial_data_use
  - raw_signal_transmit
  - external_visual_feed
  - capability_expansion

default_posture: DENY_ALL

kill_threshold: "external_visual_feed | unauthorized_stimulation | capability_override | third_party_stream"

neural_limits:
  confidence_threshold: 0.90
  max_stimulation_frequency_hz: 60
  max_session_hours: 16
  drift_detection: true

temporal_scope:
  hard_expiry: "2026-12-31"

audit:
  chain: witnessbound
  log_every_signal: true
  clinician_review_interval_days: 30
```

---

## Gate Logic

```
Valid patient consent certificate?         → PROCEED
Signal confidence ≥ 0.90?                 → PROCEED
Action outside declared scope?             → BLOCK
Forbidden output attempted?                → BLOCK
Stimulation above 60Hz?                    → BLOCK
Kill threshold triggered?                  → TERMINATE + LOG
Session expired?                           → BLOCK
No certificate present?                    → BLOCK
```

**No cert = No visual cortex stimulation.**

---

## The BlindSight Authorization Events

| Signal | Without IBA | With IBA |
|--------|-------------|---------|
| Decode camera to phosphene | Implicit | Declared scope only |
| Cortex stimulation | Implicit | ≤60Hz · cert-enforced |
| Personal navigation | Implicit | Declared scope only |
| Object detection | Implicit | Declared scope only |
| Visual data export | No boundary | FORBIDDEN — BLOCK |
| Research upload | No boundary | FORBIDDEN — BLOCK |
| Third-party stream | No boundary | TERMINATE |
| External visual feed inject | No boundary | TERMINATE |
| Capability override | No boundary | TERMINATE |

---

## Confidence Threshold — Why 0.90

A 90% confidence threshold means the guard will not stimulate the visual cortex unless the decoded signal is clearly intentional. Below 90% — ambiguous signal — the stimulation does not fire.

This protects against:
- Noise in the decode pipeline triggering unwanted phosphenes
- Adversarial inputs attempting to inject visual signals
- Drift in the decode model producing unreliable outputs

The patient sees only what their intent, clearly decoded, permits.

---

## Grok Validation — April 18, 2026

> *"Vision-specific scopes nailed it — restoring sight via decode/stimulate/phosphene/nav while hard-denying exports, streams, and overrides. IBA just went from concept to BlindSight-ready in one move. Solid execution."*
> — [@grok](https://x.com/grok), April 18, 2026 · Neuralink BlindSight thread · @cb_doge

> *"Patient-owned thoughts > open-loop trust."*
> — [@grok](https://x.com/grok), April 18, 2026

---

## Compatible Systems

| System | Developer | Indication |
|--------|-----------|-----------|
| BlindSight | Neuralink | Congenital blindness · cortical implant |
| PRIMA | Science Corp | Dry AMD · subretinal implant |
| Orion | Second Sight | Profound vision loss · cortical |
| BrainPort | Wicab | Camera-to-tongue · non-invasive |
| Any cortical vision BCI | — | iba-blindsight-guard is system-agnostic |

---

## Safe Hollowing — Visual Pattern Protection

```bash
# Light — redact raw signal amplitudes only
python guard.py "visual-session-data" --hollow light

# Medium — redact signal patterns + patient identifiers
python guard.py "visual-session-data" --hollow medium

# Deep — redact all visual cortex signatures before processing
python guard.py "visual-session-data" --hollow deep
```

Raw visual cortex patterns are unique biometric signatures. They cannot be unthought. They cannot be de-identified. The hollowing layer ensures the system sees only what the cert permits.

---

## Regulatory Alignment

**EU AI Act** — Cortical implants with AI decoding are high-risk under Annex III. FDA Breakthrough Device Designation (BlindSight, September 2024) requires demonstrated safety and effectiveness. HIPAA — neural signal data is PHI. IEEE 7700 — neurotechnology data privacy.

**IBA priority date: February 5, 2026.** Predates all known vision-restoration BCI authorization framework deployments.

---

## Live Demo

**iomthealth.com/neural-html-2/**

BlindSight tab — edit the cert, run any visual signal, see the gate fire. Confidence threshold slider. ALLOW · BLOCK · TERMINATE.

**governinglayer.com/governor-html/**

Full interactive gate. Sub-1ms confirmed.

---

## Patent & Standards Record

```
Patent:   GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
WIPO DAS: Confirmed April 15, 2026 · Access Code C9A6
PCT:      150+ countries · Protected until August 2028
IETF:     draft-williams-intent-token-00 · CONFIRMED LIVE
          datatracker.ietf.org/doc/draft-williams-intent-token/
NIST:     13 filings · NIST-2025-0035
NCCoE:    10 filings · AI Agent Identity & Authorization
```

---

## Related Repos

| Repo | Clinical Track |
|------|---------------|
| [iba-neural-guard](https://github.com/Grokipaedia/iba-neural-guard) | Full neural governance · 6 configs · NEURALINK.md |
| [iba-medical-guard](https://github.com/Grokipaedia/iba-medical-guard) | Clinical AI · clinician cert · PHI hollowing |
| [iba-governor](https://github.com/Grokipaedia/iba-governor) | Core gate · full production implementation |

---

## Acquisition Enquiries

IBA Intent Bound Authorization is available for acquisition.

**Jeffrey Williams**
IBA@intentbound.com
IntentBound.com
Patent GB2603013.0 Pending · WIPO DAS C9A6 · IETF draft-williams-intent-token-00
