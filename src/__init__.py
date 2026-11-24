from .wifi_assessment import WiFiSecurityAssessment
from .dashboard import create_main_dashboard
from .visualizations import create_charts
from .recommendations import generate_recommendations

__version__ = "1.0.0"
__author__ = "WiFi Security Team"
__description__ = "Educational WiFi Security Assessment Tool"

__all__ = [
    "WiFiSecurityAssessment",
    "create_main_dashboard",
    "create_charts",
    "generate_recommendations"
]