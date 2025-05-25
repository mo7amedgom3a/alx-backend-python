#!/usr/bin/python3
from itertools import islice
stream_users = __import__('0-stream_users').stream_users

# iterate over the generator function and print only the first 6 rows
user_stream = stream_users()
for user in islice(user_stream, 20):
    print(user)

# Exhaust the generator to ensure proper cleanup
try:
    for _ in user_stream:
        pass
except Exception:
    pass