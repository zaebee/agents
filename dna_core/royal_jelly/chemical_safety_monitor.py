"""
Hive Chemical Safety & Health Monitoring System - Bio/Sci Safety Architecture

This module implements comprehensive chemical safety monitoring that protects
the Hive system from dangerous chemical combinations and environmental conditions.
Like biological systems, it maintains homeostasis and responds to chemical threats.

Key Bio/Sci Principles:
- Continuous monitoring of chemical environment and interactions
- Proactive detection and prevention of toxic combinations
- Homeostatic regulation of chemical conditions
- Emergency response protocols for chemical hazards
- Adaptive safety thresholds based on system evolution
"""

from typing import Dict, List, Optional, Tuple, Set, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid
import math
import time
from datetime import datetime, timezone, timedelta
from collections import defaultdict, deque
import threading
import logging

from .chemical_periodic_system import (
    ChemicalElement, ToxicityLevel, PeriodicTableSystem, get_periodic_table_system
)
from .chemical_bond_engine import (
    ChemicalBond, BondState, ChemicalBondEngine, get_chemical_bond_engine
)
from .molecular_architecture import (
    SoftwareMolecule, MolecularState, MolecularArchitectureEngine, get_molecular_architecture_engine
)


class SafetyAlert(Enum):
    """Types of chemical safety alerts"""
    
    INFO = "info"                    # Informational notice
    CAUTION = "caution"             # Minor safety consideration
    WARNING = "warning"             # Significant hazard detected
    DANGER = "danger"               # Major safety risk
    CRITICAL = "critical"           # Life-threatening condition
    EMERGENCY = "emergency"         # Immediate action required


class MonitoringArea(Enum):
    """Areas of chemical monitoring"""
    
    TOXICITY = "toxicity"                   # Toxic combination detection
    STABILITY = "stability"                 # Molecular stability monitoring
    REACTIVITY = "reactivity"               # Unexpected reaction detection
    ENVIRONMENT = "environment"             # Environmental conditions
    BONDS = "bonds"                        # Chemical bond health
    CONTAMINATION = "contamination"         # Foreign element detection
    PRESSURE = "pressure"                  # System pressure monitoring
    TEMPERATURE = "temperature"            # Thermal monitoring


class EmergencyProtocol(Enum):
    """Emergency response protocols"""
    
    ISOLATION = "isolation"                 # Isolate dangerous components
    NEUTRALIZATION = "neutralization"       # Neutralize toxic reactions
    DILUTION = "dilution"                  # Dilute concentrations
    COOLING = "cooling"                    # Reduce temperature
    PRESSURE_RELIEF = "pressure_relief"    # Release pressure buildup
    EVACUATION = "evacuation"              # Remove all components
    SHUTDOWN = "shutdown"                  # Emergency system shutdown
    ANTIDOTE = "antidote"                  # Apply chemical antidote


@dataclass
class SafetyIncident:
    """Represents a chemical safety incident"""
    
    incident_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    alert_level: SafetyAlert = SafetyAlert.INFO
    monitoring_area: MonitoringArea = MonitoringArea.TOXICITY
    
    # Incident details
    incident_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    title: str = ""
    description: str = ""
    
    # Affected components
    affected_components: List[str] = field(default_factory=list)
    affected_molecules: List[str] = field(default_factory=list)
    affected_bonds: List[str] = field(default_factory=list)
    
    # Chemical analysis
    toxic_elements: List[str] = field(default_factory=list)
    danger_score: float = 5.0           # 0.0 to 10.0
    toxicity_level: ToxicityLevel = ToxicityLevel.SAFE
    
    # Environmental factors
    temperature: float = 298.15         # Kelvin
    pressure: float = 1.0              # Atmospheres
    ph_level: float = 7.0              # pH scale
    
    # Response actions
    protocols_triggered: List[EmergencyProtocol] = field(default_factory=list)
    response_time_seconds: float = 0.0
    resolution_status: str = "open"    # open, investigating, resolved
    
    # Impact assessment
    components_affected_count: int = 0
    system_downtime_seconds: float = 0.0
    safety_impact_score: float = 0.0   # Overall impact (0.0 to 10.0)


@dataclass
class SafetyThreshold:
    """Configurable safety thresholds for monitoring"""
    
    threshold_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    monitoring_area: MonitoringArea = MonitoringArea.TOXICITY
    
    # Threshold values
    caution_level: float = 3.0
    warning_level: float = 6.0
    danger_level: float = 8.0
    critical_level: float = 9.5
    
    # Adaptive properties
    is_adaptive: bool = True
    learning_rate: float = 0.01
    adjustment_history: deque = field(default_factory=lambda: deque(maxlen=100))
    
    # Context sensitivity
    component_type_modifiers: Dict[str, float] = field(default_factory=dict)
    environmental_sensitivity: float = 1.0
    
    def adjust_threshold(self, actual_value: float, outcome_severity: float):
        """Adaptively adjust threshold based on outcomes"""
        
        if not self.is_adaptive:
            return
        
        # If outcome was worse than expected, lower thresholds
        if outcome_severity > actual_value:
            adjustment = -self.learning_rate * (outcome_severity - actual_value)
        # If outcome was better than expected, can raise thresholds slightly
        else:
            adjustment = self.learning_rate * 0.1 * (actual_value - outcome_severity)
        
        # Apply adjustments
        self.caution_level = max(1.0, self.caution_level + adjustment)
        self.warning_level = max(self.caution_level + 1.0, self.warning_level + adjustment)
        self.danger_level = max(self.warning_level + 1.0, self.danger_level + adjustment)
        self.critical_level = max(self.danger_level + 0.5, self.critical_level + adjustment)
        
        # Record adjustment
        self.adjustment_history.append({
            "timestamp": datetime.now(timezone.utc),
            "adjustment": adjustment,
            "trigger_value": actual_value,
            "outcome_severity": outcome_severity
        })
    
    def get_alert_level(self, value: float, component_type: Optional[str] = None) -> SafetyAlert:
        """Determine alert level for a given value"""
        
        # Apply component-specific modifier
        if component_type and component_type in self.component_type_modifiers:
            value *= self.component_type_modifiers[component_type]
        
        if value >= self.critical_level:
            return SafetyAlert.CRITICAL
        elif value >= self.danger_level:
            return SafetyAlert.DANGER
        elif value >= self.warning_level:
            return SafetyAlert.WARNING
        elif value >= self.caution_level:
            return SafetyAlert.CAUTION
        else:
            return SafetyAlert.INFO


class ChemicalSafetyMonitor:
    """
    Chemical Safety & Health Monitoring System
    
    Provides real-time monitoring, threat detection, and emergency response
    for chemical hazards in the Hive system architecture.
    """
    
    def __init__(self):
        self.periodic_system = get_periodic_table_system()
        self.bond_engine = get_chemical_bond_engine()
        self.molecular_engine = get_molecular_architecture_engine()
        
        # Safety monitoring
        self.active_incidents: Dict[str, SafetyIncident] = {}
        self.incident_history: deque = deque(maxlen=1000)
        self.safety_thresholds: Dict[MonitoringArea, SafetyThreshold] = {}
        
        # Monitoring state
        self.monitoring_enabled: bool = True
        self.last_scan_time: datetime = datetime.now(timezone.utc)
        self.scan_interval_seconds: float = 30.0
        self.emergency_mode: bool = False
        
        # Environmental monitoring
        self.environmental_history: deque = deque(maxlen=500)
        self.acceptable_temperature_range: Tuple[float, float] = (273.15, 373.15)  # 0-100°C
        self.acceptable_pressure_range: Tuple[float, float] = (0.1, 10.0)  # atm
        self.acceptable_ph_range: Tuple[float, float] = (6.0, 8.0)
        
        # Known dangerous combinations
        self.toxic_combinations: Set[Tuple[str, str]] = set()
        self.antidote_library: Dict[str, List[str]] = {}
        
        # Performance tracking
        self.total_scans: int = 0
        self.incidents_detected: int = 0
        self.false_positives: int = 0
        self.emergency_responses: int = 0
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Initialize monitoring system
        self._initialize_safety_thresholds()
        self._initialize_toxic_combinations()
        self._initialize_antidote_library()
    
    def _initialize_safety_thresholds(self):
        """Initialize default safety thresholds for all monitoring areas"""
        
        # Toxicity thresholds
        toxicity_threshold = SafetyThreshold(
            name="Toxicity Detection",
            monitoring_area=MonitoringArea.TOXICITY,
            caution_level=2.0,
            warning_level=4.0,
            danger_level=7.0,
            critical_level=9.0
        )
        
        # Stability thresholds
        stability_threshold = SafetyThreshold(
            name="Molecular Stability",
            monitoring_area=MonitoringArea.STABILITY,
            caution_level=3.0,
            warning_level=2.0,
            danger_level=1.0,
            critical_level=0.5
        )
        
        # Reactivity thresholds  
        reactivity_threshold = SafetyThreshold(
            name="Chemical Reactivity",
            monitoring_area=MonitoringArea.REACTIVITY,
            caution_level=6.0,
            warning_level=7.5,
            danger_level=8.5,
            critical_level=9.5
        )
        
        # Temperature thresholds
        temperature_threshold = SafetyThreshold(
            name="Temperature Monitoring",
            monitoring_area=MonitoringArea.TEMPERATURE,
            caution_level=50.0,   # 50°C above normal
            warning_level=100.0,  # 100°C above normal
            danger_level=200.0,   # 200°C above normal
            critical_level=300.0  # 300°C above normal
        )
        
        # Store thresholds
        self.safety_thresholds[MonitoringArea.TOXICITY] = toxicity_threshold
        self.safety_thresholds[MonitoringArea.STABILITY] = stability_threshold
        self.safety_thresholds[MonitoringArea.REACTIVITY] = reactivity_threshold
        self.safety_thresholds[MonitoringArea.TEMPERATURE] = temperature_threshold
    
    def _initialize_toxic_combinations(self):
        """Initialize known toxic element combinations"""
        
        # Highly reactive combinations
        self.toxic_combinations.update([
            ("F", "Li"),    # Fluorine + Lithium (explosive)
            ("F", "Na"),    # Fluorine + Sodium (violent reaction)
            ("Cl", "Li"),   # Chlorine + Lithium (fire risk)
            ("O", "Li"),    # Oxygen + Lithium (combustion)
        ])
    
    def _initialize_antidote_library(self):
        """Initialize chemical antidotes and neutralization agents"""
        
        # Neutralization agents for common toxic elements
        self.antidote_library = {
            "F": ["Ca", "Mg"],      # Calcium/Magnesium neutralize fluorine
            "Cl": ["Na", "Ca"],     # Sodium/Calcium neutralize chlorine
            "acid_condition": ["Na", "Ca"],  # Base elements for acid neutralization
            "base_condition": ["C", "N"],    # Acidic elements for base neutralization
        }
    
    def perform_safety_scan(self) -> Dict[str, Any]:
        """Perform comprehensive chemical safety scan"""
        
        with self._lock:
            scan_start = datetime.now(timezone.utc)
            
            # Scan results
            scan_results = {
                "scan_id": str(uuid.uuid4()),
                "scan_time": scan_start,
                "incidents_found": [],
                "environmental_status": "normal",
                "overall_safety_score": 10.0,
                "recommendations": []
            }
            
            try:
                # 1. Toxicity scan
                toxicity_incidents = self._scan_toxicity()
                scan_results["incidents_found"].extend(toxicity_incidents)
                
                # 2. Stability scan
                stability_incidents = self._scan_stability()
                scan_results["incidents_found"].extend(stability_incidents)
                
                # 3. Reactivity scan
                reactivity_incidents = self._scan_reactivity()
                scan_results["incidents_found"].extend(reactivity_incidents)
                
                # 4. Environmental scan
                environmental_incidents = self._scan_environment()
                scan_results["incidents_found"].extend(environmental_incidents)
                
                # 5. Bond health scan
                bond_incidents = self._scan_bond_health()
                scan_results["incidents_found"].extend(bond_incidents)
                
                # Calculate overall safety score
                if scan_results["incidents_found"]:
                    max_danger = max(incident.danger_score for incident in scan_results["incidents_found"])
                    scan_results["overall_safety_score"] = max(0.0, 10.0 - max_danger)
                    
                    # Determine environmental status
                    if max_danger >= 9.0:
                        scan_results["environmental_status"] = "critical"
                    elif max_danger >= 7.0:
                        scan_results["environmental_status"] = "dangerous"
                    elif max_danger >= 5.0:
                        scan_results["environmental_status"] = "warning"
                    elif max_danger >= 3.0:
                        scan_results["environmental_status"] = "caution"
                    else:
                        scan_results["environmental_status"] = "normal"
                
                # Generate safety recommendations
                scan_results["recommendations"] = self._generate_safety_recommendations(
                    scan_results["incidents_found"]
                )
                
                # Update scan metrics
                self.total_scans += 1
                self.incidents_detected += len(scan_results["incidents_found"])
                self.last_scan_time = scan_start
                
                # Store environmental history
                self.environmental_history.append({
                    "timestamp": scan_start,
                    "safety_score": scan_results["overall_safety_score"],
                    "incident_count": len(scan_results["incidents_found"]),
                    "status": scan_results["environmental_status"]
                })
                
            except Exception as e:
                logging.error(f"Safety scan error: {e}")
                scan_results["error"] = str(e)
                scan_results["overall_safety_score"] = 0.0
                scan_results["environmental_status"] = "error"
            
            return scan_results
    
    def _scan_toxicity(self) -> List[SafetyIncident]:
        """Scan for toxic chemical combinations"""
        
        incidents = []
        threshold = self.safety_thresholds[MonitoringArea.TOXICITY]
        
        # Check active molecules for toxic combinations
        for molecule in self.molecular_engine.active_molecules.values():
            for i, element1 in enumerate(molecule.component_elements):
                for j, element2 in enumerate(molecule.component_elements[i+1:], i+1):
                    # Check if this combination is known to be toxic
                    combo1 = (element1.symbol, element2.symbol)
                    combo2 = (element2.symbol, element1.symbol)
                    
                    if combo1 in self.toxic_combinations or combo2 in self.toxic_combinations:
                        # Calculate danger score based on element toxicity levels
                        toxicity1 = self._toxicity_to_score(element1.toxicity_level)
                        toxicity2 = self._toxicity_to_score(element2.toxicity_level)
                        danger_score = (toxicity1 + toxicity2) / 2.0 + 2.0  # Bonus for combination
                        
                        alert_level = threshold.get_alert_level(danger_score)
                        
                        if alert_level != SafetyAlert.INFO:
                            incident = SafetyIncident(
                                alert_level=alert_level,
                                monitoring_area=MonitoringArea.TOXICITY,
                                title=f"Toxic Combination Detected: {element1.symbol}-{element2.symbol}",
                                description=f"Dangerous combination of {element1.name} and {element2.name} in molecule {molecule.name}",
                                affected_molecules=[molecule.molecule_id],
                                toxic_elements=[element1.symbol, element2.symbol],
                                danger_score=danger_score,
                                toxicity_level=max(element1.toxicity_level, element2.toxicity_level, key=lambda x: x.value)
                            )
                            incidents.append(incident)
        
        return incidents
    
    def _scan_stability(self) -> List[SafetyIncident]:
        """Scan for molecular stability issues"""
        
        incidents = []
        threshold = self.safety_thresholds[MonitoringArea.STABILITY]
        
        for molecule in self.molecular_engine.active_molecules.values():
            stability = molecule.calculate_stability()
            alert_level = threshold.get_alert_level(stability)
            
            if alert_level in [SafetyAlert.WARNING, SafetyAlert.DANGER, SafetyAlert.CRITICAL]:
                incident = SafetyIncident(
                    alert_level=alert_level,
                    monitoring_area=MonitoringArea.STABILITY,
                    title=f"Unstable Molecule: {molecule.name}",
                    description=f"Molecule {molecule.name} has low stability ({stability:.2f}) and may dissociate",
                    affected_molecules=[molecule.molecule_id],
                    affected_components=molecule.component_ids,
                    danger_score=10.0 - stability
                )
                incidents.append(incident)
        
        return incidents
    
    def _scan_reactivity(self) -> List[SafetyIncident]:
        """Scan for dangerous reactivity levels"""
        
        incidents = []
        threshold = self.safety_thresholds[MonitoringArea.REACTIVITY]
        
        for molecule in self.molecular_engine.active_molecules.values():
            reactivity = molecule.predict_reactivity()
            alert_level = threshold.get_alert_level(reactivity)
            
            if alert_level in [SafetyAlert.DANGER, SafetyAlert.CRITICAL]:
                incident = SafetyIncident(
                    alert_level=alert_level,
                    monitoring_area=MonitoringArea.REACTIVITY,
                    title=f"Highly Reactive Molecule: {molecule.name}",
                    description=f"Molecule {molecule.name} has high reactivity ({reactivity:.2f}) and may cause unexpected reactions",
                    affected_molecules=[molecule.molecule_id],
                    danger_score=reactivity
                )
                incidents.append(incident)
        
        return incidents
    
    def _scan_environment(self) -> List[SafetyIncident]:
        """Scan environmental conditions"""
        
        incidents = []
        
        # Get current environmental conditions from bond engine
        current_temp = self.bond_engine.global_temperature
        current_pressure = self.bond_engine.global_pressure
        current_ph = self.bond_engine.global_ph
        
        # Check temperature
        if not (self.acceptable_temperature_range[0] <= current_temp <= self.acceptable_temperature_range[1]):
            temp_celsius = current_temp - 273.15
            danger_score = abs(temp_celsius - 25.0) / 10.0  # Deviation from 25°C
            
            incident = SafetyIncident(
                alert_level=SafetyAlert.WARNING if danger_score < 7.0 else SafetyAlert.DANGER,
                monitoring_area=MonitoringArea.TEMPERATURE,
                title="Temperature Out of Range",
                description=f"System temperature is {temp_celsius:.1f}°C (safe range: 0-100°C)",
                temperature=current_temp,
                danger_score=danger_score
            )
            incidents.append(incident)
        
        # Check pressure
        if not (self.acceptable_pressure_range[0] <= current_pressure <= self.acceptable_pressure_range[1]):
            danger_score = abs(current_pressure - 1.0) * 2.0
            
            incident = SafetyIncident(
                alert_level=SafetyAlert.CAUTION if danger_score < 5.0 else SafetyAlert.WARNING,
                monitoring_area=MonitoringArea.PRESSURE,
                title="Pressure Out of Range",
                description=f"System pressure is {current_pressure:.2f} atm (safe range: 0.1-10 atm)",
                pressure=current_pressure,
                danger_score=danger_score
            )
            incidents.append(incident)
        
        # Check pH
        if not (self.acceptable_ph_range[0] <= current_ph <= self.acceptable_ph_range[1]):
            danger_score = abs(current_ph - 7.0)
            
            incident = SafetyIncident(
                alert_level=SafetyAlert.CAUTION if danger_score < 3.0 else SafetyAlert.WARNING,
                monitoring_area=MonitoringArea.ENVIRONMENT,
                title="pH Out of Range",
                description=f"System pH is {current_ph:.1f} (safe range: 6.0-8.0)",
                ph_level=current_ph,
                danger_score=danger_score
            )
            incidents.append(incident)
        
        return incidents
    
    def _scan_bond_health(self) -> List[SafetyIncident]:
        """Scan chemical bond health"""
        
        incidents = []
        
        failing_bonds = []
        for bond in self.bond_engine.active_bonds.values():
            stability = bond.calculate_bond_stability()
            
            if stability < 2.0:
                failing_bonds.append(bond)
        
        if failing_bonds:
            incident = SafetyIncident(
                alert_level=SafetyAlert.WARNING,
                monitoring_area=MonitoringArea.BONDS,
                title=f"Bond Failure Risk: {len(failing_bonds)} bonds",
                description=f"{len(failing_bonds)} chemical bonds are at risk of failure",
                affected_bonds=[bond.bond_id for bond in failing_bonds],
                danger_score=len(failing_bonds) * 0.5
            )
            incidents.append(incident)
        
        return incidents
    
    def _toxicity_to_score(self, toxicity_level: ToxicityLevel) -> float:
        """Convert toxicity level to numeric score"""
        
        toxicity_scores = {
            ToxicityLevel.SAFE: 0.0,
            ToxicityLevel.CAUTION: 2.0,
            ToxicityLevel.WARNING: 5.0,
            ToxicityLevel.DANGEROUS: 8.0,
            ToxicityLevel.LETHAL: 10.0
        }
        
        return toxicity_scores.get(toxicity_level, 0.0)
    
    def _generate_safety_recommendations(self, incidents: List[SafetyIncident]) -> List[str]:
        """Generate safety recommendations based on incidents"""
        
        recommendations = []
        
        # Count incident types
        incident_counts = defaultdict(int)
        for incident in incidents:
            incident_counts[incident.monitoring_area] += 1
        
        # Generate recommendations based on incident patterns
        if incident_counts[MonitoringArea.TOXICITY] > 0:
            recommendations.append("Isolate toxic component combinations immediately")
            recommendations.append("Review component compatibility before deployment")
        
        if incident_counts[MonitoringArea.STABILITY] > 2:
            recommendations.append("Strengthen molecular bonds with catalytic support")
            recommendations.append("Consider molecular redesign for better stability")
        
        if incident_counts[MonitoringArea.TEMPERATURE] > 0:
            recommendations.append("Implement temperature control measures")
            recommendations.append("Add thermal monitoring to affected components")
        
        if incident_counts[MonitoringArea.REACTIVITY] > 0:
            recommendations.append("Add inert buffer components to reduce reactivity")
            recommendations.append("Implement reaction rate limiters")
        
        # General recommendations
        if len(incidents) > 5:
            recommendations.append("Consider system-wide safety audit")
            recommendations.append("Implement additional monitoring checkpoints")
        
        return recommendations
    
    def trigger_emergency_protocol(self, incident: SafetyIncident) -> bool:
        """Trigger emergency response protocol for critical incidents"""
        
        with self._lock:
            if incident.alert_level not in [SafetyAlert.CRITICAL, SafetyAlert.EMERGENCY]:
                return False
            
            protocols_applied = []
            
            try:
                # Determine appropriate protocols based on incident type
                if incident.monitoring_area == MonitoringArea.TOXICITY:
                    # Isolate toxic components
                    for mol_id in incident.affected_molecules:
                        self.molecular_engine.dissociate_molecule(mol_id, force=True)
                    protocols_applied.append(EmergencyProtocol.ISOLATION)
                    
                    # Apply neutralization if antidotes available
                    for toxic_element in incident.toxic_elements:
                        if toxic_element in self.antidote_library:
                            protocols_applied.append(EmergencyProtocol.NEUTRALIZATION)
                
                elif incident.monitoring_area == MonitoringArea.TEMPERATURE:
                    # Emergency cooling
                    self.bond_engine.update_environmental_conditions(temperature=298.15)
                    protocols_applied.append(EmergencyProtocol.COOLING)
                
                elif incident.monitoring_area == MonitoringArea.PRESSURE:
                    # Pressure relief
                    self.bond_engine.update_environmental_conditions(pressure=1.0)
                    protocols_applied.append(EmergencyProtocol.PRESSURE_RELIEF)
                
                elif incident.monitoring_area == MonitoringArea.STABILITY:
                    # Emergency stabilization - break unstable bonds
                    for bond_id in incident.affected_bonds:
                        self.bond_engine.break_chemical_bond(bond_id, force=True)
                    protocols_applied.append(EmergencyProtocol.ISOLATION)
                
                # Record protocols applied
                incident.protocols_triggered = protocols_applied
                incident.response_time_seconds = (datetime.now(timezone.utc) - incident.incident_time).total_seconds()
                
                # Update emergency metrics
                self.emergency_responses += 1
                self.emergency_mode = True
                
                return True
                
            except Exception as e:
                logging.error(f"Emergency protocol failed: {e}")
                return False
    
    def get_safety_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive safety monitoring dashboard"""
        
        with self._lock:
            # Current safety status
            recent_scan = self.perform_safety_scan()
            
            # Calculate safety trends
            recent_history = list(self.environmental_history)[-20:]  # Last 20 scans
            if len(recent_history) > 1:
                avg_recent_score = sum(h["safety_score"] for h in recent_history) / len(recent_history)
                trend = "improving" if recent_history[-1]["safety_score"] > avg_recent_score else "declining"
            else:
                trend = "insufficient_data"
            
            # Active incident summary
            critical_incidents = [inc for inc in recent_scan["incidents_found"] 
                                if inc.alert_level in [SafetyAlert.CRITICAL, SafetyAlert.EMERGENCY]]
            warning_incidents = [inc for inc in recent_scan["incidents_found"] 
                               if inc.alert_level == SafetyAlert.WARNING]
            
            return {
                "dashboard_timestamp": datetime.now(timezone.utc).isoformat(),
                "current_status": {
                    "overall_safety_score": recent_scan["overall_safety_score"],
                    "environmental_status": recent_scan["environmental_status"],
                    "monitoring_enabled": self.monitoring_enabled,
                    "emergency_mode": self.emergency_mode
                },
                "incident_summary": {
                    "total_active_incidents": len(recent_scan["incidents_found"]),
                    "critical_incidents": len(critical_incidents),
                    "warning_incidents": len(warning_incidents),
                    "incidents_this_scan": len(recent_scan["incidents_found"])
                },
                "safety_trends": {
                    "trend_direction": trend,
                    "recent_average_score": avg_recent_score if recent_history else 0.0,
                    "scans_analyzed": len(recent_history)
                },
                "system_metrics": {
                    "total_scans_performed": self.total_scans,
                    "total_incidents_detected": self.incidents_detected,
                    "emergency_responses": self.emergency_responses,
                    "false_positive_rate": self.false_positives / max(1, self.incidents_detected),
                    "last_scan": self.last_scan_time.isoformat()
                },
                "environmental_conditions": {
                    "temperature_celsius": self.bond_engine.global_temperature - 273.15,
                    "pressure_atm": self.bond_engine.global_pressure,
                    "ph_level": self.bond_engine.global_ph,
                    "conditions_normal": recent_scan["environmental_status"] == "normal"
                },
                "safety_recommendations": recent_scan["recommendations"],
                "monitoring_areas": [area.value for area in MonitoringArea],
                "emergency_protocols_available": [protocol.value for protocol in EmergencyProtocol]
            }


# Global chemical safety monitor instance
_global_safety_monitor = None


def get_chemical_safety_monitor() -> ChemicalSafetyMonitor:
    """Get the global chemical safety monitor instance"""
    global _global_safety_monitor
    if _global_safety_monitor is None:
        _global_safety_monitor = ChemicalSafetyMonitor()
    return _global_safety_monitor


def perform_chemical_safety_scan() -> Dict[str, Any]:
    """Perform a chemical safety scan and return results"""
    return get_chemical_safety_monitor().perform_safety_scan()


def get_chemical_safety_dashboard() -> Dict[str, Any]:
    """Get the chemical safety monitoring dashboard"""
    return get_chemical_safety_monitor().get_safety_dashboard()