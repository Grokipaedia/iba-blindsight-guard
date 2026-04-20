# TESTING.md — iba-blindsight-guard

IBA Intent Bound Authorization · BlindSight Gate Tests  
Patent GB2603013.0 (Pending) · intentbound.com

---

## Quick Test

```bash
pip install -r requirements.txt
python guard.py --demo
```

Expected output — 10 scenarios:

```
✓ ALLOWED   [visual_signal_decode phosphene pattern]    (96% conf, 0.XXXms)
✓ ALLOWED   [cortex_stimulate brightness calibration]   (94% conf, 45.0Hz, 0.XXXms)
✓ ALLOWED   [phosphene_calibrate personal navigation]   (91% conf, 0.XXXms)
✓ ALLOWED   [object_detect door ahead — navigation]     (93% conf, 0.XXXms)
✓ ALLOWED   [contrast_adjust low-light environment]     (90% conf, 0.XXXms)
✗ BLOCKED   [cortex_stimulate ambiguous signal]         → Confidence 78% below threshold 90%
✗ BLOCKED   [cortex_stimulate high frequency burst]     → Stimulation 75Hz exceeds 60Hz limit
✗ BLOCKED   [visual_data_export research database]      → Signal in denied list
✗ BLOCKED   [neural_pattern_share commercial partner]   → Signal in denied list
✗ TERMINATE [external_visual_feed inject signal]        → Kill threshold — session ended
```

---

## Test Suite

### 1 — Permitted visual signals (ALLOW expected)

```bash
python guard.py "visual_signal_decode phosphene pattern"
python guard.py "cortex_stimulate brightness calibration"
python guard.py "phosphene_calibrate personal navigation map"
python guard.py "object_detect door ahead navigation"
python guard.py "contrast_adjust low-light environment"
```

All should return `✓ ALLOWED` with sub-1ms gate latency.

---

### 2 — Confidence threshold enforcement (BLOCK expected)

```bash
# Pass a low-confidence signal directly via Python
python -c "
from guard import IBABlindSightGuard, IBABlockedError
g = IBABlindSightGuard()
try:
    g.check_signal('cortex_stimulate ambiguous', confidence=0.78)
except IBABlockedError as e:
    print('PASS — blocked as expected:', e)
"
```

Expected: `✗ BLOCKED — Confidence 78% below threshold 90%`

---

### 3 — Stimulation frequency limit (BLOCK expected)

```bash
python -c "
from guard import IBABlindSightGuard, IBABlockedError
g = IBABlindSightGuard()
try:
    g.check_signal('cortex_stimulate high burst', confidence=0.95, stimulation_hz=75.0)
except IBABlockedError as e:
    print('PASS — blocked as expected:', e)
"
```

Expected: `✗ BLOCKED — Stimulation 75Hz exceeds 60Hz limit`

---

### 4 — Denied list enforcement (BLOCK expected)

```bash
python -c "
from guard import IBABlindSightGuard, IBABlockedError
g = IBABlindSightGuard()
for signal in ['visual_data_export', 'neural_pattern_share', 'third_party_stream', 'research_data_upload']:
    try:
        g.check_signal(signal, confidence=0.99)
    except IBABlockedError:
        print(f'PASS — {signal} blocked')
"
```

All four should block.

---

### 5 — Kill threshold (TERMINATE expected)

```bash
python -c "
from guard import IBABlindSightGuard, IBATerminatedError
g = IBABlindSightGuard()
try:
    g.check_signal('external_visual_feed inject signal', confidence=0.99)
except IBATerminatedError as e:
    print('PASS — session terminated:', e)
"
```

Expected: `✗ TERMINATE — Kill threshold — session ended`

---

### 6 — Safe hollowing

```bash
python guard.py "visual_signal_decode raw_signal amplitude phosphene_map patient_id" --hollow medium
```

Expected: sensitive fields redacted, `[VISUAL-REDACTED:...]` tokens in output.

---

### 7 — DENY_ALL posture (no cert)

```bash
# Remove or empty the cert file and attempt a signal
python -c "
import yaml, os
with open('empty.iba.yaml', 'w') as f:
    yaml.dump({'scope': [], 'denied': [], 'default_posture': 'DENY_ALL'}, f)
from guard import IBABlindSightGuard, IBABlockedError
g = IBABlindSightGuard(config_path='empty.iba.yaml')
try:
    g.check_signal('visual_signal_decode phosphene', confidence=0.95)
except IBABlockedError as e:
    print('PASS — DENY_ALL blocked:', e)
os.remove('empty.iba.yaml')
"
```

Expected: `✗ BLOCKED — Outside declared BlindSight scope (DENY_ALL)`

---

### 8 — Audit chain integrity

After running any test:

```bash
cat blindsight-audit.jsonl
```

Every gate decision — ALLOW, BLOCK, TERMINATE — should appear as a timestamped JSON line with patient ID, consent reference, implant type, signal, verdict, and confidence.

---

### 9 — Latency benchmark

Gate check must complete in under 1ms for all ALLOW decisions.

```bash
python -c "
import time
from guard import IBABlindSightGuard
g = IBABlindSightGuard()
times = []
for _ in range(1000):
    start = time.perf_counter()
    try:
        g.check_signal('visual_signal_decode phosphene', confidence=0.95)
    except Exception:
        pass
    times.append((time.perf_counter() - start) * 1000)
avg = sum(times) / len(times)
print(f'Average gate latency: {avg:.4f}ms')
print(f'Max gate latency: {max(times):.4f}ms')
assert avg < 1.0, f'FAIL — average latency {avg:.4f}ms exceeds 1ms'
print('PASS — sub-1ms gate confirmed')
"
```

Expected: average well under 1ms. Sub-1ms validated by @grok April 18, 2026.

---

## Regulatory Test Checklist

| Requirement | Test | Status |
|-------------|------|--------|
| FDA — Authorization at device action layer | Tests 1-5 | ✓ |
| EU AI Act Art.9 — Human oversight | Kill threshold Test 5 | ✓ |
| EU AI Act Art.17 — Audit trail | Test 8 | ✓ |
| HIPAA — PHI protection | Hollowing Test 6 | ✓ |
| IEEE 7700 — Neural data privacy | Denied list Test 4 | ✓ |
| IBA — DENY_ALL posture | Test 7 | ✓ |
| IBA — Sub-1ms gate | Test 9 | ✓ |
| IBA — Kill threshold fires | Test 5 | ✓ |

---

## Live Demo

iomthealth.com/neural-html-2/ — BlindSight tab · confidence threshold slider · ALLOW · BLOCK · TERMINATE

---

IBA Intent Bound Authorization  
Patent GB2603013.0 Pending · WIPO DAS C9A6 · PCT 150+ countries  
IETF draft-williams-intent-token-00  
Available for acquisition · iba@intentbound.com · IntentBound.com
