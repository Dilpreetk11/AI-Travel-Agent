from tavily import TavilyClient

import os
import streamlit as st

from dotenv import load_dotenv


# ============================================================
# LOAD .ENV
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


# ============================================================
# GET TAVILY API KEY
# ============================================================

# First try local .env
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# If not found, try Streamlit Cloud Secrets
if not TAVILY_API_KEY:
    try:
        TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY")
    except Exception:
        TAVILY_API_KEY = None


# ============================================================
# CHECK API KEY
# ============================================================

if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY is missing. "
        "Add it to your .env file or Streamlit Cloud Secrets."
    )


# ============================================================
# TAVILY CLIENT
# ============================================================

client = TavilyClient(
    api_key=TAVILY_API_KEY
)


# ============================================================
# TAVILY SEARCH
# ============================================================

def tavily_search(query):

    try:

        response = client.search(
            query=query,
            max_results=5,
            timeout=20
        )

        results = []

        for i, r in enumerate(response["results"], 1):

            title = r.get(
                "title",
                "Unknown"
            )

            url = r.get(
                "url",
                ""
            )

            snippet = r.get(
                "content",
                ""
            ).strip()

            # Keep only the first 300 characters
            if len(snippet) > 300:
                snippet = (
                    snippet[:300]
                    .rsplit(" ", 1)[0]
                    + "..."
                )

            results.append(
                f"{i}. **{title}**\n"
                f"   {url}\n"
                f"   {snippet}"
            )

        return "\n\n".join(results)

    except Exception as e:

        print(
            f"Tavily search failed: {e}"
        )

        return (
            "Hotel search is temporarily unavailable."
        )