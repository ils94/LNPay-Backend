import datetime


# correlation_id needs to be unique, otherwise it will return an error from Strike API. Using the current local
# machine time was the easiest approach I came up with. Both description and correlation_id can be used as identifiers
# for your project, but remember that correlation_id MUST BE DIFFERENT FROM ALL OTHERS EVERYTIME

def generate_correlation_id():
    now = datetime.datetime.now()

    correlation_id = now.strftime('%d%m%Y%H%M%S') + f'{now.microsecond // 10000}{(now.microsecond % 10000) // 100}'

    return correlation_id


def generate_description():
    description = ""

    # Your logic to generate a description for your invoices here

    return description
