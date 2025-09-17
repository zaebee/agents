#!/usr/bin/env python3
"""
🔍 Molecular Structure Similarity Search Engine
Advanced search system for finding similar molecular architecture patterns.

This system implements multiple similarity algorithms for chemical and architectural structures:
- Tanimoto Coefficient for structural similarity
- Jaccard Index for functional similarity
- Graph Isomorphism for topological matching
- Property Vector Similarity for quality attributes
- Molecular Fingerprinting for pattern recognition
- Substructure Search for architectural motifs
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Set, Optional, Any
from enum import Enum
from collections import defaultdict
import hashlib
import re
from datetime import datetime


class SimilarityMetric(Enum):
    """Types of molecular similarity metrics"""

    TANIMOTO = "tanimoto"  # Structural fingerprint similarity
    JACCARD = "jaccard"  # Set-based similarity
    COSINE = "cosine"  # Vector similarity
    EUCLIDEAN = "euclidean"  # Distance-based similarity
    MANHATTAN = "manhattan"  # L1 distance
    DICE = "dice"  # Dice coefficient
    OVERLAP = "overlap"  # Overlap coefficient
    SOERGEL = "soergel"  # Soergel distance
    HAMMING = "hamming"  # Bit-based distance


class MolecularFingerprint(Enum):
    """Types of molecular fingerprints for pattern matching"""

    ATCG_STRUCTURAL = "atcg_structural"  # Based on ATCG element patterns
    FUNCTIONAL_GROUPS = "functional_groups"  # Based on architectural patterns
    TOPOLOGICAL = "topological"  # Graph connectivity patterns
    PROPERTY_BASED = "property_based"  # Quality attribute patterns
    SUBSTRUCTURE = "substructure"  # Specific architectural motifs
    PHARMACOPHORE = "pharmacophore"  # Function-based patterns (adapted)
    MOLECULAR_ACCESS = "molecular_access"  # Accessibility patterns


@dataclass
class MolecularDescriptor:
    """Comprehensive molecular descriptor for similarity comparison"""

    molecule_id: str
    name: str
    formula: str

    # Structural descriptors
    atom_count: Dict[str, int] = field(default_factory=dict)  # ATCG element counts
    bond_count: Dict[str, int] = field(default_factory=dict)  # Bond type counts
    ring_count: int = 0  # Number of cycles/rings
    chain_length: int = 0  # Longest path
    branching_factor: float = 0.0  # Average branching

    # Topological descriptors
    connectivity_indices: List[float] = field(default_factory=list)
    graph_diameter: int = 0  # Longest shortest path
    clustering_coefficient: float = 0.0  # Local clustering
    centrality_measures: Dict[str, float] = field(default_factory=dict)

    # Geometric descriptors
    molecular_volume: float = 0.0  # 3D volume
    surface_area: float = 0.0  # Surface area
    asphericity: float = 0.0  # Shape measure
    eccentricity: float = 0.0  # Elongation

    # Electronic/quantum descriptors
    electronic_energy: float = 0.0  # Total electronic energy
    dipole_moment: float = 0.0  # Charge distribution
    polarizability: float = 0.0  # Response to fields

    # Property descriptors
    quality_attributes: Dict[str, float] = field(default_factory=dict)
    complexity_score: float = 0.0
    stability_score: float = 0.0

    # Fingerprints (bit vectors)
    fingerprints: Dict[MolecularFingerprint, List[int]] = field(default_factory=dict)

    def calculate_structural_hash(self) -> str:
        """Calculate hash based on structural features"""
        structure_data = f"{self.formula}_{self.ring_count}_{self.chain_length}_{self.branching_factor:.2f}"
        return hashlib.md5(structure_data.encode()).hexdigest()

    def generate_atcg_fingerprint(self, length: int = 1024) -> List[int]:
        """Generate ATCG-based structural fingerprint"""
        fingerprint = [0] * length

        # Hash structural patterns into fingerprint bits
        patterns = [
            f"A{self.atom_count.get('A', 0)}",
            f"T{self.atom_count.get('T', 0)}",
            f"C{self.atom_count.get('C', 0)}",
            f"G{self.atom_count.get('G', 0)}",
            f"rings_{self.ring_count}",
            f"chains_{self.chain_length}",
            f"branch_{int(self.branching_factor * 10)}",
        ]

        for pattern in patterns:
            # Hash pattern to multiple bit positions
            hash_obj = hashlib.md5(pattern.encode())
            hash_bytes = hash_obj.digest()

            for i in range(0, len(hash_bytes), 2):
                if i + 1 < len(hash_bytes):
                    bit_index = (hash_bytes[i] << 8 | hash_bytes[i + 1]) % length
                    fingerprint[bit_index] = 1

        self.fingerprints[MolecularFingerprint.ATCG_STRUCTURAL] = fingerprint
        return fingerprint

    def generate_functional_fingerprint(
        self, architectural_patterns: List[str], length: int = 512
    ) -> List[int]:
        """Generate fingerprint based on functional/architectural patterns"""
        fingerprint = [0] * length

        # Map architectural patterns to bits
        for pattern in architectural_patterns:
            pattern_hash = hashlib.md5(pattern.encode()).hexdigest()
            # Use multiple hash positions for robustness
            for i in range(0, 8, 2):
                hex_chars = pattern_hash[i : i + 2]
                bit_index = int(hex_chars, 16) % length
                fingerprint[bit_index] = 1

        self.fingerprints[MolecularFingerprint.FUNCTIONAL_GROUPS] = fingerprint
        return fingerprint

    def generate_property_vector(self) -> List[float]:
        """Generate property vector for similarity comparison"""
        # Standard set of properties for comparison
        properties = [
            self.complexity_score,
            self.stability_score,
            self.molecular_volume,
            self.ring_count,
            self.chain_length,
            self.branching_factor,
            self.clustering_coefficient,
            len(self.atom_count),
            len(self.bond_count),
            self.electronic_energy,
        ]

        return properties


@dataclass
class SimilarityResult:
    """Result of molecular similarity comparison"""

    query_molecule: str
    target_molecule: str
    similarity_score: float
    metric_used: SimilarityMetric
    fingerprint_type: Optional[MolecularFingerprint] = None

    # Detailed breakdown
    structural_similarity: float = 0.0
    functional_similarity: float = 0.0
    property_similarity: float = 0.0
    topological_similarity: float = 0.0

    # Matching details
    common_features: List[str] = field(default_factory=list)
    unique_features: List[str] = field(default_factory=list)

    # Statistical measures
    confidence_interval: Tuple[float, float] = (0.0, 0.0)
    p_value: float = 1.0

    timestamp: datetime = field(default_factory=datetime.now)


class MolecularSimilarityCalculator:
    """Calculator for various molecular similarity metrics"""

    @staticmethod
    def tanimoto_coefficient(fingerprint1: List[int], fingerprint2: List[int]) -> float:
        """Calculate Tanimoto coefficient: |A∩B| / |A∪B|"""
        if len(fingerprint1) != len(fingerprint2):
            raise ValueError("Fingerprints must have same length")

        intersection = sum(
            1 for a, b in zip(fingerprint1, fingerprint2) if a == 1 and b == 1
        )
        union = sum(1 for a, b in zip(fingerprint1, fingerprint2) if a == 1 or b == 1)

        return intersection / union if union > 0 else 0.0

    @staticmethod
    def jaccard_index(set1: Set[str], set2: Set[str]) -> float:
        """Calculate Jaccard index for set-based similarity"""
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    @staticmethod
    def cosine_similarity(vector1: List[float], vector2: List[float]) -> float:
        """Calculate cosine similarity between property vectors"""
        if len(vector1) != len(vector2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vector1, vector2))
        norm1 = math.sqrt(sum(a * a for a in vector1))
        norm2 = math.sqrt(sum(b * b for b in vector2))
        norms = norm1 * norm2
        return dot_product / norms if norms > 0 else 0.0

    @staticmethod
    def euclidean_distance(vector1: List[float], vector2: List[float]) -> float:
        """Calculate Euclidean distance (convert to similarity)"""
        if len(vector1) != len(vector2):
            return 0.0

        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(vector1, vector2)))
        # Convert distance to similarity (0-1 scale)
        max_possible_distance = math.sqrt(
            sum((abs(a) + abs(b)) ** 2 for a, b in zip(vector1, vector2))
        )
        return (
            1.0 - (distance / max_possible_distance)
            if max_possible_distance > 0
            else 0.0
        )

    @staticmethod
    def dice_coefficient(fingerprint1: List[int], fingerprint2: List[int]) -> float:
        """Calculate Dice coefficient: 2|A∩B| / (|A| + |B|)"""
        if len(fingerprint1) != len(fingerprint2):
            raise ValueError("Fingerprints must have same length")

        intersection = sum(
            1 for a, b in zip(fingerprint1, fingerprint2) if a == 1 and b == 1
        )
        sum_sizes = sum(fingerprint1) + sum(fingerprint2)

        return (2 * intersection) / sum_sizes if sum_sizes > 0 else 0.0

    @staticmethod
    def soergel_distance(vector1: List[float], vector2: List[float]) -> float:
        """Calculate Soergel distance (convert to similarity)"""
        if len(vector1) != len(vector2):
            return 0.0

        numerator = sum(abs(a - b) for a, b in zip(vector1, vector2))
        denominator = sum(max(a, b) for a, b in zip(vector1, vector2))
        distance = numerator / denominator if denominator > 0 else 0.0
        return 1.0 - distance  # Convert to similarity

    @staticmethod
    def calculate_similarity(
        mol1: MolecularDescriptor,
        mol2: MolecularDescriptor,
        metric: SimilarityMetric,
        fingerprint_type: Optional[MolecularFingerprint] = None,
    ) -> float:
        """Calculate similarity using specified metric"""

        if metric == SimilarityMetric.TANIMOTO:
            if (
                fingerprint_type
                and fingerprint_type in mol1.fingerprints
                and fingerprint_type in mol2.fingerprints
            ):
                return MolecularSimilarityCalculator.tanimoto_coefficient(
                    mol1.fingerprints[fingerprint_type],
                    mol2.fingerprints[fingerprint_type],
                )
            else:
                # Use ATCG structural fingerprint as default
                fp1 = mol1.generate_atcg_fingerprint()
                fp2 = mol2.generate_atcg_fingerprint()
                return MolecularSimilarityCalculator.tanimoto_coefficient(fp1, fp2)

        elif metric == SimilarityMetric.JACCARD:
            # Use atom types as sets
            atoms1 = set(mol1.atom_count.keys())
            atoms2 = set(mol2.atom_count.keys())
            return MolecularSimilarityCalculator.jaccard_index(atoms1, atoms2)

        elif metric == SimilarityMetric.COSINE:
            vec1 = mol1.generate_property_vector()
            vec2 = mol2.generate_property_vector()
            return MolecularSimilarityCalculator.cosine_similarity(vec1, vec2)

        elif metric == SimilarityMetric.EUCLIDEAN:
            vec1 = mol1.generate_property_vector()
            vec2 = mol2.generate_property_vector()
            return MolecularSimilarityCalculator.euclidean_distance(vec1, vec2)

        elif metric == SimilarityMetric.DICE:
            fp1 = mol1.generate_atcg_fingerprint()
            fp2 = mol2.generate_atcg_fingerprint()
            return MolecularSimilarityCalculator.dice_coefficient(fp1, fp2)

        elif metric == SimilarityMetric.SOERGEL:
            vec1 = mol1.generate_property_vector()
            vec2 = mol2.generate_property_vector()
            return MolecularSimilarityCalculator.soergel_distance(vec1, vec2)

        else:
            # Default to Tanimoto
            fp1 = mol1.generate_atcg_fingerprint()
            fp2 = mol2.generate_atcg_fingerprint()
            return MolecularSimilarityCalculator.tanimoto_coefficient(fp1, fp2)


class MolecularSimilaritySearchEngine:
    """Advanced search engine for molecular architecture similarity"""

    def __init__(self):
        self.molecular_database: Dict[str, MolecularDescriptor] = {}
        self.similarity_cache: Dict[
            Tuple[str, str, str], float
        ] = {}  # (mol1, mol2, metric) -> similarity
        self.inverted_indices: Dict[str, Set[str]] = defaultdict(
            set
        )  # feature -> molecules
        self.calculator = MolecularSimilarityCalculator()

        # Search parameters
        self.default_similarity_threshold = 0.6
        self.max_search_results = 100
        self.cache_enabled = True

    def add_molecule(self, descriptor: MolecularDescriptor):
        """Add molecule to search database"""
        self.molecular_database[descriptor.molecule_id] = descriptor

        # Update inverted indices for fast search
        self._update_inverted_indices(descriptor)

        # Generate fingerprints if not already present
        if MolecularFingerprint.ATCG_STRUCTURAL not in descriptor.fingerprints:
            descriptor.generate_atcg_fingerprint()

    def _update_inverted_indices(self, descriptor: MolecularDescriptor):
        """Update inverted indices for fast feature-based search"""
        mol_id = descriptor.molecule_id

        # Index by atom types
        for atom_type in descriptor.atom_count.keys():
            self.inverted_indices[f"atom_{atom_type}"].add(mol_id)

        # Index by ring count ranges
        ring_ranges = [
            (0, 1, "low_rings"),
            (2, 3, "medium_rings"),
            (4, float("inf"), "high_rings"),
        ]
        for min_rings, max_rings, label in ring_ranges:
            if min_rings <= descriptor.ring_count <= max_rings:
                self.inverted_indices[label].add(mol_id)

        # Index by complexity ranges
        complexity_ranges = [
            (0, 3, "simple"),
            (3, 7, "moderate"),
            (7, float("inf"), "complex"),
        ]
        for min_complexity, max_complexity, label in complexity_ranges:
            if min_complexity <= descriptor.complexity_score <= max_complexity:
                self.inverted_indices[f"complexity_{label}"].add(mol_id)

    def search_similar_molecules(
        self,
        query_molecule_id: str,
        similarity_metric: SimilarityMetric = SimilarityMetric.TANIMOTO,
        similarity_threshold: float = None,
        max_results: int = None,
        fingerprint_type: Optional[MolecularFingerprint] = None,
    ) -> List[SimilarityResult]:
        """Search for molecules similar to query molecule"""

        if query_molecule_id not in self.molecular_database:
            raise ValueError(
                f"Query molecule {query_molecule_id} not found in database"
            )

        threshold = similarity_threshold or self.default_similarity_threshold
        max_results = max_results or self.max_search_results

        query_molecule = self.molecular_database[query_molecule_id]
        results = []

        # Search all molecules in database
        for target_id, target_molecule in self.molecular_database.items():
            if target_id == query_molecule_id:
                continue  # Skip self-comparison

            # Check cache first
            cache_key = (query_molecule_id, target_id, similarity_metric.value)
            similarity_score = None

            if self.cache_enabled and cache_key in self.similarity_cache:
                similarity_score = self.similarity_cache[cache_key]
            else:
                # Calculate similarity
                similarity_score = self.calculator.calculate_similarity(
                    query_molecule, target_molecule, similarity_metric, fingerprint_type
                )

                # Cache result
                if self.cache_enabled:
                    self.similarity_cache[cache_key] = similarity_score

            # Add to results if above threshold
            if similarity_score >= threshold:
                result = SimilarityResult(
                    query_molecule=query_molecule_id,
                    target_molecule=target_id,
                    similarity_score=similarity_score,
                    metric_used=similarity_metric,
                    fingerprint_type=fingerprint_type,
                )

                # Calculate detailed similarity breakdown
                result.structural_similarity = self.calculator.calculate_similarity(
                    query_molecule, target_molecule, SimilarityMetric.TANIMOTO
                )
                result.functional_similarity = self.calculator.calculate_similarity(
                    query_molecule, target_molecule, SimilarityMetric.JACCARD
                )
                result.property_similarity = self.calculator.calculate_similarity(
                    query_molecule, target_molecule, SimilarityMetric.COSINE
                )

                # Find common and unique features
                query_atoms = set(query_molecule.atom_count.keys())
                target_atoms = set(target_molecule.atom_count.keys())
                result.common_features = list(query_atoms.intersection(target_atoms))
                result.unique_features = list(
                    query_atoms.symmetric_difference(target_atoms)
                )

                results.append(result)

        # Sort by similarity score (descending) and limit results
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:max_results]

    def search_by_substructure(
        self, substructure_pattern: str, exact_match: bool = False
    ) -> List[str]:
        """Search for molecules containing specific substructure patterns"""
        matching_molecules = []

        for mol_id, descriptor in self.molecular_database.items():
            # Simple pattern matching in molecule name or formula
            if exact_match:
                if (
                    substructure_pattern in descriptor.formula
                    or substructure_pattern in descriptor.name
                ):
                    matching_molecules.append(mol_id)
            else:
                # Flexible pattern matching
                pattern_regex = substructure_pattern.replace("*", ".*")
                if re.search(
                    pattern_regex, descriptor.formula, re.IGNORECASE
                ) or re.search(pattern_regex, descriptor.name, re.IGNORECASE):
                    matching_molecules.append(mol_id)

        return matching_molecules

    def search_by_properties(
        self, property_constraints: Dict[str, Tuple[float, float]]
    ) -> List[str]:
        """Search molecules by property ranges"""
        matching_molecules = []

        for mol_id, descriptor in self.molecular_database.items():
            matches_all = True

            for property_name, (min_val, max_val) in property_constraints.items():
                if property_name == "complexity_score":
                    value = descriptor.complexity_score
                elif property_name == "stability_score":
                    value = descriptor.stability_score
                elif property_name == "ring_count":
                    value = descriptor.ring_count
                elif property_name == "molecular_volume":
                    value = descriptor.molecular_volume
                else:
                    # Check quality attributes
                    value = descriptor.quality_attributes.get(property_name, 0.0)

                if not (min_val <= value <= max_val):
                    matches_all = False
                    break

            if matches_all:
                matching_molecules.append(mol_id)

        return matching_molecules

    def find_diverse_molecules(
        self,
        num_molecules: int,
        diversity_metric: SimilarityMetric = SimilarityMetric.TANIMOTO,
        min_diversity: float = 0.3,
    ) -> List[str]:
        """Find diverse set of molecules using maximum diversity selection"""
        if num_molecules <= 0 or num_molecules > len(self.molecular_database):
            return list(self.molecular_database.keys())

        selected_molecules = []
        remaining_molecules = list(self.molecular_database.keys())

        # Start with random molecule
        if remaining_molecules:
            selected_molecules.append(remaining_molecules[0])
            remaining_molecules.remove(remaining_molecules[0])

        # Greedily select most diverse molecules
        while len(selected_molecules) < num_molecules and remaining_molecules:
            best_candidate = None
            best_min_similarity = 0.0

            for candidate in remaining_molecules:
                # Calculate minimum similarity to all selected molecules
                min_similarity = float("inf")

                for selected in selected_molecules:
                    similarity = self.calculator.calculate_similarity(
                        self.molecular_database[candidate],
                        self.molecular_database[selected],
                        diversity_metric,
                    )
                    min_similarity = min(min_similarity, similarity)

                # Select candidate with maximum minimum similarity (most diverse)
                if (
                    min_similarity > best_min_similarity
                    and min_similarity >= min_diversity
                ):
                    best_min_similarity = min_similarity
                    best_candidate = candidate

            if best_candidate:
                selected_molecules.append(best_candidate)
                remaining_molecules.remove(best_candidate)
            else:
                # No more diverse candidates found
                break

        return selected_molecules

    def cluster_molecules(
        self,
        similarity_threshold: float = 0.7,
        similarity_metric: SimilarityMetric = SimilarityMetric.TANIMOTO,
    ) -> Dict[str, List[str]]:
        """Cluster molecules based on similarity"""
        clusters = {}
        unclustered = set(self.molecular_database.keys())
        cluster_id = 0

        while unclustered:
            # Start new cluster with first unclustered molecule
            seed_molecule = next(iter(unclustered))
            cluster_name = f"cluster_{cluster_id}"
            current_cluster = [seed_molecule]
            unclustered.remove(seed_molecule)

            # Find all molecules similar to seed
            seed_descriptor = self.molecular_database[seed_molecule]

            molecules_to_check = list(unclustered)
            for mol_id in molecules_to_check:
                mol_descriptor = self.molecular_database[mol_id]
                similarity = self.calculator.calculate_similarity(
                    seed_descriptor, mol_descriptor, similarity_metric
                )

                if similarity >= similarity_threshold:
                    current_cluster.append(mol_id)
                    unclustered.remove(mol_id)

            clusters[cluster_name] = current_cluster
            cluster_id += 1

        return clusters

    def get_database_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        if not self.molecular_database:
            return {"error": "No molecules in database"}

        # Basic counts
        total_molecules = len(self.molecular_database)

        # Atom type distribution
        atom_type_counts = defaultdict(int)
        ring_count_dist = defaultdict(int)
        complexity_scores = []

        for descriptor in self.molecular_database.values():
            for atom_type in descriptor.atom_count.keys():
                atom_type_counts[atom_type] += 1

            ring_count_dist[descriptor.ring_count] += 1
            complexity_scores.append(descriptor.complexity_score)

        # Calculate statistics
        avg_complexity = (
            sum(complexity_scores) / len(complexity_scores)
            if complexity_scores
            else 0.0
        )
        max_complexity = max(complexity_scores) if complexity_scores else 0.0
        min_complexity = min(complexity_scores) if complexity_scores else 0.0

        return {
            "total_molecules": total_molecules,
            "atom_type_distribution": dict(atom_type_counts),
            "ring_count_distribution": dict(ring_count_dist),
            "complexity_statistics": {
                "average": avg_complexity,
                "minimum": min_complexity,
                "maximum": max_complexity,
                "range": max_complexity - min_complexity,
            },
            "cache_statistics": {
                "cached_similarities": len(self.similarity_cache),
                "cache_hit_potential": len(self.similarity_cache)
                / max(total_molecules * (total_molecules - 1), 1),
            },
            "inverted_index_size": len(self.inverted_indices),
            "database_created": datetime.now().isoformat(),
        }


# Example usage and demonstration
def demonstrate_similarity_search():
    """Demonstrate molecular similarity search capabilities"""
    print("🔍 Molecular Structure Similarity Search - Demonstration")
    print("=" * 65)

    search_engine = MolecularSimilaritySearchEngine()

    # Create sample molecular descriptors
    print("\n📚 Building molecular database...")

    # Benzene-like hexagonal core
    benzene_desc = MolecularDescriptor(
        molecule_id="benzene_hex",
        name="Hexagonal Benzene Core",
        formula="A1C6",
        atom_count={"A": 1, "C": 6},
        bond_count={"aromatic": 6, "single": 6},
        ring_count=1,
        chain_length=0,
        branching_factor=0.0,
        complexity_score=3.0,
        stability_score=0.95,
        quality_attributes={"maintainability": 0.9, "scalability": 0.8},
    )

    # Naphthalene-like fused dual core
    naphthalene_desc = MolecularDescriptor(
        molecule_id="naphthalene_fused",
        name="Fused Naphthalene Cores",
        formula="A2C10",
        atom_count={"A": 2, "C": 10},
        bond_count={"aromatic": 14, "single": 8},
        ring_count=2,
        chain_length=0,
        branching_factor=0.5,
        complexity_score=5.5,
        stability_score=0.92,
        quality_attributes={
            "maintainability": 0.85,
            "scalability": 0.75,
            "coupling": 0.6,
        },
    )

    # Anthracene-like linear triple core
    anthracene_desc = MolecularDescriptor(
        molecule_id="anthracene_linear",
        name="Linear Anthracene Pipeline",
        formula="A3C14",
        atom_count={"A": 3, "C": 14},
        bond_count={"aromatic": 18, "single": 12},
        ring_count=3,
        chain_length=2,  # Linear chain of 3 rings
        branching_factor=0.0,
        complexity_score=7.0,
        stability_score=0.88,
        quality_attributes={"maintainability": 0.7, "throughput": 0.95},
    )

    # Fullerene-like container structure
    fullerene_desc = MolecularDescriptor(
        molecule_id="fullerene_container",
        name="Fullerene Container",
        formula="C60",
        atom_count={"C": 60},
        bond_count={"single": 90, "aromatic": 0},
        ring_count=12,  # Pentagonal and hexagonal faces
        chain_length=0,
        branching_factor=2.0,  # Highly branched sphere
        complexity_score=8.5,
        stability_score=0.80,
        quality_attributes={"isolation": 0.98, "security": 0.95},
    )

    # Add molecules to search engine
    for desc in [benzene_desc, naphthalene_desc, anthracene_desc, fullerene_desc]:
        search_engine.add_molecule(desc)

    print(f"   Added {len(search_engine.molecular_database)} molecules to database")

    # Demonstrate similarity search
    print("\n🔍 Searching for molecules similar to naphthalene...")
    results = search_engine.search_similar_molecules(
        "naphthalene_fused",
        similarity_metric=SimilarityMetric.TANIMOTO,
        similarity_threshold=0.3,
        max_results=5,
    )

    print(f"   Found {len(results)} similar molecules:")
    for result in results:
        print(
            f"   • {result.target_molecule}: {result.similarity_score:.3f} "
            f"(structural: {result.structural_similarity:.3f}, "
            f"functional: {result.functional_similarity:.3f})"
        )

    # Demonstrate substructure search
    print("\n🔎 Searching for molecules containing 'A2' pattern...")
    substructure_matches = search_engine.search_by_substructure("A2")
    print(f"   Found {len(substructure_matches)} matches: {substructure_matches}")

    # Demonstrate property-based search
    print("\n📊 Searching by complexity range (5.0-8.0)...")
    property_matches = search_engine.search_by_properties(
        {"complexity_score": (5.0, 8.0), "ring_count": (2, 10)}
    )
    print(f"   Found {len(property_matches)} matches: {property_matches}")

    # Demonstrate diversity selection
    print("\n🎯 Finding diverse set of 3 molecules...")
    diverse_set = search_engine.find_diverse_molecules(3, min_diversity=0.2)
    print(f"   Selected diverse molecules: {diverse_set}")

    # Demonstrate clustering
    print("\n🗂️ Clustering molecules by similarity...")
    clusters = search_engine.cluster_molecules(similarity_threshold=0.5)
    print(f"   Created {len(clusters)} clusters:")
    for cluster_name, molecules in clusters.items():
        print(f"   • {cluster_name}: {molecules}")

    # Show database statistics
    print("\n📈 Database statistics:")
    stats = search_engine.get_database_statistics()
    print(f"   Total molecules: {stats['total_molecules']}")
    print(f"   Atom types: {stats['atom_type_distribution']}")
    print(f"   Average complexity: {stats['complexity_statistics']['average']:.2f}")
    print(
        f"   Cache efficiency: {stats['cache_statistics']['cache_hit_potential']:.3f}"
    )

    print("\n🔍 Similarity search demonstration complete!")
    return search_engine


if __name__ == "__main__":
    # Run demonstration
    demonstrate_similarity_search()
