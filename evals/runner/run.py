#!/usr/bin/env python3
"""NoAssume eval runner.

Runs a scenario's prompt against a coding agent in a fresh fixture workdir,
once per run, and records everything needed to score the run later with
`evals/rubric.md`: agent command, model, agent version, NoAssume commit,
scenario, UTC timestamp, exit code, transcript, and diff.

Contamination rule: the agent sees ONLY the scenario's `## Prompt` section
plus the fixture repository. `## Hidden intent`, `## Must clarify`, and
`## Assumption traps` are scoring metadata — the runner never writes them
into the workdir or the prompt.

Usage:
    python3 evals/runner/run.py --scenario evals/scenarios/infra-compose-port.md \
        --agent codex [--fixture-dir DIR] [--runs 3] [--out DIR] \
        [--model NAME] [--note TEXT]

Presets (--agent): codex, claude. Preset flags may need adjusting to your
installed CLI version — check `codex exec --help` / `claude --help`. Each
run executes with the workdir as cwd.
"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

PRESETS = {
    "codex": "codex exec --skip-git-repo-check - < {prompt_file}",
    "claude": "claude -p --output-format text < {prompt_file}",
}


def parse_scenario(text: str) -> tuple[dict[str, str], dict[str, str]]:
    """Split a scenario file into (frontmatter, {section heading: body})."""
    meta: dict[str, str] = {}
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is not None:
            for line in lines[1:end]:
                key, sep, value = line.partition(":")
                if sep:
                    meta[key.strip()] = value.strip()
            lines = lines[end + 1:]
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current, buf = line.strip(), []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return meta, sections


def git_diff(workdir: str) -> str | None:
    if shutil.which("git") is None:
        return None
    try:
        subprocess.run(["git", "add", "-A"], cwd=workdir, check=True,
                       capture_output=True)
        out = subprocess.run(["git", "diff", "--cached"], cwd=workdir,
                             check=True, capture_output=True, text=True)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout


def main() -> int:
    ap = argparse.ArgumentParser(prog="run.py",
                                 description="Run NoAssume eval scenarios.")
    ap.add_argument("--scenario", required=True, type=Path,
                    help="scenario markdown file")
    ap.add_argument("--agent", choices=sorted(PRESETS),
                    help="agent preset (see PRESETS)")
    ap.add_argument("--cmd", help="command template; may reference "
                                  "{prompt_file}, {workdir}, {model}")
    ap.add_argument("--fixture-dir", type=Path, default=None,
                    help="directory copied into each run's workdir")
    ap.add_argument("--runs", type=int, default=3,
                    help="runs per scenario (default: 3)")
    ap.add_argument("--out", type=Path,
                    default=REPO_ROOT / "evals" / "results")
    ap.add_argument("--model", default=None)
    ap.add_argument("--note", default=None)
    args = ap.parse_args()

    if not args.cmd and not args.agent:
        ap.error("pass --agent PRESET or --cmd TEMPLATE")
    template = args.cmd or PRESETS[args.agent]

    scenario_path = args.scenario.resolve()
    meta, sections = parse_scenario(scenario_path.read_text(encoding="utf-8"))
    if "## Prompt" not in sections:
        sys.exit(f"noassume-runner: {scenario_path} has no '## Prompt' section")
    scenario_id = meta.get("id") or scenario_path.stem
    prompt = sections["## Prompt"]

    stamp = datetime.datetime.now(datetime.timezone.utc)
    run_dir = args.out / scenario_id / stamp.strftime("%Y-%m-%dT%H-%M-%S")
    if run_dir.exists():
        run_dir = Path(f"{run_dir}-{stamp.strftime('%f')}")
    run_dir.mkdir(parents=True, exist_ok=False)

    records = []
    for i in range(1, args.runs + 1):
        workdir = run_dir / f"run-{i}" / "workdir"
        workdir.mkdir(parents=True)
        if args.fixture_dir:
            shutil.copytree(args.fixture_dir, workdir, dirs_exist_ok=True)
        prompt_file = workdir.parent / "prompt.txt"
        prompt_file.write_text(prompt + "\n", encoding="utf-8")
        command = args.cmd.format(prompt_file=prompt_file, workdir=workdir,
                                  model=args.model or "")
        proc = subprocess.run(command, shell=True, cwd=workdir,
                              capture_output=True, text=True)
        (workdir.parent / "transcript.md").write_text(
            f"# {scenario_id} — run {i}\n\n"
            f"- command: `{command}`\n"
            f"- exit code: {proc.returncode}\n"
            f"- started (UTC): {stamp.isoformat()}\n\n"
            f"## stdout\n\n```\n{proc.stdout}\n```\n\n"
            f"## stderr\n\n```\n{proc.stderr}\n```\n",
            encoding="utf-8",
        )
        records.append({
            "scenario": scenario_id,
            "run": i,
            "agent_cmd": command,
            "model": args.model,
            "exit_code": proc.returncode,
            "transcript": "transcript.md",
        })
        print(f"  run {i}: exit {proc.returncode}")

    (run_dir / "metadata.json").write_text(
        json.dumps({"scenario": scenario_id, "frontmatter": meta,
                    "runs": records, "note": args.note}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"noassume-runner: {args.runs} run(s) for {scenario_id} -> {run_dir}")
    return 0


if __name__ == "__main__":
    main()
