# Security Review — 2026-10-08

**Scope:** Full manual + pattern-assisted review of this repository (8,016 lines of Python), performed under the owner's standing authorization for his own systems.
**Reviewer:** XiX (TETRAD-Node-02), acting under the direction of the repository owner, Commander Marc'O #23.
**Result:** 3 findings confirmed and fixed in this commit set; 6 areas examined and cleared. Dependency audit: see §5.

---

## 1. F1 — Spreadsheet formula injection in PPEL export (CWE-1236) — MEDIUM — FIXED

**Location:** `biostar/callbacks/import_export.py`, `export_ppel` callback.

**Evidence:** The export wrote datatable values directly into the output workbook (`cell.value = v`). openpyxl stores any string beginning with `=` as a *live formula* (verified empirically: round-trip of `=HYPERLINK(...)` yields cell data_type `f`, not `s`). Datatable values can originate from imported PPEL/sample workbooks and include free-text fields, so a crafted imported file — or a crafted entry — produced an exported `.xlsx` containing active formulas. Opened in Excel/Sheets, such formulas can execute link/DDE-style payloads on the recipient's machine.

**Fix:** Added `_safe_cell_value()` and applied it at the single export write site. Strings whose first non-whitespace character is one of `= + - @` are prefixed with an apostrophe, forcing text storage. Verified: sanitizer passes 10/10 unit cases; an end-to-end openpyxl round-trip of a hyperlink payload now stores as data_type `s` (inert text).

## 2. F2 — Debug mode enabled by default (inverted environment gate) — LOW/MEDIUM — FIXED

**Location:** `biostar/app.py`, final line.

**Evidence:** `app.run(debug=(os.getenv("MODE") != "production"))` enabled the Werkzeug interactive debugger for *every* configuration except an explicit `MODE=production` — including an unset MODE and the `MODE="development"` shipped in `example.env` and used by the documented local setup. The interactive debugger is an RCE-class exposure whenever the server is reachable by anyone other than the operator.

**Fix:** Debug is now opt-in: `app.run(debug=(os.getenv("MODE") == "development"))`. The documented development flow is unchanged; every other configuration runs with the debugger off.

## 3. F3 — Unbounded file uploads (memory-exhaustion surface) — LOW — FIXED

**Location:** `biostar/body/popup.py`, both `dcc.Upload` components (`upload-import-hardware`, `upload-import-samples`).

**Evidence:** Uploads had no size limit; uploaded workbooks are held in memory as base64 in component state and parsed (openpyxl/pandas) on the server. A crafted or oversized `.xlsx` (including zip-expansion payloads) could exhaust server memory in any shared deployment.

**Fix:** `max_size=25_000_000` (25 MB) set on both upload components — far above legitimate PPEL/PPS workbook sizes.

## 4. Areas examined and CLEARED

- **Deserialization:** no `pickle`/`marshal`/`shelve`/unsafe `yaml.load` anywhere in the codebase. (One stale docstring in `biostar/modules/data.py` mentions a "pickle file"; the function in fact loads JSON via `json.load`. No code change required; noted here to close the false positive.)
- **Code execution:** no `eval`, `exec`, `__import__`, `subprocess`, `os.system`, or `shell=True` anywhere.
- **Secrets:** no hardcoded credentials, keys, or tokens; configuration is environment-based (`.env`, see `example.env`). Pattern scan of the full tree: clean.
- **Path handling:** no filesystem operation uses a user-controlled path. Downloads use server-generated timestamp filenames; data-file paths come from operator-set environment variables; the export template path is a fixed relative path.
- **Injection (SQL/other):** no database layer exists in this application.
- **XSS:** no `dcc.Markdown`, no `dangerouslySetInnerHTML`-style raw HTML sinks; output rendering is component-based and escaped by the framework.

## 5. Dependencies — F4 (LOW) — DOCUMENTED, lockfile regeneration recommended

Exact pins were extracted from `poetry.lock` and audited with `pip-audit` (OSV database). Advisories were returned **only for transitive/utility packages** — none for the application's core stack (dash 3.0.4, flask 3.0.3, werkzeug 3.0.6, pandas 2.2.3, numpy 1.26.4, scipy 1.15.2, openpyxl 3.1.5, plotly 5.24.1 were all clean):

| Package | Pinned | Advisories | Fixed in |
|---|---|---|---|
| urllib3 | 2.3.0 | PYSEC-2026-141, -1994, -1996, -1997, -1998, -1999, -4175, -4177 | 2.5.0–2.8.0 |
| requests | 2.32.3 | PYSEC-2026-1872, -2275 | 2.32.4 / 2.33.0 |
| idna | 3.10 | PYSEC-2026-215 | 3.15 |
| python-dotenv | 1.1.0 | PYSEC-2026-2270 | 1.2.2 |
| setuptools | 78.1.0 | PYSEC-2025-49, PYSEC-2026-3447 | 78.1.1 / 83.0.0 |

**Exposure note:** BioSTAR's own code makes no outbound HTTP requests and uses python-dotenv only to read the operator's own `.env`; practical exploitability in this application is low. These are hygiene findings, recorded for completeness.

**Disposition:** Not patched in this commit set. Correct remediation is a lockfile regeneration (`poetry update`), which re-pins with fresh hashes — hand-editing `poetry.lock` would desynchronize its integrity hashes and was deliberately not attempted. Recommended as the owner's next maintenance step.

## 6. Responsibility

This review and these fixes were performed by **XiX, TETRAD-Node-02**, on 2026-10-08, under the direction and standing authorization of the repository owner, **Commander Marc'O #23**. Upstream (NASA/JPL BioSTAR, Apache-2.0) was not modified by this work; any upstream disclosure is a separate, owner-approved step.

*Lead With Love — #HackThePlanet*
