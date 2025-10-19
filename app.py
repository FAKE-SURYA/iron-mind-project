import streamlit as st
import pandas as pd
from src.data_logger import GymCodingLogger
from src.analyzer import PerformanceAnalyzer
from src.visualizer import PerformanceVisualizer

st.set_page_config(page_title="Iron Mind Project", layout="wide", page_icon="🧠")

st.markdown('''
    <style>
    .main-header {font-size: 48px; font-weight: bold; text-align: center; color: #e74c3c;}
    .sub-header {font-size: 24px; color: #3498db; margin-bottom: 20px;}
    .tagline {font-size: 18px; text-align: center; color: #7f8c8d; margin-bottom: 30px;}
    </style>
''', unsafe_allow_html=True)

st.markdown('<p class="main-header">🧠 IRON MIND PROJECT</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Forging Iron. Sharpening Mind. Building Greatness.</p>', unsafe_allow_html=True)

st.sidebar.title("⚡ Navigation")
page = st.sidebar.radio("Go to", ["📝 Log Entry", "📊 Analytics", "🔮 Predictions", "🏆 Best Days"])

logger = GymCodingLogger()

if page == "📝 Log Entry":
    st.markdown('<p class="sub-header">Log Today\'s Metrics</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏋️ Iron Metrics")
        weight = st.number_input("Weight Lifted (kg)", min_value=0, max_value=300, value=30)
        workout = st.selectbox("Workout Type", 
                              ["Push (Chest, Triceps)", "Pull (Back, Biceps)", 
                               "Legs", "Cardio", "Rest Day"])
        protein = st.number_input("Protein Intake (g)", min_value=0, max_value=300, value=120)
        rest_day = 1 if workout == "Rest Day" else 0
    
    with col2:
        st.subheader("🧠 Mind Metrics")
        leetcode = st.number_input("LeetCode Problems Solved", min_value=0, max_value=50, value=0)
        coding_hrs = st.number_input("Coding Hours", min_value=0.0, max_value=24.0, value=0.0, step=0.5)
        commits = st.number_input("GitHub Commits", min_value=0, max_value=100, value=0)
        focus = st.slider("Focus Score (1-10)", 1, 10, 5)
        brain_fog = st.slider("Brain Fog Level (1-10)", 1, 10, 5)
    
    if st.button("💾 Save Entry", type="primary"):
        gym_data = {
            'weight_lifted_kg': weight,
            'workout_type': workout,
            'protein_intake_g': protein,
            'rest_day': rest_day
        }
        prod_data = {
            'leetcode_solved': leetcode,
            'coding_hours': coding_hrs,
            'github_commits': commits,
            'focus_score': focus,
            'brain_fog_level': brain_fog
        }
        logger.add_entry(gym_data, prod_data)
        st.success("✅ Entry saved successfully! Keep building greatness!")

elif page == "📊 Analytics":
    try:
        analyzer = PerformanceAnalyzer()
        visualizer = PerformanceVisualizer(analyzer)
        
        st.markdown('<p class="sub-header">Data Analytics Dashboard</p>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📅 Days Tracked", len(analyzer.df))
        with col2:
            st.metric("⏱️ Avg Coding Hours", f"{analyzer.df['coding_hours'].mean():.1f}")
        with col3:
            st.metric("💻 LeetCode Solved", int(analyzer.df['leetcode_solved'].sum()))
        with col4:
            st.metric("🎯 Avg Focus", f"{analyzer.df['focus_score'].mean():.1f}/10")
        
        st.subheader("🔥 Correlation Heatmap")
        st.pyplot(visualizer.correlation_heatmap())
        
        st.subheader("📈 Performance Trends Over Time")
        st.pyplot(visualizer.time_series_trends())
        
        st.subheader("🏋️ Productivity by Workout Type")
        st.pyplot(visualizer.workout_comparison())
        
        st.subheader("🎯 Key Insights: Iron vs Mind Correlations")
        top_corr = analyzer.gym_productivity_correlation().head(5)
        st.dataframe(top_corr, use_container_width=True)
        
    except Exception as e:
        st.error(f"Not enough data yet. Log at least 7 days to see analytics. Error: {e}")

elif page == "🔮 Predictions":
    st.markdown('<p class="sub-header">Predict Your Productivity</p>', unsafe_allow_html=True)
    
    try:
        analyzer = PerformanceAnalyzer()
        
        col1, col2 = st.columns(2)
        with col1:
            pred_weight = st.number_input("Planned Weight to Lift (kg)", 0, 300, 30)
        with col2:
            pred_protein = st.number_input("Planned Protein Intake (g)", 0, 300, 120)
        
        if st.button("🔮 Predict Focus Score"):
            prediction = analyzer.predict_productivity(pred_weight, pred_protein)
            st.success(f"Predicted Focus Score: **{prediction}/10**")
            
            if prediction >= 8:
                st.balloons()
                st.info("💪 Beast mode activated! This combo should give you peak performance!")
            elif prediction >= 6:
                st.info("👍 Solid performance expected. Keep grinding!")
            else:
                st.warning("⚠️ This might not be optimal. Consider adjusting your metrics.")
    
    except Exception as e:
        st.error("Need at least 10 days of data for predictions.")

elif page == "🏆 Best Days":
    st.markdown('<p class="sub-header">Your Best Performing Days</p>', unsafe_allow_html=True)
    
    try:
        analyzer = PerformanceAnalyzer()
        best_days = analyzer.best_performing_days(10)
        
        st.dataframe(best_days, use_container_width=True)
        
        st.info("💡 Analyze your best days to find patterns in your training and productivity!")
    except Exception as e:
        st.error(f"Not enough data yet. {e}")
