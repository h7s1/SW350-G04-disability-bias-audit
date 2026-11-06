"""Send the 300 group D requests to ChatGPT and save every answer. SW350 Group 4.

  python run_d.py --check     no internet: checks the frozen data, writes run_D/plan_requests.csv and
                              run_D/example_prompt.txt (the first D request, exactly as it is sent)
  python run_d.py --run       the 300 D requests; safe to stop and start again (it continues)
  python run_d.py --status    progress and estimated cost

The sending code is Study 1's run_requests.py, unchanged (same model, same settings, same retries, same
records). This file only points it to the group D plan (groupd.py) and to the run_D folder.
"""
import argparse
import contextlib
import hashlib
import io
import sys

import study_common as S
import groupd as G

S.RUN_DIR = G.RUN_DIR                       # answers go to run_D/, never to Study 1's run/
S.build_plan = G.build_plan_d               # the 300 D requests instead of Study 1's 700
S.traveller_message = G.traveller_message_d  # A's message (with the disability sentence) for D

import run_requests as R  # noqa: E402  (imported after the three lines above, on purpose)

D_FILES = ["groupd.py", "run_d.py", "PLAN_D.md", "study_common.py", "run_requests.py"]


def write_d_info():
    """Once, when the D run starts: the time and the fingerprints of the files that decide what is sent."""
    info = G.RUN_DIR / "groupD_started.txt"
    if info.exists():
        return
    lines = [f"Group D run started: {R.now()}", f"Model: {R.MODEL}"]
    for name in D_FILES:
        lines.append(f"{name} SHA-256: {hashlib.sha256((S.HERE / name).read_bytes()).hexdigest()}")
    info.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_check():
    """Study 1's --check, for the D plan. Its messages say run/; for D the files are in run_D/."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        R.cmd_check()
    print(buf.getvalue().replace("-> run/plan_requests.csv", "-> run_D/plan_requests.csv")
          .replace("Places sent in C:", "Places sent in C and D:"), end="")


def cmd_run():
    G.RUN_DIR.mkdir(exist_ok=True)
    if not [a for a in R.read_lines(R.ANSWERS) if a.get("kind") == "answer"]:
        S.check_frozen()
        write_d_info()
    R.cmd_run()


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    if sys.version_info < (3, 10):
        raise SystemExit("Python 3.10 or newer is needed.")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    for name in ("check", "run", "status"):
        g.add_argument("--" + name, action="store_true")
    a = ap.parse_args()
    {"check": cmd_check, "run": cmd_run, "status": R.cmd_status}[next(k for k, v in vars(a).items() if v)]()


if __name__ == "__main__":
    main()
