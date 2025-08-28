import requests
from typing import Dict, Any

class GoogleSearchPlugin:
    """
    A plugin for performing Google searches.
    """
    @staticmethod
    def execute(payload: Dict[str, Any]) -> str:
        """
        Provides a response based on the user's search query.

        Args:
                payload: A dictionary containing the data for the plugin.

        Returns:

            A string with the search result.
        """
        GOOGLE_SEARCH_API = "https://www.googleapis.com/customsearch/v1"
        API_KEY = "AIzaSyAOIIoJUoEMvD7qOUEYKkewSRinxYYNhdo"  # Replace with actual API key
        SEARCH_ENGINE_ID = "51feee7a93400443e"  # Replace with actual search engine ID

        user_query = payload.get("text", "")
        if not user_query:
            return "No search query provided"

        try:
            params = {
                'key': API_KEY,
                'cx': SEARCH_ENGINE_ID,
                'q': user_query
            }
            response = requests.get(GOOGLE_SEARCH_API, params=params)
            response.raise_for_status()

            results = response.json()
            if 'items' not in results:
                return "No results found"

            summary = []
            for item in results['items'][:3]:
                summary.append(f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item['snippet']}\n")

            return "\n".join(summary)

        except requests.RequestException as e:
            return f"Error performing search: {str(e)}"