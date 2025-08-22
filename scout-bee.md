# Component: scout-bee

The Scout Bee is a specialized component responsible for exploring and analyzing external software ecosystems, such as OpenAPI specifications and GitHub repositories. It identifies key architectural components and reports back its findings.

## Aggregate

- `ScoutSessionAggregate`

## Connectors

- `GitHubConnector`: Clones a remote repository.
- `HttpConnector`: Fetches a file from a URL.

## Transformations

- `RepositoryTransformer`: Analyzes the file structure of a cloned repository.
- `SourceFileTransformer`: Parses individual source files (`.py`, `.ts`) for specific class definitions.
- `OpenApiTransformer`: Parses an OpenAPI JSON spec.

## Commands

- `ScoutRepositoryCommand`: A command to initiate the scouting of a GitHub repository.
- `ScoutApiCommand`: A command to initiate the scouting of an OpenAPI specification.

## Events

- `ScoutingReportGeneratedEvent`: An event produced when a scouting session is complete.
- `RepositoryClonedEvent`: An event indicating a repository has been successfully cloned.
- `ApiSpecFetchedEvent`: An event indicating an API spec has been successfully fetched.
