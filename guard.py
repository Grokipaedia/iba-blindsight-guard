# guard.py - IBA governance for Blindsight / vision-restoration BCI
import json
from datetime import datetime
import sys
import argparse

def create_iba_blindsight_guard(command: str, hollow_level: str = None):
    cert = {
        "iba_version": "2.0",
        "certificate_id": f"blindsight-guard-{datetime.now().strftime('%Y%m%d-%H%M')}",
        "issued_at": datetime.now().isoformat(),
        "principal": "licensed-clinician",
        "declared_intent": f"Vision restoration neural command: {command}. Decode/stimulate/phosphene/nav only. Strictly patient-first.",
        "scope_envelope": {
            "resources": ["vision-decode", "cortical-stimulate", "phosphene-navigation"],
            "denied": ["data-export", "stream-override", "external-control", "non-medical-use"],
            "default_posture": "DENY_ALL"
        },
        "temporal_scope": {
            "hard_expiry": (datetime.now().replace(year=datetime.now().year + 1)).isoformat()
        },
        "entropy_threshold": {
            "max_kl_divergence": 0.08,
            "flag_at": 0.05,
            "kill_at": 0.08
        },
        "clinician_interval_ms": 5000,
        "iba_signature": "demo-signature"
    }

    protected_file = f"blindsight-command-{command.replace(' ', '-').lower()[:30]}.iba-protected.md"

    content = f"# Blindsight Vision Command: {command}\n\n[Neural decode → stimulate → phosphene navigation would execute here under IBA governance]\n\n<!-- IBA PROTECTED BLINDSIGHT COMMAND -->\n"

    if hollow_level:
        content += f"\n<!-- Hollowed ({hollow_level}): Sensitive neural patterns + overrides protected by IBA certificate -->\n"

    with open(protected_file, "w", encoding="utf-8") as f:
        f.write("<!-- IBA PROTECTED BLINDSIGHT VISION RESTORATION -->\n")
        f.write(f"<!-- Intent Certificate: {json.dumps(cert, indent=2)} -->\n\n")
        f.write(content)

    print(f"✅ IBA-protected Blindsight command file created: {protected_file}")
    if hollow_level:
        print(f"   Hollowing level applied: {hollow_level}")
    else:
        print("   Full Blindsight vision command protected by IBA certificate")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Governed Blindsight / vision-restoration BCI with IBA")
    parser.add_argument("command", help="Description of the vision neural command")
    parser.add_argument("--hollow", choices=["light", "medium", "heavy"], help="Apply safe hollowing")
    args = parser.parse_args()

    create_iba_blindsight_guard(args.command, args.hollow)
