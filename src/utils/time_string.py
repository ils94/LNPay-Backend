from datetime import datetime, timedelta


def add_offset(minutes, time_string):
    # Parse the string into a datetime object
    time_obj = datetime.fromisoformat(time_string)

    left = 60 - int(minutes)

    # Subtract 10 minutes
    new_time_obj = time_obj + timedelta(minutes=left)

    # Convert back to ISO 8601 string
    new_time_str = new_time_obj.isoformat()

    return new_time_str
