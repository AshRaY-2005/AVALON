def workforce_estimation(area, floors, timeline, priority="Balanced"):

    total_area = area * floors
    factor = total_area / 1000

    # Speed Priority: Increase workforce density by 40%
    speed_mult = 1.4 if priority == "Speed" else 1.0

    masons = round(5 * factor * speed_mult)
    helpers = round(8 * factor * speed_mult)
    steel = round(3 * factor * speed_mult)
    carpenters = round(2 * factor * speed_mult)
    supervisors = max(1, round(1 * factor * speed_mult))

    labour_days = total_area / 40

    # Adjust workforce if timeline tight
    if timeline < labour_days:
        masons += 2
        helpers += 3

    return {
        "masons": masons,
        "helpers": helpers,
        "steel_workers": steel,
        "carpenters": carpenters,
        "supervisors": supervisors,
        "labour_days": round(labour_days)
    }
