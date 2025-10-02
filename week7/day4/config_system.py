# Simple Configuration Manager using dictionary methods and iteration with JSON persistence
import json
import os

config = {}
STORE_PATH = os.path.join(os.path.dirname(__file__), "config_store.json")
SAVE_ON_CHANGE = True

def load_config(path: str = STORE_PATH):
    global config
    try:
        with open(path, "r") as f:
            config = json.load(f)
        print(f"Loaded {len(config)} settings from {path}")
    except FileNotFoundError:
        config = {}
        print("No existing config file. Starting fresh.")
    except json.JSONDecodeError:
        config = {}
        print("Config file was invalid JSON. Starting fresh.")

def save_config(path: str = STORE_PATH):
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Saved {len(config)} settings to {path}")

def save_if_needed(): # Save if auto-save is enabled
    if SAVE_ON_CHANGE:
        save_config()

def set_setting(key, value):
    # setdefault returns existing value or sets and returns default
    if key in config: # update existing
        print(f"Updated {key} from {config[key]} to {value}")
    else: # new key
        print(f"Added {key} = {value}")
    config[key] = value
    save_if_needed()


def get_setting(key): # Get value or None
    value = config.get(key)
    if value is None: # Key not found
        print(f"{key} not found.")
    else: # Key found
        print(f"{key} = {value}")


def ensure_default(key, default_value): # Ensure default value is set
    # Only sets if missing
    value = config.setdefault(key, default_value)
    print(f"Default ensured: {key} = {value}")
    # Only persist if we actually created the default
    if value == default_value and key in config and value == default_value:
        save_if_needed()


def update_settings(new_settings): 
    # Merge another dict
    config.update(new_settings)
    print("Settings updated with:", new_settings)
    save_if_needed()


def remove_setting(key): # Remove a setting by key
    value = config.pop(key, None)
    if value is None: # Key not found
        print(f"{key} not found (nothing removed).")
    else: # Key found and removed
        print(f"Removed {key} (was {value}).")
    save_if_needed()


def list_settings(): # List all settings
    if not config: # Empty config
        print("No settings configured.")
        return
    print("Current settings:") 
    for k, v in config.items():  # iteration over dictionary
        print(f"- {k}: {v}")


def main(): # Main program loop
    # Load persisted config at startup
    load_config()
    while True:
        print("\nConfiguration Manager")
        print("1. Set setting")
        print("2. Get setting")
        print("3. Ensure default")
        print("4. Update multiple")
        print("5. Remove setting")
        print("6. List settings")
        print("7. Save settings")
        print("8. Exit")
        choice = input("Choose an option: ")
        if choice == "1": # Set setting
            key = input("Key: ")
            value = input("Value: ")
            set_setting(key, value)
        elif choice == "2": # Get setting
            key = input("Key: ")
            get_setting(key)
        elif choice == "3": # Ensure default
            key = input("Key: ")
            default_value = input("Default value: ")
            ensure_default(key, default_value)
        elif choice == "4":
            # Simple demo: prompt for two key/value pairs
            n = input("How many settings to update? ")
            try: # Validate number
                count = int(n)
            except ValueError: # Invalid input
                print("Enter a valid number.")
                continue
            updates = {} # Collect new settings
            for _ in range(count):
                k = input("Key: ")
                v = input("Value: ")
                updates[k] = v
            update_settings(updates)
        elif choice == "5":
            key = input("Key: ")
            remove_setting(key)
        elif choice == "6":
            list_settings()
        elif choice == "7":
            save_config()
        elif choice == "8":
            # Save on exit for convenience
            save_config()
            print("Goodbye")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
