import html

# ...

        col1.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Issue Type</div>
            <div class="metric-value">{html.escape(data["issue_type"])}</div>
        </div>
        """, unsafe_allow_html=True)

        # ...

        st.markdown(f"""
        <div class="card">
            <h4>
 Root Cause Analysis</h4>
            <p>{html.escape(data["root_cause"])}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 

 Recommended Fixes")

        for i, step in enumerate(data["suggested_fixes"], 1):
            st.markdown(f"""
            <div class="fix-card">
                <b>Step {i}:</b> {html.escape(step)}
            </div>
            """, unsafe_allow_html=True)


        st.markdown("### 

 AI Evaluation")

        col_j1, col_j2 = st.columns([1, 3])

        col_j1.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Score</div>
            <div class="metric-value">{judge["score"]}/10</div>
        </div>
        """, unsafe_allow_html=True)

        col_j2.markdown(f"""
        <div class="card">
            <h4>
 Feedback</h4>
            <p>{html.escape(judge["feedback"])}</p>
        </div>
        """, unsafe_allow_html=True)