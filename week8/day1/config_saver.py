# App to save and load user configuration settings
# Settings include username, email, and gender

CONFIG_FILE = "config.txt" # path to config file

def menu(): # Display menu options
    print("\n=== Config Menu ===\n")
    print("1. Set Username")
    print("2. Set Email")
    print("3. Set Gender")
    print("4. Show Current Config")
    print("5. Clear Config")
    print("6. Exit (auto-save)")

def load_config() -> dict: # Load config from file
    cfg = {"username": "", "email": "", "gender": ""} # default config
    try: # try to read existing config
        with open(CONFIG_FILE, "r") as f:
            lines = [ln.rstrip("\n") for ln in f]
        if lines: # if file has content
            if len(lines) > 0: cfg["username"] = lines[0] # first line is username
            if len(lines) > 1: cfg["email"] = lines[1] # second line is email
            if len(lines) > 2: cfg["gender"] = lines[2] # third line is gender
    except FileNotFoundError: # file does not exist
        pass
    return cfg # return config dictionary

def save_config(cfg: dict) -> None: # Save config to file
    with open(CONFIG_FILE, "w") as f:
        f.write(f"{cfg['username']}\n{cfg['email']}\n{cfg['gender']}\n")

def get_username(current: str) -> str: # Get username input
    if current:
        print(f"Current username: {current}")
    return input("Enter username: ").strip()

def get_email(current: str) -> str: # Get email input
    if current:
        print(f"Current email: {current}")
    return input("Enter email: ").strip()

def get_gender(current: str) -> str: # Get gender input
    if current:
        print(f"Current gender: {current}") # show current if exists
    return input("Enter gender: ").strip()

def clear_config(cfg: dict): # Clear all config settings
    cfg["username"] = "" # clear username
    cfg["email"] = "" # clear email
    cfg["gender"] = "" # clear gender
    save_config(cfg)
    print("Configuration cleared.")

def show_config(cfg: dict): # Display current config
    print("\nCurrent Configuration:")
    print(f"Username: {cfg['username'] or '(empty)'}") # show (empty) if blank
    print(f"Email: {cfg['email'] or '(empty)'}")
    print(f"Gender: {cfg['gender'] or '(empty)'}")

def main(): # Main program loop
    cfg = load_config() # load existing config
    while True: # Loop until user chooses to exit
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            cfg['username'] = get_username(cfg['username'])
            save_config(cfg)
            print("Saved.\n")
        elif choice == "2":
            cfg['email'] = get_email(cfg['email'])
            save_config(cfg)
            print("Saved.\n")
        elif choice == "3":
            cfg['gender'] = get_gender(cfg['gender'])
            save_config(cfg)
            print("Saved.\n")
        elif choice == "4":
            show_config(cfg)
        elif choice == "5":
            clear_config(cfg)
        elif choice == "6":
            print("Exiting...")
            break
        else: # Handle invalid menu choices
            print("Invalid choice. Please try again.")
    print("\nFinal Configuration:") # show final config
    show_config(cfg)

if __name__ == "__main__":
    main()