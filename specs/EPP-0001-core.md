# EPP-0001 Core

## Overview
The Core specification defines the fundamental structure and principles for Evoprompt Protocol (EPP) quantum-entangled JSON prompts.

## Core Principles

### Quantum Superposition
Prompts exist in multiple states simultaneously until "observed" (processed), allowing for adaptive content generation.

### Entanglement
Related prompt components are linked such that modifying one component affects all entangled components instantly.

### Uncertainty Principle  
Prompt specificity and adaptability exist in an inverse relationship - the more specific a prompt, the less adaptable it becomes.

## JSON Structure

### Base Schema
```json
{
  "epp_version": "1.0.0",
  "quantum_state": "superposed|entangled|collapsed",
  "prompt_id": "unique-identifier",
  "metadata": {
    "created": "ISO-8601-timestamp",
    "domain": "cold_email|landing_page|competitor_analysis|custom"
  },
  "content": {
    "title": "string",
    "body": "string",
    "variables": {}
  }
}
```

### Required Fields
- `epp_version`: Protocol version for compatibility
- `quantum_state`: Current state of the prompt
- `prompt_id`: Unique identifier for entanglement tracking
- `content`: The actual prompt content

## Processing States

1. **Superposed**: Multiple potential prompts exist simultaneously
2. **Entangled**: Prompts are linked and affect each other
3. **Collapsed**: A specific prompt has been selected through measurement
