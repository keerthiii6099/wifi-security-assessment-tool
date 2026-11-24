def generate_recommendations(networks):
    """Generate security recommendations based on scan results"""
    recommendations = []

    # Count vulnerabilities
    critical_count = sum(
        1 for n in networks
        if n.get('vulnerability_level') == 'Critical'
    )

    open_count = sum(
        1 for n in networks
        if n.get('encryption') == 'Open'
    )

    wep_count = sum(
        1 for n in networks
        if n.get('encryption') == 'WEP'
    )

    wpa_count = sum(
        1 for n in networks
        if n.get('encryption') == 'WPA'
    )

    if open_count > 0:
        recommendations.append(
            f"🚨 URGENT: {open_count} open network(s) detected - "
            "Enable encryption immediately"
        )

    if wep_count > 0:
        recommendations.append(
            f"🚨 URGENT: {wep_count} WEP network(s) found - "
            "Upgrade to WPA2/WPA3"
        )

    if wpa_count > 0:
        recommendations.append(
            f"⚠️ HIGH PRIORITY: {wpa_count} WPA network(s) detected - "
            "Upgrade to WPA2/WPA3"
        )

    # General recommendations
    general_recs = [
        "Use WPA3 encryption when available",
        "Implement strong, unique passwords (12+ characters with mixed case, numbers, symbols)",
        "Disable WPS (WiFi Protected Setup) to prevent PIN attacks",
        "Change default router admin credentials",
        "Enable network isolation/guest networks for visitors",
        "Regularly update router firmware",
        "Use enterprise authentication (802.1X) for business networks",
        "Implement network monitoring and intrusion detection",
        "Conduct regular security assessments"
    ]

    recommendations.extend(general_recs)

    return recommendations