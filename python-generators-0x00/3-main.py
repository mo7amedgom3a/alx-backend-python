#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_paginate


try:
    for user in lazy_paginator(20):
        print(user)

except BrokenPipeError:
    sys.stderr.close()