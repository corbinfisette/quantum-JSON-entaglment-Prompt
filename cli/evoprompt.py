"""Evoprompt Protocol CLI - Quantum-level management, validation, and generation with EPP specs."""
# Requirements: pip install colorama jsonschema
import argparse
import os
import sys
import json
from colorama import Fore, Style, init
from datetime import datetime
import jsonschema
from jsonschema import validate as json_validate, ValidationError, SchemaError
sys.path.append(os.path.dirname(__file__))
from quantum_prompts import generate_superposed_prompts, entangle_prompts, collapse_prompt

# Initialize colorama for colored output
init(autoreset=True)

# ASCII Art Logo
LOGO = r"""
 _____                 _                                 _   
| ____|_ __ ___  _ __ | | ___  _   _  ___  ___  ___  __| |  
|  _| | '_ ` _ \| '_ \| |/ _ \| | | |/ _ \/ __|/ _ \/ _` |  
| |___| | | | | | |_) | | (_) | |_| |  __/\__ \  __/ (_| |  
|_____|_| |_| |_| .__/|_|\___/ \__, |\___||___/\___|\__,_|  
                |_|            |___/                        
"""

# Utility: Discover files by extension
def discover_files(folder, ext):
    found = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(ext):
                found.append(os.path.join(root, f))
    return found

# Utility: Load JSON schema by domain
def load_schema_for_domain(domain):
    """Load the appropriate JSON schema for a given domain."""
    schema_map = {
        "cold_email": "epp.cold_email",
        "landing_page": "epp.landing_page", 
        "competitor_analysis": "epp.competitor_analysis"
    }
    
    if domain not in schema_map:
        return None
        
    schema_name = schema_map[domain]
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", schema_name, "1.0.0.json"
    )
    
    if not os.path.isfile(schema_path):
        return None
        
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        log(f"Error loading schema {schema_path}: {e}", "ERROR")
        return None

# Utility: Determine domain from JSON content
def determine_domain_from_content(data):
    """Determine the domain from JSON content."""
    if isinstance(data, dict):
        metadata = data.get("metadata", {})
        return metadata.get("domain")
    return None

# Logging utility
def log(msg, level="INFO"):
    print(f"{Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {level}: {Style.RESET_ALL}{msg}")

# Validation command
def validate(args, ctx=None):
    if not os.path.isfile(args.file):
        log(f"File not found: {args.file}", "ERROR")
        sys.exit(1)
    
    log(f"Validating file: {args.file}")
    
    # Load and parse the JSON file
    try:
        with open(args.file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        result = {"file": args.file, "valid": False, "error": f"Invalid JSON: {e}"}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"Validation result: {result}")
        return
    except IOError as e:
        result = {"file": args.file, "valid": False, "error": f"File error: {e}"}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"Validation result: {result}")
        return
    
    # Determine the domain for schema selection
    domain = determine_domain_from_content(data)
    if not domain:
        result = {"file": args.file, "valid": False, "error": "Cannot determine domain from content. Missing metadata.domain field."}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"Validation result: {result}")
        return
    
    # Load the appropriate schema
    schema = load_schema_for_domain(domain)
    if not schema:
        result = {"file": args.file, "valid": False, "error": f"No schema found for domain: {domain}"}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"Validation result: {result}")
        return
    
    # Perform JSON schema validation
    try:
        json_validate(instance=data, schema=schema)
        result = {"file": args.file, "valid": True, "domain": domain}
        if ctx:
            ctx.validation_result = result
        print(Fore.GREEN + f"Validation result: {result}")
        log(f"✓ File {args.file} is valid according to {domain} schema", "INFO")
    except ValidationError as e:
        result = {"file": args.file, "valid": False, "error": f"Schema validation failed: {e.message}", "domain": domain}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"Validation result: {result}")
        log(f"✗ Validation error at path '{'.'.join(str(p) for p in e.path)}': {e.message}", "ERROR")
    except SchemaError as e:
        result = {"file": args.file, "valid": False, "error": f"Schema error: {e.message}", "domain": domain}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"Validation result: {result}")
        log(f"✗ Schema error: {e.message}", "ERROR")

# Generation command
def generate(args, ctx=None):
    if not os.path.isfile(args.input):
        log(f"Input file not found: {args.input}", "ERROR")
        sys.exit(1)
    log(f"Generating output for: {args.input}")
    output = {"input": args.input, "output": "Generated data"}
    if ctx:
        ctx.generated_output = output
    print(Fore.CYAN + f"Generation result: {output}")

# Entangle command: validate then generate
class Context:
    def __init__(self):
        self.validation_result = None
        self.generated_output = None

def entangle(args):
    ctx = Context()
    validate(args, ctx)
    args.input = args.file
    generate(args, ctx)
    print(Fore.MAGENTA + f"Entangled results:\nValidation: {ctx.validation_result}\nGeneration: {ctx.generated_output}")

# Utility: List files in a directory with consistent formatting
def list_files_in_directory(folder_name, display_name, color):
    """Generic function to list files in a directory with consistent formatting."""
    files = discover_files(os.path.join(os.path.dirname(__file__), "..", folder_name), ".json")
    if files:
        print(color + f"Available {display_name}:")
        for f in files:
            print("  " + os.path.relpath(f, os.path.dirname(__file__)))
    else:
        print(Fore.RED + f"No {display_name.lower()} found.")

# List schemas command
def list_schemas(args):
    list_files_in_directory("schemas", "Schemas", Fore.GREEN)

# List examples command
def list_examples(args):
    list_files_in_directory("examples", "Examples", Fore.CYAN)

# Plugin stub
def plugin(args):
    print(Fore.MAGENTA + "Plugin system coming soon! Quantum extensibility awaits.")

# Quantum prompt generation command
def quantum(args):
    n = args.n if hasattr(args, 'n') else 3
    print(Fore.BLUE + "\nQuantum Prompt Generation:")
    superposed = generate_superposed_prompts(n)
    print(Fore.YELLOW + "Superposed Prompts:")
    print(json.dumps(superposed, indent=2))
    entangled = entangle_prompts(superposed)
    print(Fore.GREEN + "\nEntangled Prompt:")
    print(json.dumps(entangled, indent=2))
    collapsed = collapse_prompt(superposed)
    print(Fore.MAGENTA + "\nCollapsed Prompt (Measurement):")
    print(json.dumps(collapsed, indent=2))

# Main CLI entrypoint
def main():
    print(Fore.BLUE + LOGO)
    parser = argparse.ArgumentParser(
        description=Fore.YELLOW + "Evoprompt Protocol CLI - Quantum-level management, validation, and generation with EPP specs."
    )
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    parser_validate = subparsers.add_parser("validate", help="Validate input against a schema.")
    parser_validate.add_argument("file", help="Path to the input file to validate.")
    parser_validate.set_defaults(func=lambda args: validate(args))

    parser_generate = subparsers.add_parser("generate", help="Generate output from input data.")
    parser_generate.add_argument("input", help="Path to the input file.")
    parser_generate.set_defaults(func=lambda args: generate(args))

    parser_entangle = subparsers.add_parser("entangle", help="Validate and generate in one quantum entangled run.")
    parser_entangle.add_argument("file", help="Path to the input file to validate and generate from.")
    parser_entangle.set_defaults(func=entangle)

    parser_schemas = subparsers.add_parser("schemas", help="List available schemas.")
    parser_schemas.set_defaults(func=list_schemas)

    parser_examples = subparsers.add_parser("examples", help="List available examples.")
    parser_examples.set_defaults(func=list_examples)

    parser_plugin = subparsers.add_parser("plugin", help="Quantum plugin system (stub).")
    parser_plugin.set_defaults(func=plugin)

    parser_quantum = subparsers.add_parser("quantum", help="Generate quantum-infused JSON prompts.")
    parser_quantum.add_argument("-n", type=int, default=3, help="Number of superposed prompts to generate.")
    parser_quantum.set_defaults(func=quantum)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        log("No subcommand provided. Showing help:", "WARN")
        parser.print_help()

if __name__ == "__main__":
    main()
