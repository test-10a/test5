import os
import re

#patterns to search for
SUSPICIOUS_PATTERNS = {
    'eval_usage': r'\beval\s*\(',
    'exec_usage': r'\bexec\s*\(',
    'compile_usage': r'\bcompile\s*\(',
    'input_usage': r'\binput\s*\(',
    'os_system': r'\bos\.system\s*\(',
    'subprocess_usage': r'\bsubprocess\.',
    'base64_decode': r'base64\.b64decode\s*\(',
    'hex_decode': r'\.decode\s*\(\s*[\'"]hex[\'"]\s*\)',
    'import_dunder': r'__import__\s*\(',
    'getattr_usage': r'\bgetattr\s*\(',
    'globals_usage': r'\bglobals\s*\(',
    'threading_usage': r'\bthreading\.',
    'asyncio_usage': r'\basyncio\.',
    'mangled_var_names': r'\b(?:[lI1O0]{4,})\b',  # Variables like lIlI or O0OO
    'exec_open_file': r'exec\s*\(\s*open\s*\(',
}

def scan_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        matches = []
        for label, pattern in SUSPICIOUS_PATTERNS.items():
            if re.search(pattern, content):
                matches.append(label)
        return matches
    except Exception as e:
        return [f"Error reading file: {e}"]

def scan_directory(path):
    report = {}
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                result = scan_file(full_path)
                if result:
                    report[full_path] = result
    return report

def main():
    directory = input("Enter directory to scan: ").strip()
    if not os.path.isdir(directory):
        print("Invalid directory.")
        return
    results = scan_directory(directory)
    if not results:
        print("No suspicious patterns found.")
    else:
        print("\nSuspicious patterns detected:\n")
        for file, issues in results.items():
            print(f"{file}:")
            for issue in issues:
                print(f"  - {issue}")
            print()

if __name__ == "__main__":
    main()
