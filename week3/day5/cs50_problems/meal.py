# time conversion function
def main(): # main function
   current_time = input("What time is it? ")
    
   time_float = convert(current_time) # convert time to float

   if time_float >= 7.0 and time_float <= 8.0:
       print("breakfast time")
   elif time_float >= 12.0 and time_float <= 13.0:
       print("lunch time")
   elif time_float >= 18.0 and time_float <= 19.0:
       print("dinner time")

def convert(time): # convert time to float
   hours, minutes = map(int, time.split(":")) # split time into hours and minutes
   hours_int, minutes_int = int(hours),int( minutes) # convert to integers
   time_float = hours_int + minutes_int / 60 # convert to float
   return time_float

if __name__ == "__main__": # run the main function
   main()
