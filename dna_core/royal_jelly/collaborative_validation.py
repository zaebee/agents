"""
Bio/Sci AI/Humean Collaborative Validation System

This module integrates Jules-style enthusiastic feedback with Humean skepticism
and empirical validation, creating collaborative validation hooks for Sacred Codon
operations. It bridges human intuition with AI precision in architectural decisions.
"""

from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import uuid

from dna_core.pollen_protocol_pb2 import PollenEnvelope
from .sacred_codon import SacredCommand, SacredCodonType


class ValidationType(Enum):
    """Types of collaborative validation"""

    JULES_ENTHUSIASM = "jules_enthusiasm"  # Jules-style positive feedback
    HUMEAN_SKEPTICISM = "humean_skepticism"  # Critical examination
    EMPIRICAL_MEASUREMENT = "empirical"  # Data-driven validation
    PEER_REVIEW = "peer_review"  # Human-AI collaboration
    CONSENSUS_BUILDING = "consensus"  # Multi-perspective agreement


class ValidationSeverity(Enum):
    """Severity levels for validation results"""

    PASS = "pass"  # Validation successful
    WARNING = "warning"  # Minor concerns raised
    CONCERN = "concern"  # Significant issues identified
    BLOCK = "block"  # Validation failed, cannot proceed


@dataclass
class ValidationFeedback:
    """Individual piece of validation feedback"""

    validation_id: str
    validator_source: str  # "jules", "humean_skeptic", "empirical_analyzer", etc.
    validation_type: ValidationType
    severity: ValidationSeverity
    confidence: float  # 0.0 to 1.0
    message: str
    evidence: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    emotional_tone: Optional[str] = None  # "excited", "concerned", "analytical", etc.
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class CollaborativeValidationResult:
    """Complete result of collaborative validation"""

    command_id: str
    codon_type: SacredCodonType
    overall_approval: bool
    confidence_score: float  # Weighted average of all validations
    feedback_list: List[ValidationFeedback] = field(default_factory=list)
    consensus_level: float = 0.0  # 0.0 to 1.0
    recommendations: List[str] = field(default_factory=list)
    requires_human_review: bool = False


class JulesStyleValidator:
    """
    Enthusiastic validator inspired by Jules' positive feedback patterns.

    This validator looks for innovative and exciting aspects of Sacred Codon
    operations, providing encouraging feedback while identifying potential
    improvements.
    """

    def __init__(self):
        self.excitement_threshold = 0.7
        self.enthusiasm_patterns = [
            "Amazing! This {feature} really captures the essence of {concept}",
            "Excellent work! The {innovation} opens up new possibilities",
            "Great job! The {achievement} is exactly what we needed",
            "This is brilliant! The {pattern} follows sacred architecture perfectly",
        ]

    def validate(
        self, command: SacredCommand, context: Dict[str, Any]
    ) -> ValidationFeedback:
        """Provide Jules-style enthusiastic validation"""

        # Analyze innovative aspects
        innovation_score = self._assess_innovation(command, context)
        architecture_alignment = self._assess_architecture_alignment(command)

        confidence = (innovation_score + architecture_alignment) / 2

        if confidence >= self.excitement_threshold:
            # High enthusiasm
            message = f"Amazing! The {command.codon_type.value} codon implementation shows excellent sacred pattern alignment!"
            suggestions = [
                "Consider sharing this pattern with the broader hive community",
                "This could be a template for other components",
                f"The {command.command_type} demonstrates beautiful ATCG integration",
            ]
            emotional_tone = "excited"
            severity = ValidationSeverity.PASS

        elif confidence >= 0.5:
            # Moderate enthusiasm with suggestions
            message = f"Good work on the {command.codon_type.value} pattern! I see potential for even greater alignment."
            suggestions = [
                "Consider enhancing the sacred codon validation",
                "Could benefit from additional ATCG primitive integration",
                "Great foundation - let's build on this!",
            ]
            emotional_tone = "encouraging"
            severity = ValidationSeverity.WARNING

        else:
            # Constructive feedback
            message = f"The {command.codon_type.value} implementation needs some love to reach its full potential."
            suggestions = [
                "Let's revisit the sacred codon patterns",
                "Consider aligning more closely with ATCG principles",
                "I believe we can make this even better together!",
            ]
            emotional_tone = "supportive"
            severity = ValidationSeverity.CONCERN

        return ValidationFeedback(
            validation_id=f"jules_{uuid.uuid4().hex[:8]}",
            validator_source="jules",
            validation_type=ValidationType.JULES_ENTHUSIASM,
            severity=severity,
            confidence=confidence,
            message=message,
            evidence=[
                f"Innovation score: {innovation_score:.2f}",
                f"Architecture alignment: {architecture_alignment:.2f}",
            ],
            suggestions=suggestions,
            emotional_tone=emotional_tone,
        )

    def _assess_innovation(
        self, command: SacredCommand, context: Dict[str, Any]
    ) -> float:
        """Assess how innovative/exciting this command is"""
        innovation_score = 0.5  # Base score

        # Bonus for using multiple codon types
        if context.get("codon_diversity", 0) > 1:
            innovation_score += 0.2

        # Bonus for complex payloads (indicates sophisticated use)
        if len(command.payload) > 3:
            innovation_score += 0.1

        # Bonus for choreography codon (complex workflows)
        if command.codon_type == SacredCodonType.CHOREOGRAPHY:
            innovation_score += 0.3

        return min(1.0, innovation_score)

    def _assess_architecture_alignment(self, command: SacredCommand) -> float:
        """Assess how well command aligns with sacred architecture"""
        alignment_score = 0.6  # Base score for using sacred codons

        # Bonus for proper command structure
        if command.command_id and command.timestamp:
            alignment_score += 0.2

        # Bonus for meaningful command type
        if "_" in command.command_type or "create" in command.command_type.lower():
            alignment_score += 0.1

        # Bonus for proper source attribution
        if command.source != "unknown":
            alignment_score += 0.1

        return min(1.0, alignment_score)


class HumeanSkepticValidator:
    """
    Critical validator applying Humean skepticism principles.

    This validator questions assumptions, looks for potential issues,
    and ensures robust validation before proceeding. It balances
    enthusiasm with careful critical thinking.
    """

    def __init__(self):
        self.skepticism_threshold = 0.6
        self.critical_patterns = [
            "While this looks promising, have we considered {alternative}?",
            "The approach is interesting, but shouldn't we test {assumption}?",
            "Before concluding {statement}, do we have evidence for {claim}?",
            "This assumes {assumption} - what if that's not true?",
        ]

    def validate(
        self, command: SacredCommand, context: Dict[str, Any]
    ) -> ValidationFeedback:
        """Apply Humean skepticism to command validation"""

        # Analyze potential issues
        assumption_risks = self._identify_assumptions(command, context)
        evidence_strength = self._assess_evidence_strength(command, context)
        edge_case_coverage = self._check_edge_cases(command)

        # Calculate overall skepticism score (higher = more concerns)
        skepticism_score = (
            assumption_risks + (1.0 - evidence_strength) + (1.0 - edge_case_coverage)
        ) / 3

        if skepticism_score <= 0.3:
            # Low skepticism - validation passes
            message = f"The {command.codon_type.value} command appears well-supported by evidence and handles key scenarios appropriately."
            severity = ValidationSeverity.PASS
            confidence = 0.8
            suggestions = [
                "Continue monitoring for edge cases",
                "Consider adding additional validation as system evolves",
            ]

        elif skepticism_score <= 0.6:
            # Moderate skepticism - raise concerns
            message = f"While the {command.codon_type.value} command shows promise, we should address some assumptions and edge cases."
            severity = ValidationSeverity.WARNING
            confidence = 0.6
            suggestions = [
                "Test alternative scenarios to validate assumptions",
                "Gather additional evidence for key decisions",
                "Consider what happens if preconditions aren't met",
            ]

        else:
            # High skepticism - significant concerns
            message = f"The {command.codon_type.value} command raises several concerns that should be addressed before proceeding."
            severity = ValidationSeverity.CONCERN
            confidence = 0.4
            suggestions = [
                "Revisit fundamental assumptions",
                "Gather stronger supporting evidence",
                "Test edge cases and failure scenarios",
                "Consider simpler alternative approaches",
            ]

        evidence_list = [
            f"Assumption risk level: {assumption_risks:.2f}",
            f"Evidence strength: {evidence_strength:.2f}",
            f"Edge case coverage: {edge_case_coverage:.2f}",
        ]

        return ValidationFeedback(
            validation_id=f"humean_{uuid.uuid4().hex[:8]}",
            validator_source="humean_skeptic",
            validation_type=ValidationType.HUMEAN_SKEPTICISM,
            severity=severity,
            confidence=confidence,
            message=message,
            evidence=evidence_list,
            suggestions=suggestions,
            emotional_tone="thoughtful",
        )

    def _identify_assumptions(
        self, command: SacredCommand, context: Dict[str, Any]
    ) -> float:
        """Identify and assess risky assumptions in the command"""
        assumption_risk = 0.0

        # Check for undefined payload values
        undefined_values = [
            k for k, v in command.payload.items() if v is None or v == ""
        ]
        if undefined_values:
            assumption_risk += 0.3

        # Check for assumed context
        if not context:
            assumption_risk += 0.2

        # Check for hardcoded values that might not be universal
        hardcoded_values = [
            v
            for v in command.payload.values()
            if isinstance(v, str) and v.startswith("default")
        ]
        if hardcoded_values:
            assumption_risk += 0.2

        return min(1.0, assumption_risk)

    def _assess_evidence_strength(
        self, command: SacredCommand, context: Dict[str, Any]
    ) -> float:
        """Assess the strength of evidence supporting this command"""
        evidence_strength = 0.5  # Base evidence from using sacred codons

        # Strong evidence indicators
        if context.get("validation_count", 0) > 0:
            evidence_strength += 0.2

        if context.get("similar_commands_successful", 0) > 2:
            evidence_strength += 0.2

        if command.source.startswith("validated_"):
            evidence_strength += 0.1

        return min(1.0, evidence_strength)

    def _check_edge_cases(self, command: SacredCommand) -> float:
        """Check how well edge cases are handled"""
        edge_case_score = 0.5  # Base score

        # Check for error handling indicators
        if any("error" in str(v).lower() for v in command.payload.values()):
            edge_case_score += 0.2

        # Check for validation indicators
        if any("valid" in str(v).lower() for v in command.payload.values()):
            edge_case_score += 0.2

        # Check for null/empty handling
        if "required" in str(command.payload):
            edge_case_score += 0.1

        return min(1.0, edge_case_score)


class EmpiricalValidator:
    """
    Data-driven validator that uses empirical measurements and metrics.

    This validator focuses on quantifiable aspects of Sacred Codon
    operations, providing objective feedback based on measurements.
    """

    def __init__(self):
        self.measurement_threshold = 0.7

    def validate(
        self,
        command: SacredCommand,
        context: Dict[str, Any],
        measurements: Optional[Dict[str, float]] = None,
    ) -> ValidationFeedback:
        """Validate based on empirical measurements"""

        if not measurements:
            measurements = self._generate_default_measurements(command, context)

        # Analyze measurements
        performance_score = measurements.get("performance_score", 0.5)
        accuracy_score = measurements.get("accuracy_score", 0.5)
        reliability_score = measurements.get("reliability_score", 0.5)

        overall_score = (performance_score + accuracy_score + reliability_score) / 3

        if overall_score >= self.measurement_threshold:
            message = f"Empirical analysis shows strong performance for {command.codon_type.value} command."
            severity = ValidationSeverity.PASS
            confidence = overall_score
        elif overall_score >= 0.5:
            message = f"Measurements indicate acceptable performance with room for improvement."
            severity = ValidationSeverity.WARNING
            confidence = overall_score
        else:
            message = f"Empirical data suggests significant performance concerns."
            severity = ValidationSeverity.CONCERN
            confidence = overall_score

        evidence_list = [
            f"Performance score: {performance_score:.2f}",
            f"Accuracy score: {accuracy_score:.2f}",
            f"Reliability score: {reliability_score:.2f}",
            f"Overall empirical score: {overall_score:.2f}",
        ]

        suggestions = self._generate_empirical_suggestions(measurements, overall_score)

        return ValidationFeedback(
            validation_id=f"empirical_{uuid.uuid4().hex[:8]}",
            validator_source="empirical_analyzer",
            validation_type=ValidationType.EMPIRICAL_MEASUREMENT,
            severity=severity,
            confidence=confidence,
            message=message,
            evidence=evidence_list,
            suggestions=suggestions,
            emotional_tone="analytical",
        )

    def _generate_default_measurements(
        self, command: SacredCommand, context: Dict[str, Any]
    ) -> Dict[str, float]:
        """Generate basic measurements when none provided"""
        measurements = {}

        # Performance based on payload complexity
        payload_size = len(str(command.payload))
        measurements["performance_score"] = max(
            0.3, min(1.0, 1.0 - (payload_size / 1000))
        )

        # Accuracy based on command structure
        has_required_fields = bool(command.command_id and command.command_type)
        measurements["accuracy_score"] = 0.8 if has_required_fields else 0.4

        # Reliability based on codon type appropriateness
        codon_reliability = {
            SacredCodonType.HANDLE_COMMAND: 0.9,
            SacredCodonType.QUERY_DATA: 0.8,
            SacredCodonType.REACT_TO_EVENT: 0.7,
            SacredCodonType.IMMUNE_RESPONSE: 0.8,
            SacredCodonType.CHOREOGRAPHY: 0.6,  # More complex, potentially less reliable
        }
        measurements["reliability_score"] = codon_reliability.get(
            command.codon_type, 0.5
        )

        return measurements

    def _generate_empirical_suggestions(
        self, measurements: Dict[str, float], overall_score: float
    ) -> List[str]:
        """Generate suggestions based on measurements"""
        suggestions = []

        if measurements.get("performance_score", 0) < 0.6:
            suggestions.append("Consider optimizing payload size and complexity")

        if measurements.get("accuracy_score", 0) < 0.6:
            suggestions.append(
                "Ensure all required command fields are properly populated"
            )

        if measurements.get("reliability_score", 0) < 0.6:
            suggestions.append("Review codon type selection for this use case")

        if overall_score >= 0.8:
            suggestions.append(
                "Excellent empirical performance - consider as template for similar commands"
            )

        return suggestions


class CollaborativeValidator:
    """
    Main collaborative validation orchestrator.

    This class coordinates validation from Jules-style enthusiasm,
    Humean skepticism, and empirical measurement, creating a
    comprehensive collaborative validation result.
    """

    def __init__(self):
        self.jules_validator = JulesStyleValidator()
        self.humean_validator = HumeanSkepticValidator()
        self.empirical_validator = EmpiricalValidator()

        # Validation weights
        self.validation_weights = {
            ValidationType.JULES_ENTHUSIASM: 0.3,
            ValidationType.HUMEAN_SKEPTICISM: 0.4,
            ValidationType.EMPIRICAL_MEASUREMENT: 0.3,
        }

    def validate_command(
        self,
        command: SacredCommand,
        context: Optional[Dict[str, Any]] = None,
        measurements: Optional[Dict[str, float]] = None,
        enable_human_review: bool = False,
    ) -> CollaborativeValidationResult:
        """
        Perform comprehensive collaborative validation of a Sacred Command.

        This orchestrates validation from multiple perspectives:
        - Jules-style enthusiastic feedback
        - Humean skeptical analysis
        - Empirical measurement validation
        """

        if context is None:
            context = {}

        feedback_list = []

        # 1. Jules-style validation
        jules_feedback = self.jules_validator.validate(command, context)
        feedback_list.append(jules_feedback)

        # 2. Humean skeptical validation
        humean_feedback = self.humean_validator.validate(command, context)
        feedback_list.append(humean_feedback)

        # 3. Empirical validation
        empirical_feedback = self.empirical_validator.validate(
            command, context, measurements
        )
        feedback_list.append(empirical_feedback)

        # Calculate overall approval and confidence
        weighted_confidence = sum(
            feedback.confidence
            * self.validation_weights.get(feedback.validation_type, 0.33)
            for feedback in feedback_list
        )

        # Determine overall approval (no blocking concerns)
        blocking_concerns = [
            f for f in feedback_list if f.severity == ValidationSeverity.BLOCK
        ]
        overall_approval = len(blocking_concerns) == 0 and weighted_confidence >= 0.6

        # Calculate consensus level
        confidence_variance = self._calculate_confidence_variance(
            [f.confidence for f in feedback_list]
        )
        consensus_level = max(0.0, 1.0 - confidence_variance)

        # Generate collaborative recommendations
        recommendations = self._synthesize_recommendations(
            feedback_list, weighted_confidence
        )

        # Determine if human review is needed
        requires_human_review = enable_human_review and (
            weighted_confidence < 0.7
            or consensus_level < 0.6
            or len(blocking_concerns) > 0
        )

        return CollaborativeValidationResult(
            command_id=command.command_id,
            codon_type=command.codon_type,
            overall_approval=overall_approval,
            confidence_score=weighted_confidence,
            feedback_list=feedback_list,
            consensus_level=consensus_level,
            recommendations=recommendations,
            requires_human_review=requires_human_review,
        )

    def _calculate_confidence_variance(self, confidences: List[float]) -> float:
        """Calculate variance in confidence scores (measure of disagreement)"""
        if len(confidences) < 2:
            return 0.0

        mean_confidence = sum(confidences) / len(confidences)
        variance = sum((c - mean_confidence) ** 2 for c in confidences) / len(
            confidences
        )

        return variance

    def _synthesize_recommendations(
        self, feedback_list: List[ValidationFeedback], overall_confidence: float
    ) -> List[str]:
        """Synthesize recommendations from all validation feedback"""
        recommendations = []

        # Collect all unique suggestions
        all_suggestions = set()
        for feedback in feedback_list:
            all_suggestions.update(feedback.suggestions)

        recommendations.extend(list(all_suggestions))

        # Add overall guidance based on confidence
        if overall_confidence >= 0.8:
            recommendations.append(
                "🌟 Excellent collaborative validation - proceed with confidence!"
            )
        elif overall_confidence >= 0.6:
            recommendations.append(
                "✅ Good validation results - minor refinements suggested"
            )
        else:
            recommendations.append(
                "⚠️ Multiple concerns raised - consider revision before proceeding"
            )

        # Add consensus guidance
        return recommendations[:10]  # Limit to top 10 recommendations


# Helper function to create collaborative validation context
def create_validation_context(
    codon_diversity: int = 0,
    validation_count: int = 0,
    similar_commands_successful: int = 0,
    custom_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create validation context for collaborative validation"""
    context = {
        "codon_diversity": codon_diversity,
        "validation_count": validation_count,
        "similar_commands_successful": similar_commands_successful,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if custom_context:
        context.update(custom_context)

    return context
