def whatif_simulation(area, floors, budget):

    increased_floors_cost = area * (floors + 1) * 2300
    reduced_budget = budget * 0.9
    fast_track_time = (area * floors) / 70

    return {
        "extra_floor_cost": increased_floors_cost,
        "reduced_budget_scenario": reduced_budget,
        "fast_completion_days": fast_track_time
    }
