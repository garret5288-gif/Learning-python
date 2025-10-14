class Car: # Define a Car class
    def __init__(self, make, model, year): # Constructor with make, model, year
        self.make = make
        self.model = model
        self.year = year

    def start_stop(self, action): # Method to start or stop the car
        if action.lower() == "start":
            return f"The {self.make} {self.model} is starting."
        elif action.lower() == "stop":
            return f"The {self.make} {self.model} is stopping."
        else:
            return "Invalid action. Use 'start' or 'stop'."

    def get_description(self): # Method to get car description
        return f"{self.year} {self.make} {self.model}"

car1 = Car("Toyota", "Camry", 2020) # Create instance
car2 = Car("Honda", "Civic", 2019)
car3 = Car("Ford", "Mustang", 2021)
print(car1.start_stop("start"))
print(car2.start_stop("stop"))
print(car3.start_stop("fly"))
print(car1.get_description())
print(car2.get_description())
print(car3.get_description())