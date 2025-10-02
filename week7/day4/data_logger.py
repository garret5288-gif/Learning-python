import time
# simple data logger application
# Log file path
LOG_FILE = "data_log.txt"


def current_timestamp(): # Get current timestamp
	"""Return ISO-like timestamp string (YYYY-MM-DD HH:MM:SS)."""
	t = time.localtime() # Get local time
	# Build manually to keep it readable
	return (
		str(t.tm_year).zfill(4) + "-" +
		str(t.tm_mon).zfill(2) + "-" +
		str(t.tm_mday).zfill(2) + " " +
		str(t.tm_hour).zfill(2) + ":" +
		str(t.tm_min).zfill(2) + ":" +
		str(t.tm_sec).zfill(2)
	)


def add_entry(log): # Add a log entry
	"""Prompt user for a value and append a timestamped dict entry to the log list."""
	value = input("Enter value to log: ") # Get value from user
	entry = {"timestamp": current_timestamp(), "value": value}
	log.append(entry) # Add to log list
	print("Logged.")


def list_entries(log): # List all log entries
	if not log: # No entries
		print("(no entries)")
		return
	for i, e in enumerate(log, 1): # Enumerate for numbering
		print(f"{i}. {e['timestamp']} -> {e['value']}")


def save_log(filename, log): # Save log entries to a file
	"""Save entries to a simple CSV-like text file: timestamp|value per line."""
	try: # Open and write to the file
		f = open(filename, "w")
		try: # Write header and entries
			f.write("timestamp|value\n")
			for e in log: # Write each entry
				# Replace any newlines to keep one entry per line
				ts = str(e.get("timestamp", "")).replace("\n", " ")
				val = str(e.get("value", "")).replace("\n", " ")
				f.write(ts + "|" + val + "\n")
		finally: # Ensure file is closed
			f.close()
		print("Saved.")
	except Exception as ex: # Handle file write errors
		print("Save failed:", ex)


def load_log(filename): # Load log entries from a file
	"""Load entries from the text file into a list of dicts."""
	log = [] # Initialize empty log list
	try: # Open and read the file
		f = open(filename, "r")
		try: # Read entries
			header = f.readline()  # skip header
			for line in f:
				line = line.rstrip("\n")
				if not line:
					continue
				if "|" not in line:
					continue
				ts, val = line.split("|", 1)
				log.append({"timestamp": ts, "value": val})
		finally:
			f.close()
	except Exception:
		# If file missing or unreadable, return empty log
		pass
	return log


def main(): # Main program loop
    # Load existing log or start new
	log = load_log(LOG_FILE)
	while True:
		print("\nData Logger")
		print("1. Add entry")
		print("2. List entries")
		print("3. Save")
		print("4. Reload")
		print("5. Exit")
		choice = input("Choose (1-5): ").strip()
		if choice == "1":
			add_entry(log)
		elif choice == "2":
			list_entries(log)
		elif choice == "3":
			save_log(LOG_FILE, log)
		elif choice == "4":
			log = load_log(LOG_FILE)
			print("Reloaded.")
		elif choice == "5":
			ask = input("Save before exit? (y/n): ").strip().lower()
			if ask in ("y", "yes"):
				save_log(LOG_FILE, log)
			print("Goodbye!")
			break
		else:
			print("Invalid choice.")


if __name__ == "__main__":
	main()

