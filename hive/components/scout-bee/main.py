import json
import requests
import sys

def scout_api(openapi_url: str):
    """
    Fetches and analyzes an OpenAPI specification from a URL.

    Args:
        openapi_url: The URL of the openapi.json file.
    """
    try:
        # Ensure the URL has a scheme
        if not openapi_url.startswith(('http://', 'https://')):
            openapi_url = 'http://' + openapi_url

        response = requests.get(openapi_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        spec = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the response.", file=sys.stderr)
        sys.exit(1)

    print("Scout Bee Report:\n")
    print("="*20)
    print(f"API Title: {spec.get('info', {}).get('title', 'N/A')}")
    print(f"Version: {spec.get('info', {}).get('version', 'N/A')}")
    print(f"Description: {spec.get('info', {}).get('description', 'N/A')}")
    print("="*20)

    print("\nEndpoints Discovered:")
    paths = spec.get('paths', {})
    if not paths:
        print("No paths found in the specification.")
        return

    for path, methods in paths.items():
        print(f"\n--- Path: {path} ---")
        for method, details in methods.items():
            summary = details.get('summary', 'No summary provided.')
            print(f"  - Method: {method.upper()}")
            print(f"    Summary: {summary}")

            parameters = details.get('parameters', [])
            if parameters:
                print("    Parameters:")
                for param in parameters:
                    param_in = param.get('in', 'N/A')
                    param_name = param.get('name', 'N/A')
                    param_desc = param.get('description', 'No description.')
                    print(f"      - [{param_in}] {param_name}: {param_desc}")

            request_body = details.get('requestBody')
            if request_body:
                print("    Request Body: Yes")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url_to_scout = sys.argv[1]
        scout_api(url_to_scout)
    else:
        print("Please provide the URL of the OpenAPI specification as an argument.", file=sys.stderr)
        print("Usage: python hive/components/scout-bee/main.py <url>", file=sys.stderr)
        sys.exit(1)
