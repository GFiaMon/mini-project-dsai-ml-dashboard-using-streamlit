# utils.py
# Utility/Helper functions for the Sakila Dashboard

def get_ordinal_suffix(day):
    """
    Returns the ordinal suffix for a given day number.
    Example: 1 -> 'st', 2 -> 'nd', 3 -> 'rd', 4 -> 'th', 11 -> 'th', 21 -> 'st'
    """
    if 11 <= day <= 13:
        return 'th'
    else:
        last_digit = day % 10
        if last_digit == 1:
            return 'st'
        elif last_digit == 2:
            return 'nd'
        elif last_digit == 3:
            return 'rd'
        else:
            return 'th'

def format_date_with_ordinal(date_obj):
    """Formats a date as 'Month day_with_ordinal' (e.g., 'May 24th')"""
    day = date_obj.day
    suffix = get_ordinal_suffix(day)
    return date_obj.strftime(f'%b {day}{suffix}')  # %b = short month name