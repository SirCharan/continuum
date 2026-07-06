#!/usr/bin/env python3
"""Shared helpers for the memory hooks. Python 3.9-safe, stdlib-only.
Import works because Python puts the running script's dir on sys.path[0]."""
import os, tempfile, time, traceback

MEM = os.environ.get("CLAUDE_MEMORY_DIR") or os.path.expanduser("~/.claude/memory")
ERRLOG = os.path.expanduser("~/.claude/hooks/hook-errors.log")

def vault_ok():
    """True only if the memory dir is present — hooks no-op cleanly otherwise."""
    return os.path.isdir(MEM)

def atomic_write(path, text):
    """Write via temp file in the same dir + os.replace so a concurrent reader
    never sees a truncated/partial file. Returns True on success."""
    d = os.path.dirname(path) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp-", suffix=".swap")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
        os.replace(tmp, path)
        return True
    except Exception:
        try: os.unlink(tmp)
        except Exception: pass
        raise

def read_json(path, default=None):
    import json
    try:
        with open(path, errors="ignore") as f:
            return json.load(f)
    except Exception:
        return {} if default is None else default

def write_json(path, obj):
    import json
    atomic_write(path, json.dumps(obj))

def log_err(hook, exc):
    """Append one capped line to hook-errors.log; never raises. Keeps the log bounded."""
    try:
        line = "%s\t%s\t%s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), hook,
                                 (repr(exc) if not isinstance(exc, str) else exc)[:300])
        with open(ERRLOG, "a") as f:
            f.write(line)
        # trim if it grows past ~500 lines
        if os.path.getsize(ERRLOG) > 120_000:
            with open(ERRLOG, errors="ignore") as f:
                tail = f.readlines()[-300:]
            atomic_write(ERRLOG, "".join(tail))
    except Exception:
        pass

def tail_lines(path, max_bytes=262144):
    """Return the last ~max_bytes of a (possibly huge) file as a list of complete lines.
    Drops the first partial line. For reading the end of a 20MB+ transcript cheaply."""
    try:
        sz = os.path.getsize(path)
        with open(path, "rb") as f:
            if sz > max_bytes:
                f.seek(sz - max_bytes)
            chunk = f.read()
        text = chunk.decode("utf-8", errors="ignore")
        lines = text.split("\n")
        if sz > max_bytes and len(lines) > 1:
            lines = lines[1:]  # drop partial first line
        return lines
    except Exception:
        return []


import json as _json
def project_for(cwd):
    """Derive a project key from cwd. Default = the cwd basename (lowercased).
    Optional override: CLAUDE_PROJECT_MAP env = JSON {basename: project}."""
    if not cwd:
        return None
    b = os.path.basename(cwd.rstrip("/")).lower()
    if not b:
        return None
    try:
        m = _json.loads(os.environ.get("CLAUDE_PROJECT_MAP", "") or "{}")
        if b in m:
            return m[b]
    except Exception:
        pass
    return b
