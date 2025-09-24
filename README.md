# Evoprompt Protocol

Quantum-entangled JSON prompt management system implementing the Evoprompt Protocol (EPP) for advanced prompt engineering with quantum computing concepts.

## Overview

The Evoprompt Protocol brings quantum mechanics principles to prompt engineering:

- **Quantum Superposition**: Prompts exist in multiple states simultaneously until "observed"
- **Entanglement**: Related prompts are linked so changes affect all connected prompts
- **Uncertainty Principle**: Balance between prompt specificity and adaptability
- **Coherence**: Maintain quantum relationships across prompt transformations

## Installation

```bash
git clone https://github.com/corbinfisette/quantum-JSON-entaglment-Prompt.git
cd quantum-JSON-entaglment-Prompt
pip install colorama  # Required dependency
```

## Quick Start

### CLI Usage

#### 🌟 Guided Interactive Mode (New!)

For the best user experience, simply run the CLI without arguments to launch the interactive guided mode:

```bash
python cli/evoprompt.py
```

This will present you with a user-friendly menu to guide you through:
- 🔮 Generating quantum prompts
- ✅ Validating prompt files with helpful error messages
- 🔗 Running combined validation and generation
- 📋 Viewing available schemas and examples

#### Direct Commands

```bash
# Display help
python cli/evoprompt.py --help

# List available schemas
python cli/evoprompt.py schemas

# List example prompts  
python cli/evoprompt.py examples

# Validate a prompt file (with improved error guidance)
python cli/evoprompt.py validate examples/cold_email_input.json

# Generate quantum prompts (with enhanced visual output)
python cli/evoprompt.py quantum -n 3

# Quantum entangle validation and generation (with step-by-step feedback)
python cli/evoprompt.py entangle examples/landing_page_input.json
```

### Example: Quantum Prompt Generation

```bash
python cli/evoprompt.py quantum -n 5
```

This generates superposed prompts, entangles them, and collapses to a specific measurement.

### ✨ Enhanced User Experience Features

The CLI now provides a **well-guided app experience** with:

- **🎯 Interactive Guided Mode**: Step-by-step wizards for all common workflows
- **📱 User-Friendly Interface**: Visual indicators, emojis, and clear progress feedback  
- **❌ Smart Error Handling**: Helpful tips and actionable guidance for common mistakes
- **💡 Contextual Help**: Suggestions for next steps and available options
- **🔄 Progressive Workflow**: Validation errors prevent generation until fixed
- **📚 Discovery Features**: Easy access to examples and schemas

Perfect for both beginners learning quantum prompt engineering and experts who want efficient workflows!

## EPP Specifications

The protocol implements four core specifications:

1. **[EPP-0001 Core](specs/EPP-0001-core.md)** - Fundamental quantum prompt structure
2. **[EPP-0002 Assembly](specs/EPP-0002-assembly.md)** - Prompt composition and transformation 
3. **[EPP-0003 Context Streaming](specs/EPP-0003-context-streaming.md)** - Real-time quantum state transmission
4. **[EPP-0004 Feedback Mutation](specs/EPP-0004-feedback-mutation.md)** - Evolutionary prompt optimization

## JSON Schema Structure

All EPP prompts follow this quantum-enhanced structure:

```json
{
  "epp_version": "1.0.0",
  "quantum_state": "superposed|entangled|collapsed", 
  "prompt_id": "unique-identifier",
  "metadata": {
    "created": "2024-01-15T10:30:00Z",
    "domain": "cold_email|landing_page|competitor_analysis|custom",
    "tags": ["optional", "categorization"]
  },
  "content": {
    "title": "Prompt title or subject",
    "body": "Main prompt content with quantum properties",
    "variables": {},
    "quantum_properties": {
      "coherence": 0.85,
      "entanglement_refs": ["other_prompt_ids"]
    }
  }
}
```

## Available Domains

- **Cold Email**: B2B outreach with quantum personalization
- **Landing Page**: Product pages with superposed value propositions  
- **Competitor Analysis**: Market intelligence with quantum insights

## Examples

See the `examples/` directory for complete prompt samples:

- `cold_email_input.json` - Quantum B2B outreach
- `landing_page_input.json` - Entangled product presentation
- `competitor_analysis_input.json` - Collapsed competitive intelligence

## Testing

Test cases are defined in `tests/validation_cases.json`. Run validation:

```bash
python cli/evoprompt.py validate examples/cold_email_input.json
```

## Contributing

1. Follow EPP specifications when adding new features
2. Maintain quantum coherence in prompt relationships
3. Test entanglement effects across prompt domains
4. Update documentation for protocol changes

## License

See [LICENSE](LICENSE) for details.
