from groq import Groq
import os
import json
import re
from datetime import datetime

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_comprehensive_risks(project_data):
    """
    Comprehensive AI-powered risk analysis for construction project
    
    Args:
        project_data: Project specifications including location, start_date, soil_type, etc.
    
    Returns:
        dict: Comprehensive risk analysis with weather, site, and resource risks
    """
    
    current_date = "February 2026"
    location = project_data.get('location', 'India')
    start_date = project_data.get('start_date', '2026-02-06')
    duration_days = project_data.get('duration_days', 180)
    soil_type = project_data.get('soil_type', 'Clay')
    site_access = project_data.get('site_access', 'Easy')
    workforce_size = project_data.get('workforce_size', 20)
    machinery = project_data.get('machinery', 'Partial')
    total_cost = project_data.get('total_cost', 5000000)
    
    prompt = f"""You are a construction risk management expert analyzing potential risks for a construction project in India.

PROJECT DETAILS:
- Location: {location}, India
- Start Date: {start_date}
- Duration: {duration_days} days
- Soil Type: {soil_type}
- Site Accessibility: {site_access}
- Workforce Size: {workforce_size} workers
- Machinery: {machinery}
- Total Budget: ₹{total_cost}

COMPREHENSIVE RISK ANALYSIS REQUIRED:

1. WEATHER RISKS:
   a) Monsoon Impact:
      - Analyze if project timeline overlaps with monsoon season (June-September)
      - Calculate potential delay days due to rain
      - Assess flooding risk based on location
      - Recommend drainage and waterproofing measures
   
   b) Concrete Curing:
      - Analyze temperature and humidity conditions for start date
      - Assess curing quality risks
      - Recommend curing methods and precautions
   
   c) Seasonal Delays:
      - Identify weather-related work stoppages
      - Calculate buffer days needed
      - Estimate cost of weather protection measures

2. SITE RISKS:
   a) Soil Bearing Capacity ({soil_type} soil):
      - Assess foundation stability risks
      - Identify need for soil testing
      - Recommend foundation reinforcement if needed
      - Calculate additional foundation costs
   
   b) Groundwater Issues:
      - Assess groundwater table risk for {location}
      - Identify dewatering requirements
      - Recommend waterproofing measures
      - Calculate dewatering and waterproofing costs
   
   c) Slope and Leveling:
      - Assess site leveling requirements
      - Identify excavation challenges
      - Calculate additional earthwork costs
   
   d) Site Accessibility ({site_access}):
      - Assess material delivery challenges
      - Identify equipment access issues
      - Calculate logistics overhead

3. RESOURCE RISKS:
   a) Labor Shortage:
      - Assess labor availability in {location}
      - Identify skill shortage risks
      - Calculate wage inflation risk
      - Recommend labor retention strategies
   
   b) Equipment Breakdown:
      - Assess machinery reliability for {machinery} setup
      - Calculate downtime probability
      - Recommend backup equipment
      - Estimate breakdown cost impact
   
   c) Budget Overrun:
      - Identify cost escalation risks
      - Assess material price volatility
      - Calculate contingency adequacy
      - Recommend budget buffer
   
   d) Material Supply Chain:
      - Assess material availability in {location}
      - Identify supply chain disruption risks
      - Recommend material procurement strategy

Return ONLY a valid JSON object:
{{
    "overall_risk_score": <1-10>,
    "overall_risk_level": "Low/Medium/High/Critical",
    
    "weather_risks": {{
        "monsoon": {{
            "risk_level": "Low/Medium/High",
            "probability": <percentage>,
            "impact_days": <number>,
            "description": "Detailed monsoon impact analysis",
            "mitigation": "Specific mitigation strategies",
            "mitigation_cost": <number>
        }},
        "flooding": {{
            "risk_level": "Low/Medium/High",
            "probability": <percentage>,
            "description": "Flooding risk assessment",
            "mitigation": "Drainage and protection measures",
            "mitigation_cost": <number>
        }},
        "concrete_curing": {{
            "risk_level": "Low/Medium/High",
            "description": "Curing conditions analysis",
            "mitigation": "Curing method recommendations",
            "mitigation_cost": <number>
        }},
        "seasonal_delays": {{
            "buffer_days": <number>,
            "cost_impact": <number>,
            "protection_measures": "Weather protection recommendations"
        }}
    }},
    
    "site_risks": {{
        "soil_bearing": {{
            "risk_level": "Low/Medium/High",
            "description": "Soil bearing capacity assessment for {soil_type}",
            "testing_required": true/false,
            "mitigation": "Foundation reinforcement recommendations",
            "mitigation_cost": <number>
        }},
        "groundwater": {{
            "risk_level": "Low/Medium/High",
            "water_table_depth": "Estimated depth in meters",
            "dewatering_required": true/false,
            "mitigation": "Dewatering and waterproofing strategy",
            "mitigation_cost": <number>
        }},
        "slope_leveling": {{
            "risk_level": "Low/Medium/High",
            "additional_earthwork": <cubic meters>,
            "mitigation_cost": <number>
        }},
        "site_access": {{
            "risk_level": "Low/Medium/High",
            "challenges": "Access challenges for {site_access} accessibility",
            "logistics_overhead": <number>
        }}
    }},
    
    "resource_risks": {{
        "labor_shortage": {{
            "risk_level": "Low/Medium/High",
            "probability": <percentage>,
            "skill_gaps": ["List of potential skill shortages"],
            "wage_inflation_risk": <percentage>,
            "mitigation": "Labor retention and recruitment strategy",
            "mitigation_cost": <number>
        }},
        "equipment_breakdown": {{
            "risk_level": "Low/Medium/High",
            "downtime_probability": <percentage>,
            "estimated_downtime_days": <number>,
            "mitigation": "Backup equipment and maintenance strategy",
            "mitigation_cost": <number>
        }},
        "budget_overrun": {{
            "risk_level": "Low/Medium/High",
            "probability": <percentage>,
            "potential_overrun": <number>,
            "cost_drivers": ["List of main cost escalation factors"],
            "mitigation": "Budget control measures",
            "additional_contingency": <number>
        }},
        "supply_chain": {{
            "risk_level": "Low/Medium/High",
            "critical_materials": ["List of materials with supply risk"],
            "mitigation": "Procurement and inventory strategy",
            "mitigation_cost": <number>
        }}
    }},
    
    "critical_risks": [
        "Top 3-5 most critical risks that need immediate attention"
    ],
    
    "total_mitigation_cost": <number>,
    "recommended_contingency_percent": <percentage>,
    
    "risk_timeline": {{
        "pre_monsoon_actions": ["Actions to complete before monsoon"],
        "ongoing_monitoring": ["Continuous monitoring requirements"],
        "critical_milestones": ["Risk-sensitive project milestones"]
    }}
}}

Be SPECIFIC with numbers, costs, and probabilities. Base analysis on real construction industry data for {location}, India in {current_date}."""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=3000
        )
        
        response_text = completion.choices[0].message.content
        return parse_risk_json(response_text)
        
    except Exception as e:
        return {
            "error": f"AI risk analysis failed: {str(e)}",
            "overall_risk_score": 5,
            "overall_risk_level": "Medium",
            "weather_risks": {},
            "site_risks": {},
            "resource_risks": {},
            "critical_risks": ["AI analysis unavailable - manual risk assessment recommended"]
        }


def parse_risk_json(text):
    """Parse JSON from AI response, handling markdown code blocks"""
    try:
        # Remove markdown code blocks if present
        json_match = re.search(r'```(?:json)?\s*(\{.*\})\s*```', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON object directly
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            json_str = json_match.group(0) if json_match else text
        
        return json.loads(json_str)
    except:
        return {
            "error": "Failed to parse AI response",
            "raw_response": text[:500],
            "overall_risk_score": 5,
            "overall_risk_level": "Unknown"
        }
