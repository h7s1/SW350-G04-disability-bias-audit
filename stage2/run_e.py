"""Send the 1,000 Study 2 requests (E1 and E2) to ChatGPT and save every answer. SW350 Group 4.

  python run_e.py --check     no internet: checks the frozen data, writes run_E/plan_requests.csv and
                              run_E/example_prompt.txt (the first request, exactly as it is sent)
  python run_e.py --run       the 1,000 requests; safe to stop and start again (it continues)
  python run_e.py --status    progress and estimated cost

The sending code is Study 1's run_requests.py, unchanged (same model, same settings, same retries, same
records). This file only points it to the Study 2 plan (e_common.py) and to the run_E folder.
"""
import argparse
import contextlib
import hashlib
import io
import sys

import study_common as S
import e_common as E

S.RUN_DIR = E.RUN_DIR                            # answers go to run_E/, never to Study 1's run/
S.build_plan = E.build_plan_e                    # the 1,000 Study 2 requests instead of Study 1's 700
S.traveller_message = E.traveller_message_e      # told / not told
S.hidden_instructions = E.hidden_instructions_e  # E1: fully usable places; E2: no Facilities sentence

import run_requests as R  # noqa: E402  (imported after the lines above, on purpose)

E_FILES = ["e_common.py", "run_e.py", "PLAN_E.md", "study_common.py", "run_requests.py"]


def write_e_info():
    info = E.RUN_DIR / "study2_started.txt"
    if info.exists():
        return
    lines = [f"Study 2 run started: {R.now()}", f"Model: {R.MODEL}"]
    for name in E_FILES:
        lines.append(f"{name} SHA-256: {hashlib.sha256((S.HERE / name).read_bytes()).hexdigest()}")
    info.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_check():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        R.cmd_check()
    print(buf.getvalue().replace("-> run/plan_requests.csv", "-> run_E/plan_requests.csv")
          .replace("Places sent in C:", "Places in Study 1's filtered lists (for reference):"), end="")
    print("Places in E1's lists (fully usable only):", {d: len(v) for d, v in E.FULLY_USABLE.items()})


def cmd_run():
    E.RUN_DIR.mkdir(exist_ok=True)
    if not [a for a in R.read_lines(R.ANSWERS) if a.get("kind") == "answer"]:
        S.check_frozen()
        write_e_info()
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
