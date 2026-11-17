# WaterBuddy — One Sip Counts

A calm, session-based hydration companion built with Python and Streamlit.

**Python programming project**

## What it does

- Suggests an age-based project goal, with an editable daily goal.
- Logs a quick 250 ml or a custom whole-number amount.
- Updates total, remaining water, actual percentage, progress bar and bottle together.
- Changes Pip's expression at 50%, 75% and 100%.
- Announces a milestone once per session day when a log crosses it.
- Confirms a New Day reset and keeps the selected age and goal.
- Provides a session summary and a rotating daily tip.

The FA-1 defaults are Children 4–8: 1,200 ml; Teens 9–13: 1,700 ml;
Adults 14–64: 2,250 ml; Seniors 65+: 1,850 ml. These categories and amounts
preserve the storyboard's examples; they are instructional values, not medical
prescriptions. Drinking water logged here is different from total water from
food and all beverages. The adjustable range of 250–5,000 ml is a software
input limit, not a recommended intake range.

## Run on your computer

Use Python 3.12. In a terminal inside this folder:

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. No API key or paid service is needed.

## Files

| File | Purpose |
|---|---|
| `app.py` | Python calculations, callbacks, native widgets and SVG Pip |
| `style.css` | Ivory, navy and aqua styling with responsive rules |
| `.streamlit/config.toml` | Streamlit theme and telemetry setting |
| `requirements.txt` | Exact Streamlit version tested |
| `test_app.py` | Repeatable calculation and interaction tests |
| `TESTING.md` | Actual test results and remaining deployment checks |

## How the Python works

1. `AGE_GOALS` is a dictionary mapping an age group to its suggested goal.
2. `st.session_state` remembers the chosen goal, total, entries and reset status
   during an active session. Different visitors have separate sessions.
3. `parse_amount()` rejects empty values, text, decimals, zero, negative values
   and entries above 2,000 ml. Failed inputs leave the total unchanged.
4. `log_water()` adds the amount and records the entry. Its callback executes
   before Streamlit redraws the page, so the numbers and graphics stay in sync.
5. `calculate_progress()` returns:
   - `remaining = max(goal - total, 0)`
   - `percentage = total / goal * 100`
   - `visual_fill = min(percentage, 100)`
6. `reaction()` uses `if` conditions to select Pip's expression and message.
7. `reset_day()` clears intake only after confirmation. `Cancel` preserves it.

Example: with a 2,250 ml goal, logging 500 + 750 ml gives 1,250 ml consumed,
1,000 ml remaining and 55.6% progress. At 2,500 ml, the true percentage is
111.1%, remaining is zero, and the bottle and bar stay full.

Changing the age group loads that group's default; changing the numeric goal
keeps existing intake and recalculates immediately. The mascot reflects current
progress even after goal edits. Milestone announcements occur on logging, not
on editing a goal, and do not repeat for an already celebrated threshold.

## From FA-1 to FA-2

The original plan's age defaults, dashboard, quick logging, four Pip reactions,
over-goal rule and safe reset have been preserved. Streamlit replaces the
planned Tkinter UI because the FA-2 brief requires a web application. Inline
SVG replaces Turtle so the mascot works in a browser without a desktop window.
The page combines the storyboard's screens into one responsive flow.

## Upload to your existing GitHub repository

1. Extract the ZIP on Windows using **Extract All**.
2. Open your existing `WaterBuddy-1000700` repository on GitHub.
3. Choose **Add file → Upload files**.
4. Drag the contents of the extracted project folder into the upload area.
   Upload `app.py` and `requirements.txt` at the repository root, not inside a
   second `WaterBuddy-1000700` folder. Replace the earlier starter `app.py`.
5. Include `style.css`, `.streamlit/config.toml`, README, tests and testing notes.
   If the `.streamlit` folder is omitted by your file picker, use
   **Add file → Create new file**, name it `.streamlit/config.toml`, and paste
   the contents from the included config file.
6. Add a commit message such as `Complete WaterBuddy FA-2 app` and commit.
7. Confirm that your repository is public and all required files are visible.

## Deploy on Streamlit Community Cloud

1. Visit https://share.streamlit.io/ and sign in with the relevant GitHub account.
2. Choose **Create app** and select deployment from GitHub.
3. Select your `WaterBuddy-1000700` repository and the actual branch containing
   these files (usually `main`). Set the entrypoint to `app.py`.
4. In advanced settings choose Python 3.12, then deploy.
5. When the public app opens, test quick/custom logging, goal edits, both reset
   choices, and a narrow phone layout. Copy the actual working public URL.

Official deployment guide:
https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

Dependency guide:
https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies

If the build fails, inspect its log. Check that `app.py`, `requirements.txt` and
`style.css` are in the same root folder and that the branch/path are correct.

## Privacy and limits

There is no application database or login. Intake is held in server memory
through Streamlit session state, not permanently saved on the user's device.
Refreshing, closing a tab or restarting the server may clear it. New Day is
manual, not an automatic midnight rollover. Google Fonts may load externally;
Georgia and Arial are fallback fonts if unavailable. No reminders or medical
personalisation are claimed.

## Assessment and submission status

Local implementation and tests are complete as described in TESTING.md.
The complete project is prepared for the public repository:
https://github.com/Imrul-loq/WaterBuddy-1000700

Public Streamlit deployment is still pending verification.
No public URL is invented. After deployment, the final FA-2 submission PDF
should include the actual GitHub URL, public Streamlit URL and FA-1 storyboard
link, plus a short features/calculations/testing summary. Review the code and
follow your school's policy for acknowledging AI-assisted development.
