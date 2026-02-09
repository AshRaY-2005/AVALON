from modules.ai_client import client

def ai_analysis(analytics_data, project_data):
    """
    Generate deep strategic insights using LLM based on calculated analytics.
    """
    kpis = analytics_data.get('kpis', {})
    
    prompt = f"""Analyze these construction project metrics and provide 3-4 professional, actionable insights.
    
    PROJECT: {project_data.get('location')} | {project_data.get('quality')} Grade | {project_data.get('priority')} Priority
    AREA: {kpis.get('total_area')} sqyd | FLOORS: {project_data.get('floors')}
    
    METRICS:
    - Cost per Sq.Yd: ₹{kpis.get('cost_per_sq_yd')}
    - Daily Burn Rate: ₹{kpis.get('daily_burn_rate')}
    - Workforce Efficiency: {kpis.get('efficiency_ratio')}%
    - ESG/Sustainability Score: {kpis.get('sustainability_score')}/100
    - Regulatory Complexity: {kpis.get('regulatory_index')}/10
    
    Provide a concise, high-impact strategic summary and 3 specific bullet points for optimization. 
    Focus on financial health, execution risk, and resource efficiency.
    No preamble, return only the analysis text."""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Analysis temporarily unavailable. Basic Efficiency: {kpis.get('efficiency_ratio')}%."
