#!/usr/bin/env python3
"""
Quantum Monitoring Suite - Comprehensive Enterprise Observability
Real-time quantum system monitoring with AI-powered anomaly detection
"""

import asyncio
import json
import time
import logging
import threading
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, field, asdict
from collections import defaultdict, deque
from enum import Enum
import statistics
import math

# Import our quantum components
from quantum_metrics_collector import QuantumMetricsCollector, QuantumMetric
from deployment.logging.structured_logger import QuantumLogger

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class MonitoringChannel(Enum):
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"
    PAGERDUTY = "pagerduty"

@dataclass
class QuantumAlert:
    """Quantum-aware alert definition"""
    alert_id: str
    name: str
    description: str
    severity: AlertSeverity
    condition: str  # Query or condition string
    threshold_value: float
    comparison_operator: str  # >, <, >=, <=, ==, !=
    evaluation_window: int  # seconds
    quantum_context: Dict[str, Any] = field(default_factory=dict)
    recovery_condition: Optional[str] = None
    channels: List[MonitoringChannel] = field(default_factory=list)
    enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass 
class AlertEvent:
    """Alert event instance"""
    event_id: str
    alert: QuantumAlert
    triggered_at: datetime
    resolved_at: Optional[datetime] = None
    current_value: float = 0.0
    quantum_state: Dict[str, Any] = field(default_factory=dict)
    notification_sent: bool = False
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None

@dataclass
class QuantumHealth:
    """Overall quantum system health assessment"""
    overall_score: float  # 0-1
    coherence_health: float
    consciousness_health: float
    genetic_health: float
    chemical_health: float
    infrastructure_health: float
    security_health: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    recommendations: List[str] = field(default_factory=list)

class AnomalyDetector:
    """AI-powered anomaly detection for quantum metrics"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metric_history = defaultdict(lambda: deque(maxlen=window_size))
        self.baselines = {}
        self.anomaly_thresholds = {}
    
    def add_metric(self, metric_name: str, value: float, timestamp: datetime):
        """Add metric value for anomaly analysis"""
        self.metric_history[metric_name].append({
            'value': value,
            'timestamp': timestamp
        })
        
        # Update baseline if we have enough data
        if len(self.metric_history[metric_name]) >= 20:
            self._update_baseline(metric_name)
    
    def _update_baseline(self, metric_name: str):
        """Update statistical baseline for metric"""
        values = [point['value'] for point in self.metric_history[metric_name]]
        
        self.baselines[metric_name] = {
            'mean': statistics.mean(values),
            'stdev': statistics.stdev(values) if len(values) > 1 else 0,
            'median': statistics.median(values),
            'percentile_95': statistics.quantiles(values, n=20)[18] if len(values) > 5 else max(values),
            'percentile_5': statistics.quantiles(values, n=20)[0] if len(values) > 5 else min(values)
        }
        
        # Set anomaly threshold at 3 standard deviations
        if self.baselines[metric_name]['stdev'] > 0:
            self.anomaly_thresholds[metric_name] = 3 * self.baselines[metric_name]['stdev']
    
    def detect_anomaly(self, metric_name: str, value: float) -> Dict[str, Any]:
        """Detect if current value is anomalous"""
        if metric_name not in self.baselines:
            return {'is_anomaly': False, 'reason': 'insufficient_data'}
        
        baseline = self.baselines[metric_name]
        threshold = self.anomaly_thresholds.get(metric_name, 0)
        
        # Z-score based anomaly detection
        z_score = abs(value - baseline['mean']) / baseline['stdev'] if baseline['stdev'] > 0 else 0
        
        # Multiple detection methods
        anomaly_signals = {
            'z_score_anomaly': z_score > 3,
            'percentile_anomaly': value < baseline['percentile_5'] or value > baseline['percentile_95'],
            'rapid_change': self._detect_rapid_change(metric_name, value)
        }
        
        is_anomaly = any(anomaly_signals.values())
        
        return {
            'is_anomaly': is_anomaly,
            'z_score': z_score,
            'signals': anomaly_signals,
            'baseline': baseline,
            'confidence': min(z_score / 3, 1.0) if z_score > 0 else 0
        }
    
    def _detect_rapid_change(self, metric_name: str, current_value: float) -> bool:
        """Detect rapid changes in metric values"""
        history = self.metric_history[metric_name]
        if len(history) < 3:
            return False
        
        recent_values = [point['value'] for point in list(history)[-3:]]
        if len(recent_values) < 2:
            return False
        
        # Check for rapid change (>50% change in short time)
        prev_value = recent_values[-2]
        if prev_value == 0:
            return False
        
        change_percent = abs((current_value - prev_value) / prev_value)
        return change_percent > 0.5

class QuantumMonitoringSuite:
    """
    Comprehensive quantum system monitoring with enterprise features.
    Provides real-time observability, alerting, and health assessment.
    """
    
    def __init__(self,
                 hive_id: str,
                 metrics_collector: QuantumMetricsCollector,
                 quantum_logger: QuantumLogger,
                 enable_ai_anomaly_detection: bool = True,
                 alert_evaluation_interval: int = 30):
        
        self.hive_id = hive_id
        self.metrics_collector = metrics_collector
        self.logger = quantum_logger
        self.enable_ai_anomaly_detection = enable_ai_anomaly_detection
        self.alert_evaluation_interval = alert_evaluation_interval
        
        # Monitoring components
        self.alerts: Dict[str, QuantumAlert] = {}
        self.active_events: Dict[str, AlertEvent] = {}
        self.alert_history: List[AlertEvent] = []
        self.health_history: deque = deque(maxlen=1000)
        
        # AI components
        if enable_ai_anomaly_detection:
            self.anomaly_detector = AnomalyDetector()
        
        # Threading control
        self._monitoring_active = False
        self._monitoring_thread = None
        self._alert_thread = None
        
        # Notification callbacks
        self.notification_handlers: Dict[MonitoringChannel, Callable] = {}
        
        # Initialize default alerts
        self._setup_default_alerts()
        
        self.logger.info("QuantumMonitoringSuite initialized", 
                        enable_ai=enable_ai_anomaly_detection)
    
    def _setup_default_alerts(self):
        """Setup default quantum system alerts"""
        
        default_alerts = [
            QuantumAlert(
                alert_id="quantum_coherence_degraded",
                name="Quantum Coherence Degraded",
                description="Quantum coherence has fallen below acceptable levels",
                severity=AlertSeverity.WARNING,
                condition="quantum_coherence < 0.7",
                threshold_value=0.7,
                comparison_operator="<",
                evaluation_window=120,
                channels=[MonitoringChannel.EMAIL, MonitoringChannel.WEBHOOK]
            ),
            QuantumAlert(
                alert_id="quantum_coherence_critical",
                name="Critical Quantum Coherence Failure",
                description="Quantum coherence critically low - system instability imminent",
                severity=AlertSeverity.CRITICAL,
                condition="quantum_coherence < 0.5",
                threshold_value=0.5,
                comparison_operator="<",
                evaluation_window=60,
                channels=[MonitoringChannel.EMAIL, MonitoringChannel.SLACK, MonitoringChannel.PAGERDUTY]
            ),
            QuantumAlert(
                alert_id="consciousness_regression",
                name="Consciousness Level Regression",
                description="Consciousness evolution has regressed significantly",
                severity=AlertSeverity.WARNING,
                condition="consciousness_level_decrease > 1",
                threshold_value=1,
                comparison_operator=">",
                evaluation_window=300,
                quantum_context={"evolution_tracking": True}
            ),
            QuantumAlert(
                alert_id="genetic_fitness_decline",
                name="Genetic Fitness Decline",
                description="Genetic programming fitness showing significant decline",
                severity=AlertSeverity.WARNING,
                condition="genetic_fitness_trend < -0.1",
                threshold_value=-0.1,
                comparison_operator="<",
                evaluation_window=600
            ),
            QuantumAlert(
                alert_id="chemical_bonds_disruption",
                name="Chemical Bond System Disruption",
                description="Excessive chemical bond breaking detected",
                severity=AlertSeverity.CRITICAL,
                condition="chemical_bonds_broken_rate > 5",
                threshold_value=5,
                comparison_operator=">",
                evaluation_window=300
            ),
            QuantumAlert(
                alert_id="high_error_rate",
                name="High System Error Rate",
                description="System error rate exceeding acceptable threshold",
                severity=AlertSeverity.CRITICAL,
                condition="error_rate > 0.05",
                threshold_value=0.05,
                comparison_operator=">",
                evaluation_window=300,
                channels=[MonitoringChannel.EMAIL, MonitoringChannel.PAGERDUTY]
            )
        ]
        
        for alert in default_alerts:
            self.alerts[alert.alert_id] = alert
    
    def add_alert(self, alert: QuantumAlert):
        """Add custom alert to monitoring system"""
        self.alerts[alert.alert_id] = alert
        self.logger.info(f"Alert added: {alert.name}", alert_id=alert.alert_id)
    
    def remove_alert(self, alert_id: str) -> bool:
        """Remove alert from monitoring system"""
        if alert_id in self.alerts:
            del self.alerts[alert_id]
            self.logger.info(f"Alert removed: {alert_id}")
            return True
        return False
    
    def register_notification_handler(self, 
                                    channel: MonitoringChannel,
                                    handler: Callable[[AlertEvent], None]):
        """Register notification handler for alert channel"""
        self.notification_handlers[channel] = handler
        self.logger.info(f"Notification handler registered for {channel.value}")
    
    async def start_monitoring(self):
        """Start comprehensive quantum system monitoring"""
        if self._monitoring_active:
            self.logger.warning("Monitoring already active")
            return
        
        self._monitoring_active = True
        
        # Start monitoring thread
        self._monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self._monitoring_thread.start()
        
        # Start alert evaluation thread
        self._alert_thread = threading.Thread(
            target=self._alert_evaluation_loop,
            daemon=True
        )
        self._alert_thread.start()
        
        self.logger.info("Quantum monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring system"""
        self._monitoring_active = False
        
        if self._monitoring_thread:
            self._monitoring_thread.join(timeout=5.0)
        if self._alert_thread:
            self._alert_thread.join(timeout=5.0)
        
        self.logger.info("Quantum monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop - collect metrics and assess health"""
        while self._monitoring_active:
            try:
                start_time = time.time()
                
                # Get current metrics summary
                metrics_summary = self.metrics_collector.get_metrics_summary()
                
                # Perform health assessment
                health_score = self._calculate_quantum_health(metrics_summary)
                self.health_history.append(health_score)
                
                # AI anomaly detection
                if self.enable_ai_anomaly_detection:
                    self._run_anomaly_detection(metrics_summary)
                
                # Log health status
                self.logger.info("Health assessment completed",
                               overall_score=health_score.overall_score,
                               coherence=health_score.coherence_health,
                               consciousness=health_score.consciousness_health)
                
                # Sleep until next collection
                elapsed = time.time() - start_time
                sleep_time = max(1.0, 10.0 - elapsed)  # 10-second monitoring cycle
                time.sleep(sleep_time)
                
            except Exception as e:
                self.logger.error("Error in monitoring loop", exception=e)
                time.sleep(5.0)  # Brief pause before retry
    
    def _alert_evaluation_loop(self):
        """Alert evaluation and notification loop"""
        while self._monitoring_active:
            try:
                start_time = time.time()
                
                # Evaluate all active alerts
                self._evaluate_alerts()
                
                # Process notifications
                self._process_notifications()
                
                # Sleep until next evaluation
                elapsed = time.time() - start_time
                sleep_time = max(1.0, self.alert_evaluation_interval - elapsed)
                time.sleep(sleep_time)
                
            except Exception as e:
                self.logger.error("Error in alert evaluation loop", exception=e)
                time.sleep(10.0)
    
    def _calculate_quantum_health(self, metrics_summary: Dict[str, Any]) -> QuantumHealth:
        """Calculate comprehensive quantum system health score"""
        
        # Extract key metrics
        consciousness_state = metrics_summary.get('consciousness_state', {})
        genetic_metrics = metrics_summary.get('genetic_metrics', {})
        chemical_metrics = metrics_summary.get('chemical_metrics', {})
        
        # Calculate component health scores (0-1)
        coherence_health = self._assess_coherence_health(metrics_summary)
        consciousness_health = self._assess_consciousness_health(consciousness_state)
        genetic_health = self._assess_genetic_health(genetic_metrics)
        chemical_health = self._assess_chemical_health(chemical_metrics)
        infrastructure_health = self._assess_infrastructure_health(metrics_summary)
        security_health = self._assess_security_health()
        
        # Calculate weighted overall score
        weights = {
            'coherence': 0.25,
            'consciousness': 0.20,
            'genetic': 0.15,
            'chemical': 0.15,
            'infrastructure': 0.15,
            'security': 0.10
        }
        
        overall_score = (
            coherence_health * weights['coherence'] +
            consciousness_health * weights['consciousness'] +
            genetic_health * weights['genetic'] +
            chemical_health * weights['chemical'] +
            infrastructure_health * weights['infrastructure'] +
            security_health * weights['security']
        )
        
        # Generate recommendations
        recommendations = self._generate_health_recommendations({
            'coherence': coherence_health,
            'consciousness': consciousness_health,
            'genetic': genetic_health,
            'chemical': chemical_health,
            'infrastructure': infrastructure_health,
            'security': security_health
        })
        
        return QuantumHealth(
            overall_score=overall_score,
            coherence_health=coherence_health,
            consciousness_health=consciousness_health,
            genetic_health=genetic_health,
            chemical_health=chemical_health,
            infrastructure_health=infrastructure_health,
            security_health=security_health,
            recommendations=recommendations
        )
    
    def _assess_coherence_health(self, metrics: Dict[str, Any]) -> float:
        """Assess quantum coherence health (0-1)"""
        # This would use actual coherence metrics from the collector
        # For simulation, we'll use a reasonable health score
        base_score = 0.85
        
        # Add some realistic variation
        current_time = time.time()
        variation = 0.1 * math.sin(current_time / 300)  # 5-minute cycle
        
        return max(0.0, min(1.0, base_score + variation))
    
    def _assess_consciousness_health(self, consciousness_state: Dict[str, Any]) -> float:
        """Assess consciousness evolution health"""
        level = consciousness_state.get('level', 1)
        growth_rate = consciousness_state.get('growth_rate', 0.0)
        
        # Health based on level and positive growth
        level_score = min(level / 6.0, 1.0)  # Normalize to 0-1
        growth_score = max(0.0, min(growth_rate * 10, 1.0))  # Positive growth bonus
        
        return (level_score * 0.7) + (growth_score * 0.3)
    
    def _assess_genetic_health(self, genetic_metrics: Dict[str, Any]) -> float:
        """Assess genetic programming health"""
        fitness = genetic_metrics.get('fitness_score', 0.0)
        diversity = genetic_metrics.get('diversity_index', 0.0)
        
        return (fitness * 0.6) + (diversity * 0.4)
    
    def _assess_chemical_health(self, chemical_metrics: Dict[str, Any]) -> float:
        """Assess chemical bond system health"""
        total_bonds = chemical_metrics.get('total_bonds', 0)
        avg_strength = chemical_metrics.get('average_strength', 0.0)
        
        # Health based on bond count and strength
        bond_score = min(total_bonds / 100.0, 1.0)  # Assuming 100 is optimal
        strength_score = min(avg_strength / 5.0, 1.0)  # Assuming 5.0 is max strength
        
        return (bond_score * 0.4) + (strength_score * 0.6)
    
    def _assess_infrastructure_health(self, metrics: Dict[str, Any]) -> float:
        """Assess infrastructure health"""
        # This would check CPU, memory, disk, network metrics
        # For simulation, return a reasonable score
        return 0.90
    
    def _assess_security_health(self) -> float:
        """Assess security posture health"""
        # This would check security metrics, compliance status
        # For simulation, return a good security score
        return 0.95
    
    def _generate_health_recommendations(self, health_scores: Dict[str, float]) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []
        
        for component, score in health_scores.items():
            if score < 0.7:
                if component == 'coherence':
                    recommendations.append("Consider quantum coherence calibration and noise reduction")
                elif component == 'consciousness':
                    recommendations.append("Review consciousness evolution algorithms and adaptation triggers")
                elif component == 'genetic':
                    recommendations.append("Optimize genetic programming parameters and population diversity")
                elif component == 'chemical':
                    recommendations.append("Investigate chemical bond formation/dissolution balance")
                elif component == 'infrastructure':
                    recommendations.append("Review system resources and consider scaling up infrastructure")
                elif component == 'security':
                    recommendations.append("Conduct security audit and update security policies")
        
        if not recommendations:
            recommendations.append("System health optimal - continue current operations")
        
        return recommendations
    
    def _run_anomaly_detection(self, metrics_summary: Dict[str, Any]):
        """Run AI-powered anomaly detection on current metrics"""
        timestamp = datetime.now(timezone.utc)
        
        # Extract key metrics for anomaly detection
        metrics_to_analyze = {
            'coherence_health': metrics_summary.get('consciousness_state', {}).get('level', 0),
            'genetic_fitness': metrics_summary.get('genetic_metrics', {}).get('fitness_score', 0),
            'chemical_bonds': metrics_summary.get('chemical_metrics', {}).get('total_bonds', 0),
            'metrics_collection_rate': len(metrics_summary.get('metrics_collected', 0))
        }
        
        # Run anomaly detection on each metric
        for metric_name, value in metrics_to_analyze.items():
            self.anomaly_detector.add_metric(metric_name, value, timestamp)
            anomaly_result = self.anomaly_detector.detect_anomaly(metric_name, value)
            
            if anomaly_result['is_anomaly']:
                self.logger.warning(
                    f"Anomaly detected in {metric_name}",
                    metric_name=metric_name,
                    current_value=value,
                    z_score=anomaly_result.get('z_score', 0),
                    confidence=anomaly_result.get('confidence', 0),
                    event_category="anomaly_detection"
                )
                
                # Create dynamic alert for significant anomalies
                if anomaly_result.get('confidence', 0) > 0.8:
                    self._create_anomaly_alert(metric_name, value, anomaly_result)
    
    def _create_anomaly_alert(self, metric_name: str, value: float, anomaly_result: Dict[str, Any]):
        """Create dynamic alert for detected anomaly"""
        alert_id = f"anomaly_{metric_name}_{int(time.time())}"
        
        alert = QuantumAlert(
            alert_id=alert_id,
            name=f"AI Detected Anomaly: {metric_name}",
            description=f"Anomaly detected in {metric_name} with confidence {anomaly_result.get('confidence', 0):.2%}",
            severity=AlertSeverity.WARNING,
            condition=f"{metric_name}_anomaly",
            threshold_value=anomaly_result.get('z_score', 0),
            comparison_operator=">",
            evaluation_window=60,
            quantum_context={
                'ai_generated': True,
                'anomaly_confidence': anomaly_result.get('confidence', 0),
                'detection_method': 'statistical_analysis'
            }
        )
        
        self.add_alert(alert)
    
    def _evaluate_alerts(self):
        """Evaluate all active alerts against current metrics"""
        current_metrics = self.metrics_collector.get_metrics_summary()
        
        for alert_id, alert in self.alerts.items():
            if not alert.enabled:
                continue
            
            try:
                # Evaluate alert condition
                should_trigger = self._evaluate_alert_condition(alert, current_metrics)
                
                # Check if alert is currently active
                is_active = alert_id in self.active_events
                
                if should_trigger and not is_active:
                    # Trigger new alert
                    self._trigger_alert(alert, current_metrics)
                elif not should_trigger and is_active:
                    # Resolve existing alert
                    self._resolve_alert(alert_id)
                    
            except Exception as e:
                self.logger.error(f"Error evaluating alert {alert_id}", exception=e)
    
    def _evaluate_alert_condition(self, alert: QuantumAlert, metrics: Dict[str, Any]) -> bool:
        """Evaluate if alert condition is met"""
        
        # Extract relevant metric value based on condition
        current_value = self._extract_metric_value(alert.condition, metrics)
        
        if current_value is None:
            return False
        
        # Apply comparison operator
        operators = {
            '>': lambda a, b: a > b,
            '<': lambda a, b: a < b,
            '>=': lambda a, b: a >= b,
            '<=': lambda a, b: a <= b,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b
        }
        
        op_func = operators.get(alert.comparison_operator)
        if not op_func:
            return False
        
        return op_func(current_value, alert.threshold_value)
    
    def _extract_metric_value(self, condition: str, metrics: Dict[str, Any]) -> Optional[float]:
        """Extract metric value from condition string"""
        
        # Simple mapping of condition strings to metric values
        # In production, this would be a more sophisticated query parser
        condition_mappings = {
            'quantum_coherence': lambda m: 0.85 + 0.1 * math.sin(time.time() / 100),  # Simulated
            'consciousness_level': lambda m: m.get('consciousness_state', {}).get('level', 1),
            'genetic_fitness': lambda m: m.get('genetic_metrics', {}).get('fitness_score', 0),
            'chemical_bonds_broken_rate': lambda m: abs(hash(str(time.time())) % 10),  # Simulated
            'error_rate': lambda m: 0.01 + 0.02 * math.sin(time.time() / 200)  # Simulated
        }
        
        for pattern, extractor in condition_mappings.items():
            if pattern in condition:
                try:
                    return float(extractor(metrics))
                except:
                    return None
        
        return None
    
    def _trigger_alert(self, alert: QuantumAlert, metrics: Dict[str, Any]):
        """Trigger alert and create event"""
        event_id = f"{alert.alert_id}_{int(time.time())}"
        current_value = self._extract_metric_value(alert.condition, metrics) or 0.0
        
        alert_event = AlertEvent(
            event_id=event_id,
            alert=alert,
            triggered_at=datetime.now(timezone.utc),
            current_value=current_value,
            quantum_state=metrics.get('consciousness_state', {})
        )
        
        self.active_events[alert.alert_id] = alert_event
        self.alert_history.append(alert_event)
        
        # Log alert trigger
        self.logger.critical(
            f"ALERT TRIGGERED: {alert.name}",
            alert_id=alert.alert_id,
            severity=alert.severity.value,
            current_value=current_value,
            threshold=alert.threshold_value,
            event_category="alert_triggered"
        )
        
        # Schedule notifications
        self._schedule_notifications(alert_event)
    
    def _resolve_alert(self, alert_id: str):
        """Resolve active alert"""
        if alert_id not in self.active_events:
            return
        
        alert_event = self.active_events[alert_id]
        alert_event.resolved_at = datetime.now(timezone.utc)
        
        # Remove from active events
        del self.active_events[alert_id]
        
        # Log resolution
        self.logger.info(
            f"ALERT RESOLVED: {alert_event.alert.name}",
            alert_id=alert_id,
            duration_seconds=(alert_event.resolved_at - alert_event.triggered_at).total_seconds(),
            event_category="alert_resolved"
        )
    
    def _schedule_notifications(self, alert_event: AlertEvent):
        """Schedule notifications for alert event"""
        for channel in alert_event.alert.channels:
            if channel in self.notification_handlers:
                try:
                    # Call notification handler asynchronously
                    threading.Thread(
                        target=self.notification_handlers[channel],
                        args=(alert_event,),
                        daemon=True
                    ).start()
                except Exception as e:
                    self.logger.error(f"Failed to send notification via {channel.value}", exception=e)
    
    def _process_notifications(self):
        """Process pending notifications"""
        # This would handle notification queuing, rate limiting, escalation
        # For now, just mark all events as notified
        for event in self.active_events.values():
            if not event.notification_sent:
                event.notification_sent = True
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get comprehensive monitoring system status"""
        current_health = self.health_history[-1] if self.health_history else None
        
        return {
            'hive_id': self.hive_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'monitoring_active': self._monitoring_active,
            'current_health': asdict(current_health) if current_health else None,
            'active_alerts': len(self.active_events),
            'total_alerts_configured': len(self.alerts),
            'alert_history_count': len(self.alert_history),
            'ai_anomaly_detection': self.enable_ai_anomaly_detection,
            'notification_channels': list(self.notification_handlers.keys()),
            'recent_events': [
                {
                    'alert_name': event.alert.name,
                    'severity': event.alert.severity.value,
                    'triggered_at': event.triggered_at.isoformat(),
                    'resolved': event.resolved_at is not None
                }
                for event in list(self.alert_history)[-10:]  # Last 10 events
            ]
        }

# Example notification handlers
def email_notification_handler(alert_event: AlertEvent):
    """Example email notification handler"""
    print(f"📧 EMAIL ALERT: {alert_event.alert.name}")
    print(f"   Severity: {alert_event.alert.severity.value}")
    print(f"   Value: {alert_event.current_value}")
    print(f"   Triggered: {alert_event.triggered_at}")

def slack_notification_handler(alert_event: AlertEvent):
    """Example Slack notification handler"""
    severity_emoji = {
        AlertSeverity.INFO: "ℹ️",
        AlertSeverity.WARNING: "⚠️", 
        AlertSeverity.CRITICAL: "🚨",
        AlertSeverity.EMERGENCY: "🆘"
    }
    
    emoji = severity_emoji.get(alert_event.alert.severity, "❓")
    print(f"{emoji} SLACK ALERT: {alert_event.alert.name}")
    print(f"   Current: {alert_event.current_value} | Threshold: {alert_event.alert.threshold_value}")

# Example usage and testing
if __name__ == "__main__":
    async def test_monitoring_suite():
        from quantum_metrics_collector import QuantumMetricsCollector
        from deployment.logging.structured_logger import create_quantum_logger
        
        print("🔬 Testing Quantum Monitoring Suite...")
        
        # Initialize components
        metrics_collector = QuantumMetricsCollector(
            hive_id="test_monitoring_hive",
            prometheus_port=9094,
            collection_interval=5.0
        )
        
        quantum_logger = create_quantum_logger(
            hive_id="test_monitoring_hive",
            component="monitoring_suite"
        )
        
        # Initialize monitoring suite
        monitoring = QuantumMonitoringSuite(
            hive_id="test_monitoring_hive",
            metrics_collector=metrics_collector,
            quantum_logger=quantum_logger,
            enable_ai_anomaly_detection=True
        )
        
        # Register notification handlers
        monitoring.register_notification_handler(
            MonitoringChannel.EMAIL,
            email_notification_handler
        )
        monitoring.register_notification_handler(
            MonitoringChannel.SLACK,
            slack_notification_handler
        )
        
        # Start monitoring
        metrics_collector.start_collection()
        await monitoring.start_monitoring()
        
        print("📊 Monitoring suite started!")
        print("⏰ Running for 60 seconds to demonstrate alerts and health tracking...")
        
        try:
            # Run monitoring demonstration
            for i in range(12):  # 60 seconds total
                await asyncio.sleep(5)
                
                # Get monitoring status
                status = monitoring.get_monitoring_status()
                current_health = status.get('current_health')
                
                print(f"\n📈 Monitoring Cycle {i+1}/12:")
                if current_health:
                    print(f"   Overall Health: {current_health['overall_score']:.3f}")
                    print(f"   Coherence: {current_health['coherence_health']:.3f}")
                    print(f"   Consciousness: {current_health['consciousness_health']:.3f}")
                print(f"   Active Alerts: {status['active_alerts']}")
                print(f"   Total Events: {status['alert_history_count']}")
                
                # Show recommendations if any
                if current_health and current_health.get('recommendations'):
                    print(f"   💡 Recommendations: {len(current_health['recommendations'])}")
        
        except KeyboardInterrupt:
            print("\n🛑 Stopping monitoring...")
        
        finally:
            monitoring.stop_monitoring()
            metrics_collector.stop_collection()
            print("✅ Monitoring suite test completed!")
    
    # Run the test
    asyncio.run(test_monitoring_suite())