def material_estimation(area, floors):

    total_area = area * floors

    return {
        "cement_tons": total_area * 0.4,
        "steel_kg": total_area * 3,
        "sand_tons": total_area * 0.5,
        "aggregates_tons": total_area * 0.6,
        "water_liters": total_area * 150
    }
