def timeline_estimation(area, floors):

    total_area = area * floors
    duration = total_area / 50

    phases = [
        "Site Preparation",
        "Foundation",
        "Structure",
        "Brickwork",
        "Electrical & Plumbing",
        "Finishing & Handover"
    ]

    return {
        "duration_days": round(duration),
        "phases": phases
    }
