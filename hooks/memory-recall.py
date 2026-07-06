#!/usr/bin/env python3
"""UserPromptSubmit hook: just-in-time memory recall.
Word-boundary keyword match against the vault; requires >=2 distinct query keywords in a
note's name/description (kills generic-prompt noise). Deduped within session, capped,
project-biased. Silent on trivial/no-match prompts. Never blocks; logs failures."""
import sys, os, re, glob, json, time
sys.path.insert(0, os.path.expanduser("~/.claude/hooks"))
import _hooklib as HL

MEM = HL.MEM
STATE_DIR = os.path.join(MEM, ".recall-state")
EXCLUDE = {"MEMORY.md", "context.md", "_session-log.md"}
STOP = set("the a an and or of to in on for with is are was were be been this that these those i you "
           "it we they he she how what why when where which who do does did can could should would will "
           "just now then here there my your our their its from into out up down over about as at by so "
           "if not no yes ok okay thanks please help make add use using get got need want like also more "
           "most some any all one two new old via per etc pls better stronger strong full work works".split())
TRIVIAL = re.compile(r'^\s*(hi|hey|hello|yo|thanks|thank you|ok|okay|k|yep|yes|no|nope|cool|nice|'
                     r'got it|sure|great|perfect|done|continue|go on|next|/\w+)\s*[.!]*\s*$', re.I)


def words(s):
    return set(re.findall(r'[a-z0-9]{3,}', s.lower()))

def main():
    if not HL.vault_ok():
        return
    try:
        hook = json.loads(sys.stdin.read())
    except Exception:
        return
    prompt = (hook.get("prompt") or "").strip()
    sid = hook.get("session_id") or "nosession"
    proj = HL.project_for(hook.get("cwd", ""))
    if not prompt or TRIVIAL.match(prompt):
        return
    kw = {w for w in words(prompt) if w not in STOP}
    if len(kw) < 3:
        return

    rows = []
    for p in glob.glob(os.path.join(MEM, "*", "*.md")):
        b = os.path.basename(p)
        if b in EXCLUDE or b.startswith("_"):
            continue
        name = os.path.splitext(b)[0]
        folder = os.path.basename(os.path.dirname(p))
        try:
            head = open(p, errors="ignore").read(2048)   # cap read — hot path
        except Exception:
            continue
        m = re.search(r'^description:\s*(.+)$', head, re.M)
        desc = (m.group(1).strip().strip('"\'')) if m else ""
        nwords, dwords = words(name), words(desc)
        # DISTINCT query keywords matched as whole words in the high-signal head
        hit_name = kw & nwords
        hit_desc = kw & dwords
        head_hits = hit_name | hit_desc
        if len(head_hits) < 2:                # gate: kills generic single-word noise
            continue
        score = 5 * len(hit_name) + 3 * len(hit_desc)
        if proj and folder == proj:
            score = int(score * 1.5)
        rows.append((score, name, folder, desc[:110]))
    if not rows:
        return
    rows.sort(reverse=True)

    os.makedirs(STATE_DIR, exist_ok=True)
    sf = os.path.join(STATE_DIR, re.sub(r'[^A-Za-z0-9_-]', '_', sid) + ".json")
    seen = set(HL.read_json(sf, {}).get("injected", []))
    fresh = [r for r in rows if r[1] not in seen][:4]
    if not fresh:
        return

    out = ["=== Relevant memory (auto-recalled for this prompt) ==="]
    total = len(out[0]); picked = []
    for s, name, folder, desc in fresh:
        line = f"- [[{name}]] ({folder})" + (f" — {desc}" if desc else "")
        if total + len(line) > 1400:
            break
        out.append(line); total += len(line); picked.append(name)
    if not picked:
        return
    out.append("(Open a note or `/obsidian find <term>` for more. Recalled once per session.)")
    sys.stdout.write("\n".join(out) + "\n")

    try:
        HL.write_json(sf, {"injected": sorted(seen | set(picked)), "ts": int(time.time())})
        cutoff = time.time() - 7 * 86400
        for f in glob.glob(os.path.join(STATE_DIR, "*.json")):
            if os.path.getmtime(f) < cutoff:
                os.remove(f)
    except Exception as e:
        HL.log_err("memory-recall.state", e)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        HL.log_err("memory-recall", e)
