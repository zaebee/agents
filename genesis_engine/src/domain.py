# genesis_engine/src/domain.py
from dataclasses import dataclass, field
from typing import Dict

# This file defines the core domain models for the compiler itself.
# This is the "state" of the CompilerAggregate.

@dataclass
class CompilationJob:
    """Represents the state of a single compilation task."""
    source_path: str
    output_dir: str
    ast: Dict = field(default_factory=dict)
    generated_files: Dict[str, str] = field(default_factory=dict)
    status: str = "pending"

# --- Commands ---
@dataclass
class StartCompilation:
    source_path: str
    output_dir: str

# --- Events ---
@dataclass
class CompilationStarted:
    source_path: str

@dataclass
class CompilationFinished:
    output_dir: str
    num_files_generated: int
