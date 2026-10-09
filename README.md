# DataPulse

> A small Python automation that turns a public news API into useful files.

DataPulse searches the public Hacker News Search API, cleans the returned stories, and exports two files: a CSV that can be opened in Excel and a JSON summary with basic metrics.

This is the second portfolio project after VoteFlow. It is intentionally small: the focus is learning Python, HTTP requests, data structures, error handling, and automation instead of hiding the logic behind a large framework.

## Features

- Search stories by topic.
- Control the number of results from the command line.
- Export UTF-8 CSV data.
- Generate a JSON summary with total points, comments, and frequent authors.
- Handle network and input errors with readable messages.

## Requirements

- Python 3.10 or later.
- Internet access while collecting data.

The project uses only Python's standard library, so there is no `pip install` step.

## Run it

```bash
python datapulse.py --query python --limit 20
```

Try another topic:

```bash
python datapulse.py --query javascript --limit 50
```

The generated files appear in `output/`:

- `stories.csv`: cleaned rows for Excel or Google Sheets.
- `summary.json`: totals and the five most frequent authors.

## What happens internally

1. `argparse` reads the query and limit from the terminal.
2. `urllib` sends an HTTP request to the public API.
3. The response JSON is filtered into a smaller, consistent list of dictionaries.
4. `csv.DictWriter` turns that list into a spreadsheet-friendly file.
5. `Counter` and `json.dumps` produce the summary report.

## Project structure

```text
datapulse/
├── datapulse.py       # CLI, API request, cleaning, and exports
├── output/            # Generated files (created when the script runs)
└── README.md
```

## Responsible use

DataPulse uses the public Hacker News Search API instead of scraping pages. It sends a descriptive user agent, has a timeout, and limits the number of records. Always check a service's terms and rate limits before adapting the script to another source.

## What I practiced

Python functions, lists and dictionaries, command-line arguments, HTTP requests, JSON, CSV, file paths, counters, UTC timestamps, validation, and friendly error handling.
