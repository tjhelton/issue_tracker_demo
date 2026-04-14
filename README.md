# SafetyCulture Tools

A collection of bulk operations tools for the SafetyCulture platform. Includes a guided web UI and 30+ standalone CLI scripts for managing actions, assets, inspections, sites, templates, users, and more via the SafetyCulture API.

## Download

### Mac

> **[Download for Mac (.dmg)](https://github.com/tjhelton/issue_tracker_demo/releases/latest/download/SafetyCulture-Tools-Mac.dmg)**

Open the `.dmg` and drag **SafetyCulture Tools** to your Applications folder (or just double-click it).

### Windows

> **[Download for Windows (.zip)](https://github.com/tjhelton/issue_tracker_demo/releases/latest/download/SafetyCulture-Tools-Windows.zip)**

Extract the ZIP and double-click **SafetyCulture Tools.exe**.

### What you need

- A **SafetyCulture API Token** — [Get yours here](https://developer.safetyculture.com/reference/getting-started)

That's it. Python is bundled — no extra installs required.

## How It Works

1. Paste your API token on the home page and validate it
2. Pick a category from the sidebar (Actions, Assets, Inspections, etc.)
3. Choose a tool from the tabs within that category
4. Upload a CSV if the tool requires one (each tool shows the required columns)
5. Click Run and watch the progress
6. Download the results when complete

Your API token is stored only for the session and is never saved to disk.

## Available Tools

| Category | Tools | Operations |
|---|---|---|
| **Actions** | 5 | Export, update status, delete actions, manage schedules |
| **Assets** | 4 | Export assets/types, bulk update fields, delete |
| **Inspections** | 7 | Archive, unarchive, complete, delete, export PDFs and location changes |
| **Sites** | 4 | Create, delete, find inactive sites, manage user access |
| **Templates** | 3 | Archive, export access rules and questions |
| **Users** | 2 | Deactivate accounts, export custom field data |
| **Courses** | 1 | Assign training courses to sites |
| **Groups** | 2 | Create groups, export member details |
| **Issues** | 2 | Export public links and relationships |
| **Organizations** | 1 | Export contractor company records |
| **Schedules** | 2 | Export and update legacy schedules |

## CLI Scripts

Each tool is also available as a standalone Python script in the [scripts/](scripts/) directory. Every script has its own README with input format, usage, and examples.

```bash
cd scripts/inspections/archive_inspections/
# Edit main.py to set your API token, prepare input.csv
python main.py
```

## Running from Source

If you prefer to run the app from source instead of the standalone download:

```bash
python3 -m pip install -r requirements.txt
python3 launcher.py          # native window
# or
streamlit run app/Home.py    # browser
```

## Important Notes

- **Always test with small datasets first** — many operations (delete, archive) cannot be undone
- **Never commit API tokens** — the `.gitignore` is configured to keep secrets out of the repo
- Scripts include built-in rate limiting, retry logic, and progress tracking

## API Documentation

- [SafetyCulture API Reference](https://developer.safetyculture.com/reference/)
- [Getting Started Guide](https://developer.safetyculture.com/reference/getting-started)

## Contributing

See the [contribution guide](contribution_tools/CONTRIBUTE.md) for development setup, linting, and code quality tools.
