#!/usr/bin/env python3
"""
Quantum Hive Structured Logging System
Enterprise-grade logging with quantum context awareness
"""

import logging
import logging.config
import sys
import traceback
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from contextlib import contextmanager
from threading import local

# Structured logging (install: pip install structlog python-json-logger)
try:
    import structlog
    from pythonjsonlogger import jsonlogger

    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False
    print(
        "WARNING: structlog not available. Install with: pip install structlog python-json-logger"
    )


@dataclass
class QuantumLogContext:
    """Quantum-specific logging context"""

    hive_id: str
    coherence_level: float
    consciousness_level: int
    component: str
    quantum_state: str = "active"
    genetic_generation: Optional[int] = None
    chemical_bonds: Optional[int] = None


@dataclass
class LogEntry:
    """Structured log entry with quantum context"""

    timestamp: str
    level: str
    message: str
    hive_id: str
    component: str
    quantum_context: Dict[str, Any]
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    extra_fields: Optional[Dict[str, Any]] = None


class QuantumContextFilter(logging.Filter):
    """Inject quantum context into log records"""

    def __init__(self, quantum_context: QuantumLogContext):
        super().__init__()
        self.quantum_context = quantum_context

    def filter(self, record):
        # Add quantum context to log record
        record.hive_id = self.quantum_context.hive_id
        record.coherence_level = self.quantum_context.coherence_level
        record.consciousness_level = self.quantum_context.consciousness_level
        record.component = self.quantum_context.component
        record.quantum_state = self.quantum_context.quantum_state

        if self.quantum_context.genetic_generation:
            record.genetic_generation = self.quantum_context.genetic_generation
        if self.quantum_context.chemical_bonds:
            record.chemical_bonds = self.quantum_context.chemical_bonds

        return True


class QuantumLogger:
    """
    Quantum-aware structured logger with enterprise features.
    Provides comprehensive logging with quantum system context.
    """

    def __init__(
        self,
        hive_id: str,
        component: str,
        log_level: str = "INFO",
        enable_structured_logging: bool = True,
        enable_json_output: bool = True,
        log_file: Optional[str] = None,
        max_file_size: int = 100 * 1024 * 1024,  # 100MB
        backup_count: int = 5,
    ):
        self.hive_id = hive_id
        self.component = component
        self.enable_structured_logging = enable_structured_logging
        self.enable_json_output = enable_json_output

        # Thread-local storage for context
        self._local = local()

        # Initialize quantum context
        self.quantum_context = QuantumLogContext(
            hive_id=hive_id,
            coherence_level=0.9,
            consciousness_level=1,
            component=component,
        )

        # Setup logging configuration
        self._setup_logging(log_level, log_file, max_file_size, backup_count)

        # Initialize structured logging if available
        if STRUCTLOG_AVAILABLE and enable_structured_logging:
            self._setup_structlog()

    def _setup_logging(
        self,
        log_level: str,
        log_file: Optional[str],
        max_file_size: int,
        backup_count: int,
    ):
        """Configure standard logging with quantum context"""

        # Create logger
        self.logger = logging.getLogger(f"quantum-hive.{self.hive_id}.{self.component}")
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Clear existing handlers
        self.logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)

        if self.enable_json_output:
            # JSON formatter for structured logging
            json_formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(name)s %(levelname)s %(hive_id)s %(component)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
            console_handler.setFormatter(json_formatter)
        else:
            # Standard formatter with quantum context
            standard_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - "
                "[hive:%(hive_id)s] [component:%(component)s] "
                "[coherence:%(coherence_level).3f] [consciousness:%(consciousness_level)d] "
                "- %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            console_handler.setFormatter(standard_formatter)

        # Add quantum context filter
        quantum_filter = QuantumContextFilter(self.quantum_context)
        console_handler.addFilter(quantum_filter)

        self.logger.addHandler(console_handler)

        # File handler if specified
        if log_file:
            from logging.handlers import RotatingFileHandler

            file_handler = RotatingFileHandler(
                log_file, maxBytes=max_file_size, backupCount=backup_count
            )
            file_handler.setFormatter(
                json_formatter if self.enable_json_output else standard_formatter
            )
            file_handler.addFilter(quantum_filter)
            self.logger.addHandler(file_handler)

    def _setup_structlog(self):
        """Configure structured logging with quantum processors"""

        def add_quantum_context(logger, method_name, event_dict):
            """Add quantum context to structured logs"""
            event_dict["hive_id"] = self.quantum_context.hive_id
            event_dict["component"] = self.quantum_context.component
            event_dict["coherence_level"] = self.quantum_context.coherence_level
            event_dict["consciousness_level"] = self.quantum_context.consciousness_level
            event_dict["quantum_state"] = self.quantum_context.quantum_state

            if self.quantum_context.genetic_generation:
                event_dict["genetic_generation"] = (
                    self.quantum_context.genetic_generation
                )
            if self.quantum_context.chemical_bonds:
                event_dict["chemical_bonds"] = self.quantum_context.chemical_bonds

            return event_dict

        def add_correlation_context(logger, method_name, event_dict):
            """Add correlation IDs from thread-local storage"""
            if hasattr(self._local, "correlation_id"):
                event_dict["correlation_id"] = self._local.correlation_id
            if hasattr(self._local, "request_id"):
                event_dict["request_id"] = self._local.request_id
            if hasattr(self._local, "trace_id"):
                event_dict["trace_id"] = self._local.trace_id

            return event_dict

        # Configure structlog
        structlog.configure(
            processors=[
                add_quantum_context,
                add_correlation_context,
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="ISO"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer(),
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        # Get structured logger
        self.struct_logger = structlog.get_logger(
            f"quantum-hive.{self.hive_id}.{self.component}"
        )

    def update_quantum_context(
        self,
        coherence_level: Optional[float] = None,
        consciousness_level: Optional[int] = None,
        quantum_state: Optional[str] = None,
        genetic_generation: Optional[int] = None,
        chemical_bonds: Optional[int] = None,
    ):
        """Update quantum context for logging"""

        if coherence_level is not None:
            self.quantum_context.coherence_level = coherence_level
        if consciousness_level is not None:
            self.quantum_context.consciousness_level = consciousness_level
        if quantum_state is not None:
            self.quantum_context.quantum_state = quantum_state
        if genetic_generation is not None:
            self.quantum_context.genetic_generation = genetic_generation
        if chemical_bonds is not None:
            self.quantum_context.chemical_bonds = chemical_bonds

    @contextmanager
    def correlation_context(
        self,
        correlation_id: str,
        request_id: str = None,
        trace_id: str = None,
        user_id: str = None,
    ):
        """Context manager for correlation tracking"""

        # Store previous values
        prev_correlation = getattr(self._local, "correlation_id", None)
        prev_request = getattr(self._local, "request_id", None)
        prev_trace = getattr(self._local, "trace_id", None)
        prev_user = getattr(self._local, "user_id", None)

        try:
            # Set new values
            self._local.correlation_id = correlation_id
            if request_id:
                self._local.request_id = request_id
            if trace_id:
                self._local.trace_id = trace_id
            if user_id:
                self._local.user_id = user_id

            yield

        finally:
            # Restore previous values
            if prev_correlation:
                self._local.correlation_id = prev_correlation
            elif hasattr(self._local, "correlation_id"):
                delattr(self._local, "correlation_id")

            if prev_request:
                self._local.request_id = prev_request
            elif hasattr(self._local, "request_id"):
                delattr(self._local, "request_id")

            if prev_trace:
                self._local.trace_id = prev_trace
            elif hasattr(self._local, "trace_id"):
                delattr(self._local, "trace_id")

            if prev_user:
                self._local.user_id = prev_user
            elif hasattr(self._local, "user_id"):
                delattr(self._local, "user_id")

    def info(self, message: str, **kwargs):
        """Log info level message with quantum context"""
        if STRUCTLOG_AVAILABLE and self.enable_structured_logging:
            self.struct_logger.info(message, **kwargs)
        else:
            self.logger.info(message, extra=kwargs)

    def debug(self, message: str, **kwargs):
        """Log debug level message with quantum context"""
        if STRUCTLOG_AVAILABLE and self.enable_structured_logging:
            self.struct_logger.debug(message, **kwargs)
        else:
            self.logger.debug(message, extra=kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning level message with quantum context"""
        if STRUCTLOG_AVAILABLE and self.enable_structured_logging:
            self.struct_logger.warning(message, **kwargs)
        else:
            self.logger.warning(message, extra=kwargs)

    def error(self, message: str, exception: Exception = None, **kwargs):
        """Log error level message with quantum context and exception details"""
        if exception:
            kwargs["exception_type"] = type(exception).__name__
            kwargs["exception_message"] = str(exception)
            kwargs["stack_trace"] = traceback.format_exc()

        if STRUCTLOG_AVAILABLE and self.enable_structured_logging:
            self.struct_logger.error(message, **kwargs)
        else:
            self.logger.error(message, extra=kwargs, exc_info=exception is not None)

    def critical(self, message: str, exception: Exception = None, **kwargs):
        """Log critical level message with quantum context"""
        if exception:
            kwargs["exception_type"] = type(exception).__name__
            kwargs["exception_message"] = str(exception)
            kwargs["stack_trace"] = traceback.format_exc()

        if STRUCTLOG_AVAILABLE and self.enable_structured_logging:
            self.struct_logger.critical(message, **kwargs)
        else:
            self.logger.critical(message, extra=kwargs, exc_info=exception is not None)

    def quantum_event(self, event_type: str, details: Dict[str, Any]):
        """Log quantum-specific events with structured data"""
        self.info(
            f"Quantum Event: {event_type}",
            event_type=event_type,
            quantum_details=details,
            event_category="quantum_system",
        )

    def genetic_evolution_log(
        self,
        generation: int,
        fitness_score: float,
        mutations: int,
        successful_adaptations: int,
    ):
        """Log genetic evolution events"""
        self.update_quantum_context(genetic_generation=generation)

        self.info(
            f"Genetic Evolution - Generation {generation}",
            generation=generation,
            fitness_score=fitness_score,
            mutations=mutations,
            successful_adaptations=successful_adaptations,
            event_category="genetic_programming",
        )

    def consciousness_evolution_log(
        self,
        old_level: int,
        new_level: int,
        trigger: str,
        adaptation_details: Dict[str, Any],
    ):
        """Log consciousness evolution events"""
        self.update_quantum_context(consciousness_level=new_level)

        self.info(
            f"Consciousness Evolution: Level {old_level} → {new_level}",
            old_consciousness_level=old_level,
            new_consciousness_level=new_level,
            evolution_trigger=trigger,
            adaptation_details=adaptation_details,
            event_category="consciousness_evolution",
        )

    def chemical_bond_log(
        self,
        bond_event: str,
        bond_count: int,
        bond_strength: float,
        bond_types: Dict[str, int],
    ):
        """Log chemical bond system events"""
        self.update_quantum_context(chemical_bonds=bond_count)

        self.info(
            f"Chemical Bond Event: {bond_event}",
            bond_event=bond_event,
            total_bonds=bond_count,
            average_strength=bond_strength,
            bond_types=bond_types,
            event_category="chemical_system",
        )

    def performance_log(
        self, operation: str, duration: float, success: bool, metrics: Dict[str, Any]
    ):
        """Log performance metrics with quantum context"""
        self.info(
            f"Performance: {operation}",
            operation=operation,
            duration_seconds=duration,
            success=success,
            performance_metrics=metrics,
            event_category="performance",
        )

    def security_log(self, event_type: str, severity: str, details: Dict[str, Any]):
        """Log security events with enhanced tracking"""
        log_method = getattr(self, severity.lower(), self.warning)

        log_method(
            f"Security Event: {event_type}",
            security_event_type=event_type,
            severity=severity,
            security_details=details,
            event_category="security",
            requires_investigation=severity in ["error", "critical"],
        )

    def compliance_log(
        self,
        framework: str,
        check_type: str,
        compliance_status: bool,
        violations: List[str],
    ):
        """Log compliance check results"""
        if not compliance_status:
            self.critical(
                f"COMPLIANCE VIOLATION: {framework} - {check_type}",
                compliance_framework=framework,
                check_type=check_type,
                violations=violations,
                event_category="compliance",
                immediate_action_required=True,
            )
        else:
            self.info(
                f"Compliance Check Passed: {framework} - {check_type}",
                compliance_framework=framework,
                check_type=check_type,
                event_category="compliance",
            )

    def audit_log(
        self,
        user_id: str,
        action: str,
        resource: str,
        result: str,
        additional_context: Dict[str, Any] = None,
    ):
        """Log audit trail events"""
        self.info(
            f"Audit: {action} on {resource} by {user_id} - {result}",
            audit_user_id=user_id,
            audit_action=action,
            audit_resource=resource,
            audit_result=result,
            audit_context=additional_context or {},
            event_category="audit",
            audit_timestamp=datetime.now(timezone.utc).isoformat(),
        )


# Factory function for creating quantum loggers
def create_quantum_logger(hive_id: str, component: str, **kwargs) -> QuantumLogger:
    """Factory function to create configured quantum logger"""
    return QuantumLogger(hive_id=hive_id, component=component, **kwargs)


# Example usage and testing
if __name__ == "__main__":
    import asyncio

    async def test_quantum_logger():
        # Create logger
        logger = create_quantum_logger(
            hive_id="test_hive_001",
            component="quantum_logger_test",
            log_level="DEBUG",
            enable_json_output=True,
        )

        print("🧬 Testing Quantum Logger...")

        # Basic logging
        logger.info("Quantum Hive logger initialized")
        logger.debug("Debug message with quantum context")
        logger.warning("Warning about quantum coherence drift")

        # Quantum context updates
        logger.update_quantum_context(
            coherence_level=0.87, consciousness_level=3, quantum_state="evolving"
        )

        # Correlation context
        with logger.correlation_context(
            correlation_id="corr-123-456",
            request_id="req-789",
            trace_id="trace-abc-def",
        ):
            logger.info("Message with correlation context")

            # Quantum-specific logging
            logger.quantum_event(
                "coherence_shift",
                {
                    "previous_coherence": 0.90,
                    "current_coherence": 0.87,
                    "drift_rate": -0.01,
                },
            )

        # Genetic evolution logging
        logger.genetic_evolution_log(
            generation=15, fitness_score=0.72, mutations=8, successful_adaptations=5
        )

        # Consciousness evolution logging
        logger.consciousness_evolution_log(
            old_level=2,
            new_level=3,
            trigger="adaptation_threshold",
            adaptation_details={"complexity_increase": 0.15},
        )

        # Chemical bond logging
        logger.chemical_bond_log(
            bond_event="formation",
            bond_count=47,
            bond_strength=3.8,
            bond_types={"covalent": 30, "ionic": 12, "hydrogen": 5},
        )

        # Performance logging
        logger.performance_log(
            operation="quantum_coherence_calculation",
            duration=0.023,
            success=True,
            metrics={"cpu_usage": 0.45, "memory_mb": 128},
        )

        # Security logging
        logger.security_log(
            event_type="authentication_attempt",
            severity="info",
            details={"user_id": "quantum_user_001", "success": True},
        )

        # Compliance logging
        logger.compliance_log(
            framework="SOC2",
            check_type="data_encryption",
            compliance_status=True,
            violations=[],
        )

        # Audit logging
        logger.audit_log(
            user_id="admin_001",
            action="quantum_coherence_adjustment",
            resource="hive_core_system",
            result="success",
            additional_context={"adjustment_value": 0.05},
        )

        # Error logging with exception
        try:
            raise ValueError("Simulated quantum calculation error")
        except Exception as e:
            logger.error("Quantum calculation failed", exception=e)

        print("✅ Quantum Logger test completed!")

    # Run the test
    asyncio.run(test_quantum_logger())
