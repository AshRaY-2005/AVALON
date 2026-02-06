def weekly_schedule(duration):

    weeks = int(duration / 7) + 1

    schedule = []

    for w in range(1, weeks + 1):
        schedule.append(f"Week {w}: Construction activities in progress")

    return schedule
