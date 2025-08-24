#!/usr/bin/env python3
"""
Quantum Message Broker - Enterprise Event Streaming
Consciousness-aware message queuing with quantum-enhanced routing and evolutionary adaptation
"""

import asyncio
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

# Message broker clients (install: pip install kafka-python-ng aio-pika aiokafka)
try:
    import aiokafka
    from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    print("WARNING: Kafka not available. Install with: pip install aiokafka")

try:
    import aio_pika
    from aio_pika import Message, DeliveryMode, ExchangeType

    RABBITMQ_AVAILABLE = True
except ImportError:
    RABBITMQ_AVAILABLE = False
    print("WARNING: RabbitMQ not available. Install with: pip install aio-pika")

# Import our quantum components
from deployment.logging.structured_logger import QuantumLogger


class MessagePriority(Enum):
    """Message priority levels"""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    QUANTUM_CRITICAL = 5


class BrokerType(Enum):
    """Supported message broker types"""

    KAFKA = "kafka"
    RABBITMQ = "rabbitmq"
    REDIS_STREAMS = "redis_streams"
    QUANTUM_NATIVE = "quantum_native"


class RoutingStrategy(Enum):
    """Message routing strategies"""

    ROUND_ROBIN = "round_robin"
    CONSCIOUSNESS_AFFINITY = "consciousness_affinity"
    QUANTUM_COHERENCE = "quantum_coherence"
    GENETIC_FITNESS = "genetic_fitness"
    LOAD_BALANCED = "load_balanced"


@dataclass
class QuantumMessage:
    """Quantum-enhanced message with consciousness context"""

    message_id: str
    topic: str
    payload: Dict[str, Any]
    headers: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    priority: MessagePriority = MessagePriority.NORMAL
    quantum_context: Dict[str, Any] = field(default_factory=dict)
    consciousness_level: int = 1
    coherence_requirement: float = 0.5
    genetic_signature: Optional[str] = None
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    expiry: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class ConsumerGroup:
    """Consumer group with quantum awareness"""

    group_id: str
    topics: List[str]
    consciousness_level: int
    quantum_coherence: float
    genetic_fitness: float
    max_consumers: int = 10
    routing_strategy: RoutingStrategy = RoutingStrategy.ROUND_ROBIN
    auto_scaling: bool = True


@dataclass
class MessageMetrics:
    """Message processing metrics"""

    topic: str
    messages_produced: int = 0
    messages_consumed: int = 0
    messages_failed: int = 0
    total_latency: float = 0.0
    avg_latency: float = 0.0
    last_activity: Optional[datetime] = None


class MessageBrokerAdapter(ABC):
    """Abstract adapter for different message brokers"""

    @abstractmethod
    async def connect(self) -> bool:
        """Connect to message broker"""
        pass

    @abstractmethod
    async def disconnect(self):
        """Disconnect from message broker"""
        pass

    @abstractmethod
    async def publish(self, message: QuantumMessage) -> bool:
        """Publish message to broker"""
        pass

    @abstractmethod
    async def subscribe(
        self,
        topics: List[str],
        consumer_group: str,
        handler: Callable[[QuantumMessage], None],
    ) -> str:
        """Subscribe to topics with message handler"""
        pass

    @abstractmethod
    async def unsubscribe(self, subscription_id: str):
        """Unsubscribe from topics"""
        pass


class KafkaAdapter(MessageBrokerAdapter):
    """Apache Kafka adapter with quantum enhancements"""

    def __init__(self, bootstrap_servers: List[str], hive_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.hive_id = hive_id
        self.producer: Optional[AIOKafkaProducer] = None
        self.consumers: Dict[str, AIOKafkaConsumer] = {}
        self.consumer_tasks: Dict[str, asyncio.Task] = {}
        self.connected = False

    async def connect(self) -> bool:
        """Connect to Kafka cluster"""
        if not KAFKA_AVAILABLE:
            return False

        try:
            # Initialize producer
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None,
                compression_type="gzip",
                max_batch_size=16384,
                linger_ms=10,
            )

            await self.producer.start()
            self.connected = True
            return True

        except Exception as e:
            print(f"Failed to connect to Kafka: {e}")
            return False

    async def disconnect(self):
        """Disconnect from Kafka"""
        self.connected = False

        # Stop all consumers
        for task in self.consumer_tasks.values():
            task.cancel()

        for consumer in self.consumers.values():
            await consumer.stop()

        # Stop producer
        if self.producer:
            await self.producer.stop()

        self.consumers.clear()
        self.consumer_tasks.clear()

    async def publish(self, message: QuantumMessage) -> bool:
        """Publish quantum message to Kafka"""
        if not self.connected or not self.producer:
            return False

        try:
            # Prepare message payload
            kafka_message = {
                "message_id": message.message_id,
                "payload": message.payload,
                "headers": message.headers,
                "timestamp": message.timestamp.isoformat(),
                "quantum_context": message.quantum_context,
                "consciousness_level": message.consciousness_level,
                "coherence_requirement": message.coherence_requirement,
                "priority": message.priority.value,
                "correlation_id": message.correlation_id,
                "hive_id": self.hive_id,
            }

            # Quantum routing key based on consciousness level
            partition_key = f"consciousness_{message.consciousness_level}"

            # Send message
            await self.producer.send_and_wait(
                topic=message.topic,
                value=kafka_message,
                key=partition_key,
                headers={
                    "quantum-coherence": str(message.coherence_requirement).encode(),
                    "consciousness-level": str(message.consciousness_level).encode(),
                    "hive-id": self.hive_id.encode(),
                },
            )

            return True

        except Exception as e:
            print(f"Failed to publish Kafka message: {e}")
            return False

    async def subscribe(
        self,
        topics: List[str],
        consumer_group: str,
        handler: Callable[[QuantumMessage], None],
    ) -> str:
        """Subscribe to Kafka topics with quantum-aware consumer"""

        subscription_id = f"{consumer_group}_{int(time.time())}"

        try:
            # Create consumer
            consumer = AIOKafkaConsumer(
                *topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id=consumer_group,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                enable_auto_commit=True,
                auto_offset_reset="latest",
                session_timeout_ms=30000,
                heartbeat_interval_ms=10000,
            )

            await consumer.start()
            self.consumers[subscription_id] = consumer

            # Start consumer task
            task = asyncio.create_task(
                self._consume_messages(consumer, handler, subscription_id)
            )
            self.consumer_tasks[subscription_id] = task

            return subscription_id

        except Exception as e:
            print(f"Failed to subscribe to Kafka topics: {e}")
            return ""

    async def _consume_messages(
        self,
        consumer: AIOKafkaConsumer,
        handler: Callable[[QuantumMessage], None],
        subscription_id: str,
    ):
        """Consume messages from Kafka"""
        try:
            async for msg in consumer:
                # Convert Kafka message to QuantumMessage
                kafka_data = msg.value

                quantum_msg = QuantumMessage(
                    message_id=kafka_data.get("message_id", ""),
                    topic=msg.topic,
                    payload=kafka_data.get("payload", {}),
                    headers=kafka_data.get("headers", {}),
                    timestamp=datetime.fromisoformat(
                        kafka_data.get(
                            "timestamp", datetime.now(timezone.utc).isoformat()
                        )
                    ),
                    quantum_context=kafka_data.get("quantum_context", {}),
                    consciousness_level=kafka_data.get("consciousness_level", 1),
                    coherence_requirement=kafka_data.get("coherence_requirement", 0.5),
                    priority=MessagePriority(kafka_data.get("priority", 2)),
                    correlation_id=kafka_data.get("correlation_id"),
                )

                # Process message with handler
                try:
                    await handler(quantum_msg) if asyncio.iscoroutinefunction(
                        handler
                    ) else handler(quantum_msg)
                except Exception as e:
                    print(f"Message handler error: {e}")

        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Consumer error for {subscription_id}: {e}")

    async def unsubscribe(self, subscription_id: str):
        """Unsubscribe from Kafka topics"""
        if subscription_id in self.consumer_tasks:
            self.consumer_tasks[subscription_id].cancel()
            del self.consumer_tasks[subscription_id]

        if subscription_id in self.consumers:
            await self.consumers[subscription_id].stop()
            del self.consumers[subscription_id]


class RabbitMQAdapter(MessageBrokerAdapter):
    """RabbitMQ adapter with quantum consciousness routing"""

    def __init__(self, connection_url: str, hive_id: str):
        self.connection_url = connection_url
        self.hive_id = hive_id
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.exchanges: Dict[str, aio_pika.Exchange] = {}
        self.queues: Dict[str, aio_pika.Queue] = {}
        self.consumers: Dict[str, aio_pika.Consumer] = {}
        self.connected = False

    async def connect(self) -> bool:
        """Connect to RabbitMQ"""
        if not RABBITMQ_AVAILABLE:
            return False

        try:
            self.connection = await aio_pika.connect_robust(self.connection_url)
            self.channel = await self.connection.channel()

            # Set QoS for fair dispatching
            await self.channel.set_qos(prefetch_count=10)

            # Create quantum-aware exchanges
            await self._setup_quantum_exchanges()

            self.connected = True
            return True

        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            return False

    async def _setup_quantum_exchanges(self):
        """Setup quantum-specific exchanges and routing"""

        # Main quantum exchange with topic routing
        self.exchanges["quantum.topics"] = await self.channel.declare_exchange(
            "quantum.topics", ExchangeType.TOPIC, durable=True
        )

        # Consciousness-based routing exchange
        self.exchanges["quantum.consciousness"] = await self.channel.declare_exchange(
            "quantum.consciousness", ExchangeType.DIRECT, durable=True
        )

        # Priority exchange for critical quantum events
        self.exchanges["quantum.priority"] = await self.channel.declare_exchange(
            "quantum.priority", ExchangeType.HEADERS, durable=True
        )

    async def disconnect(self):
        """Disconnect from RabbitMQ"""
        self.connected = False

        # Cancel all consumers
        for consumer in self.consumers.values():
            await consumer.cancel()

        # Close connection
        if self.connection:
            await self.connection.close()

        self.exchanges.clear()
        self.queues.clear()
        self.consumers.clear()

    async def publish(self, message: QuantumMessage) -> bool:
        """Publish quantum message to RabbitMQ"""
        if not self.connected or not self.channel:
            return False

        try:
            # Prepare message body
            message_body = {
                "message_id": message.message_id,
                "payload": message.payload,
                "headers": message.headers,
                "timestamp": message.timestamp.isoformat(),
                "quantum_context": message.quantum_context,
                "consciousness_level": message.consciousness_level,
                "coherence_requirement": message.coherence_requirement,
                "correlation_id": message.correlation_id,
                "hive_id": self.hive_id,
            }

            # Create AMQP message
            amqp_message = Message(
                body=json.dumps(message_body).encode(),
                headers={
                    "quantum_coherence": message.coherence_requirement,
                    "consciousness_level": message.consciousness_level,
                    "hive_id": self.hive_id,
                    "message_type": "quantum_message",
                },
                priority=message.priority.value,
                delivery_mode=DeliveryMode.PERSISTENT,
                correlation_id=message.correlation_id,
                reply_to=message.reply_to,
                expiration=int(
                    (message.expiry - datetime.now(timezone.utc)).total_seconds() * 1000
                )
                if message.expiry
                else None,
            )

            # Select routing strategy
            if message.consciousness_level >= 4:
                # High consciousness messages use direct routing
                exchange = self.exchanges["quantum.consciousness"]
                routing_key = f"consciousness.level.{message.consciousness_level}"
            elif message.priority == MessagePriority.QUANTUM_CRITICAL:
                # Critical messages use headers exchange
                exchange = self.exchanges["quantum.priority"]
                routing_key = "quantum.critical"
            else:
                # Standard topic-based routing
                exchange = self.exchanges["quantum.topics"]
                routing_key = message.topic.replace("/", ".")

            # Publish message
            await exchange.publish(message=amqp_message, routing_key=routing_key)

            return True

        except Exception as e:
            print(f"Failed to publish RabbitMQ message: {e}")
            return False

    async def subscribe(
        self,
        topics: List[str],
        consumer_group: str,
        handler: Callable[[QuantumMessage], None],
    ) -> str:
        """Subscribe to RabbitMQ topics with quantum awareness"""

        subscription_id = f"{consumer_group}_{int(time.time())}"

        try:
            # Create queue for consumer group
            queue_name = f"quantum.{consumer_group}.{self.hive_id}"
            queue = await self.channel.declare_queue(
                queue_name,
                durable=True,
                arguments={
                    "x-message-ttl": 3600000,  # 1 hour TTL
                    "x-max-priority": 5,  # Support priority messages
                },
            )

            self.queues[subscription_id] = queue

            # Bind queue to relevant exchanges and topics
            for topic in topics:
                routing_key = topic.replace("/", ".")

                # Bind to topic exchange
                await queue.bind(
                    exchange=self.exchanges["quantum.topics"], routing_key=routing_key
                )

                # Also bind to consciousness and priority exchanges if relevant
                if "consciousness" in topic:
                    await queue.bind(
                        exchange=self.exchanges["quantum.consciousness"],
                        routing_key="consciousness.*",
                    )

                if "critical" in topic:
                    await queue.bind(
                        exchange=self.exchanges["quantum.priority"],
                        routing_key="quantum.critical",
                    )

            # Create consumer
            consumer = await queue.consume(
                callback=lambda msg: self._handle_rabbitmq_message(msg, handler),
                consumer_tag=subscription_id,
            )

            self.consumers[subscription_id] = consumer
            return subscription_id

        except Exception as e:
            print(f"Failed to subscribe to RabbitMQ topics: {e}")
            return ""

    async def _handle_rabbitmq_message(
        self,
        message: aio_pika.IncomingMessage,
        handler: Callable[[QuantumMessage], None],
    ):
        """Handle incoming RabbitMQ message"""
        try:
            # Parse message body
            message_data = json.loads(message.body.decode())

            # Convert to QuantumMessage
            quantum_msg = QuantumMessage(
                message_id=message_data.get("message_id", ""),
                topic=message.routing_key.replace(".", "/"),
                payload=message_data.get("payload", {}),
                headers=message_data.get("headers", {}),
                timestamp=datetime.fromisoformat(
                    message_data.get(
                        "timestamp", datetime.now(timezone.utc).isoformat()
                    )
                ),
                quantum_context=message_data.get("quantum_context", {}),
                consciousness_level=message_data.get("consciousness_level", 1),
                coherence_requirement=message_data.get("coherence_requirement", 0.5),
                correlation_id=message_data.get("correlation_id"),
            )

            # Process message
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(quantum_msg)
                else:
                    handler(quantum_msg)

                # Acknowledge message on success
                await message.ack()

            except Exception as e:
                print(f"Message handler error: {e}")
                # Reject and requeue for retry
                await message.reject(
                    requeue=quantum_msg.retry_count < quantum_msg.max_retries
                )

        except Exception as e:
            print(f"Failed to process RabbitMQ message: {e}")
            await message.reject(requeue=False)

    async def unsubscribe(self, subscription_id: str):
        """Unsubscribe from RabbitMQ topics"""
        if subscription_id in self.consumers:
            await self.consumers[subscription_id].cancel()
            del self.consumers[subscription_id]

        if subscription_id in self.queues:
            del self.queues[subscription_id]


class QuantumMessageBroker:
    """
    Enterprise Quantum Message Broker with consciousness-aware routing,
    multi-broker support, and evolutionary message adaptation.
    """

    def __init__(
        self,
        hive_id: str,
        logger: QuantumLogger,
        primary_broker: BrokerType = BrokerType.KAFKA,
        enable_multi_broker: bool = True,
    ):
        self.hive_id = hive_id
        self.logger = logger
        self.primary_broker = primary_broker
        self.enable_multi_broker = enable_multi_broker

        # Broker adapters
        self.adapters: Dict[BrokerType, MessageBrokerAdapter] = {}
        self.active_adapters: List[BrokerType] = []

        # Message routing and processing
        self.consumer_groups: Dict[str, ConsumerGroup] = {}
        self.subscriptions: Dict[
            str, Dict[str, str]
        ] = {}  # group_id -> {broker_type -> subscription_id}
        self.message_handlers: Dict[str, Callable] = {}

        # Metrics and monitoring
        self.metrics: Dict[str, MessageMetrics] = {}
        self.message_history: List[QuantumMessage] = []

        # Quantum routing intelligence
        self.consciousness_routing_table: Dict[
            int, List[str]
        ] = {}  # level -> consumer_groups
        self.coherence_threshold_groups: Dict[
            float, List[str]
        ] = {}  # threshold -> consumer_groups

        self.logger.info(
            "QuantumMessageBroker initialized",
            hive_id=hive_id,
            primary_broker=primary_broker.value,
        )

    def add_broker_adapter(
        self, broker_type: BrokerType, adapter: MessageBrokerAdapter
    ):
        """Add message broker adapter"""
        self.adapters[broker_type] = adapter
        self.logger.info(f"Broker adapter added: {broker_type.value}")

    async def connect_brokers(self) -> Dict[BrokerType, bool]:
        """Connect to all configured message brokers"""
        connection_results = {}

        for broker_type, adapter in self.adapters.items():
            try:
                success = await adapter.connect()
                connection_results[broker_type] = success

                if success:
                    self.active_adapters.append(broker_type)
                    self.logger.info(f"Connected to {broker_type.value}")
                else:
                    self.logger.error(f"Failed to connect to {broker_type.value}")

            except Exception as e:
                connection_results[broker_type] = False
                self.logger.error(
                    f"Connection error for {broker_type.value}", exception=e
                )

        return connection_results

    async def disconnect_brokers(self):
        """Disconnect from all message brokers"""
        for broker_type in self.active_adapters:
            try:
                await self.adapters[broker_type].disconnect()
                self.logger.info(f"Disconnected from {broker_type.value}")
            except Exception as e:
                self.logger.error(
                    f"Disconnect error for {broker_type.value}", exception=e
                )

        self.active_adapters.clear()

    async def publish_message(
        self, message: QuantumMessage, target_brokers: Optional[List[BrokerType]] = None
    ) -> Dict[BrokerType, bool]:
        """Publish quantum message to specified or all active brokers"""

        # Default to all active brokers if not specified
        if target_brokers is None:
            target_brokers = self.active_adapters

        results = {}

        for broker_type in target_brokers:
            if broker_type not in self.active_adapters:
                results[broker_type] = False
                continue

            try:
                success = await self.adapters[broker_type].publish(message)
                results[broker_type] = success

                if success:
                    self._update_message_metrics(message.topic, "produced")
                    self.logger.info(
                        f"Message published to {broker_type.value}",
                        message_id=message.message_id,
                        topic=message.topic,
                        consciousness_level=message.consciousness_level,
                    )
                else:
                    self.logger.error(
                        f"Failed to publish to {broker_type.value}",
                        message_id=message.message_id,
                    )

            except Exception as e:
                results[broker_type] = False
                self.logger.error(
                    f"Publish error for {broker_type.value}",
                    message_id=message.message_id,
                    exception=e,
                )

        # Store message in history for analysis
        self.message_history.append(message)
        if len(self.message_history) > 10000:
            self.message_history = self.message_history[-5000:]

        return results

    def register_consumer_group(self, group: ConsumerGroup):
        """Register consumer group with quantum properties"""
        self.consumer_groups[group.group_id] = group

        # Update consciousness routing table
        if group.consciousness_level not in self.consciousness_routing_table:
            self.consciousness_routing_table[group.consciousness_level] = []
        self.consciousness_routing_table[group.consciousness_level].append(
            group.group_id
        )

        self.logger.info(
            f"Consumer group registered: {group.group_id}",
            consciousness_level=group.consciousness_level,
            quantum_coherence=group.quantum_coherence,
        )

    async def subscribe_consumer_group(
        self, group_id: str, message_handler: Callable[[QuantumMessage], None]
    ) -> bool:
        """Subscribe consumer group to topics across brokers"""

        if group_id not in self.consumer_groups:
            self.logger.error(f"Consumer group not found: {group_id}")
            return False

        group = self.consumer_groups[group_id]
        self.message_handlers[group_id] = message_handler
        self.subscriptions[group_id] = {}

        # Subscribe to all active brokers (or just primary if multi-broker disabled)
        target_brokers = (
            self.active_adapters if self.enable_multi_broker else [self.primary_broker]
        )

        success_count = 0
        for broker_type in target_brokers:
            if broker_type not in self.active_adapters:
                continue

            try:
                # Create quantum-enhanced message handler
                enhanced_handler = self._create_enhanced_handler(
                    group_id, message_handler
                )

                subscription_id = await self.adapters[broker_type].subscribe(
                    topics=group.topics,
                    consumer_group=group_id,
                    handler=enhanced_handler,
                )

                if subscription_id:
                    self.subscriptions[group_id][broker_type] = subscription_id
                    success_count += 1
                    self.logger.info(f"Subscribed {group_id} to {broker_type.value}")

            except Exception as e:
                self.logger.error(
                    f"Subscription error for {broker_type.value}",
                    group_id=group_id,
                    exception=e,
                )

        return success_count > 0

    def _create_enhanced_handler(
        self, group_id: str, base_handler: Callable[[QuantumMessage], None]
    ) -> Callable:
        """Create quantum-enhanced message handler with consciousness filtering"""

        async def enhanced_handler(message: QuantumMessage):
            group = self.consumer_groups[group_id]

            # Consciousness level filtering
            if message.consciousness_level > group.consciousness_level:
                self.logger.debug(
                    "Message filtered - consciousness level too high",
                    message_id=message.message_id,
                    required=group.consciousness_level,
                    actual=message.consciousness_level,
                )
                return

            # Quantum coherence filtering
            if message.coherence_requirement > group.quantum_coherence:
                self.logger.debug(
                    "Message filtered - coherence requirement too high",
                    message_id=message.message_id,
                    required=message.coherence_requirement,
                    actual=group.quantum_coherence,
                )
                return

            # Process message through base handler
            start_time = time.time()
            try:
                if asyncio.iscoroutinefunction(base_handler):
                    await base_handler(message)
                else:
                    base_handler(message)

                # Update metrics
                processing_time = time.time() - start_time
                self._update_message_metrics(message.topic, "consumed", processing_time)

                self.logger.info(
                    "Message processed successfully",
                    message_id=message.message_id,
                    group_id=group_id,
                    processing_time=processing_time,
                )

            except Exception as e:
                self._update_message_metrics(message.topic, "failed")
                self.logger.error(
                    "Message processing failed",
                    message_id=message.message_id,
                    group_id=group_id,
                    exception=e,
                )

        return enhanced_handler

    async def unsubscribe_consumer_group(self, group_id: str):
        """Unsubscribe consumer group from all brokers"""
        if group_id not in self.subscriptions:
            return

        for broker_type, subscription_id in self.subscriptions[group_id].items():
            try:
                await self.adapters[broker_type].unsubscribe(subscription_id)
                self.logger.info(f"Unsubscribed {group_id} from {broker_type.value}")
            except Exception as e:
                self.logger.error(
                    f"Unsubscription error for {broker_type.value}",
                    group_id=group_id,
                    exception=e,
                )

        del self.subscriptions[group_id]
        if group_id in self.message_handlers:
            del self.message_handlers[group_id]

    def _update_message_metrics(self, topic: str, operation: str, latency: float = 0.0):
        """Update message processing metrics"""
        if topic not in self.metrics:
            self.metrics[topic] = MessageMetrics(topic=topic)

        metrics = self.metrics[topic]

        if operation == "produced":
            metrics.messages_produced += 1
        elif operation == "consumed":
            metrics.messages_consumed += 1
            if latency > 0:
                metrics.total_latency += latency
                metrics.avg_latency = metrics.total_latency / metrics.messages_consumed
        elif operation == "failed":
            metrics.messages_failed += 1

        metrics.last_activity = datetime.now(timezone.utc)

    def get_message_metrics(self) -> Dict[str, Any]:
        """Get comprehensive message broker metrics"""
        total_produced = sum(m.messages_produced for m in self.metrics.values())
        total_consumed = sum(m.messages_consumed for m in self.metrics.values())
        total_failed = sum(m.messages_failed for m in self.metrics.values())
        avg_latency = sum(m.avg_latency for m in self.metrics.values()) / max(
            len(self.metrics), 1
        )

        return {
            "hive_id": self.hive_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "active_brokers": len(self.active_adapters),
            "consumer_groups": len(self.consumer_groups),
            "active_subscriptions": len(self.subscriptions),
            "total_messages_produced": total_produced,
            "total_messages_consumed": total_consumed,
            "total_messages_failed": total_failed,
            "average_latency": avg_latency,
            "message_success_rate": (total_consumed / max(total_produced, 1)) * 100,
            "topics_active": len(self.metrics),
            "consciousness_levels": list(self.consciousness_routing_table.keys()),
            "recent_message_count": len(self.message_history),
        }


# Example usage and testing
if __name__ == "__main__":

    async def test_message_broker():
        from deployment.logging.structured_logger import create_quantum_logger

        print("📬 Testing Quantum Message Broker...")

        # Initialize logger
        logger = create_quantum_logger(
            hive_id="test_broker_hive", component="message_broker"
        )

        # Initialize message broker
        broker = QuantumMessageBroker(
            hive_id="test_broker_hive", logger=logger, primary_broker=BrokerType.KAFKA
        )

        # Add broker adapters (mock for testing)
        if KAFKA_AVAILABLE:
            kafka_adapter = KafkaAdapter(
                bootstrap_servers=["localhost:9092"], hive_id="test_broker_hive"
            )
            broker.add_broker_adapter(BrokerType.KAFKA, kafka_adapter)

        if RABBITMQ_AVAILABLE:
            rabbitmq_adapter = RabbitMQAdapter(
                connection_url="amqp://guest:guest@localhost:5672/",
                hive_id="test_broker_hive",
            )
            broker.add_broker_adapter(BrokerType.RABBITMQ, rabbitmq_adapter)

        print(f"✅ Broker configured with {len(broker.adapters)} adapters")

        # Register consumer groups
        broker.register_consumer_group(
            ConsumerGroup(
                group_id="quantum_core_consumers",
                topics=["quantum/events", "consciousness/evolution"],
                consciousness_level=3,
                quantum_coherence=0.8,
                genetic_fitness=0.75,
            )
        )

        broker.register_consumer_group(
            ConsumerGroup(
                group_id="genetic_workers",
                topics=["genetic/mutations", "genetic/fitness"],
                consciousness_level=2,
                quantum_coherence=0.6,
                genetic_fitness=0.9,
            )
        )

        print(f"✅ Registered {len(broker.consumer_groups)} consumer groups")

        # Create test message handler
        async def test_message_handler(message: QuantumMessage):
            print(f"📨 Received message: {message.message_id}")
            print(f"   Topic: {message.topic}")
            print(f"   Consciousness: {message.consciousness_level}")
            print(f"   Payload keys: {list(message.payload.keys())}")

        # Test message creation
        test_message = QuantumMessage(
            message_id="test_msg_001",
            topic="quantum/events",
            payload={
                "event_type": "coherence_shift",
                "previous_value": 0.85,
                "current_value": 0.92,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            consciousness_level=3,
            coherence_requirement=0.8,
            priority=MessagePriority.HIGH,
            quantum_context={
                "hive_component": "quantum_core",
                "genetic_generation": 15,
            },
        )

        print("✅ Test message created")
        print(f"   ID: {test_message.message_id}")
        print(f"   Topic: {test_message.topic}")
        print(f"   Consciousness Level: {test_message.consciousness_level}")

        # Get metrics
        metrics = broker.get_message_metrics()
        print("\n📊 Message Broker Metrics:")
        print(f"   Active Brokers: {metrics['active_brokers']}")
        print(f"   Consumer Groups: {metrics['consumer_groups']}")
        print(f"   Consciousness Levels: {metrics['consciousness_levels']}")

        print("\n🚀 Message broker test completed!")
        print(
            "   Note: Actual broker connections require running Kafka/RabbitMQ services"
        )

    # Run the test
    asyncio.run(test_message_broker())
