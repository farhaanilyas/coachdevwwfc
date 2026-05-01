import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(
    page_title="Wolves Coach Development Evaluation",
    page_icon="🐺",
    layout="centered"
)

# --- CONSTANTS ---

WOLVES_GOLD = "#FDB913"
WOLVES_BLACK = "#231F20"

PILLARS = [
    {
        "id": "session_design",
        "name": "Session Design & Coaching Delivery",
        "short": "Session Design",
        "questions": [
            "How well are your sessions structured to achieve clear and specific learning objectives?",
            "How effectively do your practices replicate realistic game situations and decision-making?",
            "How precise and impactful are your coaching interventions (timing, detail, clarity)?",
            "How well do you manage intensity, repetition, and flow within your sessions?",
            "How consistently do your sessions lead to visible learning and improvement?",
        ],
    },
    {
        "id": "individual_dev",
        "name": "Individual Player Development",
        "short": "Individual Dev",
        "questions": [
            "How clearly have you identified the key development needs for each player?",
            "How effectively do you design and implement individual development plans (including position-specific detail)?",
            "How consistently do you provide targeted coaching and feedback to individuals?",
            "How well do you track and evidence player improvement over time?",
            "To what extent are your players demonstrably improving in key areas relevant to their position and role?",
        ],
    },
    {
        "id": "match_impact",
        "name": "Match Impact & Game Coaching",
        "short": "Match Impact",
        "questions": [
            "How effectively do you prepare your team to execute the game model in matches?",
            "How well do you observe and interpret the game to identify key moments for intervention?",
            "How effective are your in-game decisions (adjustments, instructions, substitutions)?",
            "How clearly do players transfer training concepts into match performance?",
            "How consistently does your team show progress in match behaviour and decision-making over time?",
        ],
    },
    {
        "id": "people_leadership",
        "name": "People & Leadership",
        "short": "People & Leadership",
        "questions": [
            "How strong and consistent are your relationships with players?",
            "How effectively do you communicate expectations, feedback, and support?",
            "How well do you manage your emotions and behaviour under pressure?",
            "How effectively do you create a positive, challenging, and accountable environment?",
            "How well do you collaborate with staff, parents, and the wider multidisciplinary team?",
        ],
    },
    {
        "id": "professionalism",
        "name": "Professionalism & Work Habits",
        "short": "Professionalism",
        "questions": [
            "How well prepared are you for all sessions and match days (planning, organisation, detail)?",
            "How consistently do you meet and maintain high professional standards (punctuality, reliability, enthusiasm, organisation)?",
            "How well do you keep your KitMan Labs records of training and games up to date?",
            "How often do you act as a true ambassador for the club?",
            "How consistently do you reflect on and review your own performance?",
        ],
    },
    {
        "id": "technical",
        "name": "Technical Understanding",
        "short": "Technical",
        "questions": [
            "How high is your understanding to break down skills into teachable chunks?",
            "How effectively do you change the skill set you go after according to the ability level you are with?",
            "How often do you focus on technique during a session?",
            "How well do you understand the different skill sets different players need to progress to the next level of their journey?",
            "How much do you value technique for a professional footballer?",
        ],
    },
    {
        "id": "tactical",
        "name": "Tactical Understanding",
        "short": "Tactical",
        "questions": [
            "How much do you understand the tactical principles of Wolverhampton in any shape?",
            "How is your knowledge of different formations/shapes?",
            "How well do you adapt your tactics to suit individual players and positional requirements?",
            "How much do your tactical principles mirror those of the Wolves Game Model?",
            "How good are you at delivering a tactical plan off the pitch?",
        ],
    },
    {
        "id": "athletic_dev",
        "name": "Athletic Development",
        "short": "Athletic Dev",
        "questions": [
            "How much do you demonstrate the ability to develop players physically within sessions for long term athletic development?",
            "How much do you understand growth and maturation of individual players and how and when to modify to accommodate for growth related injuries?",
            "How effectively do you understand how different size pitches and session themes will develop different physical outcomes?",
            "How effective are you at repetition to rest within a practice?",
            "How much effect does the data produced by Sports Science affect your practice?",
        ],
    },
    {
        "id": "psychological",
        "name": "Psychological Support",
        "short": "Psychological",
        "questions": [
            "How well do you understand what drives individual player behaviours?",
            "How effectively do you adapt your coaching approach to meet individual needs?",
            "How consistently do you regulate your emotions and decision-making under pressure?",
            "How aware are you of your biases and how effectively do you minimise their impact on decisions?",
            "How effectively do you create an environment where players feel safe to express themselves and take risks?",
        ],
    },
]

TOOLBOX_TASKS = {
    "session_design": [
        "In a 6-week block, use a tactics board every session and game and report back what you notice about players and your delivery",
        "For 6-weeks, intentionally outline the demands of the game players can expect to develop in session",
        "Within a 6-week block, deliver a team-talk to players. Aim to record and review at least two",
        "For the next 6-weeks, select a less familiar intervention you will meaningfully aim to develop (e.g. Q&A, Observation & Feedback)",
    ],
    "individual_dev": [
        "Ensure IDPs are printed and pitch side for a 6-week block",
        "For the next 6-weeks, set players individual arrival tasks to practice linked to IDP",
        "Across the next 6-weeks, provide every player with a personalised demands of the game practice to develop",
        "Throughout a 6-week block take 5 minutes to ask questions about each player's IDP",
    ],
    "match_impact": [
        "In a 6-week block, use subs throughout games to capture data linked to learning outcomes (e.g. count box entries)",
        "Attend 2 home games in the next block and report back on the teams 'game plan'",
        "Accurately record match minutes by position for 6-weeks and report findings back to Lead Phase Coach",
        "Within the 6-week block, nominate set piece takers for all games and establish time in the last session of the week to practice",
    ],
    "people_leadership": [
        "In the next 6-weeks, observe another coach for a session and provide feedback on their session",
        "Across a 6-week block find out from players who they feel 'gets the best' out of them and why?",
        "For 6-weeks ensure you speak with (at least two) players and their parents informally after home games",
        "Throughout the next 6-week block, establish which coaching style each player you work with prefers",
    ],
    "professionalism": [
        "Schedule a review of your DAP/CCF with another member of staff",
        "In the next 6-weeks, update your DAP, review your progress and complete a CCF evaluation",
        "Ensure footballs are pumped, bibs and discs are clean and ready for use and sessions are set up prior to player arrival",
        "Plan, deliver and review a CPD to other members of the coaching team",
    ],
    "technical": [
        "Within a 6-week block, complete 2 separate video analysis sessions",
        "In a 6-week block, create 12 clips for the analysis best practice library",
        "Add 6 SSP sessions to the best practice library in the 6-week block",
        "In a 6-week block, leave 20 clips/comments for players on Veo",
    ],
    "tactical": [
        "In a 6-week block, find out what every player's views are on how Wolves sides play",
        "For 6-weeks, reference the competency being practiced in sessions and how/what players can expect to develop",
        "For the entire 6-week block, ensure match day planner and tactics board are pitch side at training and games",
        "In the next 6-weeks carry out an evaluation of learning preferences with a group",
    ],
    "athletic_dev": [
        "For 6-weeks, deliver clear physical intentions before each part of the session",
        "For 6-weeks, complete a 10 min. structured warm up that involves a clear physical performance marker every session",
        "For a 6-week block organise your training week into extensive and intensive training days with RPEs recorded for each session",
        "Within a 6-week block, record 2 sessions and work out the ball rolling time in each session",
    ],
    "psychological": [
        "In a 6-week period, journal your touchline behaviours and feedback to HoC or phase lead coach",
        "Within the 6-week block, arrange to collect and review player voice feedback with the intention of selecting your next development goal",
        "Within a 6-week block plan, deliver and review a competency-based workshop",
        "For 6-weeks, casually use 'what's the score' with players to gauge mood and attitude to learning before training begins",
    ],
}

AGE_GROUPS = ["U9", "U10", "U11", "U12", "U13", "U14", "U15", "U16"]
BLOCKS = ["Block 1", "Block 2", "Block 3", "Block 4", "Block 5", "Block 6"]
RATING_LABELS = {1: "Significant Gap", 2: "Developing", 3: "Competent", 4: "Strong", 5: "Exceptional"}


def get_score_color(score):
    if score <= 1.5:
        return "#e74c3c"
    if score <= 2.5:
        return "#f39c12"
    if score <= 3.5:
        return "#f1c40f"
    if score <= 4.0:
        return "#8bc34a"
    return "#27ae60"


def get_score_band(score):
    if score <= 1.5:
        return "Immediate Attention"
    if score <= 2.5:
        return "Needs Development"
    if score <= 3.5:
        return "Developing"
    if score <= 4.0:
        return "Strong"
    return "Exceptional"


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


# --- CUSTOM CSS ---

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    .wolves-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }
    .wolves-header img {
        width: 60px;
        margin-bottom: 0.5rem;
    }
    .wolves-header h1 {
        color: #FDB913 !important;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .wolves-header p {
        color: #9e9a95 !important;
        font-size: 0.85rem;
        margin: 0;
    }

    .pillar-card {
        background: #2a2520;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .pillar-card .p-name {
        font-size: 0.85rem;
        font-weight: 600;
        color: #e8e4e0 !important;
    }
    .pillar-card .p-band {
        font-size: 0.7rem;
        color: #9e9a95 !important;
    }
    .pillar-card .p-score {
        font-size: 1.6rem;
        font-weight: 700;
    }

    .score-big {
        text-align: center;
        padding: 1.5rem;
        background: rgba(253,185,19,0.08);
        border-radius: 14px;
        border: 1px solid rgba(253,185,19,0.2);
        margin-bottom: 2rem;
    }
    .score-big .number {
        font-size: 3.2rem;
        font-weight: 700;
    }
    .score-big .label {
        color: #9e9a95 !important;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 4px;
    }

    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        margin: 2rem 0 0.3rem;
    }
    .section-sub {
        color: #9e9a95 !important;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }

    .attention-item {
        background: #2a2520;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 6px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }
    .attention-dot {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 700;
        flex-shrink: 0;
        line-height: 28px;
        text-align: center;
    }
    .attention-text {
        font-size: 0.85rem;
        color: #e8e4e0 !important;
        line-height: 1.4;
    }
    .attention-pillar {
        font-size: 0.7rem;
        color: #7a7570 !important;
        margin-top: 3px;
    }

    .task-card {
        background: #2a2520;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 8px;
        border-left: 3px solid #FDB913;
    }
    .task-pillar {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #FDB913 !important;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .task-text {
        font-size: 0.85rem;
        color: #e8e4e0 !important;
        line-height: 1.5;
    }

    .strength-item {
        background: #2a2520;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 8px;
        border-left: 4px solid #27ae60;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .strength-item .s-name {
        font-size: 0.85rem;
        font-weight: 600;
        color: #e8e4e0 !important;
    }
    .strength-item .s-score {
        font-size: 1.4rem;
        font-weight: 700;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)


# --- PDF GENERATION ---


def generate_pdf(coach_name, age_group, block, pillar_scores, immediate_attn, consider_improving, strengths, tasks):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    def draw_bg():
        pdf.set_fill_color(255, 255, 255)
        pdf.rect(0, 0, 210, 297, "F")

    def check_space(needed):
        nonlocal y
        if y + needed > 272:
            pdf.add_page()
            draw_bg()
            return 20
        return y

    draw_bg()
    y = 18

    # Header
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.set_xy(20, y)
    pdf.cell(170, 5, "WOLVERHAMPTON WANDERERS ACADEMY", align="C")
    y += 5
    pdf.set_xy(20, y)
    pdf.cell(170, 5, "COACH DEVELOPMENT REPORT", align="C")
    y += 10

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(35, 31, 32)
    pdf.set_xy(20, y)
    pdf.cell(170, 10, coach_name, align="C")
    y += 12

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(120, 120, 120)
    pdf.set_xy(20, y)
    pdf.cell(170, 6, f"{age_group}  |  {block}", align="C")
    y += 7

    pdf.set_font("Helvetica", "", 9)
    pdf.set_xy(20, y)
    pdf.cell(170, 5, datetime.now().strftime("%d %B %Y"), align="C")
    y += 12

    # Overall Score
    all_avgs = [s["avg"] for s in pillar_scores]
    overall = sum(all_avgs) / len(all_avgs) if all_avgs else 0
    pdf.set_fill_color(245, 243, 240)
    pdf.rect(20, y, 170, 20, "F")
    pdf.set_font("Helvetica", "B", 24)
    r, g, b = hex_to_rgb(get_score_color(overall))
    pdf.set_text_color(r, g, b)
    pdf.set_xy(20, y + 3)
    pdf.cell(85, 14, f"{overall:.1f}", align="R")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(85, 14, f"  / 5.0  |  {get_score_band(overall)}")
    y += 26

    # Pillar Breakdown
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(35, 31, 32)
    pdf.set_xy(20, y)
    pdf.cell(170, 7, "Pillar Breakdown")
    y += 10

    for ps in pillar_scores:
        y = check_space(10)
        r, g, b = hex_to_rgb(get_score_color(ps["avg"]))
        pdf.set_fill_color(245, 243, 240)
        pdf.rect(20, y, 170, 8, "F")
        pdf.set_fill_color(r, g, b)
        pdf.rect(20, y, 2, 8, "F")
        pdf.set_xy(26, y)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 55, 50)
        pdf.cell(100, 8, ps["short"])
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(140, 135, 130)
        pdf.cell(40, 8, get_score_band(ps["avg"]), align="R")
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(r, g, b)
        pdf.cell(20, 8, f"{ps['avg']:.1f}", align="R")
        y += 10
    y += 6

    # Immediate Attention
    y = check_space(40)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(231, 76, 60)
    pdf.set_xy(20, y)
    pdf.cell(170, 7, "Immediate Attention")
    y += 7
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(140, 135, 130)
    pdf.set_xy(20, y)
    pdf.cell(170, 4, "Your 3 lowest self-ratings across all pillars")
    y += 7

    for item in immediate_attn:
        y = check_space(16)
        pdf.set_font("Helvetica", "", 9)
        text_w = 140
        lines = pdf.multi_cell(text_w, 4, item["question"], dry_run=True, output="LINES")
        h = max(10, len(lines) * 4 + 6)
        pdf.set_fill_color(245, 243, 240)
        pdf.rect(20, y, 170, h, "F")
        pdf.set_fill_color(231, 76, 60)
        pdf.rect(20, y, 2, h, "F")
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(231, 76, 60)
        pdf.set_xy(26, y + 2)
        pdf.cell(8, 5, str(item["score"]))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 55, 50)
        pdf.set_xy(36, y + 2)
        pdf.multi_cell(text_w, 4, item["question"])
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(140, 135, 130)
        pdf.set_xy(36, y + h - 5)
        pdf.cell(text_w, 3, item["pillar"])
        y += h + 2
    y += 4

    # Consider Improving
    if consider_improving["pillar"]:
        y = check_space(40)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(243, 156, 18)
        pdf.set_xy(20, y)
        pdf.cell(170, 7, "Consider Improving")
        y += 7
        ci_pillar = consider_improving["pillar"]
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(140, 135, 130)
        pdf.set_xy(20, y)
        pdf.cell(170, 4, f"3 lowest from your weakest pillar: {ci_pillar['short']} ({ci_pillar['avg']:.1f}/5)")
        y += 7

        for item in consider_improving["questions"]:
            y = check_space(16)
            pdf.set_font("Helvetica", "", 9)
            text_w = 140
            lines = pdf.multi_cell(text_w, 4, item["question"], dry_run=True, output="LINES")
            h = max(10, len(lines) * 4 + 4)
            pdf.set_fill_color(245, 243, 240)
            pdf.rect(20, y, 170, h, "F")
            pdf.set_fill_color(243, 156, 18)
            pdf.rect(20, y, 2, h, "F")
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(243, 156, 18)
            pdf.set_xy(26, y + 2)
            pdf.cell(8, 5, str(item["score"]))
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(60, 55, 50)
            pdf.set_xy(36, y + 2)
            pdf.multi_cell(text_w, 4, item["question"])
            y += h + 2
        y += 4

    # Areas of Strength
    y = check_space(35)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(39, 174, 96)
    pdf.set_xy(20, y)
    pdf.cell(170, 7, "Areas of Strength")
    y += 7
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(140, 135, 130)
    pdf.set_xy(20, y)
    pdf.cell(170, 4, "Your three highest-scoring pillars")
    y += 7

    for s in strengths:
        y = check_space(10)
        r, g, b = hex_to_rgb(get_score_color(s["avg"]))
        pdf.set_fill_color(245, 243, 240)
        pdf.rect(20, y, 170, 8, "F")
        pdf.set_fill_color(39, 174, 96)
        pdf.rect(20, y, 2, 8, "F")
        pdf.set_xy(26, y)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 55, 50)
        pdf.cell(140, 8, s["name"])
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(r, g, b)
        pdf.cell(20, 8, f"{s['avg']:.1f}", align="R")
        y += 10
    y += 6

    # Action Plan
    y = check_space(25)
    pdf.set_font("Helvetica", "B", 13)
    r, g, b = hex_to_rgb(WOLVES_GOLD)
    pdf.set_text_color(r, g, b)
    pdf.set_xy(20, y)
    pdf.cell(170, 7, "Suggested Action Plan")
    y += 7
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(140, 135, 130)
    pdf.set_xy(20, y)
    pdf.cell(170, 4, "Development tasks from the Coach Toolbox linked to your weakest pillars")
    y += 7

    for t in tasks:
        y = check_space(18)
        pdf.set_font("Helvetica", "", 9)
        text_w = 155
        lines = pdf.multi_cell(text_w, 4, t["task"], dry_run=True, output="LINES")
        h = len(lines) * 4 + 10
        pdf.set_fill_color(245, 243, 240)
        pdf.rect(20, y, 170, h, "F")
        pdf.set_fill_color(r, g, b)
        pdf.rect(20, y, 2, h, "F")
        pdf.set_xy(26, y + 1)
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(r, g, b)
        pdf.cell(155, 4, t["pillar"].upper())
        pdf.set_xy(26, y + 6)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 55, 50)
        pdf.multi_cell(text_w, 4, t["task"])
        y += h + 2

    return bytes(pdf.output())


# --- APP LOGIC ---

if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "ratings" not in st.session_state:
    st.session_state.ratings = {}

# Header
st.markdown(
    """
<div class="wolves-header">
    <img src="https://resources.premierleague.com/premierleague/badges/50/t39.png" alt="Wolves">
    <h1>Coach Development Evaluation</h1>
    <p>Wolverhampton Wanderers Academy</p>
</div>
""",
    unsafe_allow_html=True,
)

if not st.session_state.submitted:
    # --- INPUT FORM ---
    col1, col2, col3 = st.columns(3)
    with col1:
        coach_name = st.text_input("Coach Name")
    with col2:
        age_group = st.selectbox("Age Group", [""] + AGE_GROUPS, format_func=lambda x: "Select" if x == "" else x)
    with col3:
        block = st.selectbox("Block", [""] + BLOCKS, format_func=lambda x: "Select" if x == "" else x)

    if coach_name and age_group and block:
        st.divider()

        all_answered = True

        for p_idx, pillar in enumerate(PILLARS):
            st.markdown(f'<div class="section-header" style="color: {WOLVES_GOLD};">{pillar["name"]}</div>', unsafe_allow_html=True)
            st.caption("Rate yourself 1 to 5 for each question")

            for q_idx, question in enumerate(pillar["questions"]):
                key = f"{pillar['id']}_{q_idx}"
                rating = st.select_slider(
                    question,
                    options=[0, 1, 2, 3, 4, 5],
                    value=st.session_state.ratings.get(key, 0),
                    format_func=lambda x: "---" if x == 0 else f"{x} - {RATING_LABELS[x]}",
                    key=key,
                )
                st.session_state.ratings[key] = rating
                if rating == 0:
                    all_answered = False

            st.divider()

        if st.button(
            "Generate Report" if all_answered else "Complete all questions to generate report",
            disabled=not all_answered,
            type="primary" if all_answered else "secondary",
            use_container_width=True,
        ):
            st.session_state.submitted = True
            st.session_state.coach_name = coach_name
            st.session_state.age_group = age_group
            st.session_state.block = block
            st.rerun()

    else:
        st.info("Enter your name, age group, and block to begin.")

else:
    # --- RESULTS ---
    coach_name = st.session_state.coach_name
    age_group = st.session_state.age_group
    block = st.session_state.block
    ratings = st.session_state.ratings

    # Calculate pillar scores
    pillar_scores = []
    all_questions = []
    for pillar in PILLARS:
        scores = []
        for q_idx, question in enumerate(pillar["questions"]):
            key = f"{pillar['id']}_{q_idx}"
            score = ratings.get(key, 0)
            scores.append(score)
            all_questions.append({
                "pillar": pillar["name"],
                "pillar_id": pillar["id"],
                "short": pillar["short"],
                "question": question,
                "score": score,
                "q_idx": q_idx,
            })
        avg = sum(scores) / len(scores) if scores else 0
        pillar_scores.append({
            "id": pillar["id"],
            "name": pillar["name"],
            "short": pillar["short"],
            "avg": avg,
            "scores": scores,
            "questions": pillar["questions"],
        })

    overall = sum(ps["avg"] for ps in pillar_scores) / len(pillar_scores)

    sorted_pillars = sorted(pillar_scores, key=lambda x: x["avg"])
    sorted_questions = sorted(all_questions, key=lambda x: x["score"])

    immediate_attn = sorted_questions[:3]

    weakest_pillar = sorted_pillars[0]
    weakest_pillar_qs = []
    for q_idx, q in enumerate(weakest_pillar["questions"]):
        weakest_pillar_qs.append({
            "question": q,
            "score": weakest_pillar["scores"][q_idx],
        })
    weakest_pillar_qs.sort(key=lambda x: x["score"])
    consider_improving = {
        "pillar": weakest_pillar,
        "questions": weakest_pillar_qs[:3],
    }

    strengths = sorted(pillar_scores, key=lambda x: x["avg"], reverse=True)[:3]

    tasks = []
    for p in sorted_pillars[:3]:
        available = TOOLBOX_TASKS.get(p["id"], [])
        for t in available[:2]:
            tasks.append({"pillar": p["short"], "task": t})

    # --- DISPLAY ---

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1rem;">
        <img src="https://resources.premierleague.com/premierleague/badges/50/t39.png" style="width: 50px;">
        <p style="color: #9e9a95; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; margin: 8px 0 4px;">Coach Development Report</p>
        <h2 style="color: {WOLVES_GOLD} !important; margin: 0; font-weight: 700;">{coach_name}</h2>
        <p style="color: #9e9a95; font-size: 0.85rem;">{age_group} · {block}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="score-big">
        <div class="number" style="color: {get_score_color(overall)};">{overall:.1f}</div>
        <div class="label">Overall Score / 5.0 · {get_score_band(overall)}</div>
    </div>
    """, unsafe_allow_html=True)

    # Pillar Breakdown
    st.markdown(f'<div class="section-header" style="color: {WOLVES_GOLD};">Pillar Breakdown</div>', unsafe_allow_html=True)
    st.markdown("")

    for ps in pillar_scores:
        color = get_score_color(ps["avg"])
        st.markdown(f"""
        <div class="pillar-card" style="border-left: 4px solid {color};">
            <div>
                <div class="p-name">{ps["short"]}</div>
                <div class="p-band">{get_score_band(ps["avg"])}</div>
            </div>
            <div class="p-score" style="color: {color};">{ps["avg"]:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Immediate Attention
    st.markdown('<div class="section-header" style="color: #e74c3c;">Immediate Attention</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Your 3 lowest self-ratings across all pillars</div>', unsafe_allow_html=True)

    for item in immediate_attn:
        st.markdown(f"""
        <div class="attention-item" style="border-left: 4px solid #e74c3c;">
            <div class="attention-dot" style="background: #e74c3c; color: #fff;">{item["score"]}</div>
            <div>
                <div class="attention-text">{item["question"]}</div>
                <div class="attention-pillar">{item["pillar"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Consider Improving
    st.markdown('<div class="section-header" style="color: #f39c12;">Consider Improving</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">3 lowest questions from your weakest pillar: {weakest_pillar["short"]} ({weakest_pillar["avg"]:.1f}/5)</div>', unsafe_allow_html=True)

    for item in consider_improving["questions"]:
        st.markdown(f"""
        <div class="attention-item" style="border-left: 4px solid #f39c12;">
            <div class="attention-dot" style="background: #f39c12; color: #231F20;">{item["score"]}</div>
            <div>
                <div class="attention-text">{item["question"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Areas of Strength
    st.markdown('<div class="section-header" style="color: #27ae60;">Areas of Strength</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Your three highest-scoring pillars</div>', unsafe_allow_html=True)

    for s in strengths:
        st.markdown(f"""
        <div class="strength-item">
            <div class="s-name">{s["name"]}</div>
            <div class="s-score" style="color: {get_score_color(s['avg'])};">{s["avg"]:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Action Plan
    st.markdown(f'<div class="section-header" style="color: {WOLVES_GOLD};">Suggested Action Plan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Development tasks from the Coach Toolbox linked to your weakest pillars</div>', unsafe_allow_html=True)

    for t in tasks:
        st.markdown(f"""
        <div class="task-card">
            <div class="task-pillar">{t["pillar"]}</div>
            <div class="task-text">{t["task"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # Buttons
    st.markdown("")
    col1, col2, col3 = st.columns(3)

    with col1:
        pdf_bytes = generate_pdf(
            coach_name, age_group, block, pillar_scores,
            immediate_attn, consider_improving, strengths, tasks,
        )
        filename = f"Coach_Dev_Report_{coach_name.replace(' ', '_')}_{age_group}_{block.replace(' ', '_')}.pdf"
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )

    with col2:
        if st.button("Edit Responses", use_container_width=True):
            st.session_state.submitted = False
            st.rerun()

    with col3:
        if st.button("New Evaluation", use_container_width=True):
            st.session_state.submitted = False
            st.session_state.ratings = {}
            st.rerun()
