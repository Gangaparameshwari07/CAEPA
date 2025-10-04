import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def render_analytics_dashboard():
    st.title("📊 CAEPA Analytics Dashboard")
    
    try:
        response = requests.get("http://localhost:8000/dashboard")
        if response.status_code == 200:
            data = response.json()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Analyses", data["total_analyses"])
            with col2:
                st.metric("Avg Latency", f"{data['avg_latency']:.0f}ms")
            with col3:
                violation_rate = (data["status_distribution"].get("RED", 0) + 
                                data["status_distribution"].get("YELLOW", 0)) / data["total_analyses"] * 100
                st.metric("Violation Rate", f"{violation_rate:.1f}%")
            with col4:
                compliance_rate = data["status_distribution"].get("GREEN", 0) / data["total_analyses"] * 100
                st.metric("Compliance Rate", f"{compliance_rate:.1f}%")
            
            # Status Distribution Pie Chart
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Compliance Status Distribution")
                status_df = pd.DataFrame(
                    list(data["status_distribution"].items()),
                    columns=["Status", "Count"]
                )
                
                colors = {"GREEN": "#28a745", "YELLOW": "#ffc107", "RED": "#dc3545"}
                fig_pie = px.pie(
                    status_df, 
                    values="Count", 
                    names="Status",
                    color="Status",
                    color_discrete_map=colors
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.subheader("Top Violations")
                violations_df = pd.DataFrame(
                    list(data["top_violations"].items()),
                    columns=["Violation", "Count"]
                )
                
                if not violations_df.empty:
                    fig_bar = px.bar(
                        violations_df,
                        x="Count",
                        y="Violation",
                        orientation="h",
                        color="Count",
                        color_continuous_scale="Reds"
                    )
                    fig_bar.update_layout(height=400)
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No violations detected yet!")
            
            # Compliance Trend
            st.subheader("Compliance Score Trend")
            if data["compliance_trend"]:
                trend_df = pd.DataFrame(
                    list(data["compliance_trend"].items()),
                    columns=["Date", "Score"]
                )
                trend_df["Date"] = pd.to_datetime(trend_df["Date"])
                
                fig_line = px.line(
                    trend_df,
                    x="Date",
                    y="Score",
                    title="Daily Compliance Scores",
                    markers=True
                )
                fig_line.update_layout(yaxis_range=[0, 100])
                st.plotly_chart(fig_line, use_container_width=True)
            
            # Domain Breakdown
            st.subheader("Domain Analysis Breakdown")
            domain_data = []
            for domain, stats in data["domain_breakdown"].items():
                compliance_rate = ((stats["total"] - stats["violations"]) / stats["total"] * 100) if stats["total"] > 0 else 0
                domain_data.append({
                    "Domain": domain.upper(),
                    "Total Analyses": stats["total"],
                    "Violations": stats["violations"],
                    "Compliance Rate": f"{compliance_rate:.1f}%"
                })
            
            if domain_data:
                domain_df = pd.DataFrame(domain_data)
                st.dataframe(domain_df, use_container_width=True)
            
        else:
            st.error("Unable to load dashboard data")
            
    except Exception as e:
        st.error(f"Dashboard error: {str(e)}")

def render_learning_insights():
    st.title("🧠 Continuous Learning Insights")
    
    try:
        response = requests.get("http://localhost:8000/learning-insights")
        if response.status_code == 200:
            insights = response.json()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Feedback Received", insights["total_feedback"])
                st.metric("Model Accuracy", f"{insights['accuracy_rate']:.1%}")
            
            with col2:
                st.subheader("Improvement Areas")
                for area in insights["improvement_areas"]:
                    st.write(f"• {area}")
            
            # Feedback submission
            st.subheader("Provide Feedback")
            with st.form("feedback_form"):
                analysis_id = st.number_input("Analysis ID", min_value=0, value=0)
                feedback = st.selectbox("Feedback", ["correct", "incorrect"])
                
                if st.form_submit_button("Submit Feedback"):
                    feedback_response = requests.post(
                        "http://localhost:8000/feedback",
                        json={"analysis_id": analysis_id, "feedback": feedback}
                    )
                    
                    if feedback_response.status_code == 200:
                        st.success("Feedback submitted! CAEPA will learn from this.")
                    else:
                        st.error("Failed to submit feedback")
                        
    except Exception as e:
        st.error(f"Learning insights error: {str(e)}")

if __name__ == "__main__":
    st.set_page_config(page_title="CAEPA Dashboard", layout="wide")
    
    tab1, tab2 = st.tabs(["📊 Analytics", "🧠 Learning"])
    
    with tab1:
        render_analytics_dashboard()
    
    with tab2:
        render_learning_insights()