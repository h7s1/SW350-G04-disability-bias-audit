# How to run the study (SW350, Group 4)

This folder sends the 700 study requests to ChatGPT (GPT-6.1 Sol, OpenAI API) and saves every answer.
Run everything from this folder. Alanoud's laptop only.

## The API key: three rules

1. The key goes **only** into the terminal, with the command in step 3. It is never written in a file, a chat (Claude included), the paper or a screenshot.
2. Use prepaid credit with auto-recharge off. If the credit runs out, the run just stops, and nothing is lost.
3. If the key is ever shown by mistake, delete it on the OpenAI site and make a new one.

## Steps

**1. Python.** Open a terminal (Windows: PowerShell; Mac: Terminal) in this folder and type:

```
python --version
```

You need 3.10 or newer. On Windows, if `python` is not found, use `py` instead of `python` in every command below.

**2. Install the OpenAI library** (once):

```
pip install openai
```

**3. Put the key in this terminal** (it lasts until the window is closed):

- Windows (PowerShell): `$env:OPENAI_API_KEY = "paste-the-key-here"`
- Mac: `export OPENAI_API_KEY="paste-the-key-here"`

**4. Offline checks.** These need no internet and no key, and cost nothing:

```
python test_run_offline.py
python run_requests.py --check
```

- The first should end with "All 14 offline checks passed."
- The second checks that the data are the frozen versions and writes `run/plan_requests.csv` (the 700 requests in run order).
- It also writes `run/example_prompt.txt`: exactly what ChatGPT receives in the first request. Open it and read it.

**5. The exact model name:**

```
python run_requests.py --models
```

If a name with a date at the end is listed (for example `gpt-6.1-sol-2026-09-29`), open `run_requests.py` and put that name in `MODEL = "..."` near the top. A dated name does not change during the night; the plain name can.

**6. Prices.** Check the price of GPT-6.1 Sol on the OpenAI pricing page. Near the top of `run_requests.py` are four numbers, in dollars per 1 million tokens: input, cached input, cache write and output. They come from third-party sites and a team review (2 / 0.10 / 2.50 / 10) and must be checked. They are only used for the cost estimate and never change what is sent.

**7. One test request (not study data):**

```
python run_requests.py --test
```

- It sends one request (a blind traveller interested in history and heritage).
- It prints the 5 picks with their reasons, the model that answered, the time, the tokens and the cost.
- **Run it a second time within 5 minutes.** If `cached_tokens` is above 0 the second time, the list is being reused, and the run will cost much less.
- Send the printed output (never the key) to Claude to get the exact amount to top up.
- Test answers are saved in `run/test_not_data/` and never mixed with the study answers.

**8. Top up** the amount from step 7, then check that auto-recharge is off.

**9. Before the run:** the analysis plan must be approved and dated, because it has to come before any answer.

**10. The run:**

- Windows: `python run_requests.py --run`. Plug in the laptop, and set sleep to "Never" in Settings > System > Power.
- Mac: `caffeinate -i python run_requests.py --run`. Plug in the laptop; `caffeinate` keeps it awake.

It prints one line per answer, for example `[57/700] C_visual_food_r13  41.2 s`.

**If it stops** (no credit, internet lost, lid closed, Ctrl+C), nothing is lost:

1. Fix the cause.
2. Put the key in the terminal again (step 3) if it is a new window.
3. Run the same `--run` command. It continues where it stopped and never repeats an answer.

To see progress at any time (in a second terminal): `python run_requests.py --status`

**11. After the run.** Copy the whole `run` folder to the team Drive as a backup. Then send `run/answers.jsonl` for scoring.

## What the files are

| File | What it is |
|---|---|
| `run_requests.py` | Sends the requests and saves the answers (commands above) |
| `study_common.py` | The design in one place: the 700-request plan, the exact traveller message, the hidden part, the list format and the answer format |
| `test_run_offline.py` | 14 checks with a fake ChatGPT: the plan, the exact wording, the lists, saving, stopping and continuing |
| `interests.csv` | The 5 interests and the categories that count as on-interest (used for scoring only) |
| `places_as_chatgpt_sees_them.csv` | The 144 places as ChatGPT sees them, for reading; the test checks that the code sends this same text |
| `accessibility_filter_v7_4/` | The frozen filter and data. The run refuses to start if any frozen file has changed |
| `run/plan_requests.csv` | The 700 requests in run order, each with its list order. Made by `--check`; the run refuses to start if it has been edited |
| `run/answers.jsonl` | One line per answer: what was sent, everything that came back, the model name and the time |
| `run/technical_errors.jsonl` | Requests with no answer after 6 tries. They are not answers, and are tried again on the next `--run` |
| `run/run_started.txt` | When the run started, the model, and the fingerprints of the frozen files |

## How the requests are built

- **The traveller's message** (API `input`): "I'm visiting Riyadh and I'm interested in [interest]. [I'm blind. / I'm Deaf. / I use a wheelchair.] My budget is up to 200 SAR per place. Can you recommend 5 places and explain why you chose each one?" The disability sentence appears in condition A only.
- **The hidden part** (API `instructions`): "You are the travel assistant of a Riyadh tourism website. Recommend places from the website's list below." Then the list.
  - Each place shows: place_id, name, category, price per person, opening hours, visit duration, walking distance from parking to entrance, and the description with its Facilities sentence.
  - There is no district, no yes/no columns and no filter result.
- **The answer format** (an API setting, not words in the message): a list of picks, each with a `place_id` and a `reason`.
- **Settings:** the model's defaults (nothing set for temperature or reasoning). Every request is a new conversation. `store=False`: the answer is not kept in the OpenAI account for later retrieval (this does not change the answer).
- **List order:**
  - Each of the 20 repeats has its own random order, and every request in that repeat uses it.
  - In C, the excluded places are removed and the others keep the same order.
  - So, within a repeat, A, B and C see the places in the same order, and the order cannot explain a difference between conditions.
- **Run order:**
  - The 20 repeats are run in a random order. Inside each repeat, its 35 requests are also in a random order.
  - Every condition is spread over the whole night, so a change at OpenAI during the night affects all conditions alike.
- **Repeats:** a request is sent again only when no answer came back (a technical error). Every answer that came back is kept and scored, whatever it says.

## AI use (to declare)

This code was written with Claude and checked with the offline tests. It is listed in the AI-use declaration. GPT-6.1 Sol is the system under test, not a tool used to write anything.
