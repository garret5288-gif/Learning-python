# rectangle class with area and perimeter methods
# get width and height from user with input validation
# create Rectangle instance and display area and perimeter

class Rectangle: # Define Rectangle class
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self): # Calculate area
        return self.width * self.height

    def perimeter(self): # Calculate perimeter
        return 2 * (self.width + self.height)
    
def get_width_height(label): # Get width or height with validation
    while True: # Loop until valid input
        raw = input(f"Enter {label}: ").strip()
        try: # convert to float
            value = float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if value <= 0:
            print("Value must be greater than 0.")
            continue
        return value

def main(): # Main program
    print("Rectangle Calculator")
    width = get_width_height("width")
    height = get_width_height("height")
    rect = Rectangle(width, height)
    print(f"Width: {rect.width}")
    print(f"Height: {rect.height}")
    print(f"Area: {rect.area()}")
    print(f"Perimeter: {rect.perimeter()}")

if __name__ == "__main__":
    main()