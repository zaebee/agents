import json
from dna_core.royal_jelly import Transformation

class OpenApiTransformer(Transformation):
    """
    A transformation for parsing an OpenAPI JSON specification.
    """

    def transform(self, raw_content: bytes) -> dict:
        """
        Parses the raw byte content of an OpenAPI spec and generates a report.

        Args:
            raw_content: The raw bytes of the JSON file.

        Returns:
            A dictionary containing the structured report.
        """
        report = {"title": "N/A", "version": "N/A", "description": "N/A", "endpoints": []}
        try:
            spec = json.loads(raw_content)
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the response.")
            # Return the empty report
            return report

        report["title"] = spec.get('info', {}).get('title', 'N/A')
        report["version"] = spec.get('info', {}).get('version', 'N/A')
        report["description"] = spec.get('info', {}).get('description', 'N/A')

        paths = spec.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                endpoint_details = {
                    "path": path,
                    "method": method.upper(),
                    "summary": details.get('summary', 'No summary provided.'),
                    "parameters": [],
                    "request_body": bool(details.get('requestBody'))
                }
                parameters = details.get('parameters', [])
                for param in parameters:
                    endpoint_details["parameters"].append({
                        "in": param.get('in', 'N/A'),
                        "name": param.get('name', 'N/A'),
                        "description": param.get('description', 'No description.'),
                    })
                report["endpoints"].append(endpoint_details)

        return report
