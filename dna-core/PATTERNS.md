# The DNA Core: ATCG Primitives

This document defines the four fundamental, language-agnostic patterns that form the "genetic code" of all components in our Hive. Every service, regardless of its implementation language, will be composed of these primitives.

---

## A = Aggregate

*   **Concept:** An Aggregate is a cluster of associated objects that we treat as a single unit for the purpose of data changes. It is the fundamental building block of our domain logic.
*   **Purpose:** To enforce consistency. All business rules and invariants for a given concept are enforced within its Aggregate. Changes to any object within the Aggregate boundary are coordinated through a single entry point, the "Aggregate Root".
*   **Conceptual Interface:**
    *   `id`: A unique identifier.
    *   `state`: The internal data of the aggregate.
    *   `execute(command)`: Receives a command object and applies business logic. Returns a list of generated Domain Events.
    *   `apply(event)`: Mutates the aggregate's state in response to a Domain Event. This is the only way state should change.
*   **Example in a Cell:** In the `OrderCell`, an `Order` would be an Aggregate. It would contain `OrderLine` objects. You can't add an `OrderLine` directly; you must call `Order.addItem(item, quantity)`, which enforces business rules (e.g., "cannot add more than 10 of any item").

---

## T = Transformation

*   **Concept:** A pure, stateless function or domain service that encapsulates business logic that doesn't naturally fit within a single Aggregate.
*   **Purpose:** To perform calculations, transformations, or coordinate between multiple Aggregates without holding any state of its own.
*   **Conceptual Interface:**
    *   `process(input)`: Receives some input data (e.g., one or more Aggregates, values) and returns a result. It has no side effects.
*   **Example in a Cell:** A `ShippingCostCalculator` Transformation might take an `Order` Aggregate and a `User` Aggregate as input and return a shipping cost. It doesn't change either Aggregate; it just performs a calculation based on their state.

---

## C = Connector

*   **Concept:** A Connector is an adapter that handles communication between a Cell and the outside world. It is an implementation of a "Port" in Hexagonal Architecture.
*   **Purpose:** To translate external protocols and data formats into the language of our domain (Commands and Events), and vice-versa. This isolates our core logic from the details of infrastructure.
*   **Conceptual Interface:**
    *   **Inbound Connector:** `listen()`: Starts listening for external input (e.g., an HTTP request, a message queue event). When input is received, it translates it into a domain `Command` and sends it to an `Aggregate`.
    *   **Outbound Connector:** `publish(event)`: Receives a `Domain Event` from an Aggregate and translates it into an external format (e.g., a JSON message published to a queue, an email).
*   **Example in a Cell:** A `RestApiConnector` listens for HTTP requests. A `DatabaseConnector` translates repository calls into SQL.

---

## G = Genesis Event

*   **Concept:** A Domain Event. It is an immutable record of something significant that has happened within the domain.
*   **Purpose:** To capture all state changes in the system as a sequence of events. Aggregates generate events, and these events are the source of truth for state changes. They are also used for communication between Cells.
*   **Conceptual Interface:**
    *   `eventId`: A unique identifier for the event instance.
    *   `timestamp`: When the event occurred.
    *   `eventName`: The type of the event (e.g., "OrderPlaced", "StockLevelLow").
    *   `payload`: The data associated with the event.
*   **Example in a Cell:** When an `Order` Aggregate is successfully processed, it generates an `OrderPlaced` event. This event is then used to update the Order's own state and is also published by an outbound `Connector` to notify the `ShippingCell`.
