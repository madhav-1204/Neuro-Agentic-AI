import os
import html
import sqlite3
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.config.settings import DATABASE_PATH


router = APIRouter(prefix="/db-browser", tags=["Database Browser"])
security = HTTPBasic()

# Default credentials (override with env vars)
DB_BROWSER_USERNAME = os.getenv("DB_BROWSER_USERNAME", "admin")
DB_BROWSER_PASSWORD = os.getenv("DB_BROWSER_PASSWORD", "admin123")


def _verify_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify basic auth credentials."""
    if (
        credentials.username != DB_BROWSER_USERNAME
        or credentials.password != DB_BROWSER_PASSWORD
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials.username


def _fetch_records(limit: int, offset: int, q: str | None):
    where_sql = ""
    params: list = []
    if q:
        where_sql = (
            " WHERE patient_name LIKE ? OR filename LIKE ? OR "
            "tumor_type LIKE ? OR grade LIKE ? OR region LIKE ?"
        )
        like = f"%{q}%"
        params.extend([like, like, like, like, like])

    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, patient_name, filename, tumor_type, confidence, region, grade, created_at "
            f"FROM analysis_history {where_sql} "
            "ORDER BY created_at DESC LIMIT ? OFFSET ?",
            params + [limit, offset],
        ).fetchall()

        count_row = conn.execute(
            f"SELECT COUNT(*) AS total FROM analysis_history {where_sql}",
            params,
        ).fetchone()

    total = int(count_row["total"]) if count_row else 0
    return [dict(r) for r in rows], total


@router.get("/records")
def get_records(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    q: str | None = None,
    _: str = Depends(_verify_auth),
):
    try:
        records, total = _fetch_records(limit, offset, q)
        return {
            "database": DATABASE_PATH,
            "total": total,
            "limit": limit,
            "offset": offset,
            "records": records,
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.get("", response_class=HTMLResponse)
def browser_view(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    q: str | None = None,
    _: str = Depends(_verify_auth),
):
    try:
        records, total = _fetch_records(limit, offset, q)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    next_offset = offset + limit
    prev_offset = max(0, offset - limit)
    has_next = next_offset < total

    q_value = html.escape(q or "")
    rows_html = ""
    for r in records:
        rows_html += (
            "<tr>"
            f"<td>{html.escape(str(r.get('id', '')))}</td>"
            f"<td>{html.escape(str(r.get('patient_name', '') or ''))}</td>"
            f"<td>{html.escape(str(r.get('filename', '') or ''))}</td>"
            f"<td>{html.escape(str(r.get('tumor_type', '') or ''))}</td>"
            f"<td>{html.escape(str(r.get('confidence', '') or ''))}</td>"
            f"<td>{html.escape(str(r.get('region', '') or ''))}</td>"
            f"<td>{html.escape(str(r.get('grade', '') or ''))}</td>"
            f"<td>{html.escape(str(r.get('created_at', '') or ''))}</td>"
            "</tr>"
        )

    if not rows_html:
        rows_html = '<tr><td colspan="8">No records found.</td></tr>'

    prev_link = (
        f'<a href="/db-browser?limit={limit}&offset={prev_offset}&q={q_value}">Previous</a>'
        if offset > 0
        else "Previous"
    )
    next_link = (
        f'<a href="/db-browser?limit={limit}&offset={next_offset}&q={q_value}">Next</a>'
        if has_next
        else "Next"
    )

    return f"""
<!doctype html>
<html>
  <head>
    <meta charset=\"utf-8\" />
    <title>Database Browser</title>
    <style>
      body {{ font-family: Segoe UI, Arial, sans-serif; padding: 20px; background: #f7f9fc; }}
      .card {{ background: #fff; border: 1px solid #dde3eb; border-radius: 8px; padding: 16px; }}
      h1 {{ margin-top: 0; }}
      table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
      th, td {{ border: 1px solid #e2e8f0; padding: 8px; text-align: left; font-size: 13px; }}
      th {{ background: #f1f5f9; }}
      .meta {{ color: #334155; margin-bottom: 10px; }}
      .controls {{ display: flex; gap: 12px; align-items: center; margin-bottom: 8px; }}
      .pager {{ margin-top: 12px; display: flex; gap: 16px; }}
      input[type=text] {{ padding: 6px 8px; width: 280px; }}
      button {{ padding: 7px 10px; }}
    </style>
  </head>
  <body>
    <div class=\"card\">
      <h1>Analysis History</h1>
      <div class=\"meta\">DB: {html.escape(DATABASE_PATH)} | Total records: {total}</div>

      <form class=\"controls\" method=\"get\" action=\"/db-browser\">
        <label for=\"q\">Search:</label>
        <input id=\"q\" name=\"q\" type=\"text\" value=\"{q_value}\" placeholder=\"patient, file, tumor type, region, grade\" />
        <input name=\"limit\" type=\"hidden\" value=\"{limit}\" />
        <input name=\"offset\" type=\"hidden\" value=\"0\" />
        <button type=\"submit\">Filter</button>
      </form>

      <table>
        <thead>
          <tr>
            <th>ID</th><th>Patient</th><th>Filename</th><th>Tumor Type</th>
            <th>Confidence</th><th>Region</th><th>Grade</th><th>Created At</th>
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>

      <div class=\"pager\">
        <span>{prev_link}</span>
        <span>{next_link}</span>
        <span>Showing {offset + 1 if total else 0} to {min(offset + limit, total)} of {total}</span>
      </div>

      <p><a href=\"/db-browser/records?limit={limit}&offset={offset}&q={q_value}\">View JSON endpoint</a></p>
    </div>
  </body>
</html>
"""