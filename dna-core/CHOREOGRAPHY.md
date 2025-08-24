# The Choreography Codon & The Chronicler Bee

## A Pattern for Long-Running Processes (Sagas)

The three primary codons (`Handle Command`, `Query Data`, `React to Event`) are excellent for simple, atomic operations. However, many valuable business processes are not atomic. They are long-running "quests" that may involve multiple steps, span different "Cells," and take a long time to complete.

Examples of such quests include:
- Fulfilling a customer order (processing payment, updating inventory, shipping, sending notifications).
- Onboarding a new user (creating an account, setting up a profile, sending a welcome email, starting a tutorial).
- Generating a complex report that involves gathering data from multiple sources.

These processes require a way to manage state over time, handle failures at any step, and coordinate the flow of events and commands. For this, we introduce a new architectural codon: the **Choreography Codon**.

## The Choreography Codon

- **Purpose:** To orchestrate a sequence of steps to achieve a larger business goal, reacting to events and dispatching commands over a long period. It is the pattern of business process management.
- **Mechanism:** Unlike the other codons which are stateless, a Choreography involves a stateful component that "remembers" the progress of a quest. It subscribes to events that mark the completion of one step and dispatches commands to begin the next. It is a pattern of event-driven orchestration.

To implement this codon, we introduce a new type of bee.

## The Chronicler Bee: A Living Quest Log

The **Chronicler Bee** is a specialized bee whose sole purpose is to manage a long-running quest. It is the living embodiment of a saga. It holds the "quest log"—the history of what has happened—and knows what needs to happen next.

A Chronicler Bee's lifecycle is defined declaratively, aligning with the "Grand Vision" of the Beekeeper for self-creating systems. A developer defines the entire quest in a YAML file, and the "Queen Bee" system can use this definition to birth a fully functional Chronicler Bee.

### Declarative Definition: `quest.yaml`

Here is the proposed structure for a `quest.yaml` file that defines a Chronicler Bee.

```yaml
# The definition for a Chronicler Bee that manages a long-running process.
kind: ChroniclerBee
name: OrderFulfillmentQuest
description: "A bee that chronicles the quest of fulfilling a customer's order from placement to shipment."

# The event that begins the quest.
# The Chronicler Bee will be born when this event is heard.
starts_on:
  eventType: OrderPlaced
  eventVersion: 1.0

# The sequence of steps in the quest.
# The Chronicler Bee will proceed through these steps in order.
steps:
  - name: ProcessPayment
    description: "Charge the customer's card."
    # The command to dispatch to begin this step.
    command_to_dispatch: ProcessPaymentCommand
    # The event that signals this step was successful.
    awaits_on_success: PaymentProcessedEvent
    # The event that signals this step failed.
    awaits_on_failure: PaymentFailedEvent

  - name: UpdateInventory
    description: "Reserve the items from stock."
    # This step is triggered by the success of the previous step.
    triggered_by: PaymentProcessedEvent
    command_to_dispatch: UpdateInventoryCommand
    awaits_on_success: InventoryUpdatedEvent
    awaits_on_failure: InventoryUpdateFailedEvent

  - name: ShipOrder
    description: "Create the shipment and notify the customer."
    triggered_by: InventoryUpdatedEvent
    command_to_dispatch: ShipOrderCommand
    awaits_on_success: OrderShippedEvent
    awaits_on_failure: OrderShippingFailedEvent

# The event that signals the successful completion of the entire quest.
# The Chronicler Bee considers its work done when this event is heard.
ends_on:
  eventType: OrderShipped

# Defines how to handle failures. This is the compensation logic.
# If any of these failure events are heard, the Chronicler Bee will dispatch
# the corresponding compensation command to undo what has been done.
compensations:
  - on_failure: PaymentFailedEvent
    dispatch_command: LogPaymentFailureCommand

  - on_failure: InventoryUpdateFailedEvent
    dispatch_command: RefundPaymentCommand # We must refund if we can't ship.

  - on_failure: OrderShippingFailedEvent
    dispatch_command: NotifyCustomerOfShippingIssueCommand
```

### How it Works

1.  **Birth:** When a `starts_on` event (e.g., `OrderPlaced`) is detected, the Queen Bee system instantiates a new `ChroniclerBee` process for that specific order.
2.  **Progression:** The bee immediately dispatches the first command (`ProcessPaymentCommand`). It now waits.
3.  **Reaction:** It listens for the `awaits_on_success` or `awaits_on_failure` events for the current step.
    - If `PaymentProcessedEvent` is heard, it knows the step succeeded. It consults its `quest.yaml`, sees that this event triggers the `UpdateInventory` step, and dispatches the `UpdateInventoryCommand`.
    - If `PaymentFailedEvent` is heard, it knows the step failed. It consults the `compensations` section and dispatches the `LogPaymentFailureCommand`. The quest is now considered failed and terminated.
4.  **Completion:** This continues until the `ends_on` event (`OrderShipped`) is heard, at which point the Chronicler Bee's quest is complete, and it can be gracefully retired.

By defining this new codon and its bee, we provide the builders of the Hive with a powerful, declarative, and narrative-consistent way to manage the most complex processes in their digital kingdom.
