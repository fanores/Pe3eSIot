# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Install dependencies:**

```bash
pip3 install -r requirements.txt
```

**Run all tests:**

```bash
pytest
```

**Run a single test file:**

```bash
pytest tests/lib/common/test_httpClient.py
```

**Run tests with coverage:**

```bash
pytest --cov=./lib --cov-report=html --cov-branch
```

## Architecture

Pe3eSIoT is a Python IoT library for managing photovoltaic (FVE) monitoring systems, weather data, and e-ink displays.

### Module Structure

All library code lives in `lib/`, with tests mirroring the structure in `tests/lib/`.

**`lib/common/`** — Shared utilities:

- `HttpClient.py` — Thin wrapper around `requests` for HTTP GET
- `XmlParser.py` — Parses XML responses into dicts (extracts root's direct children)
- `FileProcessor.py` — Appends lines to files
- `DateTimeProcessor.py` — Date/time formatting helpers (weekday names, month names, etc.)
- `IotError.py` — Custom exception hierarchy; `IotError` is the base class, with domain-specific subclasses (`HttpClientError`, `XmlParserError`, `FveRestApiError`, etc.)

**`lib/fve/`** — Photovoltaic energy system:

- `FveRestApi.py` — Fetches measurements from a local FVE device via HTTP (`/meas.xml`, `/stat_day.xml`)
- `FveFileReporter.py` — Writes selected KPIs from FVE measurements to semicolon-delimited files

**`lib/weather/`** — Weather data:

- `OpenWeatherMapManager.py` — Wraps `pyowm` to retrieve current temperature for a city

**`lib/waveshare_epd/`** — E-ink display driver:

- `epd2in13b_V3.py` — Driver for Waveshare 2.13" B V3 display (black + red, SPI interface)

**`demo/`** — Example scripts showing how to wire the modules together (not imported by library code).

### Data Flow

FVE data path: `FveRestApi` (uses `HttpClient`) → XML response → `XmlParser` → `FveFileReporter` (uses `FileProcessor`) → CSV file

Weather path: `OpenWeatherMapManager` (uses `pyowm`) → temperature value

### Error Handling Convention

All modules raise subclasses of `IotError` (defined in `lib/common/IotError.py`). When adding a new module, add a corresponding error subclass there.

### Testing Convention

Tests use `unittest.mock` for all external dependencies (HTTP calls, file I/O, pyowm). Each module in `lib/` has a corresponding test file in `tests/lib/` at the same relative path.

## CI

GitHub Actions (`.github/workflows/python-tests.yml`) runs `pytest` on Python 3.12 for every pull request targeting `master`.
