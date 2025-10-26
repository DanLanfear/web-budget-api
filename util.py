def list_months(start_year, start_month, end_year, end_month):
    """Return a list of (year, month) tuples between start and end inclusive."""
    months = []
    year, month = start_year, start_month

    while (year, month) <= (end_year, end_month):
        months.append((year, month))

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

    return months