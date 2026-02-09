import urllib.request
import urllib.parse
import json
import http.cookiejar

base_url = "http://127.0.0.1:5000"

# Setup cookie jar to handle sessions
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

# Project data for submission
project_data = {
    "location": "Bangalore, India",
    "area": 2400,
    "floors": 2,
    "quality": "Premium",
    "priority": "Speed",
    "soil_type": "Rocky",
    "material_grade": "Premium",
    "machinery": "Full",
    "workforce_size": 50,
    "start_date": "2026-03-01",
    "site_access": "Easy",
    "budget": 5000000
}

data = urllib.parse.urlencode(project_data).encode()

print("--- Testing Project Submission ---")
try:
    req = urllib.request.Request(f"{base_url}/", data=data)
    with urllib.request.urlopen(req) as response:
        content = response.read().decode()
        print(f"Status Code: {response.getcode()}")
        print(f"Final URL: {response.geturl()}")
        
        if "/dashboard" in response.geturl():
            print("SUCCESS: Redirected to Dashboard")
            if "Total Estimate:" in content:
                print("SUCCESS: Dashboard contains Total Estimate")
            if "Project Phase Breakdown" in content:
                print("SUCCESS: Dashboard contains Phase Breakdown table")
        else:
            print("FAILURE: Did not redirect to Dashboard")
            print(content[:500])

    print("\n--- Testing Analytics Page ---")
    req_analytics = urllib.request.Request(f"{base_url}/analytics")
    with urllib.request.urlopen(req_analytics) as response:
        content_analytics = response.read().decode()
        print(f"Analytics Status: {response.getcode()}")
        if "Visual Analytics" in content_analytics:
            print("SUCCESS: Analytics page served")
            if "chartData" in content_analytics:
                print("SUCCESS: Analytics page contains chartData")
    
    print("\n--- Testing Risk Analysis Page ---")
    req_risks = urllib.request.Request(f"{base_url}/risks")
    with urllib.request.urlopen(req_risks) as response:
        content_risks = response.read().decode()
        print(f"Risks Status: {response.getcode()}")
        if "Risk Analysis" in content_risks:
            print("SUCCESS: Risk Analysis page served")

except Exception as e:
    print(f"Verification failed: {e}")
