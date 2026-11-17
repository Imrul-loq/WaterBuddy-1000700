"""WaterBuddy — a session-based hydration project for a Python programming assessment."""
from datetime import date
from pathlib import Path
import streamlit as st

AGE_GOALS = {
    "Children (4–8)": 1200,
    "Teens (9–13)": 1700,
    "Adults (14–64)": 2250,
    "Seniors (65+)": 1850,
}
TIPS = ["Keep your water bottle somewhere easy to see.",
        "Take a water break between your everyday tasks.",
        "Keep water nearby while you study."]


def calculate_progress(total, goal):
    """Keep the true percentage; cap only the visual fill."""
    if goal <= 0 or total < 0:
        raise ValueError("Goal must be positive and total cannot be negative.")
    percentage = total / goal * 100
    return max(goal - total, 0), percentage, min(percentage, 100)


def parse_amount(value):
    """Accept whole millilitres only, with a practical per-entry limit."""
    try:
        amount = int(str(value).strip())
    except (ValueError, TypeError):
        raise ValueError("Enter a whole number from 1 to 2,000 ml.") from None
    if not 1 <= amount <= 2000:
        raise ValueError("Enter a whole number from 1 to 2,000 ml.")
    return amount


def reaction(percent):
    if percent >= 100:
        return "celebrate", "You reached your goal! Amazing work!"
    if percent >= 75:
        return "wave", "Almost there! Keep it going."
    if percent >= 50:
        return "smile", "Halfway there! You're doing great."
    return "calm", "A little progress is still progress!"


def set_age_goal():
    st.session_state.goal_ml = AGE_GOALS[st.session_state.age_group]


def log_water(value):
    """Callbacks run before the screen redraws, so every value updates together."""
    try:
        amount = parse_amount(value)
    except ValueError as error:
        st.session_state.notice = ("error", str(error))
        return
    state = st.session_state
    before = state.total_ml / state.goal_ml * 100
    state.total_ml += amount
    state.entries.append(amount)
    after = state.total_ml / state.goal_ml * 100
    crossed = [point for point in (50, 75, 100)
               if before < point <= after and point not in state.celebrated]
    state.celebrated.update(crossed)
    message = f"Added {amount:,} ml."
    if crossed:
        message += f" A new milestone: {max(crossed)}%!"
    state.notice = ("success", message)


def log_custom():
    log_water(st.session_state.custom_ml)


def request_reset():
    st.session_state.confirm_reset = True


def cancel_reset():
    st.session_state.confirm_reset = False


def reset_day():
    st.session_state.total_ml = 0
    st.session_state.entries = []
    st.session_state.celebrated = set()
    st.session_state.confirm_reset = False
    st.session_state.notice = ("success", "New day, fresh start. Your goal stays the same.")


def pip_svg(mood):
    """Original SVG drawing; expression and arms follow the Python milestone."""
    mouth = '<path d="M83 122 Q100 132 117 122"/>'
    arms = '<path d="M53 122 L36 131 M147 122 L164 131"/>'
    extras = ""
    if mood in ("smile", "wave", "celebrate"):
        mouth = '<path d="M82 120 Q100 145 118 120"/>'
    if mood in ("wave", "celebrate"):
        arms = '<path d="M53 122 L36 132 M147 122 Q165 115 166 94"/>'
    if mood == "celebrate":
        arms = '<path d="M53 122 L32 95 M147 122 L168 95"/>'
        extras = '<path stroke="#b99b60" d="M28 64 l8 5 M169 57 l-5 10 M44 43 l3 8 M153 35 l-4 8"/>'
    return f'''<svg viewBox="0 0 200 190" role="img" aria-label="Pip: {mood}">
    <ellipse cx="100" cy="175" rx="48" ry="6" fill="#dbe8e5"/>
    <path d="M100 17 C88 44 47 80 47 116 A53 53 0 0 0 153 116 C153 80 112 44 100 17Z" fill="#a5d9da" stroke="#28505b" stroke-width="2"/>
    <path d="M78 69 Q63 87 62 101" fill="none" stroke="#eefafa" stroke-width="7" stroke-linecap="round"/>
    <g fill="none" stroke="#173747" stroke-width="3.5" stroke-linecap="round">{arms}{mouth}{extras}</g>
    <circle cx="80" cy="109" r="4" fill="#173747"/><circle cx="120" cy="109" r="4" fill="#173747"/>
    </svg>'''


def main():
    st.set_page_config(page_title="WaterBuddy | One Sip Counts", page_icon="💧", layout="wide")
    st.markdown(f"<style>{Path(__file__).with_name('style.css').read_text()}</style>", unsafe_allow_html=True)
    defaults = dict(age_group="Adults (14–64)", goal_ml=2250, total_ml=0,
                    entries=[], celebrated=set(), confirm_reset=False, notice=None)
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    state = st.session_state
    st.markdown('<div class="brand">waterbuddy<span>ONE SIP COUNTS</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">YOUR DAILY HYDRATION COMPANION</div><h1>Small sips.<br>Better habits.</h1><p class="intro">A little water. A moment for yourself. Every sip matters.</p>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('### 01 · Your daily goal')
        age, goal = st.columns(2)
        with age:
            st.selectbox("Choose your age group", list(AGE_GOALS), key="age_group", on_change=set_age_goal)
        with goal:
            st.number_input("Your daily goal (ml)", min_value=250, max_value=5000,
                            step=50, key="goal_ml")
        st.caption(f"Suggested project target: {AGE_GOALS[state.age_group]:,} ml · Your chosen goal: {state.goal_ml:,} ml")
        st.caption("These are FA-1 learning defaults, not personal medical recommendations. This app records drinking water only. You can adjust the goal.")
    left, right = st.columns([1.6, 1], gap="large")
    remaining, percentage, fill = calculate_progress(state.total_ml, state.goal_ml)
    mood, message = reaction(percentage)
    with left:
        with st.container(border=True):
            st.markdown('### 02 · Today’s hydration')
            st.markdown(f'<div class="progress-hero"><div><span class="eyebrow">OF YOUR CHOSEN GOAL</span><div class="big-number">{percentage:.1f}<span>%</span></div><p>{state.total_ml:,} / {state.goal_ml:,} ml</p></div><div class="bottle" role="img" aria-label="Bottle {fill:.1f} percent full"><div class="water" style="height:{fill}%"></div><div class="bottle-lines"></div></div></div>', unsafe_allow_html=True)
            st.progress(fill / 100)
            a, b = st.columns(2)
            a.metric("Consumed", f"{state.total_ml:,} ml")
            b.metric("Remaining", f"{remaining:,} ml")
            if percentage >= 100:
                st.caption("Goal reached. There is no need to drink extra to fill the bar further.")
        with st.container(border=True):
            st.markdown('### 03 · Log your water')
            st.button("+250 ml", key="quick_log", type="primary", use_container_width=True,
                      on_click=log_water, args=(250,))
            with st.form("custom_log", clear_on_submit=True):
                st.text_input("Custom amount (ml)", placeholder="For example, 350", key="custom_ml")
                st.form_submit_button("Add water", on_click=log_custom, use_container_width=True)
            st.caption("Whole millilitres, 1–2,000 per entry. Log what you actually drank.")
            if state.notice:
                kind, text = state.notice
                if kind == "error":
                    st.error(text)
                else:
                    st.success(text)
    with right:
        with st.container(border=True):
            st.markdown('### Your little cheerleader')
            st.markdown(f'<div class="pip">{pip_svg(mood)}</div><div class="pip-caption"><span class="eyebrow">MEET PIP</span><h3>{message}</h3><p>Small steps count, at your own pace.</p></div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('### A gentle reminder')
            st.write(TIPS[date.today().toordinal() % len(TIPS)])
        with st.expander("Your session summary"):
            st.write(f"{len(state.entries)} entries · {state.total_ml:,} ml logged")
            if state.entries:
                st.write(" + ".join(f"{amount:,}" for amount in state.entries) + " ml")
            else:
                st.write("Ready for your first sip? Your entries will appear here.")
    st.divider()
    st.markdown('### Ready for a fresh day?')
    st.caption("New Day clears your intake and entries, keeping your age group and goal.")
    st.button("New Day", on_click=request_reset)
    if state.confirm_reset:
        st.warning("Start a new day? Today's logged water will be cleared.")
        confirm, cancel = st.columns(2)
        confirm.button("Confirm new day", type="primary", on_click=reset_day, use_container_width=True)
        cancel.button("Cancel", on_click=cancel_reset, use_container_width=True)
    st.caption("No account needed · Data lasts for this active session only; refreshing or closing the tab may clear it. Start a new day manually.")
    st.markdown('<div class="footer">WATERBUDDY · ONE SIP COUNTS<span>Python programming project</span></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
