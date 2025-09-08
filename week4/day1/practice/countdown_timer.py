# Countdown Timer
import time # Import the time module to use sleep function
for i in range(10, 0, -1): # Countdown from 10 to 1
    print(i)
    time.sleep(1) # Wait for 1 second
print("Time's up!")