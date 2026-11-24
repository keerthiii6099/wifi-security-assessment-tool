import streamlit as st
import pandas as pd
import plotly.express as px


def create_charts(networks):
    """Create all visualization charts"""

    st.subheader("📈 Vulnerability Analysis")

    df = pd.DataFrame(networks)

    col1, col2 = st.columns(2)

    with col1:
        create_encryption_pie_chart(df)

    with col2:
        create_vulnerability_bar_chart(df)

    # Signal strength vs vulnerability scatter plot
    create_signal_vulnerability_scatter(df)


def create_encryption_pie_chart(df):
    """Create encryption distribution pie chart"""

    enc_counts = df["encryption"].value_counts()

    fig_pie = px.pie(
        values=enc_counts.values,
        names=enc_counts.index,
        title="Encryption Type Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    st.plotly_chart(fig_pie, use_container_width=True)


def create_vulnerability_bar_chart(df):
    """Create vulnerability level bar chart"""

    vuln_counts = df["vulnerability_level"].value_counts()

    colors = {
        "Critical": "#ff4444",
        "High": "#ff9900",
        "Medium": "#ffcc00",
        "Low": "#00cc00"
    }

    fig_bar = px.bar(
        x=vuln_counts.index,
        y=vuln_counts.values,
        title="Vulnerability Level Distribution",
        color=vuln_counts.index,
        color_discrete_map=colors
    )

    fig_bar.update_layout(showlegend=False)

    st.plotly_chart(fig_bar, use_container_width=True)


def create_signal_vulnerability_scatter(df):
    """Create signal strength vs vulnerability scatter plot"""

    st.subheader("🎯 Signal Strength vs Vulnerability Analysis")

    fig_scatter = px.scatter(
        df,
        x="signal",
        y="vulnerability_score",
        color="encryption",
        size="vulnerability_score",
        hover_data=["ssid", "channel"],
        title="Signal Strength vs Vulnerability Score",
        labels={
            "signal": "Signal Strength (dBm)",
            "vulnerability_score": "Vulnerability Score (0-10)"
        }
    )

    st.plotly_chart(fig_scatter, use_container_width=True)