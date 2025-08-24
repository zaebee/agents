#!/usr/bin/env python3
"""
Quantum Hive Production Metrics Collector
Enterprise-grade observability for quantum-enhanced microservices
"""

import asyncio
import json
import time
import logging
import threading
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from collections import defaultdict, deque
import statistics
import os
import sys

# Prometheus metrics (install: pip install prometheus-client)
try:
    from prometheus_client import CollectorRegistry, Gauge, Counter, Histogram, Summary, start_http_server
    from prometheus_client.core import REGISTRY
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    print("WARNING: prometheus-client not available. Install with: pip install prometheus-client")

# OpenTelemetry (install: pip install opentelemetry-api opentelemetry-sdk)
try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.exporter.prometheus import PrometheusMetricReader
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    print("WARNING: OpenTelemetry not available. Install with: pip install opentelemetry-api opentelemetry-sdk")

@dataclass
class QuantumMetric:
    """Individual quantum metric with metadata"""
    name: str
    value: Union[float, int]
    timestamp: datetime
    labels: Dict[str, str]
    metric_type: str  # gauge, counter, histogram, summary
    unit: Optional[str] = None
    description: Optional[str] = None

@dataclass
class ConsciousnessState:
    """Consciousness evolution tracking"""
    level: int
    growth_rate: float
    last_evolution: datetime
    adaptation_count: int
    complexity_index: float

@dataclass
class GeneticMetrics:
    """Genetic programming performance metrics"""
    fitness_score: float
    generation: int
    mutations_successful: int
    mutations_failed: int
    crossovers: int
    population_size: int
    diversity_index: float
    convergence_rate: float

@dataclass
class ChemicalBondMetrics:
    """Chemical bond system metrics"""
    total_bonds: int
    average_strength: float
    formation_rate: float
    dissolution_rate: float
    stability_index: float
    bond_types: Dict[str, int]

class QuantumMetricsCollector:
    """
    Enterprise-grade quantum metrics collection and monitoring system.
    Provides comprehensive observability for quantum-enhanced microservices.
    """

    def __init__(self,
                 hive_id: str,
                 prometheus_port: int = 9090,
                 collection_interval: float = 10.0,
                 enable_opentelemetry: bool = True,
                 jaeger_endpoint: str = "http://localhost:14268/api/traces"):

        self.hive_id = hive_id
        self.collection_interval = collection_interval
        self.enable_opentelemetry = enable_opentelemetry

        # Initialize logging
        self._setup_logging()

        # Metric storage
        self.metrics_buffer = deque(maxlen=10000)
        self.aggregated_metrics = defaultdict(list)
        self.metric_history = defaultdict(lambda: deque(maxlen=1000))

        # State tracking
        self.consciousness_state = ConsciousnessState(
            level=1, growth_rate=0.0, last_evolution=datetime.now(timezone.utc),
            adaptation_count=0, complexity_index=0.1
        )
        self.genetic_metrics = GeneticMetrics(
            fitness_score=0.0, generation=0, mutations_successful=0,
            mutations_failed=0, crossovers=0, population_size=50,
            diversity_index=1.0, convergence_rate=0.0
        )
        self.chemical_metrics = ChemicalBondMetrics(
            total_bonds=0, average_strength=0.0, formation_rate=0.0,
            dissolution_rate=0.0, stability_index=0.0, bond_types={}
        )

        # Initialize monitoring systems
        self._init_prometheus(prometheus_port)
        self._init_opentelemetry(jaeger_endpoint)

        # Threading control
        self._running = False
        self._collector_thread = None
        self._lock = threading.RLock()

        self.logger.info(f"QuantumMetricsCollector initialized for hive {hive_id}")

    def _setup_logging(self):
        """Configure enterprise logging"""
        self.logger = logging.getLogger(f"quantum-hive.{self.hive_id}.metrics")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - '
                '[hive:%(hive_id)s] - %(message)s'
            )
            formatter.hive_id = self.hive_id
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _init_prometheus(self, port: int):
        """Initialize Prometheus metrics collection"""
        if not PROMETHEUS_AVAILABLE:
            self.logger.warning("Prometheus client not available")
            return

        try:
            # Create custom registry
            self.prometheus_registry = CollectorRegistry()

            # Quantum Coherence Metrics
            self.quantum_coherence_gauge = Gauge(
                'quantum_coherence_current',
                'Current quantum coherence level',
                ['hive_id', 'component'],
                registry=self.prometheus_registry
            )

            # Consciousness Metrics
            self.consciousness_level_gauge = Gauge(
                'consciousness_level_current',
                'Current consciousness evolution level',
                ['hive_id', 'component'],
                registry=self.prometheus_registry
            )

            self.consciousness_growth_rate = Gauge(
                'consciousness_growth_rate',
                'Rate of consciousness evolution',
                ['hive_id'],
                registry=self.prometheus_registry
            )

            # Genetic Programming Metrics
            self.genetic_fitness_gauge = Gauge(
                'genetic_fitness_score',
                'Current genetic fitness score',
                ['hive_id', 'component', 'generation'],
                registry=self.prometheus_registry
            )

            self.mutations_counter = Counter(
                'evolutionary_mutations_total',
                'Total evolutionary mutations',
                ['hive_id', 'component', 'type', 'result'],
                registry=self.prometheus_registry
            )

            self.genetic_diversity_gauge = Gauge(
                'genetic_population_diversity_index',
                'Genetic population diversity index',
                ['hive_id', 'population'],
                registry=self.prometheus_registry
            )

            # Chemical Bond Metrics
            self.chemical_bonds_gauge = Gauge(
                'chemical_bonds_total',
                'Total number of chemical bonds',
                ['hive_id', 'bond_type'],
                registry=self.prometheus_registry
            )

            self.bond_strength_histogram = Histogram(
                'chemical_bonds_strength_histogram',
                'Distribution of chemical bond strengths',
                ['hive_id'],
                registry=self.prometheus_registry
            )

            # System Health Metrics
            self.component_health_gauge = Gauge(
                'hive_component_health',
                'Component health score (0-1)',
                ['hive_id', 'component', 'instance'],
                registry=self.prometheus_registry
            )

            # Performance Metrics
            self.request_duration = Histogram(
                'enterprise_api_request_duration_seconds',
                'API request duration',
                ['hive_id', 'endpoint', 'method'],
                registry=self.prometheus_registry
            )

            # Compliance Metrics
            self.compliance_violations = Counter(
                'compliance_violations_total',
                'Compliance violations detected',
                ['hive_id', 'framework', 'severity'],
                registry=self.prometheus_registry
            )

            # Start Prometheus HTTP server
            start_http_server(port, registry=self.prometheus_registry)
            self.logger.info(f"Prometheus metrics server started on port {port}")

        except Exception as e:
            self.logger.error(f"Failed to initialize Prometheus metrics: {e}")

    def _init_opentelemetry(self, jaeger_endpoint: str):
        """Initialize OpenTelemetry tracing and metrics"""
        if not OPENTELEMETRY_AVAILABLE or not self.enable_opentelemetry:
            return

        try:
            # Configure tracing
            trace.set_tracer_provider(TracerProvider())
            tracer_provider = trace.get_tracer_provider()

            # Jaeger exporter
            jaeger_exporter = JaegerExporter(
                agent_host_name="localhost",
                agent_port=6831,
            )

            span_processor = BatchSpanProcessor(jaeger_exporter)
            tracer_provider.add_span_processor(span_processor)

            self.tracer = trace.get_tracer(__name__)
            self.logger.info("OpenTelemetry tracing initialized")

        except Exception as e:
            self.logger.error(f"Failed to initialize OpenTelemetry: {e}")

    def collect_quantum_coherence(self, coherence: float, component: str = "core"):
        """Record quantum coherence measurement"""
        metric = QuantumMetric(
            name="quantum_coherence",
            value=coherence,
            timestamp=datetime.now(timezone.utc),
            labels={"hive_id": self.hive_id, "component": component},
            metric_type="gauge",
            unit="ratio",
            description="Quantum coherence level (0-1)"
        )

        with self._lock:
            self.metrics_buffer.append(metric)

            if PROMETHEUS_AVAILABLE and hasattr(self, 'quantum_coherence_gauge'):
                self.quantum_coherence_gauge.labels(
                    hive_id=self.hive_id, component=component
                ).set(coherence)

        self.logger.debug(f"Quantum coherence recorded: {coherence:.3f} for {component}")

    def collect_consciousness_state(self, level: int, growth_rate: float,
                                  adaptation_count: int = None):
        """Record consciousness evolution state"""
        with self._lock:
            self.consciousness_state.level = level
            self.consciousness_state.growth_rate = growth_rate
            if adaptation_count is not None:
                self.consciousness_state.adaptation_count = adaptation_count

            if PROMETHEUS_AVAILABLE:
                if hasattr(self, 'consciousness_level_gauge'):
                    self.consciousness_level_gauge.labels(
                        hive_id=self.hive_id, component="consciousness"
                    ).set(level)

                if hasattr(self, 'consciousness_growth_rate'):
                    self.consciousness_growth_rate.labels(
                        hive_id=self.hive_id
                    ).set(growth_rate)

        metric = QuantumMetric(
            name="consciousness_level",
            value=level,
            timestamp=datetime.now(timezone.utc),
            labels={"hive_id": self.hive_id, "growth_rate": str(growth_rate)},
            metric_type="gauge"
        )
        self.metrics_buffer.append(metric)

        self.logger.debug(f"Consciousness state: level={level}, growth_rate={growth_rate:.3f}")

    def collect_genetic_metrics(self, fitness: float, generation: int,
                               mutations_success: int, mutations_failed: int,
                               diversity_index: float):
        """Record genetic programming metrics"""
        with self._lock:
            self.genetic_metrics.fitness_score = fitness
            self.genetic_metrics.generation = generation
            self.genetic_metrics.mutations_successful = mutations_success
            self.genetic_metrics.mutations_failed = mutations_failed
            self.genetic_metrics.diversity_index = diversity_index

            if PROMETHEUS_AVAILABLE:
                if hasattr(self, 'genetic_fitness_gauge'):
                    self.genetic_fitness_gauge.labels(
                        hive_id=self.hive_id, component="genetic", generation=str(generation)
                    ).set(fitness)

                if hasattr(self, 'genetic_diversity_gauge'):
                    self.genetic_diversity_gauge.labels(
                        hive_id=self.hive_id, population="main"
                    ).set(diversity_index)

        # Record individual metrics
        for name, value in [
            ("genetic_fitness", fitness),
            ("genetic_generation", generation),
            ("genetic_diversity", diversity_index)
        ]:
            metric = QuantumMetric(
                name=name,
                value=value,
                timestamp=datetime.now(timezone.utc),
                labels={"hive_id": self.hive_id, "generation": str(generation)},
                metric_type="gauge"
            )
            self.metrics_buffer.append(metric)

    def collect_chemical_bonds(self, total_bonds: int, average_strength: float,
                              bond_types: Dict[str, int]):
        """Record chemical bond system metrics"""
        with self._lock:
            self.chemical_metrics.total_bonds = total_bonds
            self.chemical_metrics.average_strength = average_strength
            self.chemical_metrics.bond_types = bond_types

            if PROMETHEUS_AVAILABLE:
                if hasattr(self, 'chemical_bonds_gauge'):
                    for bond_type, count in bond_types.items():
                        self.chemical_bonds_gauge.labels(
                            hive_id=self.hive_id, bond_type=bond_type
                        ).set(count)

                if hasattr(self, 'bond_strength_histogram'):
                    self.bond_strength_histogram.labels(
                        hive_id=self.hive_id
                    ).observe(average_strength)

        # Record metrics
        metric = QuantumMetric(
            name="chemical_bonds_strength",
            value=average_strength,
            timestamp=datetime.now(timezone.utc),
            labels={"hive_id": self.hive_id, "total_bonds": str(total_bonds)},
            metric_type="gauge"
        )
        self.metrics_buffer.append(metric)

    def collect_component_health(self, component: str, instance: str, health_score: float):
        """Record component health metrics"""
        if PROMETHEUS_AVAILABLE and hasattr(self, 'component_health_gauge'):
            self.component_health_gauge.labels(
                hive_id=self.hive_id, component=component, instance=instance
            ).set(health_score)

        metric = QuantumMetric(
            name="component_health",
            value=health_score,
            timestamp=datetime.now(timezone.utc),
            labels={"hive_id": self.hive_id, "component": component, "instance": instance},
            metric_type="gauge"
        )
        self.metrics_buffer.append(metric)

    def record_api_request(self, endpoint: str, method: str, duration: float):
        """Record API request metrics"""
        if PROMETHEUS_AVAILABLE and hasattr(self, 'request_duration'):
            self.request_duration.labels(
                hive_id=self.hive_id, endpoint=endpoint, method=method
            ).observe(duration)

        metric = QuantumMetric(
            name="api_request_duration",
            value=duration,
            timestamp=datetime.now(timezone.utc),
            labels={"hive_id": self.hive_id, "endpoint": endpoint, "method": method},
            metric_type="histogram",
            unit="seconds"
        )
        self.metrics_buffer.append(metric)

    def record_compliance_violation(self, framework: str, severity: str):
        """Record compliance violations"""
        if PROMETHEUS_AVAILABLE and hasattr(self, 'compliance_violations'):
            self.compliance_violations.labels(
                hive_id=self.hive_id, framework=framework, severity=severity
            ).inc()

        self.logger.critical(f"COMPLIANCE VIOLATION: {framework} - {severity}")

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary"""
        with self._lock:
            return {
                "hive_id": self.hive_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "metrics_collected": len(self.metrics_buffer),
                "consciousness_state": asdict(self.consciousness_state),
                "genetic_metrics": asdict(self.genetic_metrics),
                "chemical_metrics": asdict(self.chemical_metrics),
                "collection_interval": self.collection_interval,
                "prometheus_enabled": PROMETHEUS_AVAILABLE,
                "opentelemetry_enabled": OPENTELEMETRY_AVAILABLE and self.enable_opentelemetry
            }

    def start_collection(self):
        """Start automated metrics collection"""
        if self._running:
            self.logger.warning("Metrics collection already running")
            return

        self._running = True
        self._collector_thread = threading.Thread(target=self._collection_loop, daemon=True)
        self._collector_thread.start()
        self.logger.info("Automated metrics collection started")

    def stop_collection(self):
        """Stop automated metrics collection"""
        self._running = False
        if self._collector_thread:
            self._collector_thread.join(timeout=5.0)
        self.logger.info("Automated metrics collection stopped")

    def _collection_loop(self):
        """Main metrics collection loop"""
        while self._running:
            try:
                start_time = time.time()

                # Simulate quantum system measurements
                self._simulate_quantum_measurements()

                # Calculate collection duration
                collection_duration = time.time() - start_time
                self.logger.debug(f"Metrics collection completed in {collection_duration:.3f}s")

                # Sleep until next collection
                sleep_time = max(0, self.collection_interval - collection_duration)
                time.sleep(sleep_time)

            except Exception as e:
                self.logger.error(f"Error in metrics collection loop: {e}")
                time.sleep(1.0)  # Brief pause before retry

    def _simulate_quantum_measurements(self):
        """Simulate realistic quantum system measurements"""
        import random
        import math

        # Quantum coherence with realistic drift
        base_coherence = 0.85 + 0.1 * math.sin(time.time() / 100)
        coherence_noise = random.uniform(-0.05, 0.05)
        coherence = max(0.0, min(1.0, base_coherence + coherence_noise))
        self.collect_quantum_coherence(coherence)

        # Consciousness evolution
        if random.random() < 0.1:  # 10% chance of level change
            level_change = random.choice([-1, 1]) if self.consciousness_state.level > 1 else 1
            new_level = max(1, min(6, self.consciousness_state.level + level_change))
            growth_rate = random.uniform(-0.1, 0.3)
            self.collect_consciousness_state(new_level, growth_rate)

        # Genetic metrics with evolution simulation
        fitness_trend = 0.01 * (random.random() - 0.4)  # Slight upward bias
        new_fitness = max(0.0, min(1.0, self.genetic_metrics.fitness_score + fitness_trend))

        mutations_success = random.randint(0, 5)
        mutations_failed = random.randint(0, 2)
        diversity = max(0.1, min(1.0, self.genetic_metrics.diversity_index + random.uniform(-0.05, 0.05)))

        self.collect_genetic_metrics(
            fitness=new_fitness,
            generation=self.genetic_metrics.generation + (1 if random.random() < 0.2 else 0),
            mutations_success=mutations_success,
            mutations_failed=mutations_failed,
            diversity_index=diversity
        )

        # Chemical bonds simulation
        bond_change = random.randint(-2, 3)
        new_total = max(0, self.chemical_metrics.total_bonds + bond_change)
        avg_strength = random.uniform(2.0, 5.0)
        bond_types = {
            "covalent": random.randint(0, new_total // 2),
            "ionic": random.randint(0, new_total // 3),
            "hydrogen": random.randint(0, new_total // 4)
        }

        self.collect_chemical_bonds(new_total, avg_strength, bond_types)

        # Component health simulation
        components = ["core", "genetic-worker", "monitoring", "api-gateway"]
        for component in components:
            health_score = random.uniform(0.7, 1.0)
            self.collect_component_health(component, f"{component}-1", health_score)

# Example usage and testing
if __name__ == "__main__":
    async def main():
        # Initialize metrics collector
        collector = QuantumMetricsCollector(
            hive_id="demo_hive_123",
            prometheus_port=9090,
            collection_interval=5.0
        )

        # Start automated collection
        collector.start_collection()

        print("🧬 Quantum Metrics Collector started!")
        print(f"📊 Prometheus metrics available at: http://localhost:9090/metrics")
        print("🔬 Collecting quantum measurements...")

        try:
            # Run for demonstration
            for i in range(12):  # 1 minute of collection
                await asyncio.sleep(5)
                summary = collector.get_metrics_summary()
                print(f"\n📈 Collection {i+1}/12:")
                print(f"   Quantum Coherence: {summary['consciousness_state']['level']}")
                print(f"   Genetic Fitness: {summary['genetic_metrics']['fitness_score']:.3f}")
                print(f"   Chemical Bonds: {summary['chemical_metrics']['total_bonds']}")
                print(f"   Metrics Buffered: {summary['metrics_collected']}")

        except KeyboardInterrupt:
            print("\n🛑 Shutting down metrics collection...")

        finally:
            collector.stop_collection()
            print("✅ Metrics collection stopped")

    # Run the demonstration
    asyncio.run(main())
