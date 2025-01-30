from datetime import datetime, timedelta


def subtract(minutes, time_string):
    # Parse the string into a datetime object
    time_obj = datetime.fromisoformat(time_string)

    # Subtract 10 minutes
    new_time_obj = time_obj - timedelta(minutes=int(minutes))

    # Convert back to ISO 8601 string
    new_time_str = new_time_obj.isoformat()

    print(new_time_str)

    return new_time_str
