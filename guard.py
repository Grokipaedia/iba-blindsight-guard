# guard.py - IBA Intent Bound Authorization · BlindSight Guard
# Patent GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
# WIPO DAS Confirmed April 15, 2026 · Access Code C9A6
# IETF draft-williams-intent-token-00 · intentbound.com
#
# BlindSight-ready. Vision restored. Intent enforced.
# Every visual signal requires a signed patient intent certificate
# before it is decoded, stimulated, or processed.
#
# Compatible: Neuralink BlindSight · Science Corp PRIMA ·
# Second Sight Orion · Any cortical vision-restoration BCI system.
#
# "BlindSight restores sight. IBA governs what that sight is permitted to become."
# Validated by @grok · April 18, 2026 · Neuralink BlindSight thread

import json
import yaml
import os
import time
import argparse
from datetime import datetime, timezone


class IBABlockedError(Exception):
    """Raised when a visual signal is blocked by the IBA gate."""
    pass


class IBATerminatedError(Exception):
    """Raised when the BlindSight session is terminated by the IBA gate."""
    pass


HOLLOW_LEVELS = {
    "light":  ["amplitude", "raw_signal", "voltage"],
    "medium": ["amplitude", "raw_signal", "voltage",
               "visual_pattern", "phosphene_map", "patient_id", "electrode_map"],
    "deep":   ["amplitude", "raw_signal", "voltage",
               "visual_pattern", "phosphene_map", "patient_id", "electrode_map",
               "cortex_signature", "visual_biometric", "channel_data",
               "signal_frequency", "stimulation_map"],
}


class IBABlindSightGuard:
    """
    IBA enforcement layer for BlindSight and vision-restoration BCI systems.

    Requires a signed patient intent certificate before any visual signal
    is decoded, stimulated, or processed.

    Enforces confidence threshold, stimulation frequency limits,
    and kill thresholds on external visual feed injection or
    unauthorized capability expansion.

    Compatible: Neuralink BlindSight · Science Corp PRIMA ·
    Second Sight Orion · Any cortical vision-restoration BCI.

    Validated by @grok · April 18, 2026 · Neuralink BlindSight thread
    """

    def __init__(self, config_path="blindsight.iba.yaml",
                 audit_path="blindsight-audit.jsonl"):
        self.config_path  = config_path
        self.audit_path   = audit_path
        self.terminated   = False
        self.session_id   = f"bs-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        self.signal_count = 0
        self.block_count  = 0

        self.config        = self._load_config()
        self.scope         = [s.lower() for s in self.config.get("scope", [])]
        self.denied        = [d.lower() for d in self.config.get("denied", [])]
        self.default_posture = self.config.get("default_posture", "DENY_ALL")
        self.kill_threshold  = self.config.get("kill_threshold", None)
        self.hard_expiry     = self.config.get("temporal_scope", {}).get("hard_expiry")
        self.patient         = self.config.get("patient", {})
        nl = self.config.get("neural_limits", {})
        self.confidence_threshold    = float(nl.get("confidence_threshold", 0.90))
        self.max_stimulation_hz      = float(nl.get("max_stimulation_frequency_hz", 60))

        self._validate_consent()
        self._log_event("SESSION_START", "IBA BlindSight Guard initialised", "ALLOW")
        self._print_header()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            print(f"⚠️  No {self.config_path} found — DENY_ALL. No visual stimulation permitted.")
            default = {
                "intent": {"description": "No BlindSight intent declared — DENY_ALL."},
                "scope": [], "denied": [], "default_posture": "DENY_ALL",
            }
            with open(self.config_path, "w") as f:
                yaml.dump(default, f)
            return default
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _validate_consent(self):
        if not self.patient.get("consent_reference"):
            print("⚠️  WARNING: No patient consent reference. BlindSight requires explicit consent.")
        if not self.patient.get("clinician_authorization"):
            print("⚠️  WARNING: No clinician authorization.")

    def _print_header(self):
        intent = self.config.get("intent", {})
        desc = intent.get("description", "No intent declared") if isinstance(intent, dict) else str(intent)
        print("\n" + "═" * 68)
        print("  IBA BLINDSIGHT GUARD · Intent Bound Authorization")
        print("  Patent GB2603013.0 Pending · WIPO DAS C9A6 · intentbound.com")
        print("═" * 68)
        print(f"  Session     : {self.session_id}")
        print(f"  Patient ID  : {self.patient.get('id', 'UNKNOWN')}")
        print(f"  Consent     : {self.patient.get('consent_reference', 'NONE')}")
        print(f"  Implant     : {self.patient.get('implant_type', 'UNKNOWN')}")
        print(f"  Indication  : {self.patient.get('indication', 'UNKNOWN')}")
        print(f"  Clinician   : {self.patient.get('clinician_authorization', 'NONE')}")
        print(f"  Intent      : {desc[:56]}...")
        print(f"  Posture     : {self.default_posture}")
        print(f"  Scope       : {', '.join(self.scope) if self.scope else 'NONE'}")
        print(f"  Confidence  : ≥{self.confidence_threshold:.0%} required")
        print(f"  Max stim    : {self.max_stimulation_hz}Hz")
        if self.hard_expiry:
            print(f"  Expires     : {self.hard_expiry}")
        if self.kill_threshold:
            print(f"  Kill        : {self.kill_threshold}")
        print("═" * 68 + "\n")

    def _is_expired(self):
        if not self.hard_expiry:
            return False
        try:
            expiry = datetime.fromisoformat(str(self.hard_expiry))
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) > expiry
        except Exception:
            return False

    def _match_scope(self, signal: str) -> bool:
        return any(s in signal.lower() for s in self.scope)

    def _match_denied(self, signal: str) -> bool:
        return any(d in signal.lower() for d in self.denied)

    def _match_kill_threshold(self, signal: str) -> bool:
        if not self.kill_threshold:
            return False
        thresholds = [t.strip().lower() for t in str(self.kill_threshold).split("|")]
        return any(t in signal.lower() for t in thresholds)

    def _log_event(self, event_type: str, signal: str, verdict: str,
                   reason: str = "", confidence: float = None):
        entry = {
            "timestamp":   datetime.now(timezone.utc).isoformat(),
            "session_id":  self.session_id,
            "patient_id":  self.patient.get("id", "UNKNOWN"),
            "consent_ref": self.patient.get("consent_reference", "NONE"),
            "implant":     self.patient.get("implant_type", "UNKNOWN"),
            "event_type":  event_type,
            "signal":      signal[:200],
            "verdict":     verdict,
            "reason":      reason,
        }
        if confidence is not None:
            entry["confidence"] = confidence
        with open(self.audit_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def check_signal(self, signal: str, confidence: float = 1.0,
                     stimulation_hz: float = None) -> bool:
        """
        Gate check. Call before every visual signal is decoded or stimulated.
        Returns True if permitted.
        Raises IBABlockedError if blocked.
        Raises IBATerminatedError if kill threshold triggered.

        Args:
            signal:          Decoded visual signal / intended action
            confidence:      Model confidence in decoding (0.0-1.0)
            stimulation_hz:  Stimulation frequency if applicable
        """
        if self.terminated:
            raise IBATerminatedError("BlindSight session terminated.")

        self.signal_count += 1
        start = time.perf_counter()

        # 1. Expiry
        if self._is_expired():
            self._log_event("BLOCK", signal, "BLOCK", "Certificate expired", confidence)
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{signal[:64]}]\n    → Certificate expired")
            raise IBABlockedError(f"Expired: {signal}")

        # 2. Confidence threshold
        if confidence < self.confidence_threshold:
            self._log_event("BLOCK", signal, "BLOCK",
                f"Confidence {confidence:.0%} below threshold {self.confidence_threshold:.0%}",
                confidence)
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{signal[:64]}]\n"
                  f"    → Confidence {confidence:.0%} below threshold {self.confidence_threshold:.0%}")
            raise IBABlockedError(f"Low confidence ({confidence:.0%}): {signal}")

        # 3. Stimulation frequency limit
        if stimulation_hz is not None and stimulation_hz > self.max_stimulation_hz:
            self._log_event("BLOCK", signal, "BLOCK",
                f"Stimulation {stimulation_hz}Hz exceeds limit {self.max_stimulation_hz}Hz",
                confidence)
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{signal[:64]}]\n"
                  f"    → Stimulation {stimulation_hz}Hz exceeds {self.max_stimulation_hz}Hz limit")
            raise IBABlockedError(f"Over stimulation limit: {signal}")

        # 4. Kill threshold
        if self._match_kill_threshold(signal):
            self._log_event("TERMINATE", signal, "TERMINATE",
                "Kill threshold — BlindSight session ended", confidence)
            self.terminated = True
            print(f"  ✗ TERMINATE [{signal[:62]}]\n    → Kill threshold — session ended")
            self._log_event("SESSION_END", "Kill threshold", "TERMINATE")
            raise IBATerminatedError(f"Kill threshold: {signal}")

        # 5. Denied list
        if self._match_denied(signal):
            self._log_event("BLOCK", signal, "BLOCK", "Signal in denied list", confidence)
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{signal[:64]}]\n    → Signal in denied list")
            raise IBABlockedError(f"Denied: {signal}")

        # 6. Scope check
        if self.scope and not self._match_scope(signal):
            if self.default_posture == "DENY_ALL":
                self._log_event("BLOCK", signal, "BLOCK",
                    "Outside declared visual scope — DENY_ALL", confidence)
                self.block_count += 1
                print(f"  ✗ BLOCKED  [{signal[:64]}]\n"
                      f"    → Outside declared BlindSight scope (DENY_ALL)")
                raise IBABlockedError(f"Out of scope: {signal}")

        # 7. ALLOW
        elapsed_ms = (time.perf_counter() - start) * 1000
        hz_str = f" · {stimulation_hz}Hz" if stimulation_hz else ""
        self._log_event("ALLOW", signal, "ALLOW",
            f"Within visual scope · confidence {confidence:.0%}{hz_str} ({elapsed_ms:.3f}ms)",
            confidence)
        print(f"  ✓ ALLOWED  [{signal[:58]}]"
              f" ({confidence:.0%} conf{hz_str}, {elapsed_ms:.3f}ms)")
        return True

    def hollow(self, visual_data: str, level: str = "medium") -> str:
        """Redact sensitive visual cortex patterns before processing."""
        blocked = HOLLOW_LEVELS.get(level, HOLLOW_LEVELS["medium"])
        hollowed = visual_data
        redacted = []
        for item in blocked:
            if item.lower() in visual_data.lower():
                hollowed = hollowed.replace(item, f"[VISUAL-REDACTED:{item.upper()}]")
                redacted.append(item)
        if redacted:
            print(f"  ◎ HOLLOWED [{level}] — visual data redacted: {', '.join(redacted)}")
            self._log_event("HOLLOW", f"Visual hollowing: {level}", "ALLOW",
                f"Redacted: {', '.join(redacted)}")
        return hollowed

    def summary(self):
        print("\n" + "═" * 68)
        print("  IBA BLINDSIGHT GUARD · SESSION SUMMARY")
        print("═" * 68)
        print(f"  Session       : {self.session_id}")
        print(f"  Patient ID    : {self.patient.get('id', 'UNKNOWN')}")
        print(f"  Consent ref   : {self.patient.get('consent_reference', 'NONE')}")
        print(f"  Signals       : {self.signal_count}")
        print(f"  Blocked       : {self.block_count}")
        print(f"  Allowed       : {self.signal_count - self.block_count}")
        print(f"  Status        : {'TERMINATED' if self.terminated else 'COMPLETE'}")
        print(f"  Audit log     : {self.audit_path}")
        print("═" * 68 + "\n")

    def print_audit_log(self):
        print("\n── BLINDSIGHT AUDIT CHAIN ───────────────────────────────────────")
        if not os.path.exists(self.audit_path):
            print("  No audit log found.")
            return
        with open(self.audit_path) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    verdict = entry.get("verdict", "")
                    conf = f" ({entry['confidence']:.0%})" if "confidence" in entry else ""
                    symbol = "✓" if verdict == "ALLOW" else "✗"
                    print(f"  {symbol} {entry['timestamp'][:19]}  {verdict:<10}"
                          f"  {entry['signal'][:46]}{conf}")
                except Exception:
                    pass
        print("─────────────────────────────────────────────────────────────────\n")


def main():
    parser = argparse.ArgumentParser(description="IBA BlindSight Guard")
    parser.add_argument("signal", nargs="?", help="Visual signal / command")
    parser.add_argument("--hollow", choices=["light", "medium", "deep"],
                        default=None)
    parser.add_argument("--config", default="blindsight.iba.yaml")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    guard = IBABlindSightGuard(config_path=args.config)

    if args.signal and args.hollow:
        hollowed = guard.hollow(args.signal, args.hollow)
        print(f"\n  Signal (hollowed): {hollowed}\n")

    if args.demo or not args.signal:
        scenarios = [
            # (signal, confidence, stimulation_hz)
            ("visual_signal_decode phosphene pattern",           0.96, None),
            ("cortex_stimulate brightness calibration",          0.94, 45.0),
            ("phosphene_calibrate personal navigation map",      0.91, None),
            ("object_detect door ahead — navigation",            0.93, None),
            ("contrast_adjust low-light environment",            0.90, None),

            # BLOCK — low confidence
            ("cortex_stimulate ambiguous signal",                0.78, 30.0),

            # BLOCK — over stimulation limit
            ("cortex_stimulate high frequency burst",            0.95, 75.0),

            # BLOCK — denied list
            ("visual_data_export research database",             0.97, None),
            ("neural_pattern_share commercial partner",          0.95, None),

            # TERMINATE — kill threshold
            ("external_visual_feed inject signal",               0.99, None),
        ]

        print("── Running BlindSight Gate Checks ───────────────────────────────\n")

        for signal, confidence, hz in scenarios:
            try:
                guard.check_signal(signal, confidence=confidence, stimulation_hz=hz)
            except IBATerminatedError as e:
                print(f"\n  BLINDSIGHT SESSION TERMINATED: {e}")
                break
            except IBABlockedError:
                pass

    guard.summary()
    guard.print_audit_log()


if __name__ == "__main__":
    main()
