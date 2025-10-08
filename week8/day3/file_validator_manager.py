import os

# Registry mapping extension to validator function
VALIDATORS = {}
LAST_REPORT = None  # store last validation result


def validator(ext):
    def wrap(func):
        VALIDATORS[ext] = func
        return func
    return wrap


@validator('.txt')
def validate_txt(path):
    if os.path.getsize(path) == 0:
        return False, ['File is empty']
    issues = []
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f, 1):
            if len(line.rstrip('\n')) > 120:
                issues.append(f'Line {i} exceeds 120 chars')
    return (len(issues) == 0), issues


@validator('.csv')
def validate_csv(path):
    issues = []
    expected_cols = None
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for i, raw in enumerate(f, 1):
            line = raw.rstrip('\n')
            if not line:
                issues.append(f'Line {i} empty')
                continue
            cols = line.split(',')
            if expected_cols is None:
                expected_cols = len(cols)
            elif len(cols) != expected_cols:
                issues.append(f'Line {i} has {len(cols)} columns (expected {expected_cols})')
    if expected_cols is None:
        issues.append('File is empty')
    return (len(issues) == 0), issues


@validator('.cfg')
@validator('.ini')
def validate_kv(path):
    issues = []
    seen = set()
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for i, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith('#') or line.startswith(';'):
                continue
            if '=' not in line:
                issues.append(f'Line {i}: missing =')
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            if not key:
                issues.append(f'Line {i}: empty key')
            if key in seen:
                issues.append(f'Line {i}: duplicate key {key!r}')
            seen.add(key)
            if value.strip() == '':
                issues.append(f'Line {i}: empty value')
    if not seen and not issues:
        issues.append('No key=value pairs found')
    return (len(issues) == 0), issues


def choose_file():
    p = input('Enter path to file: ').strip()
    if not p:
        print('No path provided')
        return None
    if not os.path.isfile(p):
        print('File not found')
        return None
    return p


def find_validator(path):
    for ext, func in VALIDATORS.items():
        if path.endswith(ext):
            return func
    return None


def validate_file():
    global LAST_REPORT
    path = choose_file()
    if not path:
        return
    validator_func = find_validator(path)
    if not validator_func:
        print('No validator registered for this file type')
        return
    ok, issues = validator_func(path)
    LAST_REPORT = (path, ok, issues)
    print(f'Validation result for {path}:')
    if ok:
        print('  PASS')
    else:
        print('  FAIL')
    if issues:
        print('  Issues:')
        for msg in issues:
            print('   -', msg)


def show_last_report():
    if not LAST_REPORT:
        print('No report yet.')
        return
    path, ok, issues = LAST_REPORT
    print(f'Last report: {path} -> {"PASS" if ok else "FAIL"}')
    if issues:
        for msg in issues:
            print(' -', msg)


def list_validators():
    if not VALIDATORS:
        print('No validators registered.')
        return
    print('Registered validators:')
    for ext in sorted(VALIDATORS):
        print(' -', ext)


def menu():
    print('\nValidator Manager')
    print('1) Validate a file')
    print('2) Show last report')
    print('3) List validators')
    print('4) Exit')
    return input('Choose: ').strip()


def main():
    while True:
        choice = menu()
        if choice == '1':
            validate_file()
        elif choice == '2':
            show_last_report()
        elif choice == '3':
            list_validators()
        elif choice == '4':
            print('Goodbye.')
            break
        else:
            print('Invalid choice.')


if __name__ == '__main__':
    main()
