import os

def ensure_backup_dir(): # Ensure backup directory exists
    backup_dir = "backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Created backup directory: {backup_dir}")
    return backup_dir

def backup_file(file_path: str): # Backup any file (binary-safe) with versioning
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return
    backup_dir = ensure_backup_dir()
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    # Find next version to avoid overwrite
    version = 1
    while True:
        candidate = f"{name}_v{version}{ext}" if version > 1 else base_name
        backup_path = os.path.join(backup_dir, candidate)
        if not os.path.exists(backup_path):
            break
        version += 1
    try:
        with open(file_path, "rb") as src, open(backup_path, "wb") as dst:
            dst.write(src.read())
        print(f"Backed up to {backup_path}")
    except OSError as e:
        print(f"Backup failed: {e}")

def add_file(file_path: str): # Add a new file to be backed up
    if not os.path.isfile(file_path):
        with open(file_path, "w") as f:
            f.write("This is a new file.\n")
        print(f"Created new file: {file_path}")
    else:
        print(f"File already exists: {file_path}")

def list_backup_files(): # Unified listing of backup files
    backup_dir = ensure_backup_dir()
    files = sorted(os.listdir(backup_dir))
    if not files:
        print("No backup files found.")
        return
    print("Backup files:")
    for f in files:
        size = os.path.getsize(os.path.join(backup_dir, f))
        print(f"- {f} ({size} bytes)")

def clear_backups(): # Clear all files in the backup directory with confirmation
    backup_dir = ensure_backup_dir()
    files = os.listdir(backup_dir)
    if not files:
        print("No backups to clear.")
        return
    confirm = input("Clear ALL backup files? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return
    for f in files:
        try:
            os.remove(os.path.join(backup_dir, f))
        except OSError as e:
            print(f"Failed to remove {f}: {e}")
    print("Cleared all backup files.")

def view_files(): # View all files in the current directory
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    if not files:
        print("No files found in the current directory.")
        return
    print("Files in current directory:")
    for f in files:
        print(f"- {f}")

def view_backup_file_directory(): # Alias to unified listing (kept for menu compatibility)
    list_backup_files()

def menu(): # Display menu options
    print("\n=== Backup Menu ===\n")
    print("1. Add text file placeholder")
    print("2. Backup any file (txt, csv, image, etc.)")
    print("3. List backup files")
    print("4. Clear backups")
    print("5. View files in current directory")
    print("6. Exit\n")

def main(): # Main program loop
    while True: # Loop until user chooses to exit
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            file_path = input("Enter file path to add: ").strip()
            if not file_path:
                print("No path provided.")
            else:
                add_file(file_path)
        elif choice == "2":
            file_path = input("Enter file path to backup: ").strip()
            if file_path:
                backup_file(file_path)
            else:
                print("No path provided.")
        elif choice == "3":
            list_backup_files()
        elif choice == "4":
            clear_backups()
        elif choice == "5":
            view_files()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()  