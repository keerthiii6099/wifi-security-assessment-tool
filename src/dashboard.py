import streamlit as st
import time
import pandas as pd

from src.visualizations import create_charts
from src.recommendations import generate_recommendations


def create_main_dashboard():
    """Main dashboard page"""

    st.title("📡 WiFi Security Assessment Tool")
    st.markdown("### Comprehensive Wireless Network Vulnerability Analysis")

    with st.sidebar:
        st.header("🛠️ Scan Settings")

        scan_mode = st.selectbox(
            "Scan Mode",
            ["Demo Mode (Simulated Data)"],
            help="Demo mode generates realistic sample data for educational purposes"
        )

        if scan_mode == "Demo Mode (Simulated Data)":

            num_networks = st.slider(
                "Number of Networks to Simulate",
                5,
                20,
                12
            )

            if st.button("🔍 Start Demo Scan", type="primary"):

                with st.spinner("Scanning for networks..."):
                    time.sleep(2)

                    networks_found = (
                        st.session_state.wifi_tool
                        .simulate_network_data(num_networks)
                    )

                    st.session_state.wifi_tool.assess_encryption_strength()

                    st.session_state.scan_completed = True

                    st.success(
                        f"Found {networks_found} networks!"
                    )

    if st.session_state.scan_completed:
        display_scan_results()
    else:
        display_welcome_screen()


def display_welcome_screen():
    """Display welcome screen before scanning"""

    st.subheader("🔐 Welcome to WiFi Security Assessment")

    st.write(
        "An educational tool for analyzing wireless network "
        "security vulnerabilities."
    )

    st.info(
        "👈 Use the sidebar to start your security assessment."
    )

    st.warning(
        "🎓 Educational Purpose: This tool is designed for learning "
        "about wireless security concepts and should only be used on "
        "networks you own or have explicit permission to test."
    )


def display_scan_results():
    """Display comprehensive scan results"""

    wifi_tool = st.session_state.wifi_tool

    display_summary_metrics(wifi_tool.networks)

    create_charts(wifi_tool.networks)

    display_network_table(wifi_tool.networks)

    display_vulnerability_details(wifi_tool.networks)

    display_recommendations(wifi_tool.networks)


def display_summary_metrics(networks):
    """Display summary metrics"""

    st.subheader("📊 Security Overview")

    col1, col2, col3, col4 = st.columns(4)

    total_networks = len(networks)

    critical_count = sum(
        1 for n in networks
        if n.get("vulnerability_level") == "Critical"
    )

    open_count = sum(
        1 for n in networks
        if n.get("encryption") == "Open"
    )

    secure_count = sum(
        1 for n in networks
        if n.get("encryption") in ["WPA3", "WPA2"]
    )

    with col1:
        st.metric(
            "Total Networks",
            total_networks
        )

    with col2:
        st.metric(
            "Critical Vulnerabilities",
            critical_count,
            delta=f"{-critical_count} to fix"
        )

    with col3:
        st.metric(
            "Open Networks",
            open_count,
            delta="High Risk" if open_count > 0 else "Good"
        )

    with col4:

        secure_percentage = (
            (secure_count / total_networks) * 100
            if total_networks > 0
            else 0
        )

        st.metric(
            "Secure Networks",
            secure_count,
            delta=f"{secure_percentage:.1f}%"
        )


def display_network_table(networks):
    """Display detailed network table"""

    st.subheader("🔍 Detailed Network Analysis")

    df = pd.DataFrame(networks)

    display_df = df[
        [
            "ssid",
            "encryption",
            "signal",
            "channel",
            "vulnerability_level",
            "vulnerability_score",
            "crack_time"
        ]
    ].copy()

    display_df.columns = [
        "Network Name",
        "Encryption",
        "Signal (dBm)",
        "Channel",
        "Risk Level",
        "Risk Score",
        "Est. Crack Time"
    ]

    display_df = display_df.sort_values(
        "Risk Score",
        ascending=False
    )

    def highlight_risk(row):

        if row["Risk Level"] == "Critical":
            return ["background-color: #ffe6e6"] * len(row)

        elif row["Risk Level"] == "High":
            return ["background-color: #fff2e6"] * len(row)

        elif row["Risk Level"] == "Medium":
            return ["background-color: #fffde6"] * len(row)

        else:
            return ["background-color: #e6ffe6"] * len(row)

    st.dataframe(
        display_df.style.apply(
            highlight_risk,
            axis=1
        ),
        use_container_width=True,
        hide_index=True
    )


def display_vulnerability_details(networks):
    """Display vulnerability details for selected network"""

    st.subheader("⚠️ Vulnerability Details")

    selected_network = st.selectbox(
        "Select network for detailed analysis:",
        options=[n["ssid"] for n in networks]
    )

    if selected_network:

        network_data = next(
            n for n in networks
            if n["ssid"] == selected_network
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"**Network:** {network_data['ssid']}"
            )

            st.markdown(
                f"**Encryption:** {network_data['encryption']}"
            )

            st.markdown(
                f"**Signal Strength:** "
                f"{network_data['signal']} dBm"
            )

            st.markdown(
                f"**Channel:** {network_data['channel']}"
            )

            st.markdown(
                f"**Risk Level:** "
                f"{network_data['vulnerability_level']}"
            )

            st.markdown(
                f"**Risk Score:** "
                f"{network_data['vulnerability_score']}/10"
            )

        with col2:

            st.markdown("**Specific Vulnerabilities:**")

            for vuln in network_data["vulnerabilities"]:
                st.markdown(f"• {vuln}")

            st.markdown(
                f"**Estimated Crack Time:** "
                f"{network_data['crack_time']}"
            )


def display_recommendations(networks):
    """Display security recommendations"""

    st.subheader("🛡️ Security Recommendations")

    recommendations = generate_recommendations(networks)

    for i, rec in enumerate(recommendations, 1):

        if "URGENT" in rec:
            st.error(f"{i}. {rec}")

        elif "HIGH PRIORITY" in rec:
            st.warning(f"{i}. {rec}")

        else:
            st.info(f"{i}. {rec}")