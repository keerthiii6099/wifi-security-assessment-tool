import random

class WiFiSecurityAssessment:
    def __init__(self):
        self.networks = []
        self.vulnerability_report = {}
        self.common_passwords = [
            "password", "123456789", "password123", "admin", "12345678",
            "qwerty", "abc123", "Password1", "welcome", "letmein"
        ]
    
    def simulate_network_data(self, num_networks=10):
        """Generate realistic network data for demonstration"""
        ssid_prefixes = ["HomeNetwork", "OfficeWiFi", "PublicWiFi", "SecureNet", "RouterNet", 
                        "WiFi", "Network", "Internet", "Broadband", "Wireless"]
        encryption_types = ["Open", "WEP", "WPA", "WPA2", "WPA3"]
        channels = [1, 3, 6, 11, 36, 40, 44, 48, 149, 153, 157, 161, 165]
        
        sample_networks = []
        for i in range(num_networks):
            network = {
                "ssid": f"{random.choice(ssid_prefixes)}_{random.randint(100, 999)}",
                "encryption": random.choices(encryption_types, weights=[5, 10, 15, 50, 20])[0],
                "signal": random.randint(-80, -25),
                "channel": random.choice(channels),
                "mac_address": ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
            }
            sample_networks.append(network)
        
        # Add some specific vulnerable networks for demo
        vulnerable_examples = [
            {"ssid": "FreeWiFi", "encryption": "Open", "signal": -35, "channel": 6, "mac_address": "aa:bb:cc:dd:ee:ff"},
            {"ssid": "OldRouter_WEP", "encryption": "WEP", "signal": -45, "channel": 11, "mac_address": "11:22:33:44:55:66"},
            {"ssid": "DefaultRouter", "encryption": "WPA", "signal": -52, "channel": 1, "mac_address": "77:88:99:aa:bb:cc"}
        ]
        
        self.networks = sample_networks + vulnerable_examples
        return len(self.networks)
    
    def assess_encryption_strength(self):
        """Assess encryption strength and vulnerabilities"""
        vulnerability_levels = {
            'Open': {'level': 'Critical', 'score': 10, 'color': '#ff4444'},
            'WEP': {'level': 'Critical', 'score': 9, 'color': '#ff6666'},
            'WPA': {'level': 'High', 'score': 7, 'color': '#ff9900'},
            'WPA2': {'level': 'Medium', 'score': 4, 'color': '#ffcc00'},
            'WPA3': {'level': 'Low', 'score': 2, 'color': '#00cc00'}
        }
        
        vulnerability_descriptions = {
            'Open': ['No encryption - all data transmitted in plaintext', 'Susceptible to man-in-the-middle attacks', 'Easy traffic interception'],
            'WEP': ['Weak 40/104-bit encryption', 'Vulnerable to IV attacks', 'RC4 stream cipher weaknesses', 'Can be cracked in minutes'],
            'WPA': ['TKIP vulnerabilities', 'Susceptible to dictionary attacks', '4-way handshake weaknesses'],
            'WPA2': ['Vulnerable to KRACK attacks', 'WPS PIN vulnerabilities', 'Dictionary attacks on weak passwords'],
            'WPA3': ['Most secure current standard', 'Resistant to offline attacks', 'Minor timing attack vulnerabilities']
        }
        
        for network in self.networks:
            encryption = network.get('encryption', 'Unknown')
            vuln_info = vulnerability_levels.get(encryption, {'level': 'Unknown', 'score': 5, 'color': '#cccccc'})
            
            network['vulnerability_level'] = vuln_info['level']
            network['vulnerability_score'] = vuln_info['score']
            network['color'] = vuln_info['color']
            network['vulnerabilities'] = vulnerability_descriptions.get(encryption, ['Unknown vulnerabilities'])
            
            # Calculate crack time estimation
            network['crack_time'] = self.estimate_crack_time(encryption, network.get('signal', -60))
    
    def estimate_crack_time(self, encryption, signal_strength):
        """Estimate time to crack based on encryption and signal strength"""
        base_times = {
            'Open': 'Immediate',
            'WEP': '2-10 minutes',
            'WPA': '2-8 hours (dictionary), days-weeks (brute force)',
            'WPA2': '4-24 hours (dictionary), months-years (brute force)', 
            'WPA3': 'Years to decades (current technology)'
        }
        
        # Adjust based on signal strength (stronger signal = easier to attack)
        if signal_strength > -40:
            modifier = " (Strong signal - easier attack)"
        elif signal_strength < -70:
            modifier = " (Weak signal - harder attack)"
        else:
            modifier = ""
            
        return base_times.get(encryption, 'Unknown') + modifier