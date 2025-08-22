import requests
from dna_core.royal_jelly import Connector

class HttpConnector(Connector[str, bytes]):
    """
    A connector for fetching data from an HTTP/HTTPS URL.
    Element: C (Connector)
    """

    def process(self, url: str) -> bytes:
        """
        Fetches the content from a given URL.

        Args:
            url: The URL to fetch.

        Returns:
            The raw content of the response as bytes.
        """
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url

            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            raise
