"""
Extracted from YouTube Tutorial
Title: Is "finally" useless in Python?
Source: https://www.youtube.com/watch?v=92JdbyISpCo&t=4s
Duration: 7:01
IDE/Theme: Unknown

This code was automatically extracted and reconstructed from video frames.
Only code visible in the original video frames is included.
"""

try:
    raise ValueError('Bad value')
except ValueError:
    print('Handling ValueError...')
finally:
    print('finally is being executed...')

try:
    raise ValueError('Bad value')
except ValueError:
    print('Handling ValueError...')
    print('finally is being executed...')

print('Handling ValueError...')
sys.exit('Terminating program')
print('finally is being executed...')

try:
    raise ValueError('Bad value')
except ValueError:
    print('Handling ValueError...')
    return 1
finally:
    return 0
```