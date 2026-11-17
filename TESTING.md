# WaterBuddy verification record

Date: 17 November 2026
Environment: Python 3.12, Streamlit 1.51.0.

## Completed tests

Command: `python -m unittest discover -s WaterBuddy-1000700 -v`
(or `python -m unittest -v` from inside the project directory).

**Result: 5 test methods passed, including the subcases below.**

| Scenario | Verified result |
|---|---|
| Four age groups | Correct defaults: 1200 / 1700 / 2250 / 1850 ml |
| Quick button twice | 500 ml total |
| Custom entry after quick logs | 500 + 750 = 1250 ml |
| Zero, negatives, text, blank, oversized amount | Error; total unchanged |
| Decimal, NaN and infinity inputs | Rejected by validation |
| 50%, 75%, 100% | Correct message and expression selection |
| Logging above goal | True total and percentage retained; visual fill capped |
| Goal edited during session | Remaining and percentage recalculate immediately |
| New Day cancelled | Intake preserved |
| New Day confirmed | Intake, entries and milestones cleared; goal retained |
| Several logs | Displayed metrics match the accumulated total on each rerun |
| Repeat logs after goal | No duplicate milestone announcement |
| New independent session | Separate default state, without another session's intake |
| Zero goal passed directly to calculation | Raises ValueError before division |

Interaction tests use Streamlit's AppTest to operate real application widgets
and inspect rendered element values. These are automated local checks, not a
claim of testing by classmates or public users.

## Remaining verification

Desktop and mobile visual inspection could not be completed in this execution
environment: browser launch was blocked, and a browser download failed. Native
Streamlit columns and a 640 px CSS breakpoint are implemented, but no browser
layout pass is claimed. Public GitHub contents and Streamlit Cloud deployment
have not been verified.

After deploying, check the actual app at desktop width and on a phone:

- Confirm labels, bottle, Pip, cards and buttons are visible without clipping.
- Verify keyboard navigation and visible focus on interactive controls.
- Test +250 ml and custom 350 ml, then invalid 0 and text.
- Set a 1000 ml goal; log to 500, 750, 1000 and 1250 ml.
- Confirm percentage and remaining update; the bottle stops at full.
- Try Cancel and Confirm in the New Day confirmation.
- Open a separate private window to verify an independent new session.
- Check that the actual public URL opens for someone who is not signed in.

Do not describe these remaining checks as passed until performed.
