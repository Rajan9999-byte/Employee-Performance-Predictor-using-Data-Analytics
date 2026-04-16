import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie

# ==============================================================
#  PAGE CONFIG
# ==============================================================
st.set_page_config(
    page_title="EmpIQ - Employee Intelligence Hub",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================
#  PREMIUM CSS - single <style> block, @import for fonts
#  (Streamlit 1.56 compatible - no <link> tag)
# ==============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=Orbitron:wght@700;900&display=swap');

:root {
  --bg:      #070b14;
  --bg2:     #0d1424;
  --cyan:    #00ffe7;
  --purple:  #a855f7;
  --pink:    #f72585;
  --gold:    #ffd60a;
  --green:   #39ff14;
  --red:     #ff3131;
  --card:    rgba(255,255,255,0.04);
  --border:  rgba(0,255,231,0.18);
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: var(--bg) !important; }
.stApp > header { background: transparent !important; }
section[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border);
}
.block-container { padding-top: 1.5rem !important; }

/* HERO */
.hero {
  background: linear-gradient(135deg, #0d1424 0%, #11072d 50%, #070b14 100%);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 36px 44px;
  margin-bottom: 26px;
  position: relative;
  overflow: hidden;
  animation: slideDown 0.8s ease both;
}
.hero::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background:
    radial-gradient(ellipse at top left,  rgba(0,255,231,0.09) 0%, transparent 55%),
    radial-gradient(ellipse at bottom right, rgba(168,85,247,0.09) 0%, transparent 55%);
  pointer-events: none;
}
.hero-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 2.5rem; font-weight: 900;
  background: linear-gradient(90deg, var(--cyan), var(--purple), var(--pink));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 8px 0; line-height: 1.15;
}
.hero-sub { color: #94a3b8; font-size: 0.98rem; font-weight: 300; margin: 0; }

/* KPI STRIP */
.kpi-row { display: flex; gap: 14px; margin-bottom: 22px; flex-wrap: wrap; }
.kpi {
  flex: 1; min-width: 140px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px 22px;
  position: relative; overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  animation: rise 0.6s ease both;
}
.kpi:hover { transform: translateY(-4px); box-shadow: 0 8px 32px rgba(0,255,231,0.14); }
.kpi::after {
  content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 3px;
}
.kpi.c::after { background: linear-gradient(90deg, var(--cyan),   transparent); }
.kpi.p::after { background: linear-gradient(90deg, var(--purple), transparent); }
.kpi.g::after { background: linear-gradient(90deg, var(--gold),   transparent); }
.kpi.k::after { background: linear-gradient(90deg, var(--pink),   transparent); }
.kpi.n::after { background: linear-gradient(90deg, var(--green),  transparent); }

.kpi-icon  { font-size: 1.9rem; margin-bottom: 6px; }
.kpi-lbl   { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1.5px; color: #64748b; margin-bottom: 4px; }
.kpi-val   { font-size: 1.8rem; font-weight: 700; }
.kpi-val.c { color: var(--cyan);   }
.kpi-val.p { color: var(--purple); }
.kpi-val.g { color: var(--gold);   }
.kpi-val.k { color: var(--pink);   }
.kpi-val.n { color: var(--green);  }
.kpi-sub   { font-size: 0.72rem; color: #94a3b8; margin-top: 3px; }

/* GLASS PANEL */
.panel {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px 24px 16px;
  margin-bottom: 16px;
  animation: rise 0.7s ease both;
}
.ptitle {
  font-size: 0.82rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1.5px;
  color: var(--cyan); margin-bottom: 14px;
}

/* RESULT CARD */
.rcard {
  border-radius: 18px; padding: 26px 30px; margin: 12px 0;
  text-align: center; animation: glow 2.5s ease-in-out infinite;
}
.rcard.high   { background: linear-gradient(135deg,rgba(57,255,20,.10),rgba(0,255,231,.05));  border:2px solid var(--green);  box-shadow: 0 0 28px rgba(57,255,20,.20); }
.rcard.medium { background: linear-gradient(135deg,rgba(255,214,10,.10),rgba(255,165,0,.05)); border:2px solid var(--gold);   box-shadow: 0 0 28px rgba(255,214,10,.20); }
.rcard.low    { background: linear-gradient(135deg,rgba(255,49,49,.12),rgba(247,37,133,.05));border:2px solid var(--red);    box-shadow: 0 0 28px rgba(255,49,49,.20); }
.rlabel { font-size: 0.78rem; letter-spacing: 2px; text-transform: uppercase; color: #94a3b8; margin-bottom: 4px; }
.rband  { font-family: 'Orbitron', sans-serif; font-size: 2.3rem; font-weight: 900; margin: 0; }
.rband.high   { color: var(--green); }
.rband.medium { color: var(--gold);  }
.rband.low    { color: var(--red);   }
.rdesc  { font-size: 0.86rem; color: #94a3b8; margin-top: 8px; }

/* PIP CARDS */
.pip { border-radius: 14px; padding: 20px; margin-bottom: 12px; border-left: 4px solid; animation: rise 0.5s ease both; }
.pip.d30 { background: rgba(0,255,231,.06);  border-color: var(--cyan);   }
.pip.d60 { background: rgba(168,85,247,.06); border-color: var(--purple); }
.pip.d90 { background: rgba(57,255,20,.06);  border-color: var(--green);  }
.pip-day { font-size: 0.70rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; margin-bottom: 5px; }
.pip.d30 .pip-day { color: var(--cyan);   }
.pip.d60 .pip-day { color: var(--purple); }
.pip.d90 .pip-day { color: var(--green);  }
.pip-ttl { font-size: 0.96rem; font-weight: 600; margin-bottom: 6px; color: #e2e8f0; }
.pip-bdy { font-size: 0.82rem; color: #94a3b8; line-height: 1.65; }

/* BADGES */
.badge { display: inline-block; padding: 5px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin: 4px 3px; }
.b-fire { background: rgba(255,49,49,.15);  color: var(--red);   border: 1px solid rgba(255,49,49,.3); }
.b-skil { background: rgba(255,214,10,.12); color: var(--gold);  border: 1px solid rgba(255,214,10,.3); }
.b-eng  { background: rgba(247,37,133,.12); color: var(--pink);  border: 1px solid rgba(247,37,133,.3); }
.b-ok   { background: rgba(57,255,20,.10);  color: var(--green); border: 1px solid rgba(57,255,20,.25); }

/* SIDEBAR */
.sb-brand { font-family: 'Orbitron',sans-serif; font-size: 1.2rem; font-weight: 900; background: linear-gradient(90deg,var(--cyan),var(--purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 4px; }
.sb-tag   { font-size: 0.72rem; color: #64748b; margin-bottom: 22px; }
.ndivider { height: 1px; background: linear-gradient(90deg,transparent,var(--cyan),transparent); margin: 20px 0; opacity: 0.35; }

/* BUTTON */
div.stButton > button {
  background: linear-gradient(135deg, #00ffe7, #a855f7) !important;
  color: #070b14 !important; font-weight: 800 !important;
  border: none !important; border-radius: 12px !important;
  padding: 12px 28px !important; transition: all 0.3s ease !important;
  box-shadow: 0 4px 20px rgba(0,255,231,0.2) !important;
}
div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 30px rgba(0,255,231,0.4) !important; }

/* SCROLLBAR */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* KEYFRAMES */
@keyframes slideDown { from { opacity:0; transform:translateY(-18px); } to { opacity:1; transform:translateY(0); } }
@keyframes rise      { from { opacity:0; transform:translateY(14px);  } to { opacity:1; transform:translateY(0); } }
@keyframes glow      { 0%,100%{ box-shadow: 0 0 18px rgba(0,255,231,.12); } 50%{ box-shadow: 0 0 36px rgba(0,255,231,.32); } }
</style>
""", unsafe_allow_html=True)


# ==============================================================
#  HELPERS
# ==============================================================
def load_lottie(url):
    try:
        r = requests.get(url, timeout=4)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

LOTTIES = {
    "hr":      "https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json",
    "success": "https://assets9.lottiefiles.com/packages/lf20_pqnfmone.json",
    "warn":    "https://assets4.lottiefiles.com/packages/lf20_kuhijlvx.json",
    "growth":  "https://assets10.lottiefiles.com/packages/lf20_ydznbgr6.json",
    "analysis":"https://assets3.lottiefiles.com/packages/lf20_qp1q7mct.json",
}

CHART_BASE = dict(
    plot_bgcolor  = "rgba(0,0,0,0)",
    paper_bgcolor = "rgba(0,0,0,0)",
    font_color    = "#94a3b8",
    font_family   = "Inter",
)
NEON = ["#00ffe7","#a855f7","#f72585","#ffd60a","#39ff14","#3b82f6"]

def theme(fig, h=None):
    kw = dict(**CHART_BASE, margin=dict(l=8,r=8,t=36,b=8),
              legend=dict(bgcolor="rgba(0,0,0,0)", font_color="#94a3b8"))
    if h:
        kw["height"] = h
    fig.update_layout(**kw)
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False)
    return fig


# ==============================================================
#  LOAD ASSETS
# ==============================================================
@st.cache_resource(show_spinner=False)
def load_assets():
    model   = joblib.load('models/performance_model.pkl')
    scaler  = joblib.load('models/scaler.pkl')
    le_dept = joblib.load('models/le_dept.pkl')
    le_gen  = joblib.load('models/le_gender.pkl')
    df      = pd.read_csv('data/employee_performance.csv')
    return model, scaler, le_dept, le_gen, df

model, scaler, le_dept, le_gen, df = load_assets()


# ==============================================================
#  SIDEBAR
# ==============================================================
with st.sidebar:
    st.markdown('<div class="sb-brand">EmpIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tag">Employee Intelligence Hub</div>', unsafe_allow_html=True)

    la = load_lottie(LOTTIES["hr"])
    if la:
        st_lottie(la, height=140, key="sb_anim")

    st.markdown('<div class="ndivider"></div>', unsafe_allow_html=True)
    page = st.radio("nav", ["Overview","Predict","Interventions","Analytics"],
                    label_visibility="collapsed",
                    format_func=lambda x: {
                        "Overview":"🏠  Overview",
                        "Predict":"🔍  Predict",
                        "Interventions":"⚠️  Interventions",
                        "Analytics":"📊  Analytics"
                    }[x])
    st.markdown('<div class="ndivider"></div>', unsafe_allow_html=True)

    total  = len(df)
    low_n  = (df['Performance_Score']=='Low').sum()
    risk_n = (df['Attrition_Risk']>0.6).sum()

    st.markdown(f"""
    <div style='font-size:.78rem;color:#64748b;line-height:2.1'>
      👥 Total &nbsp;<b style='color:#00ffe7'>{total}</b><br>
      🚨 Low Band &nbsp;<b style='color:#ff3131'>{low_n}</b><br>
      ⚡ High Attrition &nbsp;<b style='color:#ffd60a'>{risk_n}</b>
    </div>""", unsafe_allow_html=True)


# ==============================================================
#  PAGE: OVERVIEW
# ==============================================================
if page == "Overview":
    st.markdown("""
    <div class="hero">
      <div class="hero-title">Employee Intelligence Hub</div>
      <div class="hero-sub">AI-powered performance analytics · intervention planning · workforce insights</div>
    </div>""", unsafe_allow_html=True)

    hp = round((df['Performance_Score']=='High').mean()*100, 1)
    mp = round((df['Performance_Score']=='Medium').mean()*100, 1)
    lp = round((df['Performance_Score']=='Low').mean()*100, 1)
    ae = round(df['Engagement_Score'].mean(), 2)

    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi c"><div class="kpi-icon">👥</div><div class="kpi-lbl">Workforce</div><div class="kpi-val c">{total:,}</div><div class="kpi-sub">6 departments</div></div>
      <div class="kpi n"><div class="kpi-icon">🏆</div><div class="kpi-lbl">High Band</div><div class="kpi-val n">{hp}%</div><div class="kpi-sub">Top talent</div></div>
      <div class="kpi g"><div class="kpi-icon">📈</div><div class="kpi-lbl">Medium Band</div><div class="kpi-val g">{mp}%</div><div class="kpi-sub">Growth candidates</div></div>
      <div class="kpi k"><div class="kpi-icon">⚠️</div><div class="kpi-lbl">Low Band</div><div class="kpi-val k">{lp}%</div><div class="kpi-sub">PIP candidates</div></div>
      <div class="kpi p"><div class="kpi-icon">💡</div><div class="kpi-lbl">Avg Engagement</div><div class="kpi-val p">{ae}/5</div><div class="kpi-sub">Company-wide</div></div>
    </div>
    <div class="ndivider"></div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel"><div class="ptitle">🎯 Performance Distribution</div>', unsafe_allow_html=True)
        bc = df['Performance_Score'].value_counts().reset_index()
        bc.columns = ['Band','Count']
        fig = px.pie(bc, names='Band', values='Count', hole=0.55,
                     color='Band', color_discrete_map={'High':'#39ff14','Medium':'#ffd60a','Low':'#ff3131'})
        fig.update_traces(textfont_size=13, textfont_color='white',
                          marker=dict(line=dict(color='#070b14', width=2)))
        theme(fig, 300)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel"><div class="ptitle">🏢 Dept vs Band Heatmap</div>', unsafe_allow_html=True)
        dp = df.groupby(['Department','Performance_Score']).size().reset_index(name='N')
        pv = dp.pivot(index='Department', columns='Performance_Score', values='N').fillna(0)
        fig = px.imshow(pv, color_continuous_scale=[[0,'#0d1424'],[0.5,'#a855f7'],[1,'#00ffe7']],
                        text_auto=True, aspect='auto')
        theme(fig, 300); fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="panel"><div class="ptitle">🎻 Training Hours by Band</div>', unsafe_allow_html=True)
        fig = px.violin(df, x='Performance_Score', y='Training_Hours', color='Performance_Score',
                        color_discrete_map={'High':'#39ff14','Medium':'#ffd60a','Low':'#ff3131'},
                        box=True, points=False)
        theme(fig, 290); fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="panel"><div class="ptitle">💼 Engagement vs Projects</div>', unsafe_allow_html=True)
        s = df.sample(min(300, len(df)), random_state=7)
        fig = px.scatter(s, x='Engagement_Score', y='Projects_Completed',
                         size='Training_Hours', color='Performance_Score', opacity=0.75,
                         color_discrete_map={'High':'#39ff14','Medium':'#ffd60a','Low':'#ff3131'})
        theme(fig, 290)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="ptitle">🌐 Dept → Gender → Band Sunburst</div>', unsafe_allow_html=True)
    fig = px.sunburst(df, path=['Department','Gender','Performance_Score'],
                      color_discrete_sequence=NEON)
    theme(fig, 420)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================
#  PAGE: PREDICT
# ==============================================================
elif page == "Predict":
    st.markdown("""
    <div class="hero">
      <div class="hero-title" style="font-size:2rem">🔍 Individual Prediction Engine</div>
      <div class="hero-sub">Enter employee metrics to get an AI-driven performance forecast and trajectory analysis.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="ptitle">👤 Employee Profile</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        dept   = st.selectbox("Department",    le_dept.classes_)
        gender = st.selectbox("Gender",        le_gen.classes_)
        age    = st.number_input("Age",        22, 60, 30)
        years  = st.number_input("Tenure (Yrs)", 1, 15, 3)
    with c2:
        level   = st.number_input("Job Level (1–5)", 1, 5, 2)
        sal     = st.slider("Salary Hike %", 5, 25, 10)
        prev1   = st.selectbox("Last Rating",     ["Low","Medium","High"])
        prev2   = st.selectbox("Previous Rating", ["Low","Medium","High"])
    with c3:
        hours   = st.slider("Weekly Hours",     35, 60, 40)
        train   = st.slider("Training Hrs/Yr", 10, 100, 40)
        proj    = st.slider("Projects",          1, 10,  4)
        attend  = st.slider("Attendance %",     80, 100, 95)
        eng     = st.slider("Engagement",       1.0, 5.0, 3.5, 0.1)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("⚡  Run AI Prediction"):
        rmap = {"Low":0,"Medium":1,"High":2}
        row = pd.DataFrame({
            'Department':      [le_dept.transform([dept])[0]],
            'Age':             [age],
            'Gender':          [le_gen.transform([gender])[0]],
            'Years_At_Company':[years],
            'Job_Level':       [level],
            'Weekly_Hours':    [hours],
            'Training_Hours':  [train],
            'Projects_Completed':[proj],
            'Attendance_Rate': [attend/100],
            'Engagement_Score':[eng],
            'Salary_Hike_Pct': [sal],
            'Prev_Rating_1':   [rmap[prev1]],
            'Prev_Rating_2':   [rmap[prev2]]
        })
        scaled   = scaler.transform(row)
        pred     = model.predict(scaled)[0]
        proba    = model.predict_proba(scaled)[0]
        res      = ["Low","Medium","High"][pred]
        cls      = res.lower()

        anim_key = "success" if res=="High" else ("growth" if res=="Medium" else "warn")
        la = load_lottie(LOTTIES[anim_key])

        a1, a2 = st.columns([1,1])
        with a1:
            if la:
                st_lottie(la, height=190, key="res_anim")
        with a2:
            desc = {
                "High":  "Exceptional contributor. Strong candidate for promotion and mentoring.",
                "Medium":"Solid performer. Targeted upskilling could elevate to High band.",
                "Low":   "Immediate intervention needed. Review workload, training & engagement."
            }
            st.markdown(f"""
            <div class="rcard {cls}">
              <div class="rlabel">Predicted Performance Band</div>
              <div class="rband {cls}">{res.upper()}</div>
              <div class="rdesc">{desc[res]}</div>
            </div>""", unsafe_allow_html=True)

        # Confidence chart
        st.markdown('<div class="panel"><div class="ptitle">📊 Prediction Confidence</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=["Low","Medium","High"], y=proba,
            marker_color=["#ff3131","#ffd60a","#39ff14"],
            text=[f"{v:.0%}" for v in proba], textposition='outside',
            textfont=dict(color='white', size=14)
        ))
        theme(fig, 250); fig.update_layout(yaxis=dict(range=[0,1.2], showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Trajectory
        st.markdown('<div class="panel"><div class="ptitle">📈 Performance Trajectory (3 Cycles)</div>', unsafe_allow_html=True)
        hist   = [rmap[prev2], rmap[prev1], pred]
        tcols  = ["#ff3131" if v==0 else "#ffd60a" if v==1 else "#39ff14" for v in hist]
        labels = [["Low","Med","High"][v] for v in hist]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=["Cycle -2","Cycle -1","Predicted"], y=hist,
            mode='lines+markers+text',
            line=dict(color='#00ffe7', width=3),
            marker=dict(color=tcols, size=18, line=dict(color='white', width=2)),
            text=labels, textposition='top center',
            textfont=dict(color='white', size=12)
        ))
        theme(fig, 250)
        fig.update_yaxes(ticktext=["Low","Medium","High"], tickvals=[0,1,2], range=[-0.5,2.5])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Attrition gauge
        risk = 0.0
        if hours > 55:   risk += 0.4
        if eng   < 2.0:  risk += 0.4
        if res == "Low": risk += 0.2
        risk = min(risk + np.random.uniform(0, 0.05), 1.0)

        st.markdown('<div class="panel"><div class="ptitle">🚨 Attrition Risk</div>', unsafe_allow_html=True)
        gc = '#ff3131' if risk>0.6 else '#ffd60a' if risk>0.35 else '#39ff14'
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=round(risk*100, 1),
            delta={'reference':30,'increasing':{'color':'#ff3131'},'decreasing':{'color':'#39ff14'}},
            number={'suffix':'%','font':{'color':gc,'size':40}},
            gauge={'axis':{'range':[0,100],'tickcolor':'#64748b'},
                   'bar':{'color':gc},'bgcolor':'rgba(0,0,0,0)','borderwidth':0,
                   'steps':[{'range':[0,40],'color':'rgba(57,255,20,.08)'},
                             {'range':[40,70],'color':'rgba(255,214,10,.08)'},
                             {'range':[70,100],'color':'rgba(255,49,49,.10)'}],
                   'threshold':{'line':{'color':'white','width':3},'thickness':0.75,'value':70}}
        ))
        theme(fig, 250); fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================
#  PAGE: INTERVENTIONS
# ==============================================================
elif page == "Interventions":
    st.markdown("""
    <div class="hero">
      <div class="hero-title" style="font-size:2rem">⚠️ Performance Intervention Center</div>
      <div class="hero-sub">Deep-dive analytics, root-cause analysis &amp; structured 30-60-90 day improvement plans for at-risk employees.</div>
    </div>""", unsafe_allow_html=True)

    low_df   = df[df['Performance_Score']=='Low']
    selected = st.selectbox("Select At-Risk Employee", low_df['Employee_ID'].tolist())
    emp      = df[df['Employee_ID']==selected].iloc[0]

    st.markdown(f"""
    <div class="panel" style="border-color:rgba(255,49,49,.35)">
      <div class="ptitle" style="color:#ff3131">🚩 Employee Profile — {selected}</div>
      <div style="display:flex;gap:28px;flex-wrap:wrap;font-size:.86rem;color:#94a3b8">
        <span>🏢 <b style="color:white">{emp['Department']}</b></span>
        <span>🎂 Age <b style="color:white">{emp['Age']}</b></span>
        <span>📅 Tenure <b style="color:white">{emp['Years_At_Company']}y</b></span>
        <span>🎯 Level <b style="color:white">{int(emp['Job_Level'])}</b></span>
        <span>📊 Last Rating <b style="color:#ffd60a">{["Low","Medium","High"][int(emp["Prev_Rating_1"])]}</b></span>
        <span>📉 Current <b style="color:#ff3131">LOW</b></span>
      </div>
    </div>""", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        lwarn = load_lottie(LOTTIES["warn"])
        if lwarn:
            st_lottie(lwarn, height=150, key="warn_anim")

        # Root cause badges
        st.markdown('<div class="panel"><div class="ptitle">🔎 Root Cause Analysis</div>', unsafe_allow_html=True)
        badges = ""
        if emp['Weekly_Hours']   > 55:  badges += '<span class="badge b-fire">🔥 Burnout Risk</span>'
        if emp['Training_Hours'] < 30:  badges += '<span class="badge b-skil">📚 Skill Gap</span>'
        if emp['Engagement_Score'] < 3: badges += '<span class="badge b-eng">💔 Disengaged</span>'
        if emp['Attendance_Rate']  < .88: badges += '<span class="badge b-fire">📅 Poor Attendance</span>'
        if not badges: badges = '<span class="badge b-ok">✅ No Major Blockers</span>'
        st.markdown(badges + "<br><br>", unsafe_allow_html=True)

        # Progress bars
        for col, lo, hi, lbl, fmt in [
            ('Training_Hours',   10,  100, '📚 Training Hours', '{:.0f} hrs'),
            ('Projects_Completed', 1,  10, '📁 Projects/Year',  '{:.0f}'),
            ('Engagement_Score',   1,   5, '💡 Engagement',     '{:.1f}/5'),
            ('Attendance_Rate',   .8,   1, '📅 Attendance',     '{:.0%}'),
        ]:
            val = emp[col]
            pct = int((val-lo)/(hi-lo)*100)
            clr = "#39ff14" if pct>60 else "#ffd60a" if pct>35 else "#ff3131"
            st.markdown(f"""
            <div style="margin-bottom:12px">
              <div style="display:flex;justify-content:space-between;font-size:.8rem;margin-bottom:4px">
                <span style="color:#94a3b8">{lbl}</span>
                <span style="color:{clr};font-weight:700">{fmt.format(val)}</span>
              </div>
              <div style="background:rgba(255,255,255,.06);border-radius:6px;height:8px">
                <div style="width:{pct}%;background:{clr};height:8px;border-radius:6px"></div>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        # Radar chart
        st.markdown('<div class="panel"><div class="ptitle">🕸️ Skills Radar vs High Performer</div>', unsafe_allow_html=True)
        cats = ['Training_Hours','Projects_Completed','Attendance_Rate','Engagement_Score','Weekly_Hours']
        high_avg = df[df['Performance_Score']=='High'][cats].mean()
        def norm(s):
            return ((s-df[cats].min())/(df[cats].max()-df[cats].min())*10).values.tolist()
        ev = norm(pd.Series({c:emp[c] for c in cats}))
        hv = norm(high_avg)
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=ev+[ev[0]], theta=cats+[cats[0]],
            fill='toself', name=selected, line_color='#ff3131', fillcolor='rgba(255,49,49,.12)'))
        fig.add_trace(go.Scatterpolar(r=hv+[hv[0]], theta=cats+[cats[0]],
            fill='toself', name='Top Performer Avg', line_color='#39ff14', fillcolor='rgba(57,255,20,.08)'))
        fig.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True,range=[0,10],gridcolor='rgba(255,255,255,.1)',color='#64748b'),
            angularaxis=dict(color='#64748b')), showlegend=True, height=320)
        theme(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Attrition gauge
        rv = float(emp['Attrition_Risk'])
        gc = '#ff3131' if rv>0.6 else '#ffd60a' if rv>0.35 else '#39ff14'
        st.markdown('<div class="panel"><div class="ptitle">🚨 Attrition Risk Score</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(rv*100,1),
            number={'suffix':'%','font':{'color':gc,'size':32}},
            gauge={'axis':{'range':[0,100],'tickcolor':'#64748b'},'bar':{'color':gc},
                   'bgcolor':'rgba(0,0,0,0)','borderwidth':0,
                   'steps':[{'range':[0,40],'color':'rgba(57,255,20,.08)'},
                             {'range':[40,70],'color':'rgba(255,214,10,.08)'},
                             {'range':[70,100],'color':'rgba(255,49,49,.10)'}]}
        ))
        theme(fig, 210); fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # PIP Roadmap
    st.markdown('<div class="ndivider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ptitle" style="font-size:.9rem">🗓️ AI-Generated 30-60-90 Day Improvement Plan</div>', unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("""
        <div class="pip d30">
          <div class="pip-day">⚡ Day 1-30 — Stabilize</div>
          <div class="pip-ttl">Reset &amp; Align</div>
          <div class="pip-bdy">
            • Weekly 1-on-1 with direct manager<br>
            • Reduce project load by 30%<br>
            • Complete mandatory learning module<br>
            • Map blockers with HR<br>
            • Define 3 measurable micro-goals
          </div>
        </div>""", unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="pip d60">
          <div class="pip-day">🚀 Day 31-60 — Rebuild</div>
          <div class="pip-ttl">Skill &amp; Output Growth</div>
          <div class="pip-bdy">
            • Enroll in 2 targeted skill courses<br>
            • Pair-programming / job shadowing<br>
            • Deliver 1 end-to-end project<br>
            • Mid-point performance check-in<br>
            • Peer-feedback collection cycle
          </div>
        </div>""", unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="pip d90">
          <div class="pip-day">🏆 Day 61-90 — Elevate</div>
          <div class="pip-ttl">Band Elevation Review</div>
          <div class="pip-bdy">
            • Final performance reassessment<br>
            • Present completed project outcomes<br>
            • Manager calibration meeting<br>
            • HR band reclassification review<br>
            • Formal development plan handoff
          </div>
        </div>""", unsafe_allow_html=True)

    lg = load_lottie(LOTTIES["growth"])
    if lg:
        _, gc2, _ = st.columns([1,2,1])
        with gc2:
            st_lottie(lg, height=130, key="growth_anim")

    if st.button("📄 Generate Official HR Intervention Report"):
        st.success(f"PIP Report for **{selected}** compiled and flagged for HR review.")


# ==============================================================
#  PAGE: ANALYTICS
# ==============================================================
elif page == "Analytics":
    st.markdown("""
    <div class="hero">
      <div class="hero-title" style="font-size:2rem">📊 Workforce Analytics Lab</div>
      <div class="hero-sub">Holistic pattern analysis · attrition risk landscape · department deep-dives</div>
    </div>""", unsafe_allow_html=True)

    la2 = load_lottie(LOTTIES["analysis"])
    if la2:
        _, ac, _ = st.columns([3,1,3])
        with ac:
            st_lottie(la2, height=120, key="an_anim")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel"><div class="ptitle">📦 Weekly Hours by Band</div>', unsafe_allow_html=True)
        fig = px.box(df, x='Performance_Score', y='Weekly_Hours', color='Performance_Score',
                     color_discrete_map={'High':'#39ff14','Medium':'#ffd60a','Low':'#ff3131'}, points=False)
        theme(fig,290); fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel"><div class="ptitle">💰 Salary Hike Distribution</div>', unsafe_allow_html=True)
        fig = px.histogram(df, x='Salary_Hike_Pct', color='Performance_Score', barmode='overlay',
                           color_discrete_map={'High':'#39ff14','Medium':'#ffd60a','Low':'#ff3131'}, opacity=0.78)
        theme(fig,290)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="ptitle">🌡️ Attrition Risk Density — Engagement vs Hours</div>', unsafe_allow_html=True)
    fig = px.density_contour(df, x='Engagement_Score', y='Weekly_Hours', z='Attrition_Risk', histfunc='avg')
    fig.update_traces(contours_coloring="fill", colorscale=[[0,'#0d1424'],[0.5,'#f72585'],[1,'#ff3131']])
    theme(fig, 360)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="panel"><div class="ptitle">🎓 Avg Training by Department</div>', unsafe_allow_html=True)
        dt = df.groupby('Department')['Training_Hours'].mean().reset_index().sort_values('Training_Hours')
        fig = px.bar(dt, x='Training_Hours', y='Department', orientation='h',
                     color='Training_Hours', color_continuous_scale=['#0d1424','#a855f7','#00ffe7'])
        theme(fig,290); fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="panel"><div class="ptitle">🔗 Feature Correlation Matrix</div>', unsafe_allow_html=True)
        cols = ['Age','Training_Hours','Projects_Completed','Engagement_Score','Weekly_Hours','Attrition_Risk']
        corr = df[cols].corr().round(2)
        fig = px.imshow(corr, text_auto=True, aspect='auto',
                        color_continuous_scale=['#ff3131','#0d1424','#39ff14'], range_color=[-1,1])
        theme(fig,290)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Sunburst
    st.markdown('<div class="panel"><div class="ptitle">🌐 Full Workforce Breakdown</div>', unsafe_allow_html=True)
    fig = px.sunburst(df, path=['Department','Performance_Score','Gender'], color_discrete_sequence=NEON)
    theme(fig,430)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
