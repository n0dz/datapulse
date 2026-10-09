"""DataPulse: coleta notícias de tecnologia e gera arquivos para análise.

Uso:
    python datapulse.py --query python --limit 20
"""

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://hn.algolia.com/api/v1/search_by_date"
OUTPUT_DIR = Path(__file__).parent / "output"


def fetch_stories(query: str, limit: int) -> list[dict]:
    """Busca histórias públicas na API do Hacker News Search."""
    params = urlencode({"query": query, "tags": "story", "hitsPerPage": limit})
    request = Request(f"{API_URL}?{params}", headers={"User-Agent": "DataPulse/1.0"})

    with urlopen(request, timeout=15) as response:
        payload = json.load(response)

    stories = []
    for story in payload.get("hits", []):
        title = story.get("title") or story.get("story_title")
        if not title:
            continue
        stories.append(
            {
                "title": title.strip(),
                "author": story.get("author") or "unknown",
                "points": story.get("points") or 0,
                "comments": story.get("num_comments") or 0,
                "url": story.get("url") or story.get("story_url") or "",
                "published_at": story.get("created_at") or "",
            }
        )
    return stories


def write_csv(stories: list[dict], path: Path) -> None:
    """Salva os dados numa tabela que pode ser aberta no Excel."""
    columns = ["title", "author", "points", "comments", "url", "published_at"]
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(stories)


def build_summary(stories: list[dict], query: str) -> dict:
    authors = Counter(story["author"] for story in stories)
    return {
        "query": query,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "story_count": len(stories),
        "total_points": sum(story["points"] for story in stories),
        "total_comments": sum(story["comments"] for story in stories),
        "top_authors": authors.most_common(5),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Coleta notícias e gera um relatório DataPulse.")
    parser.add_argument("--query", default="python", help="Tema a pesquisar")
    parser.add_argument("--limit", type=int, default=20, help="Quantidade máxima de resultados (1-100)")
    args = parser.parse_args()

    if not 1 <= args.limit <= 100:
        parser.error("--limit precisa estar entre 1 e 100")

    try:
        stories = fetch_stories(args.query, args.limit)
    except Exception as error:  # Uma mensagem amigável é melhor que um traceback para quem está começando.
        print(f"Não foi possível consultar a API: {error}", file=sys.stderr)
        return 1

    OUTPUT_DIR.mkdir(exist_ok=True)
    csv_path = OUTPUT_DIR / "stories.csv"
    summary_path = OUTPUT_DIR / "summary.json"
    write_csv(stories, csv_path)
    summary_path.write_text(json.dumps(build_summary(stories, args.query), indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✓ {len(stories)} histórias salvas em {csv_path}")
    print(f"✓ Resumo salvo em {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
