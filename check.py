"""Synthetic CI producer; stdlib, no network or environment access."""
import argparse
import json
from pathlib import Path


def validate(data):
    return (
        type(data) is dict
        and set(data) == {"schema", "control_value", "label"}
        and type(data["schema"]) is int
        and data["schema"] == 1
        and type(data["control_value"]) is int
        and data["control_value"] == 271828
        and data["label"] == "synthetic-m3-only"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    raw = Path(__file__).with_name("fixture.json").read_bytes()
    if len(raw) > 1024:
        return 24
    data = json.loads(raw)
    if args.negative:
        data["control_value"] = 999999
    if not validate(data):
        print("M3_REJECT_999999_EXIT_23" if args.negative else "M3_UNEXPECTED_REJECTION")
        return 23
    print("M3_ACCEPT_271828")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
