import uuid
from .command import HelloHiveCommand
from .aggregate import HelloHiveAggregate


class HelloHiveConnector:
    """
    The connector for the hello-hive component.
    It translates external requests into domain commands.
    """

    def process_request(self, data: dict) -> None:
        """
        Simulates processing an external request.
        """
        # In a real app, this data would come from an HTTP request, a message queue, etc.
        print(f"Connector received request for hello-hive: {data}")

        # 1. Create the command
        command = HelloHiveCommand(payload=data)

        # 2. Create a new aggregate instance
        # In a real app, you might fetch an existing aggregate from a repository.
        aggregate_id = str(uuid.uuid4())
        aggregate = HelloHiveAggregate(aggregate_id)

        # 3. Handle the command
        aggregate.handle_command(command)

        # 4. Publish events
        # In a real app, an application service or repository would get the
        # uncommitted events from the aggregate and publish them on an event bus.
        uncommitted_events = aggregate.get_uncommitted_events()
        print(f"Events produced by aggregate: {uncommitted_events}")
        # event_bus.publish(uncommitted_events)
        aggregate.clear_uncommitted_events()

        print(f"HelloHive process complete. Aggregate ID: {aggregate.id}")
