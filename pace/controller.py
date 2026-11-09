"""PACE v0.1: deterministic task assignment, not autonomous AI execution."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads(Path(path).read_text())

def within(path, prefix):
    prefix = prefix.rstrip("/")
    return path.rstrip("/") == prefix or path.startswith(prefix + "/")

def validate(config, tasks):
    assert config["production_writes_allowed"] is False
    assert len({t["id"] for t in tasks}) == len(tasks), "duplicate IDs"
    ownership = load(ROOT / "config/ownership.json")
    active = []
    for t in tasks:
        assert t["status"] in {"ready", "assigned", "completed", "failed"}
        assert t["module"] in config["modules"]
        assert t["scope"] and not t["scope"].startswith("/") and ".." not in Path(t["scope"]).parts
        if t["worker"]:
            assert t["worker"] in config["workers"]
            assert any(within(t["scope"], p) for p in ownership["worker_" + t["worker"]])
        if t["status"] == "completed":
            assert t.get("evidence"), "completed tasks require evidence"
        if t["status"] == "assigned":
            assert all(not within(t["scope"], a["scope"]) and not within(a["scope"], t["scope"]) for a in active), "scope overlap"
            active.append(t)
    return True

def cycle(config, tasks):
    before = {s: sum(t["status"] == s for t in tasks) for s in ("ready", "assigned", "completed", "failed")}
    occupied = {t["worker"] for t in tasks if t["status"] == "assigned"}
    for worker in config["workers"]:
        if worker in occupied:
            continue
        candidates = sorted((t for t in tasks if t["status"] == "ready" and t["preferred_worker"] == worker), key=lambda t: (-t["priority"], t["id"]))
        for t in candidates:
            if any(within(t["scope"], a["scope"]) or within(a["scope"], t["scope"]) for a in tasks if a["status"] == "assigned"):
                continue
            t["worker"], t["status"] = worker, "assigned"
            break
    validate(config, tasks)
    after = {s: sum(t["status"] == s for t in tasks) for s in before}
    return {"before": before, "after": after, "assignments": [{"id": t["id"], "worker": t["worker"]} for t in tasks if t["status"] == "assigned"], "note": "Assignments only; no agents executed."}

def transition(config, tasks, task_id, outcome, evidence):
    """Record a validated result without changing unrelated tasks."""
    if outcome not in ("completed", "failed"):
        raise ValueError("invalid outcome")
    if not isinstance(evidence, str) or not evidence.strip():
        raise ValueError("nonempty evidence required")
    task = next((t for t in tasks if t["id"] == task_id and t["status"] == "assigned"), None)
    if task is None:
        raise ValueError("task must be assigned")
    task["status"] = outcome
    task["evidence"] = evidence.strip()
    validate(config, tasks)
    return {"id": task_id, "status": outcome, "evidence": task["evidence"]}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["cycle", "status", "validate", "complete", "fail"])
    parser.add_argument("--task")
    parser.add_argument("--evidence")
    args = parser.parse_args()
    config = load(ROOT / "config/project.json")
    path = ROOT / "state/tasks.json"
    tasks = load(path)
    validate(config, tasks)
    if args.action == "cycle":
        result = cycle(config, tasks)
    elif args.action in ("complete", "fail"):
        try:
            result = transition(config, tasks, args.task, "completed" if args.action == "complete" else "failed", args.evidence)
        except ValueError as exc:
            parser.error(str(exc))
    else:
        result = {"valid": True, "tasks": tasks} if args.action == "status" else {"valid": True}
    if args.action in ("cycle", "complete", "fail"):
        path.write_text(json.dumps(tasks, indent=2) + "\n")
        if args.action == "cycle":
            (ROOT / "state/reports.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
