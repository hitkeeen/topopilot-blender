import argparse
import json
import sys
from pathlib import Path

from .diagnosis import diagnose_mesh


def _sample_path():
    return Path(__file__).with_name("fixtures") / "sample_mesh.json"


def build_parser():
    parser = argparse.ArgumentParser(prog="topopilot", description="Local-first mesh diagnosis tools.")
    commands = parser.add_subparsers(dest="command", required=True)
    diagnose = commands.add_parser("diagnose", help="diagnose a JSON mesh fixture")
    source = diagnose.add_mutually_exclusive_group(required=True)
    source.add_argument("--sample", action="store_true", help="use the bundled mesh fixture")
    source.add_argument("--input", type=Path, help="path to a mesh JSON file")
    diagnose.add_argument("--output", type=Path, help="write the report to this path")
    return parser


def main(argv=None):
    if argv is not None:
        argv = [str(value) for value in argv]
    args = build_parser().parse_args(argv)
    if args.command == "diagnose":
        path = _sample_path() if args.sample else args.input
        try:
            mesh = json.loads(path.read_text(encoding="utf-8"))
            report = diagnose_mesh(mesh, name=path.stem)
        except (OSError, ValueError, KeyError) as error:
            print("topopilot: unable to diagnose mesh: {}".format(error), file=sys.stderr)
            return 1
        payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(payload, encoding="utf-8")
        else:
            print(payload, end="")
        return 0
    return 0
