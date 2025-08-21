#!/usr/bin/env python3
"""
ATCG Architectural Linter - Validate Sacred Genetic Patterns

The world's first genetic code linter for software architecture.
Validates that code follows the sacred ATCG patterns and Sacred Codons.

Based on the Hive Constitution and the Beekeeper's wisdom.
"""

import ast
import re
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any, Tuple
from enum import Enum

class LintSeverity(Enum):
    """Severity levels for ATCG lint violations"""
    INFO = "info"           # Suggestions for improvement
    WARNING = "warning"     # Architectural smell, should be fixed
    ERROR = "error"         # Violates sacred patterns
    CRITICAL = "critical"   # Breaks genetic code integrity

class ATCGElement(Enum):
    """The four sacred genetic elements"""
    AGGREGATE = "A"         # Business logic containers
    TRANSFORMATION = "T"    # Pure functions and services
    CONNECTOR = "C"         # Adapters and interfaces
    GENESIS_EVENT = "G"     # Domain events

@dataclass
class LintViolation:
    """A violation of ATCG architectural patterns"""
    severity: LintSeverity
    element_type: Optional[ATCGElement]
    message: str
    file_path: str
    line_number: int
    column: int = 0
    suggestion: str = ""
    sacred_pattern: str = ""

@dataclass 
class ATCGFile:
    """Represents a file analyzed for ATCG patterns"""
    path: Path
    element_type: Optional[ATCGElement]
    class_names: List[str] = field(default_factory=list)
    function_names: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

class ATCGLinter:
    """
    The ATCG Architectural Linter - validates sacred genetic patterns.
    
    This linter enforces the genetic code of the Hive:
    - A (Aggregate): Must encapsulate state and enforce invariants
    - T (Transformation): Must be pure and stateless
    - C (Connector): Must translate protocols correctly
    - G (Genesis Event): Must follow event patterns
    
    Also validates Sacred Codons:
    - Handle Command (C→A→G)
    - Query Data (C→T→C)
    - React to Event (G→C→A→G)
    - Immune Response (G→C→A→C)
    - Choreography (complex workflows)
    """
    
    def __init__(self):
        self.violations: List[LintViolation] = []
        self.files_analyzed: List[ATCGFile] = []
        self.sacred_patterns = {
            "aggregate_patterns": [
                r"class\s+\w*Aggregate",
                r"class\s+\w*Entity", 
                r"class\s+\w*Root"
            ],
            "transformation_patterns": [
                r"class\s+\w*Service",
                r"class\s+\w*Calculator",
                r"def\s+transform_",
                r"def\s+process_"
            ],
            "connector_patterns": [
                r"class\s+\w*Adapter",
                r"class\s+\w*Connector",
                r"class\s+\w*Repository",
                r"class\s+\w*Controller"
            ],
            "event_patterns": [
                r"class\s+\w*Event",
                r"class\s+\w*Happened",
                r"class\s+\w*Occurred"
            ]
        }
        
        # Sacred Codon patterns
        self.sacred_codons = {
            "handle_command": {
                "pattern": r"def\s+handle_\w*command",
                "expected_flow": "C→A→G",
                "description": "Command handling pattern"
            },
            "query_data": {
                "pattern": r"def\s+(query|get|find)_\w+",
                "expected_flow": "C→T→C", 
                "description": "Data query pattern"
            },
            "react_to_event": {
                "pattern": r"def\s+(on_|handle_)\w*event",
                "expected_flow": "G→C→A→G",
                "description": "Event reaction pattern"
            },
            "immune_response": {
                "pattern": r"def\s+(handle_|respond_to_)\w*mutation",
                "expected_flow": "G→C→A→C",
                "description": "Immune system response pattern"
            }
        }
    
    def lint_project(self, project_path: str) -> Dict[str, Any]:
        """
        Lint an entire project for ATCG compliance.
        
        Args:
            project_path: Path to the project root
            
        Returns:
            Comprehensive linting report
        """
        project_root = Path(project_path)
        print(f"🔬 ATCG Linter analyzing project: {project_root}")
        
        # Reset state
        self.violations = []
        self.files_analyzed = []
        
        # Find all Python files
        python_files = list(project_root.rglob("*.py"))
        
        for file_path in python_files:
            try:
                self._lint_file(file_path)
            except Exception as e:
                self.violations.append(LintViolation(
                    severity=LintSeverity.ERROR,
                    element_type=None,
                    message=f"Failed to analyze file: {e}",
                    file_path=str(file_path),
                    line_number=1
                ))
        
        return self._generate_report()
    
    def _lint_file(self, file_path: Path):
        """Lint a single Python file for ATCG compliance"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST
        try:
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError as e:
            self.violations.append(LintViolation(
                severity=LintSeverity.ERROR,
                element_type=None,
                message=f"Syntax error prevents ATCG analysis: {e}",
                file_path=str(file_path),
                line_number=e.lineno or 1
            ))
            return
        
        # Determine file's ATCG element type
        element_type = self._classify_file(file_path, content)
        
        atcg_file = ATCGFile(
            path=file_path,
            element_type=element_type
        )
        
        # Extract classes and functions
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                atcg_file.class_names.append(node.name)
                self._lint_class(node, file_path, element_type)
            elif isinstance(node, ast.FunctionDef):
                atcg_file.function_names.append(node.name)
                self._lint_function(node, file_path, element_type)
            elif isinstance(node, ast.Import):
                atcg_file.imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    atcg_file.imports.append(node.module)
        
        # Validate ATCG architectural constraints
        self._validate_atcg_constraints(atcg_file, content)
        
        # Validate Sacred Codon patterns
        self._validate_sacred_codons(atcg_file, content)
        
        self.files_analyzed.append(atcg_file)
    
    def _classify_file(self, file_path: Path, content: str) -> Optional[ATCGElement]:
        """Classify a file as one of the ATCG elements"""
        file_name = file_path.name.lower()
        
        # Check file naming patterns
        if any(pattern in file_name for pattern in ['aggregate', 'entity', 'root']):
            return ATCGElement.AGGREGATE
        elif any(pattern in file_name for pattern in ['service', 'transformation', 'calculator']):
            return ATCGElement.TRANSFORMATION
        elif any(pattern in file_name for pattern in ['adapter', 'connector', 'repository', 'controller']):
            return ATCGElement.CONNECTOR
        elif any(pattern in file_name for pattern in ['event', 'genesis']):
            return ATCGElement.GENESIS_EVENT
        
        # Check content patterns
        for element, patterns in self.sacred_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    if element == "aggregate_patterns":
                        return ATCGElement.AGGREGATE
                    elif element == "transformation_patterns":
                        return ATCGElement.TRANSFORMATION
                    elif element == "connector_patterns":
                        return ATCGElement.CONNECTOR
                    elif element == "event_patterns":
                        return ATCGElement.GENESIS_EVENT
        
        return None
    
    def _lint_class(self, node: ast.ClassDef, file_path: Path, element_type: Optional[ATCGElement]):
        """Lint a class definition for ATCG compliance"""
        class_name = node.name
        
        if element_type == ATCGElement.AGGREGATE:
            self._lint_aggregate_class(node, file_path)
        elif element_type == ATCGElement.TRANSFORMATION:
            self._lint_transformation_class(node, file_path)
        elif element_type == ATCGElement.CONNECTOR:
            self._lint_connector_class(node, file_path)
        elif element_type == ATCGElement.GENESIS_EVENT:
            self._lint_event_class(node, file_path)
        
        # General naming conventions
        if not class_name[0].isupper():
            self.violations.append(LintViolation(
                severity=LintSeverity.WARNING,
                element_type=element_type,
                message=f"Class '{class_name}' should start with uppercase letter",
                file_path=str(file_path),
                line_number=node.lineno,
                suggestion="Use PascalCase for class names",
                sacred_pattern="Beauty and clarity principle"
            ))
    
    def _lint_aggregate_class(self, node: ast.ClassDef, file_path: Path):
        """Lint an Aggregate class for sacred pattern compliance"""
        class_name = node.name
        
        # Aggregates should end with "Aggregate" or be clear domain entities
        if not (class_name.endswith('Aggregate') or class_name.endswith('Entity') or class_name.endswith('Root')):
            self.violations.append(LintViolation(
                severity=LintSeverity.WARNING,
                element_type=ATCGElement.AGGREGATE,
                message=f"Aggregate class '{class_name}' should have clear naming (e.g., UserAggregate)",
                file_path=str(file_path),
                line_number=node.lineno,
                suggestion="Consider naming pattern: [Domain]Aggregate",
                sacred_pattern="A (Aggregate) naming convention"
            ))
        
        # Check for state management methods
        method_names = [method.name for method in node.body if isinstance(method, ast.FunctionDef)]
        
        if 'execute' not in method_names and 'handle' not in [m.split('_')[0] for m in method_names]:
            self.violations.append(LintViolation(
                severity=LintSeverity.ERROR,
                element_type=ATCGElement.AGGREGATE,
                message=f"Aggregate '{class_name}' missing command execution method",
                file_path=str(file_path),
                line_number=node.lineno,
                suggestion="Add execute(command) or handle_* methods",
                sacred_pattern="A (Aggregate) must handle commands"
            ))
        
        if 'apply' not in method_names:
            self.violations.append(LintViolation(
                severity=LintSeverity.WARNING,
                element_type=ATCGElement.AGGREGATE,
                message=f"Aggregate '{class_name}' should have apply(event) method for state changes",
                file_path=str(file_path),
                line_number=node.lineno,
                suggestion="Add apply(event) method for event sourcing",
                sacred_pattern="A (Aggregate) event application"
            ))
    
    def _lint_transformation_class(self, node: ast.ClassDef, file_path: Path):
        """Lint a Transformation class for purity and statelessness"""
        class_name = node.name
        
        # Check for state variables (transformations should be stateless)
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and not target.id.isupper():
                        self.violations.append(LintViolation(
                            severity=LintSeverity.ERROR,
                            element_type=ATCGElement.TRANSFORMATION,
                            message=f"Transformation '{class_name}' has instance state variable '{target.id}'",
                            file_path=str(file_path),
                            line_number=item.lineno,
                            suggestion="Transformations must be stateless - use parameters instead",
                            sacred_pattern="T (Transformation) statelessness"
                        ))
        
        # Check for proper naming
        if not any(suffix in class_name.lower() for suffix in ['service', 'calculator', 'transformer', 'processor']):
            self.violations.append(LintViolation(
                severity=LintSeverity.INFO,
                element_type=ATCGElement.TRANSFORMATION,
                message=f"Transformation '{class_name}' could have clearer naming",
                file_path=str(file_path),
                line_number=node.lineno,
                suggestion="Consider names like: Calculator, Service, Processor",
                sacred_pattern="T (Transformation) naming clarity"
            ))
    
    def _lint_connector_class(self, node: ast.ClassDef, file_path: Path):
        """Lint a Connector class for protocol translation patterns"""
        class_name = node.name
        
        # Connectors should have clear directional naming
        if not any(suffix in class_name.lower() for suffix in ['adapter', 'connector', 'repository', 'controller', 'client', 'gateway']):
            self.violations.append(LintViolation(
                severity=LintSeverity.WARNING,
                element_type=ATCGElement.CONNECTOR,
                message=f"Connector '{class_name}' should have clear adapter naming",
                file_path=str(file_path),
                line_number=node.lineno,
                suggestion="Use patterns like: [Technology]Adapter, [Domain]Repository",
                sacred_pattern="C (Connector) naming convention"
            ))
        
        # Check for translation methods
        method_names = [method.name for method in node.body if isinstance(method, ast.FunctionDef)]
        translation_methods = [m for m in method_names if any(pattern in m.lower() for pattern in ['translate', 'convert', 'map', 'adapt'])]
        
        if not translation_methods and len(method_names) > 2:  # Allow simple connectors
            self.violations.append(LintViolation(
                severity=LintSeverity.INFO,
                element_type=ATCGElement.CONNECTOR,
                message=f"Connector '{class_name}' might benefit from explicit translation methods",
                file_path=str(file_path),
                line_number=node.lineno,
                suggestion="Consider methods like: translate_to_domain(), adapt_from_external()",
                sacred_pattern="C (Connector) protocol translation"
            ))
    
    def _lint_event_class(self, node: ast.ClassDef, file_path: Path):
        """Lint a Genesis Event class for immutability and structure"""
        class_name = node.name
        
        # Events should end with "Event" or use past tense
        if not (class_name.endswith('Event') or class_name.endswith('Happened') or class_name.endswith('Occurred')):
            # Check if it uses past tense
            if not re.search(r'(ed|d)$', class_name.lower()):
                self.violations.append(LintViolation(
                    severity=LintSeverity.WARNING,
                    element_type=ATCGElement.GENESIS_EVENT,
                    message=f"Event '{class_name}' should use past tense or end with 'Event'",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    suggestion="Use patterns like: OrderPlaced, UserRegisteredEvent",
                    sacred_pattern="G (Genesis Event) naming"
                ))
        
        # Check for immutability (should have dataclass or readonly properties)
        has_dataclass_decorator = any(
            isinstance(decorator, ast.Name) and decorator.id == 'dataclass'
            for decorator in node.decorator_list
        )
        
        if not has_dataclass_decorator:
            # Check for setter methods (events should be immutable)
            setter_methods = [
                method.name for method in node.body 
                if isinstance(method, ast.FunctionDef) and method.name.startswith('set_')
            ]
            
            if setter_methods:
                self.violations.append(LintViolation(
                    severity=LintSeverity.ERROR,
                    element_type=ATCGElement.GENESIS_EVENT,
                    message=f"Event '{class_name}' has setter methods - events must be immutable",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    suggestion="Remove setter methods or use @dataclass(frozen=True)",
                    sacred_pattern="G (Genesis Event) immutability"
                ))
    
    def _lint_function(self, node: ast.FunctionDef, file_path: Path, element_type: Optional[ATCGElement]):
        """Lint a function for ATCG compliance"""
        function_name = node.name
        
        # Check Sacred Codon patterns
        for codon_name, codon_info in self.sacred_codons.items():
            if re.search(codon_info["pattern"], function_name):
                self._validate_sacred_codon_implementation(node, file_path, codon_name, codon_info)
    
    def _validate_sacred_codon_implementation(self, node: ast.FunctionDef, file_path: Path, 
                                           codon_name: str, codon_info: Dict[str, str]):
        """Validate that a Sacred Codon is implemented correctly"""
        function_name = node.name
        
        # This is a simplified validation - in a real implementation, 
        # we would analyze the actual call flow to ensure C→A→G patterns
        
        if codon_name == "handle_command":
            # Should return events or have side effects that generate events
            has_return = any(isinstance(stmt, ast.Return) for stmt in ast.walk(node))
            if not has_return:
                self.violations.append(LintViolation(
                    severity=LintSeverity.WARNING,
                    element_type=None,
                    message=f"Command handler '{function_name}' should return events",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    suggestion="Return List[GenesisEvent] from command handlers",
                    sacred_pattern=f"Sacred Codon: {codon_info['expected_flow']}"
                ))
        
        elif codon_name == "query_data":
            # Should be pure and return data
            has_assignments = any(isinstance(stmt, ast.Assign) for stmt in ast.walk(node))
            if has_assignments:
                # Check if assignments are just local variables, not state mutation
                self.violations.append(LintViolation(
                    severity=LintSeverity.INFO,
                    element_type=None,
                    message=f"Query '{function_name}' should avoid state mutations",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    suggestion="Keep queries pure and side-effect free",
                    sacred_pattern=f"Sacred Codon: {codon_info['expected_flow']}"
                ))
    
    def _validate_atcg_constraints(self, atcg_file: ATCGFile, content: str):
        """Validate architectural constraints between ATCG elements"""
        if not atcg_file.element_type:
            return
        
        # Check import dependencies
        forbidden_imports = self._get_forbidden_imports(atcg_file.element_type)
        
        for import_name in atcg_file.imports:
            for forbidden_pattern in forbidden_imports:
                if re.search(forbidden_pattern, import_name, re.IGNORECASE):
                    self.violations.append(LintViolation(
                        severity=LintSeverity.ERROR,
                        element_type=atcg_file.element_type,
                        message=f"{atcg_file.element_type.value} should not import {import_name}",
                        file_path=str(atcg_file.path),
                        line_number=1,
                        suggestion=f"Move {forbidden_pattern} dependencies to Connector layer",
                        sacred_pattern="ATCG dependency rules"
                    ))
    
    def _get_forbidden_imports(self, element_type: ATCGElement) -> List[str]:
        """Get list of forbidden import patterns for each ATCG element"""
        if element_type == ATCGElement.AGGREGATE:
            return [
                r"requests",      # HTTP client
                r"sqlalchemy",    # Database ORM
                r"redis",         # Cache client
                r"kafka",         # Message queue
                r"flask",         # Web framework
                r"fastapi"        # Web framework
            ]
        elif element_type == ATCGElement.TRANSFORMATION:
            return [
                r"flask",         # Web framework
                r"fastapi",       # Web framework
                r"sqlalchemy\.orm"  # ORM sessions
            ]
        
        return []  # Connectors and Events can import infrastructure
    
    def _validate_sacred_codons(self, atcg_file: ATCGFile, content: str):
        """Validate Sacred Codon patterns in the file"""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Look for Sacred Codon violations
            if re.search(r"def\s+\w*command\w*", line) and "handle" not in line.lower():
                self.violations.append(LintViolation(
                    severity=LintSeverity.INFO,
                    element_type=atcg_file.element_type,
                    message="Consider using 'handle_command' pattern for command processing",
                    file_path=str(atcg_file.path),
                    line_number=line_num,
                    suggestion="Rename to handle_[command_name] for Sacred Codon compliance",
                    sacred_pattern="Handle Command Codon (C→A→G)"
                ))
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive linting report"""
        violation_counts = {}
        for severity in LintSeverity:
            violation_counts[severity.value] = len([v for v in self.violations if v.severity == severity])
        
        element_counts = {}
        for element in ATCGElement:
            element_counts[element.value] = len([f for f in self.files_analyzed if f.element_type == element])
        
        # Calculate health scores
        total_violations = len(self.violations)
        total_files = len(self.files_analyzed)
        
        health_score = max(0, 100 - (total_violations * 10 / max(1, total_files)))
        
        sacred_compliance = 100 - (violation_counts.get('error', 0) * 25 + violation_counts.get('critical', 0) * 50)
        sacred_compliance = max(0, sacred_compliance)
        
        return {
            "summary": {
                "files_analyzed": total_files,
                "total_violations": total_violations,
                "health_score": round(health_score, 1),
                "sacred_compliance": round(sacred_compliance, 1)
            },
            "violation_counts": violation_counts,
            "element_distribution": element_counts,
            "violations": [
                {
                    "severity": v.severity.value,
                    "element": v.element_type.value if v.element_type else "unknown",
                    "message": v.message,
                    "file": v.file_path,
                    "line": v.line_number,
                    "suggestion": v.suggestion,
                    "pattern": v.sacred_pattern
                }
                for v in self.violations
            ],
            "files": [
                {
                    "path": str(f.path),
                    "element_type": f.element_type.value if f.element_type else "unclassified",
                    "classes": f.class_names,
                    "functions": f.function_names
                }
                for f in self.files_analyzed
            ]
        }
    
    def print_report(self, report: Dict[str, Any]):
        """Print a beautiful report to console"""
        print("\n" + "="*80)
        print("🧬 ATCG ARCHITECTURAL LINTER REPORT")
        print("="*80)
        
        summary = report["summary"]
        print(f"\n📊 SUMMARY:")
        print(f"  Files Analyzed: {summary['files_analyzed']}")
        print(f"  Total Violations: {summary['total_violations']}")
        print(f"  Health Score: {summary['health_score']}/100")
        print(f"  Sacred Compliance: {summary['sacred_compliance']}/100")
        
        print(f"\n🧪 ELEMENT DISTRIBUTION:")
        for element, count in report["element_distribution"].items():
            print(f"  {element}: {count} files")
        
        print(f"\n⚠️ VIOLATIONS BY SEVERITY:")
        for severity, count in report["violation_counts"].items():
            if count > 0:
                emoji = {"critical": "🚨", "error": "❌", "warning": "⚠️", "info": "💡"}
                print(f"  {emoji.get(severity, '•')} {severity.upper()}: {count}")
        
        if report["violations"]:
            print(f"\n🔍 DETAILED VIOLATIONS:")
            for violation in report["violations"][:10]:  # Show first 10
                print(f"\n  {violation['file']}:{violation['line']}")
                print(f"    {violation['severity'].upper()}: {violation['message']}")
                if violation['suggestion']:
                    print(f"    💡 {violation['suggestion']}")
                if violation['pattern']:
                    print(f"    📜 Pattern: {violation['pattern']}")
            
            if len(report["violations"]) > 10:
                print(f"\n  ... and {len(report['violations']) - 10} more violations")
        
        print("\n" + "="*80)

# CLI Interface
def main():
    """Command-line interface for the ATCG Linter"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ATCG Architectural Linter - Validate Sacred Genetic Patterns")
    parser.add_argument("project_path", help="Path to the project to analyze")
    parser.add_argument("--output", "-o", help="Output report to JSON file")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only show summary")
    
    args = parser.parse_args()
    
    linter = ATCGLinter()
    report = linter.lint_project(args.project_path)
    
    if not args.quiet:
        linter.print_report(report)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 Report saved to: {args.output}")
    
    # Exit with error code if there are critical violations
    critical_violations = report["violation_counts"].get("critical", 0)
    if critical_violations > 0:
        exit(1)

if __name__ == "__main__":
    main()