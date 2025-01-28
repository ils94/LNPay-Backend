import random
import string


def generate_random_key(length):
    characters = string.ascii_letters + string.digits  # Uppercase, lowercase, and digits
    random_key = ''.join(random.choices(characters, k=length))
    return random_key


# You can use this script to generate a random 10 + character length key to create webhook subscriptions
# Your key must be 10 in length, otherwise, Strike will return an error
# No idea of the maximum size limit, but you can test it if you want :)
print(generate_random_key(10))
