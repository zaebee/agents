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

---
---

# The Book of Codons: Architectural Patterns

The ATCG Primitives are the "letters" of our genetic alphabet. The **Codons** are the "words" they spell. These are the three fundamental patterns that every Cell uses to interact with the world and perform its duties.

## 1. The "Handle Command" Codon (`C -> A -> G`)

*   **Purpose:** To change the state of the system in a safe and consistent way. This is the only pattern that should result in a state change.
*   **Sequence:**
    1.  An inbound **C**onnector receives an external request (e.g., an HTTP POST).
    2.  It translates the request into a domain `Command` object.
    3.  It passes the `Command` to the appropriate **A**ggregate.
    4.  The **A**ggregate validates the `Command` against its internal business rules.
    5.  If valid, the **A**ggregate produces one or more **G**enesis Events.
    6.  These **G**enesis Events are the only things that can mutate the **A**ggregate's internal state.
    7.  The Events are returned to the **C**onnector, which may publish them on an event bus.
*   **Conceptual Interface (`ICommandHandler`):** `handle(command): Promise<GenesisEvent[]>`

## 2. The "Query Data" Codon (`C -> T -> C`)

*   **Purpose:** To read and project the state of the system for a specific use case, without changing any state.
*   **Sequence:**
    1.  An inbound **C**onnector receives a request for data (e.g., an HTTP GET).
    2.  It calls a stateless **T**ransformation function.
    3.  The **T**ransformation gathers data from one or more sources (e.g., a read-optimized database, another Cell's API).
    4.  It transforms the raw data into a specific Data Transfer Object (DTO) tailored for the requester.
    5.  The DTO is passed back through an outbound **C**onnector.
*   **Conceptual Interface (`IQueryHandler`):** `handle(query): Promise<DTO>`

## 3. The "React to Event" Codon (`G -> C -> A -> G`)

*   **Purpose:** To allow Cells to react to changes in other parts of the system, enabling choreography and asynchronous workflows.
*   **Sequence:**
    1.  A listening **C**onnector is subscribed to a specific type of **G**enesis Event from an event bus.
    2.  When it receives a relevant Event, it translates it into a domain `Command`.
    3.  It passes the `Command` to an **A**ggregate within its own Cell.
    4.  This triggers the "Handle Command" codon within the receiving Cell, which may produce its own new **G**enesis Events.
*   **Conceptual Interface (`IEventHandler`):** `handle(event): Promise<void>`

## 4. The "Immune Response" Codon (`G -> C -> A -> C`)

*   **Purpose:** To create a self-healing system that can react to errors or "mutations" and issue corrective commands.
*   **Note:** This is an advanced pattern. The full doctrine, including the Taxonomy of Mutations and the different types of Immune Cells, is detailed in the `IMMUNITY.md` document.
*   **Conceptual Interface (`IImmuneHandler`):** `handle(mutationEvent): Promise<CorrectiveCommand>`
