#!/usr/bin/env python3
"""Stop hook: append a one-line capture of the finished exchange to today's daily note.
Distilled from a <!--CAPTURE: ...--> footer if present, else a raw fallback from the user msg.
Reads only the TAIL of the (possibly 20MB+) transcript. Never blocks; logs failures."""
import sys, os, json, re
from datetime import datetime
sys.path.insert(0, os.path.expanduser("~/.claude/hooks"))
import _hooklib as HL

def main():
    if not HL.vault_ok():
        return
    try:
        hook = json.loads(sys.stdin.read())
    except Exception:
        return
    if hook.get("stop_hook_active"):
        return
    tpath = hook.get("transcript_path")
    if not tpath or not os.path.exists(tpath):
        return
    cwd = hook.get("cwd") or ""
    branch = hook.get("gitBranch") or ""
    proj = os.path.basename(cwd.rstrip("/")) if cwd else ""

    last_user = last_asst = None
    for ln in HL.tail_lines(tpath):          # tail only — not the whole file
        ln = ln.strip()
        if not ln:
            continue
        try:
            o = json.loads(ln)
        except Exception:
            continue
        if o.get("isSidechain"):             # skip subagent turns
            continue
        t = o.get("type"); msg = o.get("message") or {}
        c = msg.get("content")
        if t == "user":
            if isinstance(c, str) and c.strip():
                last_user = c.strip()
            elif isinstance(c, list):
                txt = " ".join(b.get("text", "") for b in c
                               if isinstance(b, dict) and b.get("type") == "text")
                if txt.strip():
                    last_user = txt.strip()   # real text turn, not a tool_result
        elif t == "assistant" and isinstance(c, list):
            txt = "\n".join(b.get("text", "") for b in c
                            if isinstance(b, dict) and b.get("type") == "text")
            if txt.strip():
                last_asst = txt.strip()

    captured_type = None
    m = re.search(r'<!--\s*CAPTURE:\s*(.*?)\s*-->', last_asst or "", re.S)
    if m:
        entry = re.sub(r'\s+', ' ', m.group(1)).strip()
        tm = re.search(r'\btype:\s*(decision|win|incident|context|research|learning)\b', entry, re.I)
        if tm:
            captured_type = tm.group(1).lower()
            entry = f"({captured_type}) " + re.sub(r'\|\|\s*type:\s*\w+', '', entry).strip(" |")
    elif last_user:
        u = re.sub(r'\s+', ' ', last_user).strip()
        entry = "(raw) " + (u[:140] + ("…" if len(u) > 140 else ""))
    else:
        return

    now = datetime.now()
    ddir = os.path.join(HL.MEM, "Daily")
    os.makedirs(ddir, exist_ok=True)
    day = now.strftime("%Y-%m-%d")
    dfile = os.path.join(ddir, day + ".md")
    # exclusive create of the header (no double-header race between concurrent Stops)
    try:
        with open(dfile, "x") as f:
            f.write(f"---\nname: {day}\ntags: [journal, meta]\n---\n\n# {day}\n\n"
                    f"Auto-captured exchanges (via `capture-exchange` Stop hook). ↩ [[_Home]]\n\n")
    except FileExistsError:
        pass
    ctx = f" [{proj}" + (f"@{branch}" if branch else "") + "]" if proj else ""
    with open(dfile, "a") as f:              # append is atomic for a single small write
        f.write(f"- **{now.strftime('%H:%M')}**{ctx} — {entry}\n")

    # research/learning → durable promote-queue (safety net so curation is never lost)
    if captured_type in ("research", "learning"):
        q = os.path.join(HL.MEM, "_infra", "_promote-queue.md")
        try:
            os.makedirs(os.path.dirname(q), exist_ok=True)
            try:
                with open(q, "x") as f:
                    f.write("---\nname: _promote-queue\ntags: [meta, type/index]\n---\n\n"
                            "# Promote queue\n\nResearch/learnings flagged for curation into atomic "
                            "notes. `/obsidian consolidate` sweeps this; check off when a curated note "
                            "exists. \u21a9 [[_Home]]\n\n")
            except FileExistsError:
                pass
            with open(q, "a") as f:
                f.write(f"- [ ] {day} {now.strftime('%H:%M')}{ctx} — {entry}\n")
        except Exception as e:
            HL.log_err("capture-exchange.queue", e)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        HL.log_err("capture-exchange", e)
