#!/usr/bin/env python3
"""
Fetch weekly trending Movies, TV Series, and Anime from TMDB.
Outputs a clean JSON file containing only title + poster URL.
"""

import os
import json
import sys
import urllib.request
import urllib.error
import urllib.parse

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

if not TMDB_API_KEY:
    print("ERROR: TMDB_API_KEY environment variable is not set.", file=sys.stderr)
    sys.exit(1)

ANIMATION_GENRE_ID = 16  # TMDB genre id for Animation


def tmdb_get(path, params=None):
    """Call TMDB API v3 using the API key (legacy api_key param, works without a Bearer token)."""
    base = f"https://api.themoviedb.org/3{path}"
    query = {"api_key": TMDB_API_KEY, "language": "en-US"}
    if params:
        query.update(params)
    qs = urllib.parse.urlencode(query)
    url = f"{base}?{qs}"

    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP error calling {path}: {e.code} {e.reason}", file=sys.stderr)
        raise
    except urllib.error.URLError as e:
        print(f"Network error calling {path}: {e.reason}", file=sys.stderr)
        raise


def build_poster_url(poster_path):
    if not poster_path:
        return None
    return f"{IMAGE_BASE_URL}{poster_path}"


def simplify_movie(item):
    return {
        "title": item.get("title") or item.get("original_title"),
        "poster": build_poster_url(item.get("poster_path")),
    }


def simplify_tv(item):
    return {
        "title": item.get("name") or item.get("original_name"),
        "poster": build_poster_url(item.get("poster_path")),
    }


def is_anime(item):
    """Heuristic: Animation genre + Japanese original language."""
    genre_ids = item.get("genre_ids", [])
    original_language = item.get("original_language")
    return ANIMATION_GENRE_ID in genre_ids and original_language == "ja"


def fetch_trending_movies():
    data = tmdb_get("/trending/movie/week")
    results = data.get("results", [])
    return [simplify_movie(item) for item in results]


def fetch_trending_tv():
    data = tmdb_get("/trending/tv/week")
    results = data.get("results", [])
    # Split into anime vs regular TV series
    anime = [simplify_tv(item) for item in results if is_anime(item)]
    tv_series = [simplify_tv(item) for item in results if not is_anime(item)]
    return tv_series, anime


def main():
    print("Fetching trending movies...")
    movies = fetch_trending_movies()

    print("Fetching trending TV series & anime...")
    tv_series, anime = fetch_trending_tv()

    output = {
        "movies": movies,
        "tv_series": tv_series,
        "anime": anime,
    }

    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", "trending.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(movies)} movies, {len(tv_series)} tv series, {len(anime)} anime to {output_path}")


if __name__ == "__main__":
    main()
