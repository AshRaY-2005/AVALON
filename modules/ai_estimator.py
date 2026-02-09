from modules.ai_client import client
import json
import re

def ai_estimate(project):
    total_area = project['area'] * project['floors']
    current_date = "February 2026"
    
    soil_type = project.get('soil_type', 'Clay')
    material_grade = project.get('material_grade', 'Standard')
    machinery = project.get('machinery', 'Partial')
    workforce_size = project.get('workforce_size', 20)
    start_date = project.get('start_date', '2026-02-06')
    site_access = project.get('site_access', 'Easy')

    # System-level role and formatting instructions
    system_msg = "You are a professional construction cost estimator for projects in India. You must return only valid JSON."

    prompt = f"""Provide a RIGOROUS construction estimation for a {total_area} sq. yard building in {project['location']}, India.
Start Date: {start_date}. Material Grade: {material_grade}. Quality: {project['quality']}.

MATHEMATICAL VERIFICATION RULES (MANDATORY):
1. total_cost MUST EQUAL EXACTLY THE SUM of all 7 phase costs.
2. total_cost MUST EQUAL EXACTLY THE SUM of all 5 resource_costs.
3. Provide a 'calculation_logic' field explaining the exact math used to reach these numbers.
4. Use realistic market rates for {project['location']} as of {current_date}.

Include:
1. Phase breakdown (7 phases: site_prep, foundation, structural, brickwork, elec_plumbing, finishing, handover)
2. Resource costs (labor, material, machinery, overhead, contingency)
3. Workforce allocation (masons, helpers, steel_workers, carpenters, supervisors)
4. AI Insight and Risk Analysis.

Return ONLY a minified JSON object. NO markdown, NO code blocks, NO preamble.

JSON Structure:
{{
    "total_cost": number,
    "cost_per_sqyd": number,
    "phase_breakdown": {{
        "site_preparation": {{"cost": number, "duration_days": number, "description": "text"}},
        "foundation": {{"cost": number, "duration_days": number, "description": "text"}},
        "structural_work": {{"cost": number, "duration_days": number, "description": "text"}},
        "brickwork": {{"cost": number, "duration_days": number, "description": "text"}},
        "electrical_plumbing": {{"cost": number, "duration_days": number, "description": "text"}},
        "finishing": {{"cost": number, "duration_days": number, "description": "text"}},
        "handover": {{"cost": number, "duration_days": number, "description": "text"}}
    }},
    "resource_costs": {{
        "labor_cost": number,
        "machinery_cost": number,
        "material_cost": number,
        "overhead": number,
        "contingency": number
    }},
    "calculation_logic": "Explain exactly how total_cost sum matches phases and resources. Show the math.",
    "timeline": {{
        "total_days": number,
        "critical_path": ["list"],
        "weather_delays": number,
        "seasonal_notes": "text"
    }},
    "workforce": {{
        "masons": number, "helpers": number, "steel_workers": number, "carpenters": number, "supervisors": number
    }},
    "ai_insight": "Strategic optimization advice",
    "risk": "Top risks considering {project['quality']} standards"
}}"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=3000
    )

    text = completion.choices[0].message.content
    return parse_json(text)

def parse_json(text):
    try:
        # Clean text: remove markdown if present
        text = re.sub(r'```(?:json)?\s*|\s*```', '', text)
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        return get_fallback_data("No JSON found in response")
    except Exception as e:
        return get_fallback_data(f"Parsing error: {str(e)}")

def get_fallback_data(error_msg):
    return {
        "total_cost": 0,
        "cost_per_sqyd": 0,
        "phase_breakdown": {
            "site_preparation": {"cost": 0, "duration_days": 0, "description": error_msg},
            "foundation": {"cost": 0, "duration_days": 0, "description": error_msg},
            "structural_work": {"cost": 0, "duration_days": 0, "description": error_msg},
            "brickwork": {"cost": 0, "duration_days": 0, "description": error_msg},
            "electrical_plumbing": {"cost": 0, "duration_days": 0, "description": error_msg},
            "finishing": {"cost": 0, "duration_days": 0, "description": error_msg},
            "handover": {"cost": 0, "duration_days": 0, "description": error_msg}
        },
        "resource_costs": {"labor_cost": 0, "machinery_cost": 0, "material_cost": 0, "overhead": 0, "contingency": 0},
        "timeline": {"total_days": 0, "critical_path": [], "weather_delays": 0, "seasonal_notes": error_msg},
        "workforce": {"masons": 0, "helpers": 0, "steel_workers": 0, "carpenters": 0, "supervisors": 0},
        "ai_insight": f"Analysis system encountered an issue: {error_msg}. Please try again.",
        "risk": "System error",
        "breakdown_explanation": {"material_details": error_msg, "labour_details": error_msg, "overhead_details": error_msg, "cost_justification": error_msg}
    }
