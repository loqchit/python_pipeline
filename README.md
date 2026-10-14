# GeoJSON to PostGIS Pipeline

Load the included Quang Ngai GeoJSON into PostGIS, transform its geometries to EPSG:32648, calculate areas in square metres, and export `output/stats.csv`.

This is a batch pipeline. The app exits successfully after creating the CSV and running its test; the database keeps running. There is no web interface.

## Run with Docker

1. Start Docker Desktop with Linux containers enabled.
2. Clone this repository and open its folder:

   ```powershell
   git clone https://github.com/loqchit/python_pipeline.git
   cd python_pipeline
   ```

3. Build and run the pipeline:

   ```powershell
   docker compose up --build
   ```

4. Look for `1 passed` and an app exit code of `0`, then open `output/stats.csv`. The included dataset produces 5,166 rows.

The input file, `data/quangngai_2026_ky18_checked.geojson`, is included in the repository. Output files and Python caches are generated locally and ignored by Git.

## Run with Python on Windows

Use Python 3.14 and run these commands from the repository folder:

```powershell
py -3.14 -m pip install -r requirements.txt
docker compose up -d --wait db
py -3.14 main.py
py -3.14 -m pytest test_main.py
```

`main.py` resolves input and output paths relative to its own location, so running it by absolute path from another directory also works.

## Run in VS Code

1. Open the repository folder in VS Code.
2. Install the Microsoft Python and Python Debugger extensions if needed.
3. Install the Python dependencies using the command above and start Docker Desktop.
4. Select **Run and Debug > Run minipipeline**, then press **F5**.

The launch task starts the database and waits for a successful connection before running Python. The supplied Windows configuration expects Python at `%LOCALAPPDATA%/Programs/Python/Python314/python.exe`. If Python is installed elsewhere, update `python` in `.vscode/launch.json` and `python.defaultInterpreterPath` in `.vscode/settings.json`. Code Runner uses `py -3.14 -u`.

## Database configuration

The database image is `postgis/postgis:16-3.5`. Local connections use `localhost:5434`; the app container uses `db:5432`.

| Variable | Local default |
| --- | --- |
| `DB_HOST` | `localhost` |
| `DB_PORT` | `5434` |
| `DB_USER` | `user` |
| `DB_PASS` | `password` |
| `DB_NAME` | `geodb` |

These are local development credentials. Database contents persist in the Compose volume `<project>_pgdata`; an existing folder named `minipipeline` uses `minipipeline_pgdata`.

Keep PostgreSQL 16 when reusing a volume initialized by PostgreSQL 16. Starting that volume with PostgreSQL 15 produces the error `database files are incompatible with server`. Changing `POSTGRES_USER` or `POSTGRES_DB` does not create users or databases in an already initialized volume.

To inspect a failed run:

```powershell
docker compose ps -a
docker compose logs --tail 50 db app
```

The normal completed state is a healthy database and an app that exited with code `0`. If local Python reports `connection refused`, start the database with `docker compose up -d --wait db`. If port `5434` is already occupied by another checkout, use that existing checkout or stop its database before starting a second one.

## File updates

See [CHANGELOG.md](CHANGELOG.md) for the repair history and a note for each changed, added, removed, or retained project file.
