import uuid
import shutil
from typing import Union
from dna_core.royal_jelly import Aggregate

# Import this component's primitives
from .scout_repository_command import ScoutRepositoryCommand
from .scout_api_command import ScoutApiCommand
from .scouting_report_generated_event import ScoutingReportGeneratedEvent
from .http_connector import HttpConnector
from .git_hub_connector import GitHubConnector
from .open_api_transformer import OpenApiTransformer
from .repository_transformer import RepositoryTransformer
from .source_file_transformer import SourceFileTransformer

# Define a Union type for the commands this aggregate can handle
TCommand = Union[ScoutRepositoryCommand, ScoutApiCommand]

class ScoutSessionAggregate(Aggregate[TCommand, ScoutingReportGeneratedEvent]):
    """
    The aggregate for the scout-bee component.
    It orchestrates the scouting of external resources.
    Element: A (Aggregate)
    """

    def __init__(self, aggregate_id: str):
        self.id = aggregate_id
        # Initialize connectors and transformers
        self.http_connector = HttpConnector()
        self.github_connector = GitHubConnector()
        self.openapi_transformer = OpenApiTransformer()
        self.repo_transformer = RepositoryTransformer()
        self.source_file_transformer = SourceFileTransformer()
        # State
        self.report = None
        self.status = "INITIALIZED"

    def handle(self, command: TCommand) -> ScoutingReportGeneratedEvent:
        """Handles the incoming command and returns the resulting event."""
        if isinstance(command, ScoutRepositoryCommand):
            report_data = self._handle_scout_repository(command)
        elif isinstance(command, ScoutApiCommand):
            report_data = self._handle_scout_api(command)
        else:
            raise TypeError(f"Unhandled command type: {type(command)}")

        event = ScoutingReportGeneratedEvent(
            aggregate_id=self.id,
            report=report_data
        )
        self._apply(event) # Apply the event to self
        return event

    def _handle_scout_api(self, command: ScoutApiCommand) -> dict:
        """Orchestrates the scouting of an OpenAPI specification."""
        print(f"--- Scout Bee received command to scout API: {command.url} ---")
        try:
            raw_content = self.http_connector.process(command.url)
            report_data = self.openapi_transformer.execute(raw_content)
            self._print_api_report(report_data)
            return report_data
        except Exception as e:
            print(f"An error occurred during API scouting: {e}")
            self.status = "FAILED"
            return {"error": str(e)}

    def _handle_scout_repository(self, command: ScoutRepositoryCommand) -> dict:
        """Orchestrates the scouting of a GitHub repository."""
        print(f"--- Scout Bee received command to scout repo: {command.url} ---")
        temp_dir = None
        try:
            repo_input = {"url": command.url, "github_token": command.github_token}
            temp_dir = self.github_connector.process(repo_input)

            discovered_components = {"aggregates": [], "transformations": [], "connectors": []}

            source_files = self.repo_transformer.execute(temp_dir)
            for filepath in source_files:
                file_components = self.source_file_transformer.execute(filepath)
                for key in discovered_components:
                    discovered_components[key].extend(file_components[key])

            report_data = {
                "repository": command.url,
                "components": discovered_components
            }
            self._print_repo_report(report_data)
            return report_data

        except Exception as e:
            print(f"An error occurred during repository scouting: {e}")
            self.status = "FAILED"
            return {"error": str(e)}
        finally:
            if temp_dir:
                print("\nScouting mission complete. Cleaning up temporary files.")
                shutil.rmtree(temp_dir)

    def _print_api_report(self, report: dict):
        """Prints a formatted report for an API scan."""
        print("\n--- OpenAPI Scout Bee Report ---")
        print("="*20)
        print(f"API Title: {report.get('title', 'N/A')}")
        print(f"Version: {report.get('version', 'N/A')}")
        print(f"Description: {report.get('description', 'N/A')}")
        print("="*20)
        print("\nEndpoints Discovered:")
        if not report.get('endpoints'):
            print("No paths found in the specification.")
            return
        for endpoint in report.get('endpoints', []):
            print(f"\n--- Path: {endpoint.get('path')} ---")
            print(f"  - Method: {endpoint.get('method')}")
            print(f"    Summary: {endpoint.get('summary', 'No summary provided.')}")
            if endpoint.get('parameters'):
                print("    Parameters:")
                for param in endpoint.get('parameters', []):
                     print(f"      - [{param.get('in', 'N/A')}] {param.get('name', 'N/A')}: {param.get('description', 'No description.')}")
            if endpoint.get('request_body'):
                print("    Request Body: Yes")

    def _print_repo_report(self, report: dict):
        """Prints a formatted report for a repository scan."""
        print("\n--- GitHub Scout Bee Report ---")
        print(f"Repository: {report.get('repository')}")
        print("\nDiscovered Potential ATCG Components:")
        components = report.get('components', {})
        for comp_type, comp_list in components.items():
            if comp_list:
                print(f"\n  {comp_type.replace('_', ' ').title()}:")
                for item in sorted(list(set(comp_list))):
                    print(f"    - {item}")

    def _apply(self, event: ScoutingReportGeneratedEvent) -> None:
        """Applies an event to the aggregate's state."""
        self.report = event.report
        if "error" not in self.report:
            self.status = "COMPLETED"
        else:
            self.status = "FAILED"
        print(f"\nApplied ScoutingReportGeneratedEvent to aggregate {self.id}. Status is now {self.status}.")
