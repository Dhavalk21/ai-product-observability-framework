import streamlit as st
import pandas as pd
import re
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration for modern premium widescreen layout
st.set_page_config(
    page_title="AI Product Evals & Observability Controller",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States for Playground Presets
if 'play_context' not in st.session_state:
    st.session_state.play_context = "we have 2 plan one for gold client 20 euro - 14 day refund policy and silver plan 10 euro - no refund policy"
if 'play_query' not in st.session_state:
    st.session_state.play_query = "What is the cost of the silver plan, and what is your refund policy?"
if 'play_output' not in st.session_state:
    st.session_state.play_output = "Silver plan cost 10 euro and 10 day return policy"

# Default Baseline Sliders
if 'faithfulness' not in st.session_state:
    st.session_state.faithfulness = 80
if 'relevancy' not in st.session_state:
    st.session_state.relevancy = 85
if 'hallucination' not in st.session_state:
    st.session_state.hallucination = 12

# Header / Personal Branding
st.markdown("""
<div style="background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 24px;">
    <div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 8px;">
        <span style="background-color: #f1f5f9; color: #475569; font-size: 11px; font-weight: 600; padding: 4px 12px; border-radius: 9999px; border: 1px solid #cbd5e1;">
            AI Product Operations • Quality Assurance Framework
        </span>
        <span style="background-color: #e0e7ff; color: #4338ca; font-size: 11px; font-weight: 600; padding: 4px 12px; border-radius: 9999px; border: 1px solid #c7d2fe;">
            Designed by Dhaval Kareliya | 
            <a href="https://linkedin.com/in/YOUR_USERNAME" target="_blank" style="text-decoration: none; color: #3730a3; font-weight: bold;">LinkedIn</a> • 
            <a href="https://github.com/YOUR_USERNAME" target="_blank" style="text-decoration: none; color: #3730a3; font-weight: bold;">GitHub</a>
        </span>
    </div>
    <h1 style="color: #0f172a; font-size: 26px; font-weight: 800; margin: 0 0 4px 0; tracking: -0.025em;">
        Production AI Evals & Observability Controller
    </h1>
    <p style="color: #64748b; font-size: 14px; margin: 0; line-height: 1.5;">
        Verify and monitor LLM system performance. Define multi-dimensional criteria (Faithfulness, Relevancy, Hallucinations) to dynamically predict customer churn, CSAT, and system reliability.
    </p>
</div>
""", unsafe_allow_html=True)

# Collapsible Step-by-Step Educational Guide
with st.expander("📖 Show Guide: How to Run LLM Quality Evaluations (With Examples)", expanded=False):
    st.markdown("""
    ### Why do we need AI Evals?
    Product managers run evaluations (Evals) using golden datasets to avoid deploying LLMs that output false facts or generate off-topic noise.
    
    #### 📋 Step-by-Step Instructions:
    1. Click on any of the preloaded scenario buttons inside the **Live Evaluation Playground** (e.g. *⚠️ Hallucinated Fact*).
    2. Inspect how the LLM response differs from the database facts.
    3. Click the blue **"Run AI-Judge Evaluation Simulation"** button. The Python judge analyzes context alignment in real-time.
    4. Check the **Overall Quality Index**, **Predicted Churn**, and **Projected CSAT** to determine release readiness.
    
    #### 📁 Real-World Scenarios to Study:
    """)
    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        st.info("**Scenario A: Hallucinated Fact**\nThe model promised a '10-day return policy' when the source context states 'no refund policy'.\n\n*Expected Result: Low Faithfulness (~60%), High Hallucination Rate (~45%).*")
    with g_col2:
        st.warning("**Scenario B: Off-Topic Answer**\nThe model ignored a core pricing query entirely, trying to sell shoes instead.\n\n*Expected Result: Normal Grounding, but extremely Low Relevancy (~30%).*")
    with g_col3:
        st.success("**Scenario C: Perfect Grounding**\nThe model correctly extracted metadata and complied strictly with the silver/gold plans.\n\n*Expected Result: Flawless Grounding (>90%), Churn Risk Minimized.*")

# Main Content Columns
col_left, col_right = st.columns([4, 6])

with col_left:
    st.subheader("Interactive Evaluation Playground")
    
    # Preset triggers using Streamlit button triggers
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        if st.button("⚠️ Hallucinated Fact", use_container_width=True):
            st.session_state.play_context = "we have 2 plan one for gold client 20 euro - 14 day refund policy and silver plan 10 euro - no refund policy"
            st.session_state.play_query = "What is the cost of the silver plan, and what is your refund policy?"
            st.session_state.play_output = "Silver plan cost 10 euro and 10 day return policy"
    with p_col2:
        if st.button("❌ Off-Topic Answer", use_container_width=True):
            st.session_state.play_context = "Our premium tier costs €49/month and includes 100 API credits. Our basic tier costs €19/month and includes 10 API credits. No refunds are allowed."
            st.session_state.play_query = "What is the cost of the premium tier, and what is your refund policy?"
            st.session_state.play_output = "We are running a special sale on shoes today! Get up to 50% off on all sneakers by using code SALE50."
    with p_col3:
        if st.button("✅ Perfect Compliance", use_container_width=True):
            st.session_state.play_context = "we have 2 plan one for gold client 20 euro - 14 day refund policy and silver plan 10 euro - no refund policy"
            st.session_state.play_query = "What is the cost of the silver plan, and what is your refund policy?"
            st.session_state.play_output = "The silver plan costs 10 euro and has no refund policy."

    # Sandbox Textareas
    text_context = st.text_area("Grounded Source Context (Fact Base)", value=st.session_state.play_context, height=80, key="context_input")
    text_query = st.text_input("User Question", value=st.session_state.play_query, key="query_input")
    text_output = st.text_area("Generated Output Response", value=st.session_state.play_output, height=80, key="output_input")
    
    # Python-side Heuristic Judge Engine
    if st.button("🔍 Run AI-Judge Evaluation Simulation", type="primary", use_container_width=True):
        c = text_context.lower().strip()
        q = text_query.lower().strip()
        o = text_output.lower().strip()
        
        evaluated_faithfulness = 100
        evaluated_relevancy = 100
        evaluated_hallucination = 0
        
        # Heuristics A: Find numerical mismatch & temporal pairing
        output_numbers = re.findall(r'\b\d+\b', o)
        for num in output_numbers:
            output_idx = o.find(num)
            if output_idx != -1:
                # Get surrounding string slice
                start_pt = max(0, output_idx - 25)
                end_pt = min(len(o), output_idx + 25)
                snippet = o[start_pt:end_pt]
                
                is_output_temporal = any(w in snippet for w in ['day', 'days', 'week', 'month', 'year', 'return', 'refund', 'policy', 'guarantee'])
                
                context_idx = c.find(num)
                if context_idx != -1:
                    c_snippet = c[max(0, context_idx - 25): min(len(c), context_idx + 25)]
                    is_context_temporal = any(w in c_snippet for w in ['day', 'days', 'week', 'month', 'year'])
                    
                    # Target dimension mismatch
                    if is_output_temporal and not is_context_temporal:
                        evaluated_faithfulness -= 40
                        evaluated_hallucination += 45
                else:
                    # Number completely made up
                    evaluated_faithfulness -= 30
                    evaluated_hallucination += 30

        # Heuristics B: Policy contradiction mapping
        if "no refund" in c or "no return" in c:
            has_refund_claim = any(word in o for word in ['day', 'days', 'return', 'refund', 'policy', 'guarantee']) and not any(w in o for w in ['no refund', 'no return'])
            if has_refund_claim:
                evaluated_faithfulness -= 45
                evaluated_hallucination += 40

        # Heuristics C: Relevancy validation
        query_words = [w for w in q.split() if len(w) > 3]
        match_count = sum(1 for w in query_words if w in o)
        if query_words:
            overlap_ratio = match_count / len(query_words)
            evaluated_relevancy = int(30 + (overlap_ratio * 70))
        else:
            evaluated_relevancy = 50

        # Apply limits
        st.session_state.faithfulness = min(100, max(10, evaluated_faithfulness))
        st.session_state.relevancy = min(100, max(10, evaluated_relevancy))
        st.session_state.hallucination = min(80, max(0, evaluated_hallucination))
        
        st.success("Analysis complete! Sliders and KPIs updated below.")

    st.markdown("---")
    
    # Benchmarking controls
    st.subheader("1. System Metric Calibration")
    slide_faithfulness = st.slider(
        "Faithfulness (Ragas) (%)", 
        min_value=10, max_value=100, step=5, 
        key="faithfulness",
        help="Checks if claims in output exist in the source document. 💡 Ideal Target: > 85%"
    )
    slide_relevancy = st.slider(
        "Answer Relevancy (DeepEval) (%)", 
        min_value=10, max_value=100, step=5, 
        key="relevancy",
        help="Checks if the output directly answers the user's question. 💡 Ideal Target: > 80%"
    )
    slide_hallucination = st.slider(
        "Hallucination Rate (DeepEval) (%)", 
        min_value=0, max_value=80, step=2, 
        key="hallucination",
        help="Detects fabricated statements that contradict the source context. 💡 Ideal Target: < 5%"
    )

    st.subheader("2. KPI Weight Configuration")
    weight_faith = st.slider(
        "Faithfulness Weight", 
        min_value=0, max_value=100, step=5, value=40,
        help="Priority multiplier inside the Overall Quality Index. 💡 Ideal Range: 30% - 50%"
    )
    weight_rel = st.slider(
        "Answer Relevancy Weight", 
        min_value=0, max_value=100, step=5, value=40,
        help="Priority multiplier inside the Overall Quality Index. 💡 Ideal Range: 30% - 50%"
    )
    weight_hall = st.slider(
        "Hallucination Penalty Weight", 
        min_value=0, max_value=100, step=5, value=20,
        help="Multiplies safety penalty. 💡 Ideal Range: 15% - 30%"
    )

# Mathematical Engine & Projections
total_weight = weight_faith + weight_rel + weight_hall
f_factor = (weight_faith / total_weight) if total_weight > 0 else 0
r_factor = (weight_rel / total_weight) if total_weight > 0 else 0
h_factor = (weight_hall / total_weight) if total_weight > 0 else 0

quality_score = (slide_faithfulness * f_factor) + (slide_relevancy * r_factor) + ((100 - slide_hallucination) * h_factor)

churn_risk = (100 - quality_score) * 1.5
if slide_hallucination > 15:
    churn_risk += (slide_hallucination - 15) * 2.2
churn_risk = min(99.5, max(1.5, churn_risk))

projected_csat = 1.0 + (quality_score / 100.0) * 4.0

# Right Panel Layout
with col_right:
    # 3 High-Impact KPI Cards
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.metric(
            label="Overall Quality Index",
            value=f"{quality_score:.1f}%",
            delta=f"{'Acceptable' if quality_score >= 80 else 'Unsafe'}",
            delta_color="normal" if quality_score >= 80 else "inverse"
        )
    with kpi_col2:
        st.metric(
            label="Predicted Churn Risk",
            value=f"{churn_risk:.1f}%",
            delta=f"{'Low Risk' if churn_risk <= 15 else 'High Churn Alert'}",
            delta_color="inverse" if churn_risk > 15 else "normal"
        )
    with kpi_col3:
        st.metric(
            label="Projected Customer CSAT",
            value=f"{projected_csat:.2f} / 5.0",
            delta=f"{'Target Met' if projected_csat >= 4.0 else 'Below SLA'}",
            delta_color="normal" if projected_csat >= 4.0 else "inverse"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Plotly Evaluation Timeline
    st.subheader("Quality Baseline Timeline")
    baseline_runs = [55.0, 58.5, 62.0, 71.5, 76.0]
    runs = baseline_runs + [quality_score]
    x_runs = ["Run 1", "Run 2", "Run 3", "Run 4", "Run 5", "Active Run"]

    fig = go.Figure()
    # Safe Target Line
    fig.add_trace(go.Scatter(
        x=x_runs, y=[80]*6,
        mode="lines",
        name="Target Threshold (80%)",
        line=dict(color="red", dash="dash", width=1.5)
    ))
    # Active timeline curve
    fig.add_trace(go.Scatter(
        x=x_runs, y=runs,
        mode="lines+markers",
        name="Evaluated Score",
        line=dict(color="#4f46e5", width=3),
        marker=dict(size=8, color="#10b981" if quality_score >= 80 else "#ef4444")
    ))
    fig.update_layout(
        yaxis_range=[0, 100],
        margin=dict(l=10, r=10, t=10, b=10),
        height=220,
        paper_bgcolor="#f8fafc",
        plot_bgcolor="#f8fafc",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Industry Standards Info Card
    st.markdown("""
    <div style="background-color: white; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 24px;">
        <span style="font-size: 11px; font-weight: bold; background-color: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">
            Ragas &amp; DeepEval Framework Compliance
        </span>
        <div style="display: grid; grid-template-columns: 1fr; gap: 12px; margin-top: 12px;">
            <div>
                <p style="font-size: 12px; font-weight: bold; color: #1e293b; margin: 0;">Ragas Framework (Faithfulness)</p>
                <p style="font-size: 11px; color: #64748b; margin: 4px 0 0 0; line-height: 1.4;">
                    Evaluates factual consistency. Ragas segments generated text into structural statements and queries an LLM to check if each assertion is explicitly mapped back to the source context vector.
                </p>
            </div>
            <div>
                <p style="font-size: 12px; font-weight: bold; color: #1e293b; margin: 0;">DeepEval (Relevancy &amp; Hallucinations)</p>
                <p style="font-size: 11px; color: #64748b; margin: 4px 0 0 0; line-height: 1.4;">
                    Measures user alignment. DeepEval calculates sentence vector alignments (cosine similarity) to establish relevancy and maps contradictions to output a strict hallucination rate.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Dynamic Strategy Memo Container
    st.subheader("System Quality Release Briefing")
    memo = f"""### 💼 PRODUCT OPERATIONS & LLM EVALUATION BRIEF
Generated: {datetime.now().strftime('%B %d, %Y')}
Author: Dhaval Kareliya | AI Product Management Operations
=========================================================================

1. EVALUATION CRITERIA METRICS (Industry Standard Frameworks)
-------------------------------------------------------------------------
* Faithfulness Score (Ragas Grounding) : {slide_faithfulness}%
* Answer Relevancy Score (DeepEval)    : {slide_relevancy}%
* Hallucination Rate (DeepEval)        : {slide_hallucination}%
>> Overall System Quality Index        : {quality_score:.1f}%

2. ALIGNMENT TO PRODUCT COHORT RETENTION
-------------------------------------------------------------------------
* Projected Customer CSAT Score        : {projected_csat:.2f} / 5.0 Stars
* Predicted Churn Risk (CSAT-impact)   : {churn_risk:.1f}%

DECISION ROADMAP:
"""
    if quality_score >= 85.0 and slide_hallucination <= 5:
        memo += f"- **Recommendation: APPROVED FOR STABLE RELEASE.** System quality matches production-grade thresholds. Hallucination index is strictly contained below 5%. Excellent faithfulness metrics assure reliable CSAT protection."
    elif quality_score < 70.0 or slide_hallucination > 15:
        memo += f"- **Recommendation: BLOCK DEPLOYMENT (REGRESSION DETECTED).** High hallucination rates ({slide_hallucination}%) pose critical branding and user churn liabilities. Prompt optimizations are required to ground output vectors."
    else:
        memo += f"- **Recommendation: CONDITIONAL ROLLOUT (MONITOR CLOSELY).** System performance is borderline acceptable. Latency and grounding indicators should be watched with an automated anomaly triage workflow."

    st.code(memo, language="markdown")
