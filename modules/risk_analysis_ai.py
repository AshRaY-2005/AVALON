from modules.ai_client import client
import re
import json

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
    
    prompt = f"""You are a senior geotechnical and construction risk engineer. Perform a TECHNICAL risk assessment for a project in {location}, India.
Location Data: {location}. Start Date: {start_date}. Duration: {duration_days} days. 
Sub-surface Context: {soil_type} soil. Machinery: {machinery}.

ANALYSIS REQUIREMENTS:
1. SEASONAL & ENVIRONMENTAL:
   - MONSOON: Precise impact check (Start: {start_date}). Calculate probability and days of delay. Provide concrete dewatering and site-sealing solutions.
   - TEMPERATURE & HUDMIDITY: Analyze impact on CURING TIME. Explain how extreme heat (March-June) or cooling (Nov-Jan) affects structural strength.
   - FLOODING: Assess local topography risks and provide drainage infrastructure solutions.

2. GEOTECHNICAL & STRUCTURAL:
   - BEARING CAPACITY: Analyze {soil_type} specific risks (e.g. expansiveness, settlement). Provide foundation reinforcement strategies.
   - GROUNDWATER: Detect seepage risks. Propose specific dewatering or waterproofing measures.

3. RESOURCE & EXECUTION:
   - Identify "High-Probability Error zones" (e.g. poor curing, shuttering misalignment).
   - Quantify OVERRUN PROBABILITY and MITIGATION COSTS in INR (₹).

Return ONLY a minified JSON object. NO markdown, NO code blocks, NO preamble.

JSON Structure:
{{
    "overall_risk_score": number, 
    "overall_risk_level": "string",
    "risk_categories": [
        {{
            "category": "Environmental & Seasonal",
            "risks": [
                {{
                    "title": "Monsoon & Flooding",
                    "probability": number,
                    "potential_delay": number,
                    "mitigation_strategy": "string",
                    "mitigation_cost": number,
                    "risk_level": "string"
                }},
                {{
                    "title": "Curing & Temp Variance",
                    "probability": number,
                    "impact_description": "Effect on concrete strength and schedule",
                    "mitigation_strategy": "Season-specific curing protocols",
                    "mitigation_cost": number,
                    "risk_level": "string"
                }}
            ]
        }},
        {{
            "category": "Geotechnical & Site",
            "risks": [
                {{
                    "title": "Soil Bearing Capacity",
                    "description": "Risks related to foundation settlement or expansion in {soil_type} soil",
                    "mitigation_strategy": "Foundation reinforcement methods",
                    "mitigation_cost": number,
                    "risk_level": "string"
                }},
                {{
                    "title": "Groundwater Seepage",
                    "mitigation_strategy": "Dewatering and site waterproofing",
                    "mitigation_cost": number,
                    "risk_level": "string"
                }}
            ]
        }},
        {{
            "category": "Resource & Financial",
            "risks": [
                {{
                    "title": "Budget & Overrun",
                    "overrun_probability": number,
                    "potential_overrun": number,
                    "additional_contingency": number,
                    "risk_level": "string"
                }}
            ]
        }}
    ],
    "risk_management_timeline": [
        {{ "phase": "Pre-Construction / Pre-Monsoon", "items": ["string"] }},
        {{ "phase": "Ongoing Monitoring", "items": ["string"] }}
    ],
    "total_mitigation_cost": number,
    "recommended_contingency_percent": number
}}"""

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
    try:
        # Clean text: remove markdown if present
        text = re.sub(r'```(?:json)?\s*|\s*```', '', text)
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        return {
            "error": "No JSON found in response",
            "overall_risk_score": 5,
            "overall_risk_level": "Medium"
        }
    except Exception as e:
        return {
            "error": f"Failed to parse AI response: {str(e)}",
            "overall_risk_score": 5,
            "overall_risk_level": "Unknown"
        }
