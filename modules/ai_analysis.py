def ai_analysis(workforce, cost, timeline, context):
    
    quality = context.get('quality', 'Standard')
    priority = context.get('priority', 'Balanced')
    location = context.get('location', 'Unknown')
    occupancy = context.get('occupancy', 'Standard')

    # Simulate intelligent insight generation based on params
    insights = []
    risks = []

    # Quality Insights
    if quality == "Luxury":
        insights.append(f"Budget reflects high-end finishes. Ensure procurement of premium materials early to avoid delays.")
    elif quality == "Economy":
        insights.append("Cost-optimized approach. Focus on structural integrity over cosmetic finishes.")

    # Priority Insights
    if priority == "Speed":
        insights.append("Timeline is compressed. Workforce has been ramped up by 40%. Requires daily supervision.")
        risks.append("High risk of coordination clashes due to fast-tracking.")
    
    # General
    insights.append(f"Project in {location} for {occupancy} occupancy.")
    
    return {
        "insight": " ".join(insights) or "Standard construction plan proceeding normally.",
        "risk": " ".join(risks) or "No critical risks identified at this stage.",
        "summary": f"{quality} Grade project | {priority} Priority"
    }
