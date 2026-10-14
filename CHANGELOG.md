# Change log

## 2026-10-14 - Repair Docker, Python, and VS Code execution

The database could not start because PostgreSQL 15 was opening a PostgreSQL 16 data volume. Local Python could connect to the wrong database on port 5432 or fail to find its input when started from another directory.

### File-by-file updates

| File | Status | Update |
| --- | --- | --- |
| `docker-compose.yml` | Updated | Use PostgreSQL 16 / PostGIS 3.5, retain the named `pgdata` volume, expose local port 5434 on loopback, verify an authenticated database query in the health check, and remove the obsolete Compose version field. |
| `main.py` | Updated | Select the declared `psycopg2` driver explicitly, use port 5434 for local connections, and resolve GeoJSON and CSV paths relative to the script. |
| `test_main.py` | Updated | Match the local database port and driver, resolve the CSV relative to the project, and retain the checks for 5,166 CSV and database rows. |
| `.vscode/launch.json` | Added | Provide the `Run minipipeline` debugger configuration with the tested Windows Python 3.14 interpreter, local database settings, and a database startup task. |
| `.vscode/tasks.json` | Added | Start the Compose database and wait until it is healthy before launching Python. |
| `.vscode/settings.json` | Added | Configure the tested Windows Python interpreter and Code Runner command and working directory. |
| `.gitignore` | Updated | Replace UTF-16 encoding with UTF-8; ignore generated CSVs, caches, virtual environments, local environment files, and unrelated data while retaining the required GeoJSON input. |
| `README.md` | Updated | Document Docker, Python, and VS Code steps; explain normal completion, database ports, persistence, and startup troubleshooting. |
| `CHANGELOG.md` | Added | Record the cause of the failures and the update to each project file. |
| `data/sample.geojson` | Removed | Remove the unused example dataset; the pipeline reads the checked Quang Ngai input. |
| `output/stats.csv` | Untracked | Keep generated results local; each pipeline run recreates this file. |

### Required files retained without changes

| File | Purpose |
| --- | --- |
| `Dockerfile` | Build the Python 3.10 Docker environment and install the declared dependencies. |
| `requirements.txt` | Declare GeoPandas, SQLAlchemy, GeoAlchemy2, psycopg2-binary, pytest, and pandas. |
| `data/quangngai_2026_ky18_checked.geojson` | Supply the 5,166 input features used by the pipeline and its integration test. |

### Verification

The repaired local project completed a Python 3.14 run from outside its directory, a run through the VS Code debugger, and its CSV/database integration test. A Docker run also exited successfully with `1 passed`.

Before publication, the exact staged files were exported to a clean directory and built with Docker against a fresh PostgreSQL 16 volume. The app exited with code 0, its integration test passed, and all 5,166 exported areas were present and positive. The verification database used only the internal Docker network to avoid changing the running local database.

The original local PostgreSQL 16 volume was backed up before recovery. Database volumes, backups, generated output, and caches are not included in this update.
