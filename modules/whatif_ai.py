from groq import Groq
import os
import json
import re

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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
    
    prompt = f"""You are a construction project management expert analyzing fast-track scenarios.

ORIGINAL PROJECT BASELINE:
- Duration: {base_project.get('duration_days', 180)} days
- Total Cost: ₹{base_project.get('total_cost', 5000000)}
- Workforce: {base_project.get('workforce_size', 20)} workers
- Machinery: {base_project.get('machinery', 'Partial')}
- Location: {base_project.get('location', 'India')}

SCENARIO: Complete project {time_reduction_percent}% FASTER

ANALYSIS REQUIREMENTS:

1. WORKFORCE INCREASE:
   - Calculate additional workers needed for {time_reduction_percent}% time reduction
   - Consider coordination overhead with larger teams
   - Account for supervision requirements

2. OVERTIME COSTS:
   - Overtime wage rate: 1.5x normal wage
   - Calculate overtime hours needed
   - Total overtime cost impact

3. MACHINERY ADDITIONS:
   - Additional equipment needed (cranes, mixers, etc.)
   - Rental cost increase
   - Operational efficiency impact

4. MATERIAL WASTAGE:
   - Faster work increases wastage by 5-10%
   - Calculate additional material costs
   - Quality control measures needed

5. COORDINATION OVERHEAD:
   - Site management complexity
   - Additional supervisors needed
   - Communication and safety costs

6. QUALITY RISKS:
   - Risk of defects due to rushed work
   - Rework probability
   - Quality assurance measures

7. RESOURCE STRAIN:
   - Worker fatigue (1-10 scale)
   - Equipment utilization (1-10 scale)
   - Overall project stress (1-10 scale)

Return ONLY a valid JSON object:
{{
    "new_duration_days": <number - reduced by {time_reduction_percent}%>,
    "new_total_cost": <number - increased cost>,
    "cost_increase_amount": <number>,
    "cost_increase_percent": <number>,
    "time_saved_days": <number>,
    
    "workforce_changes": {{
        "original_size": <number>,
        "new_size": <number>,
        "increase_percent": <number>,
        "additional_supervisors": <number>
    }},
    
    "cost_breakdown": {{
        "overtime_cost": <number>,
        "additional_machinery_cost": <number>,
        "material_wastage_cost": <number>,
        "coordination_overhead": <number>,
        "quality_assurance_cost": <number>
    }},
    
    "machinery_additions": "List of additional equipment needed (e.g., 1 additional crane, 2 concrete mixers)",
    
    "risks": [
        "Risk 1: Description and probability",
        "Risk 2: Description and probability",
        "Risk 3: Description and probability"
    ],
    
    "resource_strain": {{
        "worker_fatigue_score": <1-10>,
        "equipment_utilization_score": <1-10>,
        "overall_stress_score": <1-10>,
        "explanation": "Brief explanation of strain levels"
    }},
    
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        "Recommendation 3"
    ],
    
    "feasibility": "High/Medium/Low - with brief justification"
}}

Use realistic calculations based on construction industry standards for {current_date}."""

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
    
    prompt = f"""You are a construction project management expert analyzing budget-constrained scenarios.

ORIGINAL PROJECT BASELINE:
- Duration: {base_project.get('duration_days', 180)} days
- Total Cost: ₹{base_project.get('total_cost', 5000000)}
- Workforce: {base_project.get('workforce_size', 20)} workers
- Material Grade: {base_project.get('material_grade', 'Standard')}
- Quality Level: {base_project.get('quality', 'Standard')}

SCENARIO: Reduce budget by {budget_reduction_percent}%
New Budget: ₹{base_project.get('total_cost', 5000000) * (100 - budget_reduction_percent) / 100}

ANALYSIS REQUIREMENTS:

1. WORKFORCE REDUCTION:
   - Calculate workforce reduction needed
   - Impact on timeline
   - Critical skills that must be retained

2. MATERIAL DOWNGRADE:
   - Switch from {base_project.get('material_grade', 'Standard')} to lower grade
   - Cost savings
   - Quality impact
   - Structural integrity considerations

3. TIMELINE EXTENSION:
   - Additional days needed with reduced resources
   - Phase-wise slowdown
   - Critical path impact

4. QUALITY RISKS:
   - Structural quality concerns
   - Finishing quality impact
   - Long-term durability issues

5. MACHINERY CHANGES:
   - Reduce equipment rental
   - Use more manual labor
   - Productivity impact

6. PHASE SLOWDOWN:
   - Which phases are most affected
   - Delay distribution across 7 phases

Return ONLY a valid JSON object:
{{
    "new_duration_days": <number - increased>,
    "new_total_cost": <number - reduced by {budget_reduction_percent}%>,
    "cost_reduction_amount": <number>,
    "delay_days": <number>,
    "delay_percent": <number>,
    
    "workforce_changes": {{
        "original_size": <number>,
        "new_size": <number>,
        "reduction_percent": <number>
    }},
    
    "material_changes": {{
        "original_grade": "{base_project.get('material_grade', 'Standard')}",
        "new_grade": "Economy/Basic",
        "quality_impact": "Description of quality impact"
    }},
    
    "phase_delays": {{
        "site_preparation": <additional days>,
        "foundation": <additional days>,
        "structural_work": <additional days>,
        "brickwork": <additional days>,
        "electrical_plumbing": <additional days>,
        "finishing": <additional days>,
        "handover": <additional days>
    }},
    
    "quality_risks": [
        "Risk 1: Description and severity",
        "Risk 2: Description and severity",
        "Risk 3: Description and severity"
    ],
    
    "cost_savings_breakdown": {{
        "labor_savings": <number>,
        "material_savings": <number>,
        "machinery_savings": <number>,
        "overhead_savings": <number>
    }},
    
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        "Recommendation 3"
    ],
    
    "feasibility": "High/Medium/Low - with brief justification",
    "not_recommended_if": "Conditions under which this scenario should be avoided"
}}

Use realistic calculations based on construction industry standards for {current_date}."""

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
            "raw_response": text[:500]
        }
