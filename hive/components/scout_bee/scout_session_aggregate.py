import uuid
import shutil
from datetime import datetime, timezone
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp
from dna_core.pollen_protocol_pb2 import PollenEnvelope
from dna_core.royal_jelly import Aggregate

# Import this component's primitives
from .scout_repository_command import ScoutRepositoryCommand
from .scout_api_command import ScoutApiCommand
from .http_connector import HttpConnector
from .git_hub_connector import GitHubConnector
from .open_api_transformer import OpenApiTransformer
from .repository_transformer import RepositoryTransformer
from .source_file_transformer import SourceFileTransformer

class ScoutSessionAggregate(Aggregate):
    """
    The aggregate for the scout-bee component.
    It orchestrates the scouting of external resources.
    """

    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        # Initialize connectors and transformers
        self.http_connector = HttpConnector()
        self.github_connector = GitHubConnector()
        self.openapi_transformer = OpenApiTransformer()
        self.repo_transformer = RepositoryTransformer()
        self.source_file_transformer = SourceFileTransformer()
        # State
        self.report = None
        self.status = "INITIALIZED"

    def handle_command(self, command):
        """Handles the incoming command."""
        if isinstance(command, ScoutRepositoryCommand):
            self._handle_scout_repository(command)
        elif isinstance(command, ScoutApiCommand):
            self._handle_scout_api(command)
        else:
            print(f"Warning: Unhandled command type {type(command)}")

    def _handle_scout_api(self, command: ScoutApiCommand):
        """Orchestrates the scouting of an OpenAPI specification."""
        print(f"--- Scout Bee received command to scout API: {command.url} ---")
        try:
            raw_content = self.http_connector.fetch(command.url)
            report_data = self.openapi_transformer.transform(raw_content)
            self._print_api_report(report_data)
            self._record_report_event(report_data)
        except Exception as e:
            print(f"An error occurred during API scouting: {e}")
            self.status = "FAILED"

    def _handle_scout_repository(self, command: ScoutRepositoryCommand):
        """Orchestrates the scouting of a GitHub repository."""
        print(f"--- Scout Bee received command to scout repo: {command.url} ---")
        temp_dir = None
        try:
            temp_dir = self.github_connector.clone(command.url, command.github_token)

            discovered_components = {"aggregates": [], "transformations": [], "connectors": []}

            for filepath in self.repo_transformer.transform(temp_dir):
                file_components = self.source_file_transformer.transform(filepath)
                for key in discovered_components:
                    discovered_components[key].extend(file_components[key])

            report_data = {
                "repository": command.url,
                "components": discovered_components
            }
            self._print_repo_report(report_data)
            self._record_report_event(report_data)

        except Exception as e:
            print(f"An error occurred during repository scouting: {e}")
            self.status = "FAILED"
        finally:
            if temp_dir:
                print("\nScouting mission complete. Cleaning up temporary files.")
                shutil.rmtree(temp_dir)

    def _print_api_report(self, report: dict):
        """Prints a formatted report for an API scan."""
        print("\n--- OpenAPI Scout Bee Report ---")
        print("="*20)
        print(f"API Title: {report['title']}")
        print(f"Version: {report['version']}")
        print(f"Description: {report['description']}")
        print("="*20)
        print("\nEndpoints Discovered:")
        if not report['endpoints']:
            print("No paths found in the specification.")
            return
        for endpoint in report['endpoints']:
            print(f"\n--- Path: {endpoint['path']} ---")
            print(f"  - Method: {endpoint['method']}")
            print(f"    Summary: {endpoint['summary']}")
            if endpoint['parameters']:
                print("    Parameters:")
                for param in endpoint['parameters']:
                     print(f"      - [{param['in']}] {param['name']}: {param['description']}")
            if endpoint['request_body']:
                print("    Request Body: Yes")

    def _print_repo_report(self, report: dict):
        """Prints a formatted report for a repository scan."""
        print("\n--- GitHub Scout Bee Report ---")
        print(f"Repository: {report['repository']}")
        print("\nDiscovered Potential ATCG Components:")
        for comp_type, comp_list in report['components'].items():
            if comp_list:
                print(f"\n  {comp_type.replace('_', ' ').title()}:")
                for item in sorted(list(set(comp_list))):
                    print(f"    - {item}")

    def _record_report_event(self, report_data: dict):
        """Creates and records a ScoutingReportGeneratedEvent."""
        payload_struct = Struct()
        payload_struct.update(report_data)
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.now(timezone.utc))

        event = PollenEnvelope(
            event_id=str(uuid.uuid4()),
            event_type="ScoutingReportGeneratedEvent",
            event_version="1.0",
            aggregate_id=self.id,
            timestamp=timestamp,
            payload=payload_struct,
        )
        self._record_event(event)

    def _apply_event(self, event: PollenEnvelope) -> None:
        """Applies an event to the aggregate's state."""
        if event.event_type == "ScoutingReportGeneratedEvent":
            self.report = dict(event.payload)
            self.status = "COMPLETED"
            print(f"\nApplied {event.event_type} to aggregate {self.id}. Status is now {self.status}.")
        else:
            print(f"Warning: Unhandled event type {event.event_type}")
