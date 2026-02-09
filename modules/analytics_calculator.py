def calculate_advanced_metrics(result):
    """
    Calculate comprehensive KPIs and analytics for the visual analysis page.
    Handles zeroed or missing data gracefully and uses AI-driven metrics.
    """
    if not result:
        return get_empty_metrics()

    base_project = result.get('params', {})
    cost_data = result.get('cost', {})
    total_cost = cost_data.get('total_cost', 0)
    
    # Get total_days with multiple fallback paths
    timeline = result.get('timeline', {})
    duration_days = timeline.get('duration_days', result.get('duration_days', 0))
    if duration_days <= 0: duration_days = 1 # Prevent division by zero
    
    workforce_size = base_project.get('workforce_size', 20)
    area = base_project.get('area', 1000)
    floors = base_project.get('floors', 1)
    total_area_sqyd = area * floors if area and floors else 1
    
    # 1. Base KPIs
    cost_per_sq_yd = total_cost / total_area_sqyd
    daily_burn_rate = total_cost / duration_days
    
    # 2. Workforce Metrics
    benchmark_effort = total_area_sqyd / 50 
    actual_effort = workforce_size * duration_days
    efficiency_ratio = (benchmark_effort / actual_effort * 100) if actual_effort > 0 else 75
    
    # 3. Phase Analytics
    phase_breakdown = result.get('phase_breakdown', {})
    if not phase_breakdown:
        return get_empty_metrics()
        
    phases = list(phase_breakdown.keys())
    phase_display_names = [p.replace('_', ' ').capitalize() for p in phases]
    phase_costs = [p.get('cost', 0) for p in phase_breakdown.values()]
    phase_durations = [p.get('duration_days', 0) for p in phase_breakdown.values()]
    
    # Cumulative Progress & Burn Rate Trend
    cumulative_progress = []
    burn_rate_trend = []
    total_duration = sum(phase_durations)
    if total_duration <= 0: total_duration = duration_days
    
    current_duration = 0
    for i, d in enumerate(phase_durations):
        current_duration += d
        progress = (current_duration / total_duration * 100) if total_duration > 0 else 0
        cumulative_progress.append(round(progress, 1))
        # Simulated burn rate fluctuation
        multiplier = 1.2 if i < len(phases) and ("structural" in phases[i].lower() or "finishing" in phases[i].lower()) else 0.8
        burn_rate_trend.append(round(daily_burn_rate * multiplier, 2))

    # 4. Material Intensity
    material_cost = cost_data.get('material_cost', total_cost * 0.45)
    material_breakdown = {
        "Cement": material_cost * 0.25,
        "Steel": material_cost * 0.35,
        "Sand & Aggregate": material_cost * 0.15,
        "Bricks/Blocks": material_cost * 0.10,
        "Finishing Mat": material_cost * 0.15
    }

    # 5. Risk Profiling (Dynamic from AI)
    risk_data = result.get('risk_analysis', {})
    risk_categories = {"Weather": 3, "Site": 3, "Resource": 3, "Regulatory": 3, "Financial": 3, "Execution": 3}
    
    if risk_data:
        risk_categories["Weather"] = risk_data.get("overall_risk_score", 3)
        # Map levels for other categories
        level_map = {"Low": 2, "Medium": 5, "High": 8, "Critical": 10}
        risk_categories["Site"] = level_map.get(risk_data.get("site_risks", {}).get("foundation_errors", {}).get("risk_level", "Medium"), 5)
        risk_categories["Execution"] = level_map.get(risk_data.get("execution_risks", {}).get("quality_defects", {}).get("risk_level", "Low"), 2)

    # 6. Cost Variance
    variance_labels = ["Optimistic", "Realistic", "Pessimistic"]
    variance_data = [total_cost * 0.95, total_cost, total_cost * 1.2]

    # 7. Workforce Allocation Trend
    workforce_allocation = []
    for i in range(len(phases)):
        if i < 2: factor = 0.5
        elif i < 5: factor = 1.0
        else: factor = 0.6
        workforce_allocation.append(round(workforce_size * factor))

    # 8. Sustainability & ESG Impact
    quality_grade = base_project.get("quality", "Standard")
    sustainability_map = {"Economy": 40, "Standard": 75, "Premium": 88, "Luxury": 95}
    base_sustain = sustainability_map.get(quality_grade, 75)
    sustainability_metrics = {
        "Carbon Footprint": max(2, 10 - (base_sustain / 10)),
        "Recyclability": (base_sustain / 10) - 1,
        "Energy Efficiency": base_sustain / 10,
        "Water Conservation": (base_sustain / 10) - 2,
        "Waste Reduction": 9 if base_project.get("machinery") == "Full" else 6
    }

    reg_complexity = 3 + (floors * 1.5) + (2 if quality_grade in ["Premium", "Luxury"] else 0)
    reg_complexity = min(10, reg_complexity)

    # 10. Labor vs Material Cost Trend (Dynamic)
    labor_total = cost_data.get('labor_cost', total_cost * 0.3)
    material_total = cost_data.get('material_cost', total_cost * 0.5)
    labor_trend = [round(labor_total * (0.8 + 0.4 * (i/len(phases)))) for i in range(len(phases))]
    material_trend = [round(material_total * (1.1 - 0.3 * (i/len(phases)))) for i in range(len(phases))]

    return {
        "kpis": {
            "cost_per_sq_yd": round(cost_per_sq_yd, 2),
            "daily_burn_rate": round(daily_burn_rate, 2),
            "efficiency_ratio": round(efficiency_ratio, 1),
            "budget_utilization": 85,
            "total_area": total_area_sqyd,
            "sustainability_score": base_sustain,
            "regulatory_index": round(reg_complexity, 1)
        },
        "charts": {
            "timeline": {"labels": phase_display_names, "progress": cumulative_progress},
            "phase_costs": {"labels": phase_display_names, "data": phase_costs},
            "resource_distribution": {
                "labels": ["Material", "Labor", "Overhead", "Contingency"],
                "data": [cost_data.get("material_cost", 0), cost_data.get("labor_cost", 0), cost_data.get("overhead", 0), cost_data.get("contingency", 0)]
            },
            "risk_radar": {"labels": list(risk_categories.keys()), "data": list(risk_categories.values())},
            "workforce_trends": {"labels": phase_display_names, "data": workforce_allocation},
            "material_intensity": {"labels": list(material_breakdown.keys()), "data": [round(v, 2) for v in material_breakdown.values()]},
            "burn_rate_trend": {"labels": phase_display_names, "data": burn_rate_trend},
            "cost_variance": {"labels": variance_labels, "data": variance_data},
            "phase_productivity": {"labels": phase_display_names, "data": [round(efficiency_ratio * (0.8 + 0.4 * (i/len(phases))), 1) for i in range(len(phases))]},
            "sustainability_radar": {"labels": list(sustainability_metrics.keys()), "data": list(sustainability_metrics.values())},
            "labor_material_trend": {
                "labels": phase_display_names,
                "labor": labor_trend,
                "material": material_trend
            },
            "regulatory_polar": {
                "labels": ["Permits", "Inspection", "Safety", "Local Codes", "Environmental"],
                "data": [reg_complexity, reg_complexity-1, 8, reg_complexity+1, 5]
            },
            "machinery_efficiency": {
                "labels": ["Excavation", "Concreting", "Transport", "Finishing"],
                "data": [90, 85, 75, 95] if base_project.get("machinery") == "Full" else [60, 50, 40, 70]
            }
        }
    }

def get_empty_metrics():
    """Return safe empty structure to prevent template crashes."""
    empty_label = ["N/A"]
    empty_data = [0]
    return {
        "kpis": {"cost_per_sq_yd": 0, "daily_burn_rate": 0, "efficiency_ratio": 0, "budget_utilization": 0, "total_area": 0, "sustainability_score": 0, "regulatory_index": 0},
        "charts": {
            "timeline": {"labels": empty_label, "progress": empty_data},
            "phase_costs": {"labels": empty_label, "data": empty_data},
            "resource_distribution": {"labels": empty_label, "data": empty_data},
            "risk_radar": {"labels": empty_label, "data": empty_data},
            "workforce_trends": {"labels": empty_label, "data": empty_data},
            "material_intensity": {"labels": empty_label, "data": empty_data},
            "burn_rate_trend": {"labels": empty_label, "data": empty_data},
            "cost_variance": {"labels": empty_label, "data": empty_data},
            "phase_productivity": {"labels": empty_label, "data": empty_data},
            "sustainability_radar": {"labels": empty_label, "data": empty_data},
            "labor_material_trend": {"labels": empty_label, "labor": empty_data, "material": empty_data},
            "regulatory_polar": {"labels": empty_label, "data": empty_data},
            "machinery_efficiency": {"labels": empty_label, "data": empty_data}
        }
    }
