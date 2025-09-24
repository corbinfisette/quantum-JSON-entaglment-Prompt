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
        result = {"file": args.file, "valid": False, "error": f"File not found: {args.file}"}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"❌ Validation result: {result}")
        log(f"✗ File not found: {args.file}", "ERROR")
        print(Fore.YELLOW + f"💡 Tip: Check if the file path is correct and the file exists.")
        print(Fore.CYAN + f"💡 Available examples: Run 'python cli/evoprompt.py examples' to see sample files.")
        return
    
    log(f"Validating file: {args.file}")
    
    # Load and parse the JSON file
    try:
        with open(args.file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        result = {"file": args.file, "valid": False, "error": f"Invalid JSON: {e}"}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"❌ Validation result: {result}")
        print(Fore.YELLOW + f"💡 Tip: Check your JSON syntax. Common issues include missing commas, quotes, or brackets.")
        return
    except IOError as e:
        result = {"file": args.file, "valid": False, "error": f"File error: {e}"}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"❌ Validation result: {result}")
        return
    
    # Determine the domain for schema selection
    domain = determine_domain_from_content(data)
    if not domain:
        result = {"file": args.file, "valid": False, "error": "Cannot determine domain from content. Missing metadata.domain field."}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"❌ Validation result: {result}")
        print(Fore.YELLOW + f"💡 Tip: Add a 'metadata' section with a 'domain' field to your JSON file.")
        print(Fore.CYAN + f"💡 Supported domains: cold_email, landing_page, competitor_analysis")
        return
    
    # Load the appropriate schema
    schema = load_schema_for_domain(domain)
    if not schema:
        result = {"file": args.file, "valid": False, "error": f"No schema found for domain: {domain}"}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"❌ Validation result: {result}")
        print(Fore.YELLOW + f"💡 Available schemas: Run 'python cli/evoprompt.py schemas' to see supported domains.")
        return
    
    # Perform JSON schema validation
    try:
        json_validate(instance=data, schema=schema)
        result = {"file": args.file, "valid": True, "domain": domain}
        if ctx:
            ctx.validation_result = result
        print(Fore.GREEN + f"✅ Validation result: {result}")
        log(f"✓ File {args.file} is valid according to {domain} schema", "INFO")
        print(Fore.CYAN + f"🎉 Success! Your quantum prompt is properly structured for the {domain} domain.")
    except ValidationError as e:
        result = {"file": args.file, "valid": False, "error": f"Schema validation failed: {e.message}", "domain": domain}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"❌ Validation result: {result}")
        log(f"✗ Validation error at path '{'.'.join(str(p) for p in e.path)}': {e.message}", "ERROR")
        print(Fore.YELLOW + f"💡 Tip: Check the field '{'.'.join(str(p) for p in e.path)}' in your JSON file.")
        print(Fore.CYAN + f"💡 Example: Look at examples/{domain}_input.json for proper structure.")
    except SchemaError as e:
        result = {"file": args.file, "valid": False, "error": f"Schema error: {e.message}", "domain": domain}
        if ctx:
            ctx.validation_result = result
        print(Fore.RED + f"❌ Validation result: {result}")
        log(f"✗ Schema error: {e.message}", "ERROR")

# Generation command
def generate(args, ctx=None):
    if not os.path.isfile(args.input):
        print(Fore.RED + f"❌ Input file not found: {args.input}")
        log(f"✗ File not found: {args.input}", "ERROR")
        print(Fore.YELLOW + f"💡 Tip: Check if the file path is correct and the file exists.")
        print(Fore.CYAN + f"💡 Available examples: Run 'python cli/evoprompt.py examples' to see sample files.")
        return
    log(f"Generating output for: {args.input}")
    output = {"input": args.input, "output": "Generated data"}
    if ctx:
        ctx.generated_output = output
    print(Fore.CYAN + f"🔄 Generation result: {output}")
    print(Fore.GREEN + f"✨ Generation completed! Your quantum prompt has been processed.")

# Entangle command: validate then generate
class Context:
    def __init__(self):
        self.validation_result = None
        self.generated_output = None

def entangle(args):
    print(Fore.MAGENTA + "\n🔗 Quantum Entanglement Process")
    print(Fore.CYAN + "Performing validation and generation in quantum entangled state...")
    
    ctx = Context()
    print(Fore.BLUE + "\n1️⃣  Validation Phase:")
    validate(args, ctx)
    
    if ctx.validation_result and ctx.validation_result.get('valid'):
        print(Fore.BLUE + "\n2️⃣  Generation Phase:")
        args.input = args.file
        generate(args, ctx)
        
        print(Fore.MAGENTA + f"\n🔗 Quantum Entangled Results:")
        print(Fore.GREEN + f"   Validation: {ctx.validation_result}")
        print(Fore.CYAN + f"   Generation: {ctx.generated_output}")
        print(Fore.GREEN + "\n✨ Quantum entanglement process completed successfully!")
    else:
        print(Fore.RED + "\n❌ Entanglement failed: Validation phase unsuccessful.")
        print(Fore.YELLOW + "💡 Fix validation errors before proceeding with generation.")

# List schemas command
def list_schemas(args):
    schemas = discover_files(os.path.join(os.path.dirname(__file__), "..", "schemas"), ".json")
    if schemas:
        print(Fore.GREEN + "Available Schemas:")
        for s in schemas:
            print("  " + os.path.relpath(s, os.path.dirname(__file__)))
    else:
        print(Fore.RED + "No schemas found.")

# List examples command
def list_examples(args):
    examples = discover_files(os.path.join(os.path.dirname(__file__), "..", "examples"), ".json")
    if examples:
        print(Fore.CYAN + "Available Examples:")
        for e in examples:
            print("  " + os.path.relpath(e, os.path.dirname(__file__)))
    else:
        print(Fore.RED + "No examples found.")

# Plugin stub
def plugin(args):
    print(Fore.MAGENTA + "Plugin system coming soon! Quantum extensibility awaits.")

# Quantum prompt generation command
def quantum(args):
    n = args.n if hasattr(args, 'n') else 3
    print(Fore.BLUE + "\n🔮 Quantum Prompt Generation:")
    print(Fore.CYAN + f"Generating {n} superposed quantum prompts...")
    
    superposed = generate_superposed_prompts(n)
    print(Fore.YELLOW + "\n⚛️  Superposed Prompts:")
    print(json.dumps(superposed, indent=2))
    
    entangled = entangle_prompts(superposed)
    print(Fore.GREEN + "\n🔗 Entangled Prompt:")
    print(json.dumps(entangled, indent=2))
    
    collapsed = collapse_prompt(superposed)
    print(Fore.MAGENTA + "\n📏 Collapsed Prompt (Measurement):")
    print(json.dumps(collapsed, indent=2))
    
    print(Fore.GREEN + "\n✨ Quantum generation completed!")
    print(Fore.CYAN + "💡 These quantum prompts demonstrate superposition, entanglement, and wave function collapse.")

# Interactive guided mode
def guided_mode():
    """Interactive guided mode for new users."""
    print(Fore.GREEN + "\n🌟 Welcome to the Evoprompt Protocol Guided Experience!")
    print(Fore.CYAN + "\nThis interactive mode will help you get started with quantum prompt engineering.")
    
    while True:
        print(Fore.YELLOW + "\n" + "="*60)
        print(Fore.WHITE + "What would you like to do? Choose an option:")
        print(Fore.CYAN + "1. 🔮 Generate quantum prompts (quantum)")
        print(Fore.CYAN + "2. ✅ Validate an existing prompt file (validate)")
        print(Fore.CYAN + "3. 🔗 Validate and generate combined (entangle)")
        print(Fore.CYAN + "4. 📋 View available schemas (schemas)")
        print(Fore.CYAN + "5. 📚 View example files (examples)")
        print(Fore.CYAN + "6. ❓ Show CLI help")
        print(Fore.CYAN + "7. 🚪 Exit")
        
        try:
            choice = input(Fore.WHITE + "\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                guided_quantum_generation()
            elif choice == "2":
                guided_validation()
            elif choice == "3":
                guided_entanglement()
            elif choice == "4":
                print(Fore.GREEN + "\n📋 Available Schemas:")
                list_schemas(None)
            elif choice == "5":
                print(Fore.GREEN + "\n📚 Example Files:")
                list_examples(None)
            elif choice == "6":
                show_detailed_help()
            elif choice == "7":
                print(Fore.GREEN + "\n👋 Thank you for using Evoprompt Protocol! Quantum coherence maintained.")
                break
            else:
                print(Fore.RED + "❌ Invalid choice. Please enter a number between 1-7.")
                
        except KeyboardInterrupt:
            print(Fore.GREEN + "\n\n👋 Goodbye! Quantum coherence maintained.")
            break
        except EOFError:
            print(Fore.GREEN + "\n\n👋 Goodbye! Quantum coherence maintained.")
            break

def guided_quantum_generation():
    """Guide user through quantum prompt generation."""
    print(Fore.GREEN + "\n🔮 Quantum Prompt Generation")
    print(Fore.CYAN + "Generate superposed quantum prompts that exist in multiple states simultaneously.")
    
    try:
        n = input(Fore.WHITE + "\nHow many quantum prompts would you like to generate? (default: 3): ").strip()
        if not n:
            n = 3
        else:
            n = int(n)
            if n < 1 or n > 10:
                print(Fore.YELLOW + "⚠️  Adjusting to safe quantum range (1-10). Using 3.")
                n = 3
                
        print(Fore.BLUE + f"\n🎯 Generating {n} quantum prompts...")
        
        # Create a mock args object
        class Args:
            def __init__(self, n):
                self.n = n
        
        quantum(Args(n))
        
    except ValueError:
        print(Fore.RED + "❌ Invalid number. Using default value of 3.")
        quantum(Args(3))
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Quantum generation interrupted.")

def guided_validation():
    """Guide user through file validation."""
    print(Fore.GREEN + "\n✅ File Validation")
    print(Fore.CYAN + "Validate your quantum prompt files against EPP schemas.")
    
    # Show available examples first
    print(Fore.BLUE + "\n📚 Available example files:")
    list_examples(None)
    
    file_path = input(Fore.WHITE + "\nEnter the path to your JSON file (or press Enter to validate an example): ").strip()
    
    if not file_path:
        file_path = "examples/cold_email_input.json"
        print(Fore.BLUE + f"📁 Using example file: {file_path}")
    
    if not os.path.isfile(file_path):
        print(Fore.RED + f"❌ File not found: {file_path}")
        return
        
    # Create a mock args object
    class Args:
        def __init__(self, file):
            self.file = file
    
    print(Fore.BLUE + f"\n🔍 Validating {file_path}...")
    validate(Args(file_path))

def guided_entanglement():
    """Guide user through entangled validation and generation."""
    print(Fore.GREEN + "\n🔗 Quantum Entanglement (Validate + Generate)")
    print(Fore.CYAN + "Perform quantum entangled validation and generation in one operation.")
    
    # Show available examples first
    print(Fore.BLUE + "\n📚 Available example files:")
    list_examples(None)
    
    file_path = input(Fore.WHITE + "\nEnter the path to your JSON file (or press Enter to use an example): ").strip()
    
    if not file_path:
        file_path = "examples/landing_page_input.json"
        print(Fore.BLUE + f"📁 Using example file: {file_path}")
    
    if not os.path.isfile(file_path):
        print(Fore.RED + f"❌ File not found: {file_path}")
        return
        
    # Create a mock args object
    class Args:
        def __init__(self, file):
            self.file = file
    
    print(Fore.BLUE + f"\n🔗 Entangling {file_path}...")
    entangle(Args(file_path))

def show_detailed_help():
    """Show detailed CLI help with examples."""
    print(Fore.GREEN + "\n❓ Evoprompt Protocol CLI Help")
    print(Fore.CYAN + "\nCommand Usage Examples:")
    print(Fore.WHITE + "  python cli/evoprompt.py quantum -n 5")
    print(Fore.GRAY + "    → Generate 5 quantum prompts")
    print(Fore.WHITE + "  python cli/evoprompt.py validate examples/cold_email_input.json")
    print(Fore.GRAY + "    → Validate a prompt file")
    print(Fore.WHITE + "  python cli/evoprompt.py entangle examples/landing_page_input.json")
    print(Fore.GRAY + "    → Validate and generate from a prompt file")
    print(Fore.WHITE + "  python cli/evoprompt.py schemas")
    print(Fore.GRAY + "    → List available JSON schemas")
    print(Fore.WHITE + "  python cli/evoprompt.py examples")
    print(Fore.GRAY + "    → List example prompt files")

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
        # Show help hint before launching guided mode
        print(Fore.YELLOW + "\n💡 Tip: You can also use specific commands directly:")
        print(Fore.CYAN + "   python cli/evoprompt.py --help  (for command reference)")
        print(Fore.CYAN + "   python cli/evoprompt.py quantum  (quick quantum generation)")
        print(Fore.CYAN + "   python cli/evoprompt.py validate <file>  (validate a file)")
        print("")
        # Launch guided mode instead of just showing help
        guided_mode()

if __name__ == "__main__":
    main()
