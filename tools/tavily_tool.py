from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()


# https://www.tavily.com/ 
# Signup and login, On dashboard- > under api keys you will see the default key.
# Use that or click on + to create new one. Then save it in .env file

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

# test it
#################################
# response = client.search(
    # query="Best hotels in Dubai"
# )

# print(response)

####################################



def tavily_search(query):

    try:
        response = client.search(
            query=query,
            max_results=5,
            timeout=20
        )

        results = []

        for i, r in enumerate(response["results"], 1):
            title = r.get("title", "Unknown")
            url = r.get("url", "")
            snippet = r.get("content", "").strip()

            # Keep only the first 300 characters
            if len(snippet) > 300:
                snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

            results.append(
                f"{i}. **{title}**\n"
                f"   {url}\n"
                f"   {snippet}"
            )

        return "\n\n".join(results)

    except Exception as e:
        print(f"Tavily search failed: {e}")
        return "Hotel search is temporarily unavailable."