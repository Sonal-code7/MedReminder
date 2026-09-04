import streamlit as st
from datetime import datetime, date, time
import json
from pathlib import Path
import streamlit.components.v1 as components

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MedReminder",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SESSION STATE
# =========================================================

if "reminders" not in st.session_state:
    st.session_state.reminders = [
        {
            "id": 1,
            "name": "Vitamin D",
            "dosage": "1000 IU",
            "time": time(9, 0),
            "frequency": "Daily",
            "instructions": "After breakfast",
            "taken": True,
            "date": date.today()
        },
        {
            "id": 2,
            "name": "Paracetamol",
            "dosage": "500 mg",
            "time": time(20, 0),
            "frequency": "Daily",
            "instructions": "After food",
            "taken": False,
            "date": date.today()
        }
    ]

if "next_id" not in st.session_state:
    st.session_state.next_id = 3

if "streak" not in st.session_state:
    st.session_state.streak = 7

if "history" not in st.session_state:
    st.session_state.history = []


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: #f8fafc;
}

/* Remove top padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Main title */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
    margin-top: 5px;
}

/* Stat cards */
.stat-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.05);
    transition: 0.25s ease;
}

.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.08);
}

.stat-icon {
    font-size: 28px;
}

.stat-number {
    font-size: 30px;
    font-weight: 800;
    color: #0f172a;
}

.stat-label {
    color: #64748b;
    font-size: 14px;
}

/* Medicine cards */
.medicine-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
}

.medicine-name {
    font-size: 19px;
    font-weight: 700;
    color: #0f172a;
}

.medicine-info {
    color: #64748b;
    font-size: 14px;
    margin-top: 5px;
}

/* Next medicine */
.next-card {
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    border-radius: 22px;
    padding: 30px;
    color: white;
    box-shadow: 0 10px 30px rgba(37, 99, 235, 0.25);
}

.next-label {
    font-size: 13px;
    font-weight: 600;
    opacity: 0.8;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.next-name {
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

.next-time {
    font-size: 17px;
    opacity: 0.9;
}

/* Section headings */
.section-title {
    font-size: 23px;
    font-weight: 750;
    color: #0f172a;
    margin-top: 30px;
    margin-bottom: 15px;
}

/* Progress */
.progress-container {
    background: #172033 !important;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 24px;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    border: none;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
}

/* Form */
[data-testid="stForm"] {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
}

/* Divider */
hr {
    border-color: #e2e8f0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🩺 MedReminder")
    st.caption("Your medication companion")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "💊 Medicines",
            "📊 Analytics",
            "📅 History"
        ]
    )

    st.divider()

    st.markdown("### 💡 Did you know?")
    st.caption(
        "Keeping a consistent medication schedule "
        "can make it easier to remember daily doses."
    )

    st.divider()

    st.caption("MedReminder v2.0")
    st.caption("Built with Python + Streamlit")


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def format_time(t):
    return t.strftime("%I:%M %p").lstrip("0")


def get_progress():

    total = len(st.session_state.reminders)

    if total == 0:
        return 0

    taken = sum(
        1 for r in st.session_state.reminders
        if r["taken"]
    )

    return int((taken / total) * 100)


def get_next_medicine():

    upcoming = [
        r for r in st.session_state.reminders
        if not r["taken"]
    ]

    if not upcoming:
        return None

    upcoming.sort(key=lambda x: x["time"])

    return upcoming[0]


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    now = datetime.now()

    greeting = "Good morning"

    if now.hour >= 12:
        greeting = "Good afternoon"

    if now.hour >= 18:
        greeting = "Good evening"

    st.markdown(
        f'<div class="main-title">{greeting} 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Here is your medication overview for today.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # -------------------------------
    # STATISTICS
    # -------------------------------

    total = len(st.session_state.reminders)

    taken = sum(
        1 for r in st.session_state.reminders
        if r["taken"]
    )

    remaining = total - taken

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">💊</div>
                <div class="stat-number">{total}</div>
                <div class="stat-label">Scheduled today</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">✅</div>
                <div class="stat-number">{taken}</div>
                <div class="stat-label">Medicines taken</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">⏳</div>
                <div class="stat-number">{remaining}</div>
                <div class="stat-label">Remaining</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">🔥</div>
                <div class="stat-number">{st.session_state.streak}</div>
                <div class="stat-label">Day streak</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------
    # NEXT MEDICINE
    # -------------------------------

    st.markdown(
        '<div class="section-title">⏰ Next Medicine</div>',
        unsafe_allow_html=True
    )

    next_med = get_next_medicine()

    if next_med:

        st.markdown(
            f"""
            <div class="next-card">
                <div class="next-label">Upcoming medication</div>
                <div class="next-name">💊 {next_med["name"]}</div>
                <div class="next-time">
                    🕘 {format_time(next_med["time"])}
                    &nbsp; • &nbsp;
                    {next_med["dosage"]}
                </div>
                <br>
                <div>{next_med["instructions"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "✓  Mark as Taken",
            key=f"dashboard_take_{next_med['id']}",
            use_container_width=True
        ):
            next_med["taken"] = True
            st.session_state.history.append({
                "name": next_med["name"],
                "time": datetime.now(),
                "status": "Taken"
            })
            st.rerun()

    else:

        st.success(
            "🎉 All medicines for today have been completed!"
        )

    # -------------------------------
    # PROGRESS
    # -------------------------------

    st.markdown(
        '<div class="section-title">📈 Today\'s Progress</div>',
        unsafe_allow_html=True
    )

    progress = get_progress()

    st.markdown(
        f"""
        <div class="progress-container">
            <b>Medication adherence</b>
            <br><br>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(progress / 100)

    st.markdown(
        f"**{progress}% completed**",
        unsafe_allow_html=True
    )

    # -------------------------------
    # TODAY'S SCHEDULE
    # -------------------------------

    st.markdown(
        '<div class="section-title">📅 Today\'s Schedule</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.reminders:

        st.info(
            "No medicines scheduled. "
            "Go to 💊 Medicines to add one."
        )

    else:

        sorted_reminders = sorted(
            st.session_state.reminders,
            key=lambda x: x["time"]
        )

        for reminder in sorted_reminders:

            status = "✅ Taken" if reminder["taken"] else "⏳ Upcoming"

            col1, col2 = st.columns([5, 1])

            with col1:

                st.markdown(
                    f"""<div class="medicine-card">
                <div class="medicine-name">💊 {reminder["name"]}</div>
                <div class="medicine-info">
                🕘 {format_time(reminder["time"])}
                &nbsp; • &nbsp;
                {reminder["dosage"]}
                &nbsp; • &nbsp;
                {reminder["frequency"]}
                </div>
                </div>""",
                     unsafe_allow_html=True
                )


# =========================================================
# MEDICINES PAGE
# =========================================================

elif page == "💊 Medicines":

    st.markdown(
        '<div class="main-title">💊 Medicines</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Manage your medication schedule.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # -------------------------------
    # ADD MEDICINE
    # -------------------------------

    st.subheader("➕ Add Medicine")

    with st.form("add_medicine"):

        col1, col2 = st.columns(2)

        with col1:

            medicine_name = st.text_input(
                "Medicine name",
                placeholder="e.g. Paracetamol"
            )

            dosage = st.text_input(
                "Dosage",
                placeholder="e.g. 500 mg"
            )

            instructions = st.text_input(
                "Instructions",
                placeholder="e.g. After food"
            )

        with col2:

            medicine_time = st.time_input(
                "Reminder time",
                value=time(20, 0)
            )

            frequency = st.selectbox(
                "Frequency",
                [
                    "Daily",
                    "Once",
                    "Weekdays",
                    "Weekends"
                ]
            )

        submitted = st.form_submit_button(
            "➕ Add Reminder",
            use_container_width=True
        )

        if submitted:

            if not medicine_name.strip():

                st.warning(
                    "Please enter a medicine name."
                )

            else:

                st.session_state.reminders.append(
                    {
                        "id": st.session_state.next_id,
                        "name": medicine_name,
                        "dosage": dosage or "Not specified",
                        "time": medicine_time,
                        "frequency": frequency,
                        "instructions": instructions or "No instructions",
                        "taken": False,
                        "date": date.today()
                    }
                )

                st.session_state.next_id += 1

                st.success(
                    f"✅ {medicine_name} has been added!"
                )

    # -------------------------------
    # ACTIVE MEDICINES
    # -------------------------------

    st.markdown(
        '<div class="section-title">📋 Active Reminders</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.reminders:

        st.info(
            "No active reminders yet."
        )

    else:

        for reminder in st.session_state.reminders:

            col1, col2, col3 = st.columns([5, 1, 1])

            with col1:

                st.markdown(
                    f"""<div class="medicine-card">
               <div class="medicine-name">💊 {reminder["name"]}</div>
               <div class="medicine-info">
               🕘 {format_time(reminder["time"])}
                &nbsp; • &nbsp;
               💊 {reminder["dosage"]}
                &nbsp; • &nbsp;
                🔁 {reminder["frequency"]}
                </div>
                <div class="medicine-info">
                ℹ️ {reminder["instructions"]}
                </div>
                </div>""",
                    unsafe_allow_html=True
                )

            with col2:

                if reminder["taken"]:

                    st.success("Taken")

                else:

                    if st.button(
                        "✓ Take",
                        key=f"take_{reminder['id']}"
                    ):
                        reminder["taken"] = True

                        st.session_state.history.append({
                            "name": reminder["name"],
                            "time": datetime.now(),
                            "status": "Taken"
                        })

                        st.rerun()

            with col3:

                if st.button(
                    "🗑️",
                    key=f"delete_{reminder['id']}"
                ):

                    st.session_state.reminders.remove(
                        reminder
                    )

                    st.rerun()


# =========================================================
# ANALYTICS PAGE
# =========================================================

elif page == "📊 Analytics":

    st.markdown(
        '<div class="main-title">📊 Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Understand your medication consistency.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    progress = get_progress()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Today's adherence",
            f"{progress}%"
        )

    with col2:

        st.metric(
            "Current streak",
            f"{st.session_state.streak} days"
        )

    with col3:

        st.metric(
            "Total medicines",
            len(st.session_state.reminders)
        )

    st.divider()

    st.subheader("📈 Today's Adherence")

    st.progress(progress / 100)

    if progress == 100:

        st.success(
            "Excellent! All scheduled medicines are completed."
        )

    elif progress >= 50:

        st.info(
            "You're making good progress today."
        )

    else:

        st.warning(
            "You still have medicines remaining today."
        )

    st.subheader("🔥 Consistency")

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-icon">🔥</div>
            <div class="stat-number">
                {st.session_state.streak} days
            </div>
            <div class="stat-label">
                Current medication streak
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("💡 Insight")

    if progress >= 80:

        st.success(
            "Your adherence today is strong. Keep maintaining the routine!"
        )

    else:

        st.info(
            "Try checking your reminder schedule regularly "
            "to avoid missing doses."
        )


# =========================================================
# HISTORY PAGE
# =========================================================

elif page == "📅 History":

    st.markdown(
        '<div class="main-title">📅 Medication History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Review your recorded medication activity.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if not st.session_state.history:

        st.info(
            "No medication history recorded yet."
        )

    else:

        for item in reversed(st.session_state.history):

            st.markdown(
                f"""<div class="medicine-card">
            <div class="medicine-name">✅ {item["name"]}</div>
            <div class="medicine-info">
            🕘 {item["time"].strftime("%d %b %Y, %I:%M %p")}
            &nbsp; • &nbsp;
            {item["status"]}
            </div>
            </div>""",
                 unsafe_allow_html=True
            )
    st.divider()

    st.subheader("📌 Today's Summary")

    total = len(st.session_state.reminders)

    taken = sum(
        1
        for r in st.session_state.reminders
        if r["taken"]
    )

    st.write(
        f"You have completed **{taken} out of {total}** "
        "scheduled medicines today."
    )