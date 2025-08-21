#!/usr/bin/env python3
"""
The Chemical Registry Connector - Database of Molecular Components
Catalogs, searches, and manages all known molecular components in the Hive.

This connector maintains a comprehensive registry of stable component "compounds",
their properties, reactions, and evolutionary history.
"""

import json
import sqlite3
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime, timezone
from enum import Enum

class ComponentStability(Enum):
    """Stability classifications for components"""
    EXPERIMENTAL = "experimental"     # Newly created, untested
    STABLE = "stable"                # Proven in production  
    DEPRECATED = "deprecated"        # Being phased out
    RADIOACTIVE = "radioactive"      # Known to cause issues
    AROMATIC = "aromatic"           # Extra stable, widely used

@dataclass
class MolecularComponent:
    """A registered molecular component with full metadata"""
    name: str
    molecular_formula: str
    element_composition: Dict[str, int]
    stability: ComponentStability
    bond_energy: float
    creation_date: datetime
    created_by: str
    version: str = "1.0"
    description: str = ""
    properties: Dict[str, any] = field(default_factory=dict)
    similar_components: List[str] = field(default_factory=list)
    usage_count: int = 0
    last_used: Optional[datetime] = None
    isotopes: List[str] = field(default_factory=list)  # Version variants
    reaction_products: List[str] = field(default_factory=list)  # What reactions create this
    decomposition_products: List[str] = field(default_factory=list)  # What this breaks down into
    
    def __post_init__(self):
        if isinstance(self.creation_date, str):
            self.creation_date = datetime.fromisoformat(self.creation_date)
        if isinstance(self.last_used, str):
            self.last_used = datetime.fromisoformat(self.last_used)
        if isinstance(self.stability, str):
            self.stability = ComponentStability(self.stability)

@dataclass
class SearchQuery:
    """Query parameters for searching the chemical registry"""
    name_pattern: Optional[str] = None
    molecular_formula: Optional[str] = None
    elements: Optional[List[str]] = None
    stability: Optional[ComponentStability] = None
    min_bond_energy: Optional[float] = None
    max_bond_energy: Optional[float] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    properties: Optional[Dict[str, any]] = None

class ChemicalRegistry:
    """
    The Chemical Registry - A comprehensive database of molecular components.
    
    Features:
    - Component cataloging with full metadata
    - Search by properties, formula, or structure  
    - Version control (isotopes) for components
    - Usage analytics and popularity tracking
    - Similarity detection and clustering
    - Evolution history tracking
    """
    
    def __init__(self, db_path: str = "chemical_registry.db"):
        self.db_path = db_path
        self._init_database()
        print(f"🧪 Chemical Registry initialized at {db_path}")
    
    def _init_database(self):
        """Initialize the SQLite database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS components (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    molecular_formula TEXT NOT NULL,
                    element_composition TEXT NOT NULL,  -- JSON
                    stability TEXT NOT NULL,
                    bond_energy REAL NOT NULL,
                    creation_date TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    version TEXT NOT NULL,
                    description TEXT,
                    properties TEXT,  -- JSON
                    similar_components TEXT,  -- JSON array
                    usage_count INTEGER DEFAULT 0,
                    last_used TEXT,
                    isotopes TEXT,  -- JSON array
                    reaction_products TEXT,  -- JSON array
                    decomposition_products TEXT  -- JSON array
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS reactions (
                    id TEXT PRIMARY KEY,
                    reactants TEXT NOT NULL,  -- JSON array
                    products TEXT NOT NULL,   -- JSON array
                    catalysts TEXT,           -- JSON array
                    energy_change REAL,
                    success_rate REAL,
                    first_discovered TEXT,
                    discovery_count INTEGER DEFAULT 1
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS usage_history (
                    component_id TEXT,
                    used_date TEXT,
                    context TEXT,
                    performance_score REAL,
                    FOREIGN KEY (component_id) REFERENCES components (id)
                )
            ''')
            
            # Create indexes for faster searches
            conn.execute('CREATE INDEX IF NOT EXISTS idx_formula ON components (molecular_formula)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_stability ON components (stability)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_elements ON components (element_composition)')
            
            conn.commit()
    
    def register_component(self, component: MolecularComponent) -> str:
        """Register a new molecular component in the registry"""
        
        # Generate unique ID based on name and formula
        component_id = self._generate_component_id(component.name, component.molecular_formula)
        
        with sqlite3.connect(self.db_path) as conn:
            # Check if component already exists
            existing = conn.execute(
                'SELECT id FROM components WHERE id = ?', (component_id,)
            ).fetchone()
            
            if existing:
                # Update existing component (create new isotope)
                self._create_isotope(component_id, component)
                print(f"🔬 Created new isotope for existing component: {component.name}")
                return component_id
            
            # Insert new component
            conn.execute('''
                INSERT INTO components (
                    id, name, molecular_formula, element_composition, stability,
                    bond_energy, creation_date, created_by, version, description,
                    properties, similar_components, usage_count, last_used,
                    isotopes, reaction_products, decomposition_products
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                component_id,
                component.name,
                component.molecular_formula,
                json.dumps(component.element_composition),
                component.stability.value,
                component.bond_energy,
                component.creation_date.isoformat(),
                component.created_by,
                component.version,
                component.description,
                json.dumps(component.properties),
                json.dumps(component.similar_components),
                component.usage_count,
                component.last_used.isoformat() if component.last_used else None,
                json.dumps(component.isotopes),
                json.dumps(component.reaction_products),
                json.dumps(component.decomposition_products)
            ))
            
            conn.commit()
        
        print(f"✅ Registered new component: {component.name} ({component.molecular_formula})")
        return component_id
    
    def search_components(self, query: SearchQuery) -> List[MolecularComponent]:
        """Search for components matching the given criteria"""
        
        where_clauses = []
        params = []
        
        if query.name_pattern:
            where_clauses.append('name LIKE ?')
            params.append(f'%{query.name_pattern}%')
        
        if query.molecular_formula:
            where_clauses.append('molecular_formula = ?')
            params.append(query.molecular_formula)
        
        if query.stability:
            where_clauses.append('stability = ?')
            params.append(query.stability.value)
        
        if query.min_bond_energy:
            where_clauses.append('bond_energy >= ?')
            params.append(query.min_bond_energy)
        
        if query.max_bond_energy:
            where_clauses.append('bond_energy <= ?')
            params.append(query.max_bond_energy)
        
        if query.created_after:
            where_clauses.append('creation_date >= ?')
            params.append(query.created_after.isoformat())
        
        if query.created_before:
            where_clauses.append('creation_date <= ?')
            params.append(query.created_before.isoformat())
        
        # Build SQL query
        sql = 'SELECT * FROM components'
        if where_clauses:
            sql += ' WHERE ' + ' AND '.join(where_clauses)
        sql += ' ORDER BY usage_count DESC'
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql, params).fetchall()
        
        components = []
        for row in rows:
            component = self._row_to_component(row)
            
            # Additional filtering for elements and properties
            if query.elements:
                if not all(element in component.element_composition for element in query.elements):
                    continue
            
            if query.properties:
                if not all(component.properties.get(k) == v for k, v in query.properties.items()):
                    continue
            
            components.append(component)
        
        print(f"🔍 Search found {len(components)} components")
        return components
    
    def get_component(self, component_id: str) -> Optional[MolecularComponent]:
        """Get a specific component by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute('SELECT * FROM components WHERE id = ?', (component_id,)).fetchone()
        
        return self._row_to_component(row) if row else None
    
    def find_similar_components(self, component_id: str, similarity_threshold: float = 0.8) -> List[Tuple[MolecularComponent, float]]:
        """Find components similar to the given component"""
        base_component = self.get_component(component_id)
        if not base_component:
            return []
        
        all_components = self.search_components(SearchQuery())
        similar = []
        
        for comp in all_components:
            if comp.name == base_component.name:
                continue
            
            similarity = self._calculate_similarity(base_component, comp)
            if similarity >= similarity_threshold:
                similar.append((comp, similarity))
        
        # Sort by similarity (highest first)
        similar.sort(key=lambda x: x[1], reverse=True)
        
        return similar
    
    def record_usage(self, component_id: str, context: str = "", performance_score: float = 1.0):
        """Record usage of a component for analytics"""
        with sqlite3.connect(self.db_path) as conn:
            # Update usage count and last used
            conn.execute('''
                UPDATE components 
                SET usage_count = usage_count + 1, last_used = ?
                WHERE id = ?
            ''', (datetime.now(timezone.utc).isoformat(), component_id))
            
            # Record detailed usage history
            conn.execute('''
                INSERT INTO usage_history (component_id, used_date, context, performance_score)
                VALUES (?, ?, ?, ?)
            ''', (component_id, datetime.now(timezone.utc).isoformat(), context, performance_score))
            
            conn.commit()
    
    def get_popularity_rankings(self, limit: int = 10) -> List[Tuple[MolecularComponent, int]]:
        """Get the most popular components by usage count"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                'SELECT * FROM components ORDER BY usage_count DESC LIMIT ?', 
                (limit,)
            ).fetchall()
        
        return [(self._row_to_component(row), row['usage_count']) for row in rows]
    
    def analyze_composition_trends(self) -> Dict[str, Dict[str, int]]:
        """Analyze trends in element composition across all components"""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute('SELECT element_composition, stability FROM components').fetchall()
        
        trends = {
            'total_elements': {'A': 0, 'T': 0, 'C': 0, 'G': 0},
            'by_stability': {}
        }
        
        for row in rows:
            composition = json.loads(row[0])
            stability = row[1]
            
            # Count total elements
            for element, count in composition.items():
                if element in trends['total_elements']:
                    trends['total_elements'][element] += count
            
            # Count by stability
            if stability not in trends['by_stability']:
                trends['by_stability'][stability] = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
            
            for element, count in composition.items():
                if element in trends['by_stability'][stability]:
                    trends['by_stability'][stability][element] += count
        
        return trends
    
    def export_registry(self, file_path: str, format: str = "json") -> bool:
        """Export the entire registry to a file"""
        try:
            all_components = self.search_components(SearchQuery())
            
            if format.lower() == "json":
                data = {
                    'export_date': datetime.now(timezone.utc).isoformat(),
                    'total_components': len(all_components),
                    'components': [asdict(comp) for comp in all_components]
                }
                
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
            
            elif format.lower() == "csv":
                import csv
                with open(file_path, 'w', newline='') as f:
                    if all_components:
                        writer = csv.DictWriter(f, fieldnames=asdict(all_components[0]).keys())
                        writer.writeheader()
                        for comp in all_components:
                            writer.writerow(asdict(comp))
            
            print(f"📁 Registry exported to {file_path} ({len(all_components)} components)")
            return True
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def _generate_component_id(self, name: str, formula: str) -> str:
        """Generate a unique ID for a component"""
        data = f"{name}:{formula}".encode('utf-8')
        return hashlib.md5(data).hexdigest()[:12]
    
    def _create_isotope(self, component_id: str, new_component: MolecularComponent):
        """Create a new isotope (version) of an existing component"""
        with sqlite3.connect(self.db_path) as conn:
            # Get existing isotopes
            existing_isotopes = conn.execute(
                'SELECT isotopes FROM components WHERE id = ?', (component_id,)
            ).fetchone()[0]
            
            isotopes = json.loads(existing_isotopes) if existing_isotopes else []
            isotopes.append(new_component.version)
            
            # Update the isotopes list
            conn.execute(
                'UPDATE components SET isotopes = ? WHERE id = ?',
                (json.dumps(isotopes), component_id)
            )
            
            conn.commit()
    
    def _row_to_component(self, row: sqlite3.Row) -> MolecularComponent:
        """Convert a database row to a MolecularComponent object"""
        return MolecularComponent(
            name=row['name'],
            molecular_formula=row['molecular_formula'],
            element_composition=json.loads(row['element_composition']),
            stability=ComponentStability(row['stability']),
            bond_energy=row['bond_energy'],
            creation_date=datetime.fromisoformat(row['creation_date']),
            created_by=row['created_by'],
            version=row['version'],
            description=row['description'] or "",
            properties=json.loads(row['properties']) if row['properties'] else {},
            similar_components=json.loads(row['similar_components']) if row['similar_components'] else [],
            usage_count=row['usage_count'],
            last_used=datetime.fromisoformat(row['last_used']) if row['last_used'] else None,
            isotopes=json.loads(row['isotopes']) if row['isotopes'] else [],
            reaction_products=json.loads(row['reaction_products']) if row['reaction_products'] else [],
            decomposition_products=json.loads(row['decomposition_products']) if row['decomposition_products'] else []
        )
    
    def _calculate_similarity(self, comp1: MolecularComponent, comp2: MolecularComponent) -> float:
        """Calculate similarity between two components (0-1 scale)"""
        # Element composition similarity
        elements1 = set(comp1.element_composition.keys())
        elements2 = set(comp2.element_composition.keys())
        common_elements = elements1.intersection(elements2)
        
        if not common_elements:
            return 0.0
        
        element_similarity = len(common_elements) / len(elements1.union(elements2))
        
        # Bond energy similarity (normalized)
        energy_diff = abs(comp1.bond_energy - comp2.bond_energy)
        energy_similarity = max(0, 1 - energy_diff / 500.0)  # Assuming max diff of 500
        
        # Stability similarity
        stability_similarity = 1.0 if comp1.stability == comp2.stability else 0.5
        
        # Weighted average
        total_similarity = (
            element_similarity * 0.5 +
            energy_similarity * 0.3 +
            stability_similarity * 0.2
        )
        
        return total_similarity

# Example usage and testing
if __name__ == "__main__":
    registry = ChemicalRegistry()
    
    # Register some example components
    hex_core = MolecularComponent(
        name="HexagonalCore",
        molecular_formula="A1C6",
        element_composition={'A': 1, 'C': 6},
        stability=ComponentStability.AROMATIC,
        bond_energy=350.0,
        creation_date=datetime.now(timezone.utc),
        created_by="genesis_engine",
        description="Stable hexagonal architecture core like benzene"
    )
    
    command_handler = MolecularComponent(
        name="CommandHandler",
        molecular_formula="C1A1G1",
        element_composition={'C': 1, 'A': 1, 'G': 1},
        stability=ComponentStability.STABLE,
        bond_energy=185.0,
        creation_date=datetime.now(timezone.utc),
        created_by="template_engine",
        description="Command handling pattern implementation"
    )
    
    # Register components
    hex_id = registry.register_component(hex_core)
    cmd_id = registry.register_component(command_handler)
    
    # Test search
    search_results = registry.search_components(SearchQuery(
        stability=ComponentStability.STABLE,
        min_bond_energy=100.0
    ))
    
    print(f"\n🔍 Search results: {len(search_results)} components found")
    for comp in search_results:
        print(f"  - {comp.name}: {comp.molecular_formula} ({comp.stability.value})")
    
    # Test similarity
    similar = registry.find_similar_components(hex_id)
    print(f"\n🎯 Similar to HexagonalCore: {len(similar)} components")
    
    # Record some usage
    registry.record_usage(hex_id, "production deployment", 0.95)
    registry.record_usage(cmd_id, "user service", 0.88)
    
    # Get popularity rankings
    popular = registry.get_popularity_rankings()
    print(f"\n🏆 Popular components:")
    for comp, usage in popular:
        print(f"  {comp.name}: {usage} uses")
    
    # Export registry
    registry.export_registry("registry_export.json")