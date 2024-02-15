# py-ttl-dict
Python Dictionary that supports expiring keys.

## Usage
```Python
import ttldict
import time

my_dict = ttldict.TTLDict()

my_dict.set("key", "value," 2)  # Expire Key after 2 seconds

print(my_dict.get("key"))        # Prints "value"

time.sleep(3)

print(my_dict.get("key"))        # Prints "None"
```

## Install
```Bash
$ pip install py-ttl-dict
```

## Additional Usage
### Convert to a Python Dict
```Python
import ttldict
import time

my_dict = ttldict.TTLDict()

my_dict.set("key", "value," 10)

python_dict = my_dict.as_dict()

print(python_dict)
```

## Implementation Details
This implementation maintains a `map` of KV-pairs as well as a `heap` of expiry times. Insert is `O(logn)`, Update TTL is `O(n)` and all accessors are `O(klogn)` where `k` is the number of entries that must be evicted.
