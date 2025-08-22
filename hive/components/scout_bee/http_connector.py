import requests
from dna_core.royal_jelly import Connector

class HttpConnector(Connector):
    """
    A connector for fetching data from an HTTP/HTTPS URL.
    """

    def fetch(self, url: str) -> bytes:
        """
        Fetches the content from a given URL.

        Args:
            url: The URL to fetch.

        Returns:
            The raw content of the response as bytes.

        Raises:
            requests.exceptions.RequestException: If there is an error fetching the URL.
        """
        try:
            # Ensure the URL has a scheme
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url

            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            raise
