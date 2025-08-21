#!/usr/bin/env python3
"""
ATCG Architectural Formatter - Auto-format Code to Match Sacred Patterns

The world's first genetic code formatter for software architecture.
Automatically formats code to follow ATCG patterns and Sacred Codons.

Based on the Hive Constitution and the Beekeeper's wisdom.
"""

import ast
import re
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Any, Tuple
from enum import Enum

class FormatRule(Enum):
    """Types of formatting rules applied"""
    IMPORT_ORDER = "import_order"           # ATCG-based import ordering
    CLASS_NAMING = "class_naming"          # Sacred naming conventions
    METHOD_NAMING = "method_naming"        # Sacred Codon patterns
    DOCSTRING = "docstring"               # ATCG documentation
    SPACING = "spacing"                   # Sacred geometry spacing
    STRUCTURE = "structure"               # File structure patterns

@dataclass
class FormatChange:
    """A formatting change applied to the code"""
    rule: FormatRule
    line_number: int
    old_content: str
    new_content: str
    reason: str
    sacred_pattern: str

class ATCGFormatter:
    """
    The ATCG Architectural Formatter - auto-formats code for sacred patterns.
    
    This formatter applies the genetic code principles:
    - Organizes imports in ATCG order (A, T, C, G)
    - Formats class and method names to follow Sacred patterns
    - Adds ATCG documentation templates
    - Applies sacred geometry spacing
    - Restructures files according to Hive architecture
    """
    
    def __init__(self):
        self.changes_applied: List[FormatChange] = []
        
        # Sacred import order: A -> T -> C -> G -> External
        self.import_order = {
            'aggregates': 0,    # A - Domain aggregates first
            'transforms': 1,    # T - Transformations second
            'connectors': 2,    # C - Connectors third
            'events': 3,        # G - Genesis events fourth
            'external': 4       # External libraries last
        }
        
        # Sacred naming patterns
        self.naming_patterns = {
            'aggregate_suffixes': ['Aggregate', 'Entity', 'Root'],
            'transformation_suffixes': ['Service', 'Calculator', 'Processor', 'Transformer'],
            'connector_suffixes': ['Adapter', 'Connector', 'Repository', 'Controller', 'Gateway'],
            'event_suffixes': ['Event', 'Happened', 'Occurred']
        }
        
        # Sacred Codon method patterns
        self.codon_patterns = {
            'handle_command': r'^(handle|execute)_\w*command',
            'query_data': r'^(query|get|find|retrieve)_\w+',
            'react_to_event': r'^(on|handle)_\w*event',
            'immune_response': r'^(handle|respond_to)_\w*mutation'
        }
        
        # Documentation templates
        self.docstring_templates = {
            'aggregate': '''"""
    {class_name} Aggregate - Core domain entity
    
    Responsibilities:
    - Enforce business invariants
    - Handle domain commands
    - Generate domain events
    - Maintain consistency within aggregate boundary
    
    Sacred Pattern: A (Aggregate) - The vital organ of the domain
    """''',
            'transformation': '''"""
    {class_name} Transformation - Pure business logic
    
    Responsibilities:
    - Process domain data without side effects
    - Perform calculations and transformations
    - Coordinate between aggregates
    - Maintain statelessness
    
    Sacred Pattern: T (Transformation) - The magical enzyme
    """''',
            'connector': '''"""
    {class_name} Connector - Protocol translation bridge
    
    Responsibilities:
    - Translate between domain and external protocols
    - Adapt external services to domain interfaces
    - Handle external communication concerns
    - Isolate domain from infrastructure details
    
    Sacred Pattern: C (Connector) - The senses of the hive
    """''',
            'event': '''"""
    {class_name} Genesis Event - Domain occurrence record
    
    Responsibilities:
    - Capture significant domain events
    - Provide immutable event history
    - Enable event-driven communication
    - Support event sourcing patterns
    
    Sacred Pattern: G (Genesis Event) - The waggle dance
    """'''
        }
    
    def format_project(self, project_path: str, dry_run: bool = False) -> Dict[str, Any]:
        """
        Format an entire project for ATCG compliance.
        
        Args:
            project_path: Path to the project root
            dry_run: If True, show changes without applying them
            
        Returns:
            Comprehensive formatting report
        """
        project_root = Path(project_path)
        print(f"🎨 ATCG Formatter analyzing project: {project_root}")
        
        # Reset state
        self.changes_applied = []
        
        # Find all Python files
        python_files = list(project_root.rglob("*.py"))
        
        for file_path in python_files:
            try:
                self._format_file(file_path, dry_run)
            except Exception as e:
                print(f"❌ Failed to format {file_path}: {e}")
        
        return self._generate_report()
    
    def _format_file(self, file_path: Path, dry_run: bool = False):
        """Format a single Python file for ATCG compliance"""
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Parse the AST
        try:
            tree = ast.parse(original_content, filename=str(file_path))
        except SyntaxError as e:
            print(f"⚠️ Syntax error in {file_path}, skipping: {e}")
            return
        
        # Apply formatting rules
        formatted_content = original_content
        
        # 1. Format imports in ATCG order
        formatted_content = self._format_imports(formatted_content, file_path)
        
        # 2. Format class names and add docstrings
        formatted_content = self._format_classes(formatted_content, tree, file_path)
        
        # 3. Format method names for Sacred Codon patterns
        formatted_content = self._format_methods(formatted_content, tree, file_path)
        
        # 4. Apply sacred geometry spacing
        formatted_content = self._apply_sacred_spacing(formatted_content, file_path)
        
        # 5. Add file-level documentation
        formatted_content = self._add_file_header(formatted_content, file_path)
        
        # Apply changes if not dry run
        if not dry_run and formatted_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            print(f"✅ Formatted: {file_path}")
        elif dry_run and formatted_content != original_content:
            print(f"🔍 Would format: {file_path}")
    
    def _format_imports(self, content: str, file_path: Path) -> str:
        """Format imports in ATCG order"""
        lines = content.split('\n')
        import_lines = []
        non_import_lines = []
        import_section_ended = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check if this is an import line
            if stripped.startswith('import ') or stripped.startswith('from '):
                if not import_section_ended:
                    import_lines.append((i, line, self._classify_import(stripped)))
                else:
                    # Import after code - leave as is for now
                    non_import_lines.append(line)
            else:
                if stripped and not stripped.startswith('#') and not stripped.startswith('"""'):
                    import_section_ended = True
                non_import_lines.append(line)
        
        if import_lines:
            # Sort imports by ATCG order
            sorted_imports = sorted(import_lines, key=lambda x: (x[2], x[1]))
            
            # Group imports by category
            grouped_imports = self._group_imports_by_category(sorted_imports)
            
            # Build new import section
            new_import_lines = []
            for category, imports in grouped_imports.items():
                if imports:
                    new_import_lines.extend([imp[1] for imp in imports])
                    new_import_lines.append('')  # Add spacing between groups
            
            # Remove trailing empty line
            if new_import_lines and new_import_lines[-1] == '':
                new_import_lines.pop()
            
            # Record change
            if new_import_lines != [line[1] for line in import_lines]:
                self.changes_applied.append(FormatChange(
                    rule=FormatRule.IMPORT_ORDER,
                    line_number=import_lines[0][0] if import_lines else 1,
                    old_content="imports in original order",
                    new_content="imports in ATCG order",
                    reason="Organize imports following A→T→C→G→External pattern",
                    sacred_pattern="ATCG import hierarchy"
                ))
            
            # Rebuild content
            first_non_import = next((i for i, line in enumerate(lines) if line.strip() and not (line.strip().startswith('import ') or line.strip().startswith('from '))), len(lines))
            
            return '\n'.join(new_import_lines + [''] + lines[first_non_import:])
        
        return content
    
    def _classify_import(self, import_line: str) -> int:
        """Classify an import into ATCG categories"""
        import_line_lower = import_line.lower()
        
        # A - Aggregates, entities, domain
        if any(word in import_line_lower for word in ['aggregate', 'entity', 'domain', 'model']):
            return self.import_order['aggregates']
        
        # T - Transformations, services, processors
        elif any(word in import_line_lower for word in ['service', 'transform', 'process', 'calculat']):
            return self.import_order['transforms']
        
        # C - Connectors, adapters, repositories
        elif any(word in import_line_lower for word in ['adapter', 'connector', 'repository', 'controller', 'client']):
            return self.import_order['connectors']
        
        # G - Genesis events, events
        elif any(word in import_line_lower for word in ['event', 'genesis', 'message']):
            return self.import_order['events']
        
        # External libraries
        else:
            return self.import_order['external']
    
    def _group_imports_by_category(self, sorted_imports: List[Tuple[int, str, int]]) -> Dict[str, List[Tuple[int, str, int]]]:
        """Group imports by ATCG category"""
        groups = {
            'aggregates': [],
            'transforms': [],
            'connectors': [],
            'events': [],
            'external': []
        }
        
        for import_data in sorted_imports:
            category_order = import_data[2]
            
            if category_order == self.import_order['aggregates']:
                groups['aggregates'].append(import_data)
            elif category_order == self.import_order['transforms']:
                groups['transforms'].append(import_data)
            elif category_order == self.import_order['connectors']:
                groups['connectors'].append(import_data)
            elif category_order == self.import_order['events']:
                groups['events'].append(import_data)
            else:
                groups['external'].append(import_data)
        
        return groups
    
    def _format_classes(self, content: str, tree: ast.AST, file_path: Path) -> str:
        """Format class names and add sacred docstrings"""
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                
                # Determine ATCG element type
                element_type = self._classify_class(class_name)
                
                # Check if class needs renaming
                suggested_name = self._suggest_class_name(class_name, element_type)
                
                if suggested_name != class_name:
                    # Update class name in content
                    class_line = lines[node.lineno - 1]
                    new_class_line = re.sub(
                        rf'\bclass\s+{re.escape(class_name)}\b',
                        f'class {suggested_name}',
                        class_line
                    )
                    lines[node.lineno - 1] = new_class_line
                    
                    self.changes_applied.append(FormatChange(
                        rule=FormatRule.CLASS_NAMING,
                        line_number=node.lineno,
                        old_content=f"class {class_name}",
                        new_content=f"class {suggested_name}",
                        reason=f"Apply sacred naming for {element_type} pattern",
                        sacred_pattern=f"{element_type} naming convention"
                    ))
                    
                    class_name = suggested_name  # Use new name for docstring
                
                # Add or update docstring
                if element_type and self._needs_docstring(node):
                    docstring = self._generate_class_docstring(class_name, element_type)
                    
                    # Insert docstring after class definition
                    insert_line = node.lineno  # Line after class definition
                    
                    # Check if there's already a docstring
                    existing_docstring_line = None
                    if (len(lines) > insert_line and 
                        lines[insert_line].strip().startswith('"""')):
                        existing_docstring_line = insert_line
                        
                        # Find end of existing docstring
                        end_line = insert_line
                        for j in range(insert_line + 1, len(lines)):
                            if '"""' in lines[j]:
                                end_line = j
                                break
                        
                        # Replace existing docstring
                        lines[insert_line:end_line + 1] = [docstring]
                    else:
                        # Insert new docstring
                        lines.insert(insert_line, docstring)
                    
                    self.changes_applied.append(FormatChange(
                        rule=FormatRule.DOCSTRING,
                        line_number=node.lineno + 1,
                        old_content="missing or inadequate docstring",
                        new_content="sacred ATCG docstring",
                        reason=f"Add sacred documentation for {element_type}",
                        sacred_pattern=f"{element_type} documentation template"
                    ))
        
        return '\n'.join(lines)
    
    def _classify_class(self, class_name: str) -> Optional[str]:
        """Classify a class as an ATCG element type"""
        class_name_lower = class_name.lower()
        
        # Check for explicit ATCG patterns
        if any(suffix.lower() in class_name_lower for suffix in self.naming_patterns['aggregate_suffixes']):
            return 'aggregate'
        elif any(suffix.lower() in class_name_lower for suffix in self.naming_patterns['transformation_suffixes']):
            return 'transformation'
        elif any(suffix.lower() in class_name_lower for suffix in self.naming_patterns['connector_suffixes']):
            return 'connector'
        elif any(suffix.lower() in class_name_lower for suffix in self.naming_patterns['event_suffixes']):
            return 'event'
        
        return None
    
    def _suggest_class_name(self, class_name: str, element_type: Optional[str]) -> str:
        """Suggest a better class name following sacred patterns"""
        if not element_type:
            return class_name
        
        # Check if name already follows pattern
        class_name_lower = class_name.lower()
        
        if element_type == 'aggregate':
            if not any(suffix.lower() in class_name_lower for suffix in self.naming_patterns['aggregate_suffixes']):
                return f"{class_name}Aggregate"
        elif element_type == 'transformation':
            if not any(suffix.lower() in class_name_lower for suffix in self.naming_patterns['transformation_suffixes']):
                # Suggest based on common patterns
                if 'calculat' in class_name_lower:
                    return f"{class_name}Calculator" if not class_name.endswith('Calculator') else class_name
                else:
                    return f"{class_name}Service"
        elif element_type == 'connector':
            if not any(suffix.lower() in class_name_lower for suffix in self.naming_patterns['connector_suffixes']):
                if 'repo' in class_name_lower:
                    return f"{class_name}Repository" if not class_name.endswith('Repository') else class_name
                else:
                    return f"{class_name}Adapter"
        elif element_type == 'event':
            if not any(suffix.lower() in class_name_lower for suffix in self.naming_patterns['event_suffixes']):
                return f"{class_name}Event"
        
        return class_name
    
    def _needs_docstring(self, node: ast.ClassDef) -> bool:
        """Check if a class needs a docstring"""
        # Check if first statement is a docstring
        if (node.body and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Str)):
            docstring = node.body[0].value.s
            # Check if it's a sacred docstring (contains "Sacred Pattern")
            return "Sacred Pattern" not in docstring
        return True
    
    def _generate_class_docstring(self, class_name: str, element_type: str) -> str:
        """Generate a sacred docstring for a class"""
        template = self.docstring_templates.get(element_type, "")
        return template.format(class_name=class_name).strip()
    
    def _format_methods(self, content: str, tree: ast.AST, file_path: Path) -> str:
        """Format method names for Sacred Codon patterns"""
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                method_name = node.name
                
                # Skip private methods and special methods
                if method_name.startswith('_'):
                    continue
                
                # Check for Sacred Codon patterns and suggest improvements
                suggested_name = self._suggest_method_name(method_name)
                
                if suggested_name != method_name:
                    # Update method name in content
                    method_line = lines[node.lineno - 1]
                    new_method_line = re.sub(
                        rf'\bdef\s+{re.escape(method_name)}\b',
                        f'def {suggested_name}',
                        method_line
                    )
                    lines[node.lineno - 1] = new_method_line
                    
                    self.changes_applied.append(FormatChange(
                        rule=FormatRule.METHOD_NAMING,
                        line_number=node.lineno,
                        old_content=f"def {method_name}",
                        new_content=f"def {suggested_name}",
                        reason="Apply Sacred Codon naming pattern",
                        sacred_pattern="Sacred Codon method naming"
                    ))
        
        return '\n'.join(lines)
    
    def _suggest_method_name(self, method_name: str) -> str:
        """Suggest a better method name following Sacred Codon patterns"""
        method_lower = method_name.lower()
        
        # Handle command pattern
        if 'command' in method_lower and not method_lower.startswith('handle_'):
            return f"handle_{method_name}" if not method_name.startswith('handle_') else method_name
        
        # Query pattern
        if any(word in method_lower for word in ['get', 'find', 'retrieve']) and not method_lower.startswith('query_'):
            if method_lower.startswith('get_'):
                return method_name.replace('get_', 'query_', 1)
            elif method_lower.startswith('find_'):
                return method_name.replace('find_', 'query_', 1)
        
        # Event handling pattern
        if 'event' in method_lower and not (method_lower.startswith('on_') or method_lower.startswith('handle_')):
            return f"on_{method_name}" if not method_name.startswith('on_') else method_name
        
        return method_name
    
    def _apply_sacred_spacing(self, content: str, file_path: Path) -> str:
        """Apply sacred geometry spacing (golden ratio inspired)"""
        lines = content.split('\n')
        new_lines = []
        
        in_class = False
        class_method_count = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Track class context
            if stripped.startswith('class '):
                in_class = True
                class_method_count = 0
                # Ensure spacing before class
                if i > 0 and lines[i-1].strip() and not lines[i-1].strip().startswith('#'):
                    new_lines.append('')
                    new_lines.append('')
            elif stripped.startswith('def ') and in_class:
                class_method_count += 1
                # Add spacing between methods (golden ratio: every 3rd method gets extra space)
                if class_method_count % 3 == 0 and i > 0 and lines[i-1].strip():
                    new_lines.append('')
            elif stripped and not stripped.startswith(' ') and not stripped.startswith('\t'):
                in_class = False
            
            new_lines.append(line)
        
        # Record spacing changes
        if len(new_lines) != len(lines):
            self.changes_applied.append(FormatChange(
                rule=FormatRule.SPACING,
                line_number=1,
                old_content="original spacing",
                new_content="sacred geometry spacing",
                reason="Apply golden ratio spacing patterns",
                sacred_pattern="Sacred geometry and aesthetic balance"
            ))
        
        return '\n'.join(new_lines)
    
    def _add_file_header(self, content: str, file_path: Path) -> str:
        """Add file-level ATCG documentation header"""
        lines = content.split('\n')
        
        # Check if file already has proper header
        has_atcg_header = any("ATCG" in line or "Sacred" in line for line in lines[:10])
        
        if not has_atcg_header and not str(file_path).endswith('__init__.py'):
            # Determine file type
            file_element_type = self._classify_file_by_content(content)
            
            if file_element_type:
                header = self._generate_file_header(file_path, file_element_type)
                
                # Find insertion point (after shebang and encoding if present)
                insert_index = 0
                for i, line in enumerate(lines):
                    if line.startswith('#!') or 'coding:' in line or 'encoding:' in line:
                        insert_index = i + 1
                    else:
                        break
                
                # Insert header
                lines.insert(insert_index, header)
                lines.insert(insert_index + 1, '')
                
                self.changes_applied.append(FormatChange(
                    rule=FormatRule.STRUCTURE,
                    line_number=insert_index + 1,
                    old_content="missing file header",
                    new_content="ATCG file header",
                    reason=f"Add sacred documentation for {file_element_type} file",
                    sacred_pattern="ATCG file documentation"
                ))
        
        return '\n'.join(lines)
    
    def _classify_file_by_content(self, content: str) -> Optional[str]:
        """Classify file by its content"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['aggregate', 'entity', 'class.*aggregate']):
            return 'aggregate'
        elif any(word in content_lower for word in ['service', 'transform', 'calculat', 'process']):
            return 'transformation'
        elif any(word in content_lower for word in ['adapter', 'connector', 'repository', 'controller']):
            return 'connector'
        elif any(word in content_lower for word in ['event', 'genesis', 'happened', 'occurred']):
            return 'event'
        
        return None
    
    def _generate_file_header(self, file_path: Path, element_type: str) -> str:
        """Generate a sacred file header"""
        element_descriptions = {
            'aggregate': "Domain Aggregates - The vital organs of business logic",
            'transformation': "Transformations - Pure business logic processors",
            'connector': "Connectors - Protocol translation bridges",
            'event': "Genesis Events - Domain occurrence records"
        }
        
        element_symbols = {
            'aggregate': 'A',
            'transformation': 'T', 
            'connector': 'C',
            'event': 'G'
        }
        
        description = element_descriptions.get(element_type, "Sacred ATCG component")
        symbol = element_symbols.get(element_type, '?')
        
        return f'''"""
{file_path.name} - {description}

Sacred Element: {symbol} ({element_type.title()})
Part of the Hive Molecular Architecture System
Following the Beekeeper's wisdom and ATCG genetic patterns
"""'''
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive formatting report"""
        rule_counts = {}
        for rule in FormatRule:
            rule_counts[rule.value] = len([c for c in self.changes_applied if c.rule == rule])
        
        total_changes = len(self.changes_applied)
        
        return {
            "summary": {
                "total_changes": total_changes,
                "files_modified": len(set(c.old_content for c in self.changes_applied)),
                "most_common_rule": max(rule_counts.items(), key=lambda x: x[1])[0] if rule_counts else None
            },
            "rule_counts": rule_counts,
            "changes": [
                {
                    "rule": c.rule.value,
                    "line": c.line_number,
                    "old": c.old_content,
                    "new": c.new_content,
                    "reason": c.reason,
                    "pattern": c.sacred_pattern
                }
                for c in self.changes_applied
            ]
        }
    
    def print_report(self, report: Dict[str, Any]):
        """Print a beautiful formatting report"""
        print("\n" + "="*80)
        print("🎨 ATCG ARCHITECTURAL FORMATTER REPORT")
        print("="*80)
        
        summary = report["summary"]
        print(f"\n📊 SUMMARY:")
        print(f"  Total Changes Applied: {summary['total_changes']}")
        print(f"  Files Modified: {summary.get('files_modified', 0)}")
        if summary.get('most_common_rule'):
            print(f"  Most Common Rule: {summary['most_common_rule']}")
        
        print(f"\n🎯 CHANGES BY RULE:")
        for rule, count in report["rule_counts"].items():
            if count > 0:
                emoji = {
                    "import_order": "📚",
                    "class_naming": "🏷️",
                    "method_naming": "⚡",
                    "docstring": "📝",
                    "spacing": "📐",
                    "structure": "🏗️"
                }
                print(f"  {emoji.get(rule, '•')} {rule.replace('_', ' ').title()}: {count}")
        
        if report["changes"]:
            print(f"\n🔧 SAMPLE CHANGES:")
            for i, change in enumerate(report["changes"][:5]):  # Show first 5
                print(f"\n  {i+1}. {change['rule'].replace('_', ' ').title()} (Line {change['line']})")
                print(f"     Old: {change['old']}")
                print(f"     New: {change['new']}")
                print(f"     📜 {change['pattern']}")
            
            if len(report["changes"]) > 5:
                print(f"\n  ... and {len(report['changes']) - 5} more changes")
        
        print("\n✨ Your code now follows the sacred ATCG patterns!")
        print("="*80)

# CLI Interface
def main():
    """Command-line interface for the ATCG Formatter"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ATCG Architectural Formatter - Auto-format to Sacred Patterns")
    parser.add_argument("project_path", help="Path to the project to format")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Show changes without applying them")
    parser.add_argument("--output", "-o", help="Output report to JSON file")
    
    args = parser.parse_args()
    
    formatter = ATCGFormatter()
    report = formatter.format_project(args.project_path, dry_run=args.dry_run)
    
    formatter.print_report(report)
    
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 Report saved to: {args.output}")

if __name__ == "__main__":
    main()