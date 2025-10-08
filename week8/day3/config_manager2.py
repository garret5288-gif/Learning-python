import os

# Simple validator registry
VALIDATORS = {} # ext -> func
LAST_REPORT = None # (path, ok, issues)


def register(ext): # Decorator to register a validator
    def wrapper(func):
        VALIDATORS[ext] = func # Register the validator function
        return func
    return wrapper


@register('.txt')
def validate_txt(path): # Validate .txt files (non-empty, lines <= 100 chars)
    if os.path.getsize(path) == 0:
        return False, ['File is empty']
    errs = [] # collect errors
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f, 1): # read lines
            if len(line.rstrip('\n')) > 100: # line length check
                errs.append(f'Line {i} longer than 100 chars')
    return (len(errs) == 0), errs


@register('.cfg')
def validate_cfg(path): # Validate .cfg files (key=value pairs, no duplicates)
    errs = []
    keys = set()
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for i, raw in enumerate(f, 1): # read lines
            line = raw.strip()
            if not line or line.startswith('#'): # skip comments/blank
                continue
            if '=' not in line:
                errs.append(f'Line {i}: missing =')
                continue
            k, v = line.split('=', 1) # split at first =
            k = k.strip() # strip whitespace
            v = v.strip() # strip whitespace
            if not k:
                errs.append(f'Line {i}: empty key')
            if k in keys:
                errs.append(f'Line {i}: duplicate key {k!r}')
            keys.add(k)
            if v == '':
                errs.append(f'Line {i}: empty value')
    if not keys and not errs:  # No key=value pairs found
        errs.append('No key=value pairs found')
    return (len(errs) == 0), errs


def choose_file(): # Prompt user for file path
    while True: # Loop until valid file or cancel
        p = input("Enter file path (blank to cancel): ").strip()
        if p == '':
            return None
        if os.path.isfile(p):
            return p
        print('File not found.')


def find_validator(path): # Find validator based on file extension
    for ext, func in VALIDATORS.items():
        if path.endswith(ext):
            return func
    return None


def run_validation(): # Run the validation process
    global LAST_REPORT
    path = choose_file()
    if not path:
        return
    func = find_validator(path)
    if not func:
        print('No validator for this type.')
        return
    ok, issues = func(path)
    LAST_REPORT = (path, ok, issues)
    print(f'Validation result for {path}: {"PASS" if ok else "FAIL"}')
    if issues:
        for msg in issues:
            print(' -', msg)


def show_last(): # Show last validation report
    if not LAST_REPORT:
        print('No report yet.')
        return
    path, ok, issues = LAST_REPORT
    print(f'Last report: {path} -> {"PASS" if ok else "FAIL"}')
    if issues:
        for msg in issues:
            print(' -', msg)


def list_validators(): # List all registered validators
    if not VALIDATORS:
        print('No validators registered.')
        return
    print('Validators:')
    for ext in sorted(VALIDATORS):
        print(' -', ext)


def menu(): # Display menu options
    print('\nValidator Menu')
    print('1) Validate file')
    print('2) Show last report')
    print('3) List validators')
    print('4) Exit')
    return input('Choose: ').strip()


def main(): # Main program loop
    while True:
        choice = menu()
        if choice == '1':
            run_validation()
        elif choice == '2':
            show_last()
        elif choice == '3':
            list_validators()
        elif choice == '4':
            print('Exiting...')
            break
        else:
            print('Invalid choice.')


if __name__ == '__main__':
    main()

