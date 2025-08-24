# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands and Development Workflow

### Genesis Engine Commands
The Genesis Engine is the core scaffolding tool built using the Hive Architecture itself:

```bash
# Navigate to genesis-engine directory first
cd genesis-engine

# Scaffold different component patterns (codons)
python main.py hatch command <component_name>    # Creates C->A->G pattern (Handle Command)
python main.py hatch query <component_name>      # Creates C->T->C pattern (Query Data)
python main.py hatch event <component_name>      # Creates G->C->A->G pattern (React to Event)
python main.py hatch immune <component_name>     # Creates G->C->A->C pattern (Immune Response)

# Add testing/infrastructure (under construction)
python main.py spin <component_name>
```

### ElizaOS Agent Commands
For running the AI agents defined in this repository:

```bash
# Start individual agents (illustrative - depends on ElizaOS setup)
elizaos agent start --character Eddy.json       # Developer support agent
elizaos agent start --character Eliza.json      # Playful personality agent
elizaos agent start --character Jules.json      # Software engineering agent

# Run multiple agents together
elizaos project start --agents "Eddy.json,Eliza.json,Jules.json"
```

## Architecture Overview

This repository implements the **Hive Architecture** - a sophisticated, nature-inspired approach to building distributed systems. The architecture operates on multiple conceptual levels:

### Core Philosophy: The Eight Levels of the Hive

1. **The Organism** - The entire digital ecosystem
2. **The Cell** - Individual bounded contexts/services with strong API boundaries
3. **The Codons** - Four fundamental interaction patterns (see below)
4. **ATCG Primitives** - The genetic building blocks of all components
5. **Codeons** - Pure, testable implementation functions
6. **The Physics** - The underlying environment (OS, network, CPU)
7. **The Intent** - The philosophical "why" behind the system
8. **The Immune System** - Error handling and self-healing capabilities

### The ATCG Genetic Code

Every component in the Hive is built from four fundamental primitives:

- **A**ggregate: Domain entities that enforce business rules and maintain consistency
- **T**ransformation: Pure, stateless functions that process data
- **C**onnector: Adapters that handle external communication (Hexagonal Architecture ports)
- **G**enesis Event: Immutable records of domain changes that enable loose coupling

### The Four Sacred Codons (Interaction Patterns)

1. **Handle Command (`C -> A -> G`)**: Changes system state safely
   - Connector receives external request → Aggregate validates and processes → Genesis Event records the change

2. **Query Data (`C -> T -> C`)**: Reads system state without side effects
   - Connector receives query → Transformation processes data → Result returned through Connector

3. **React to Event (`G -> C -> A -> G`)**: Enables choreography between components
   - Genesis Event triggers → Connector translates to command → Aggregate processes → New events generated

4. **Immune Response (`G -> C -> A -> C`)**: Self-healing system responses
   - Error/mutation detected → Connector translates to corrective action → Aggregate fixes issue

### Multi-Agent Communication Protocol (MCP)

The repository includes a draft MCP for structured communication between AI agents:

- **Message Structure**: JSON-based with performatives (TASK_REQUEST, TASK_ACCEPT, INFORM_RESULT, etc.)
- **Ontology System**: Semantic context using URN-like identifiers (e.g., `elizaos:ontology:code/python/debug_request`)
- **Agent Collaboration**: Enables agents like Eddy (support) to delegate coding tasks to Jules (engineer)

## Repository Structure

```
agents/
├── genesis-engine/           # Python-based scaffolding tool implementing Hive Architecture
│   ├── main.py              # CLI entry point with click commands
│   ├── aggregates/          # Domain logic components (A primitive)
│   ├── transformations/     # Pure business logic functions (T primitive)
│   └── connectors/          # External interface adapters (C primitive)
├── tRNA/                    # Template files for code generation
│   ├── *.py.tpl            # Python templates for different component types
├── dna-core/               # Core architectural documentation
│   ├── PATTERNS.md         # ATCG primitive definitions
│   ├── CHOREOGRAPHY.md     # Event-driven coordination patterns
│   └── IMMUNITY.md         # Error handling and self-healing patterns
├── hive/                   # Generated components live here
├── *.json                  # ElizaOS agent configurations (Eddy, Eliza, Jules)
├── HIVE_CONSTITUTION.md    # The foundational tale and philosophy
├── GRIMOIRE.md            # Technical implementation guide
└── MCP_DRAFT.md           # Multi-Agent Communication Protocol specification
```

## Key Concepts for Development

### Component Generation
- All new components should be generated using the Genesis Engine rather than written manually
- The engine ensures architectural consistency and follows the ATCG primitive patterns
- Templates in `tRNA/` define the structure for each component type

### Event-Driven Design
- State changes are recorded as Genesis Events (Domain Events)
- Components communicate through events rather than direct coupling
- Follow the "Pollen Protocol" for event structure consistency

### Hexagonal Architecture
- Domain core (Aggregates, Transformations) is isolated from infrastructure
- Connectors handle all external communication (HTTP, databases, file systems)
- Business logic remains pure and testable

### Agent Configurations
- `Eddy.json`: Developer support agent with ElizaOS framework knowledge
- `Eliza.json`: Conversational agent with playful personality
- `Jules.json`: Software engineering specialist for complex coding tasks
- Each agent has defined message examples, actions, and knowledge bases

### Architectural Validation
- The Immune System detects "mutations" (architectural violations)
- Components should follow the established patterns and not break encapsulation
- Genesis Events provide audit trails for all system changes

This repository represents a proof-of-concept for building self-organizing, nature-inspired software systems that can adapt and evolve while maintaining architectural integrity.