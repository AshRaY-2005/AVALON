from modules.ai_client import client

def whatif_faster_completion(base_project, time_reduction_percent=20):
    """
    Simulate faster completion scenario using AI analysis
    
    Args:
        base_project: Original project data with timeline, cost, workforce
        time_reduction_percent: How much faster to complete (default 20%)
    
    Returns:
        dict: Scenario analysis with new costs, timeline, risks
    """
    
    current_date = "February 2026"
    
    prompt = f"""You are a construction project management expert. Analyze a FAST-TRACK scenario.

ORIGINAL BASELINE:
- Duration: {base_project.get('duration_days', 180)} days
- Total Cost: ₹{base_project.get('total_cost', 5000000)}
- Workforce: {base_project.get('workforce_size', 20)} workers

SCENARIO: Complete project {time_reduction_percent}% FASTER.

TASK:
1. Calculate the exact new_total_cost by adding specific "Speed Premiums":
   - Overtime wages (1.5x) for {time_reduction_percent}% of the remaining work.
   - Additional machinery rental costs.
   - Efficiency loss (10%) due to crowded site.
2. Provide explicit math in an 'explanation' field.

Return ONLY a minified JSON object. NO markdown, NO code blocks, NO preamble.

JSON Structure:
{{
    "new_duration_days": number,
    "new_total_cost": number,
    "cost_increase_amount": number,
    "cost_increase_percent": number,
    "time_saved_days": number,
    "workforce_changes": {{
        "original_size": {base_project.get('workforce_size', 20)},
        "new_size": number,
        "increase_percent": number
    }},
    "cost_breakdown": {{
        "overtime_cost": number,
        "additional_machinery_cost": number,
        "material_wastage_cost": number,
        "coordination_overhead": number
    }},
    "recommendations": ["list of 3 items"],
    "feasibility": "string",
    "explanation": "Detailed math showing the cost/speed tradeoff logic"
}}
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=2000
        )
        
        response_text = completion.choices[0].message.content
        return parse_whatif_json(response_text)
        
    except Exception as e:
        return {
            "error": f"AI analysis failed: {str(e)}",
            "new_duration_days": base_project.get('duration_days', 180) * (100 - time_reduction_percent) / 100,
            "new_total_cost": base_project.get('total_cost', 5000000) * 1.15,
            "cost_increase_percent": 15,
            "feasibility": "Unknown - AI analysis unavailable"
        }


def whatif_reduced_budget(base_project, budget_reduction_percent=10):
    """
    Simulate reduced budget scenario using AI analysis
    
    Args:
        base_project: Original project data
        budget_reduction_percent: Budget cut percentage (default 10%)
    
    Returns:
        dict: Scenario analysis with timeline delays, quality impacts
    """
    
    current_date = "February 2026"
    
    prompt = f"""You are a construction project management expert. Analyze a BUDGET-CUT scenario.

ORIGINAL BASELINE:
- Duration: {base_project.get('duration_days', 180)} days
- Total Cost: ₹{base_project.get('total_cost', 5000000)}
- Material Grade: {base_project.get('material_grade', 'Standard')}

SCENARIO: Reduce budget by {budget_reduction_percent}%.
Target Budget: ₹{base_project.get('total_cost', 5000000) * (100 - budget_reduction_percent) / 100}

TASK:
1. Identify exact cost-saving measures (Workforce cuts, Material downgrades, Machinery reduction).
2. Calculate the "Timeline Penalty" (additional days added due to reduced resources).
3. Provide explicit math in an 'explanation' field.

Return ONLY a minified JSON object. NO markdown, NO code blocks, NO preamble.

JSON Structure:
{{
    "new_duration_days": number,
    "new_total_cost": number,
    "cost_reduction_amount": number,
    "delay_days": number,
    "workforce_changes": {{
        "original_size": {base_project.get('workforce_size', 20)},
        "new_size": number,
        "reduction_percent": number
    }},
    "material_changes": {{
        "original_grade": "{base_project.get('material_grade', 'Standard')}",
        "new_grade": "Economy",
        "quality_impact": "string"
    }},
    "cost_savings_breakdown": {{
        "labor_savings": number,
        "material_savings": number,
        "machinery_savings": number
    }},
    "recommendations": ["list of 3 items"],
    "feasibility": "string",
    "not_recommended_if": "string",
    "explanation": "Detailed math showing the cost/delay tradeoff logic"
}}
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=2000
        )
        
        response_text = completion.choices[0].message.content
        return parse_whatif_json(response_text)
        
    except Exception as e:
        return {
            "error": f"AI analysis failed: {str(e)}",
            "new_duration_days": base_project.get('duration_days', 180) * 1.15,
            "new_total_cost": base_project.get('total_cost', 5000000) * (100 - budget_reduction_percent) / 100,
            "delay_days": base_project.get('duration_days', 180) * 0.15,
            "feasibility": "Unknown - AI analysis unavailable"
        }


def parse_whatif_json(text):
    try:
        # Clean text
        text = re.sub(r'```(?:json)?\s*|\s*```', '', text)
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            data = json.loads(json_str)
            if "new_duration_days" not in data: data["new_duration_days"] = 0
            if "new_total_cost" not in data: data["new_total_cost"] = 0
            return data
        return {
            "error": "No JSON found in response",
            "new_duration_days": 180,
            "new_total_cost": 5000000,
            "feasibility": "Unknown"
        }
    except Exception as e:
        return {
            "error": f"Failed to parse AI response: {str(e)}",
            "new_duration_days": 0,
            "new_total_cost": 0,
            "feasibility": "Error"
        }
