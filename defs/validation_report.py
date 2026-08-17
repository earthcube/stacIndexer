"""Parse raw pystac/jsonschema validation errors into human-readable reports.

`walkstac.validate_stac_catalog()` collects errors as raw strings that mix a
pystac prefix, a jsonschema message, and a schema excerpt. This module turns
those strings into structured records, groups the repeats, and renders
Markdown/HTML. The raw strings in the JSON report are left untouched.
"""

import os
import re
from html import escape

# "Validation failed for Feature at /path/x.json with ID X against schema at https://..."
_HEADER_RE = re.compile(
    r"Validation failed for (?P<kind>\w+) at (?P<href>.+?) "
    r"with ID (?P<id>.+?) against schema at (?P<schema>\S+)"
)

# The pystac-side prefix that walkstac puts in front of every error.
_CONTEXT_RES = (
    (re.compile(r"^Item '(?P<id>.+?)' in collection '(?P<parent>.+?)' validation failed: "),
     "Item", "validation"),
    (re.compile(r"^Collection '(?P<id>.+?)' validation failed: "), "Collection", "validation"),
    (re.compile(r"^Catalog '(?P<id>.+?)' validation failed: "), "Catalog", "validation"),
    (re.compile(r"^Root catalog validation failed: "), "Catalog", "validation"),
    (re.compile(r"^Failed to get items for collection '(?P<id>.+?)': "), "Collection", "traversal"),
    (re.compile(r"^Failed to get children for catalog '(?P<id>.+?)': "), "Catalog", "traversal"),
    (re.compile(r"^Failed to load catalog: "), "Catalog", "load"),
)

_KEYWORD_RE = re.compile(r"Failed validating '(?P<keyword>[\w$]+)' in schema")
_INSTANCE_RE = re.compile(r"^On instance(?P<path>.*):$", re.MULTILINE)
_PATH_PART_RE = re.compile(r"\['([^']+)'\]|\[(\d+)\]")

# Object kinds ordered by how structural the problem is — catalog/collection
# breakage matters more than one bad item, so it sorts first.
_SEVERITY = {"Catalog": 0, "Collection": 1, "Item": 2, "Unknown": 3}


def _pretty_path(raw_path: str) -> str:
    """`['properties']['start_datetime']` -> `properties.start_datetime`."""
    parts = [name or index for name, index in _PATH_PART_RE.findall(raw_path)]
    return ".".join(parts)


def _short_schema(url: str) -> str:
    """Turn a schema URL into something readable, e.g. `scientific v1.0.0`."""
    if not url:
        return ""
    m = re.search(r"stac-extensions\.github\.io/([^/]+)/([^/]+)/", url)
    if m:
        return f"{m.group(1)} extension {m.group(2)}"
    m = re.search(r"schemas\.stacspec\.org/(v[^/]+)/([^/]+)/", url)
    if m:
        return f"STAC {m.group(1)} {m.group(2)}"
    return url


def parse_error(raw: str) -> dict:
    """Break one raw error string into structured fields.

    Unrecognized text still yields a record — `message` falls back to the raw
    string so nothing is ever silently dropped.
    """
    rec = {
        "raw": raw,
        "object_type": "Unknown",
        "object_id": None,
        "parent": None,
        "failure": "validation",
        "href": None,
        "schema": None,
        "schema_label": None,
        "keyword": None,
        "path": None,
        "value": None,
        "message": None,
    }

    body = raw
    for pattern, kind, failure in _CONTEXT_RES:
        m = pattern.match(raw)
        if m:
            groups = m.groupdict()
            rec["object_type"] = kind
            rec["failure"] = failure
            rec["object_id"] = groups.get("id")
            rec["parent"] = groups.get("parent")
            body = raw[m.end():]
            break

    lines = body.split("\n")
    header = _HEADER_RE.match(lines[0]) if lines else None
    if header:
        rec["href"] = header.group("href")
        rec["schema"] = header.group("schema")
        rec["schema_label"] = _short_schema(header.group("schema"))
        if not rec["object_id"]:
            rec["object_id"] = header.group("id")
        rest = lines[1:]
    else:
        # Not a schema failure (traversal/load error) — the whole body is the message.
        rec["message"] = body.strip()
        return rec

    # The jsonschema message is the first non-empty block after the header.
    message_lines = []
    for line in rest:
        if not line.strip():
            if message_lines:
                break
            continue
        message_lines.append(line.strip())
    rec["message"] = " ".join(message_lines)

    kw = _KEYWORD_RE.search(body)
    if kw:
        rec["keyword"] = kw.group("keyword")

    inst = _INSTANCE_RE.search(body)
    if inst:
        rec["path"] = _pretty_path(inst.group("path"))
        tail = body[inst.end():].strip().split("\n")
        if tail and tail[0].strip():
            rec["value"] = tail[0].strip()

    return rec


def _explain(rec: dict) -> tuple[str, str, str]:
    """Return (title, what_it_means, suggested_fix) for a parsed error."""
    keyword, path, message = rec["keyword"], rec["path"] or "", rec["message"] or ""
    schema_label = rec["schema_label"] or "the STAC schema"

    if rec["failure"] == "traversal":
        return (
            f"{rec['object_type']} children could not be read",
            f"Walking into `{rec['object_id']}` failed, so anything below it was never "
            "validated. The counts in the summary are therefore incomplete.",
            "Check that the child links resolve (correct href, reachable network, valid JSON).",
        )
    if rec["failure"] == "load":
        return (
            "Catalog could not be loaded",
            "The root catalog never parsed, so no validation ran at all.",
            "Verify the --configfile path or URL points at a valid STAC catalog document.",
        )

    if keyword == "pattern" and "+00:00|Z" in message:
        return (
            f"`{path}` is not a valid RFC 3339 UTC timestamp",
            "STAC requires date-times to carry an explicit UTC marker. These values are "
            "bare dates (e.g. `2023-04-12`) with no time or timezone, so they fail the "
            "schema's `(\\+00:00|Z)$` pattern.",
            "Emit full timestamps ending in `Z`, e.g. `2023-04-12T00:00:00Z`.",
        )
    if keyword == "const" and "'Feature' was expected" in message:
        return (
            f"{rec['object_type']} is being checked against an Item-only schema",
            f"The `{schema_label}` schema asserts `type: Feature`, which only Items have. "
            f"A {rec['object_type']} can never satisfy it, so this fires for every "
            f"{rec['object_type'].lower()} that declares the extension. This usually means "
            "the extension URL or version in `stac_extensions` is wrong for this object "
            "type, rather than the metadata itself being bad.",
            "Check the `stac_extensions` entry — use the version of the extension whose "
            "schema covers Collections, or drop it from Collection documents.",
        )
    if keyword == "required":
        return (
            f"Missing required property in `{path or 'the document'}`",
            message or "A property the schema marks as required is absent.",
            "Add the missing property.",
        )
    if keyword == "type":
        return (
            f"`{path}` has the wrong type",
            message or "The value's JSON type does not match the schema.",
            "Correct the value's type.",
        )

    title = f"`{path}` failed schema check" if path else "Schema validation failed"
    return (title, message or rec["raw"], "Review the value against the schema excerpt below.")


def _signature(rec: dict) -> tuple:
    """Group key: same defect shape, regardless of which object or value hit it."""
    message = rec["message"] or ""
    if rec["value"]:
        # Drop the offending literal so differing values collapse into one group.
        message = message.replace(rec["value"], "<value>")
    return (rec["object_type"], rec["failure"], rec["schema"], rec["keyword"], rec["path"], message)


def group_errors(errors: list) -> list:
    """Parse and group raw error strings, most structural / most frequent first."""
    groups = {}
    for raw in errors:
        rec = parse_error(str(raw))
        key = _signature(rec)
        if key not in groups:
            title, meaning, fix = _explain(rec)
            groups[key] = {
                "title": title,
                "meaning": meaning,
                "fix": fix,
                "object_type": rec["object_type"],
                "schema": rec["schema"],
                "schema_label": rec["schema_label"],
                "keyword": rec["keyword"],
                "path": rec["path"],
                "count": 0,
                "objects": [],
                "values": [],
                "raws": [],
                "example": rec,
            }
        g = groups[key]
        g["count"] += 1
        g["raws"].append(rec["raw"])
        if rec["object_id"]:
            label = f"{rec['object_id']} ({rec['parent']})" if rec["parent"] else rec["object_id"]
            g["objects"].append({"label": label, "href": rec["href"]})
        if rec["value"] and rec["value"] not in g["values"]:
            g["values"].append(rec["value"])

    return sorted(
        groups.values(),
        key=lambda g: (_SEVERITY.get(g["object_type"], 3), -g["count"]),
    )


def _sample(values: list, limit: int = 8) -> str:
    shown = ", ".join(f"`{v}`" for v in values[:limit])
    extra = len(values) - limit
    return f"{shown}, … and {extra} more" if extra > 0 else shown


# The rendered reports live here, so local file links are made relative to it.
_REPORT_DIR = "./data/validation_reports"


def _link_href(href) -> str | None:
    """Turn a STAC object href into something linkable from the report page.

    Remote catalogs give http(s) URLs (used as-is); local catalogs give absolute
    filesystem paths, which are rewritten relative to the report directory so the
    links work in an editor and on GitHub.
    """
    if not href:
        return None
    if href.startswith(("http://", "https://")):
        return href
    try:
        return os.path.relpath(href, os.path.abspath(_REPORT_DIR))
    except ValueError:  # e.g. different drive on Windows
        return None


def _object_links_md(objects: list, limit: int = 8) -> str:
    parts = []
    for obj in objects[:limit]:
        link = _link_href(obj["href"])
        parts.append(f"[`{obj['label']}`]({link})" if link else f"`{obj['label']}`")
    extra = len(objects) - limit
    return ", ".join(parts) + (f", … and {extra} more" if extra > 0 else "")


def render_markdown(report: dict) -> str:
    """Render the validation report as Markdown."""
    summary = report["summary"]
    status = report["overall_status"]
    status_icon = "✅" if status == "VALID" else "❌"
    errors = report.get("errors", [])
    groups = group_errors(errors)

    lines = [
        "# STAC Validation Report",
        "",
        f"- **Catalog:** `{report['catalog_url']}`",
        f"- **Status:** {status_icon} **{status}**",
        f"- **Generated:** {report.get('timestamp', '')}",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Catalogs validated | {summary['total_catalogs']} |",
        f"| Collections validated | {summary['total_collections']} |",
        f"| Items validated | {summary['total_items']} |",
        f"| Validation errors | {summary['validation_errors']} |",
        f"| Validation warnings | {summary['validation_warnings']} |",
        f"| Distinct issues | {len(groups)} |",
        "",
    ]

    if not errors:
        lines += ["## Issues", "", "No validation errors found. 🎉", ""]
    else:
        lines += [
            f"## Issues ({len(groups)} distinct, {len(errors)} errors)",
            "",
            "| # | Scope | Issue | Errors |",
            "| ---: | --- | --- | ---: |",
        ]
        for i, g in enumerate(groups, 1):
            scope = g["object_type"]
            if scope in ("Catalog", "Collection"):
                scope = f"**{scope}** ⚠️"
            lines.append(f"| {i} | {scope} | {g['title']} | {g['count']} |")
        lines.append("")

        for i, g in enumerate(groups, 1):
            flag = " ⚠️" if g["object_type"] in ("Catalog", "Collection") else ""
            lines += [
                f"### {i}. {g['title']}{flag}",
                "",
                f"- **Affects:** {g['count']} {g['object_type'].lower()}"
                f"{'s' if g['count'] != 1 else ''}",
            ]
            if g["path"]:
                lines.append(f"- **Property:** `{g['path']}`")
            if g["keyword"]:
                lines.append(f"- **Failed schema keyword:** `{g['keyword']}`")
            if g["schema"]:
                lines.append(f"- **Schema:** [{g['schema_label']}]({g['schema']})")
            if g["values"]:
                lines.append(f"- **Offending values:** {_sample(g['values'])}")
            if g["objects"]:
                lines.append(f"- **Objects:** {_object_links_md(g['objects'])}")
            lines += [
                "",
                f"**What it means:** {g['meaning']}",
                "",
                f"**Suggested fix:** {g['fix']}",
                "",
                "<details><summary>Example raw error</summary>",
                "",
                "```",
                g["example"]["raw"].rstrip(),
                "```",
                "",
                "</details>",
                "",
                f"<details><summary>All {g['count']} raw errors</summary>",
                "",
            ]
            for n, raw in enumerate(g["raws"], 1):
                lines += [f"**{n}.**", "", "```", str(raw).rstrip(), "```", ""]
            lines += ["</details>", ""]

    warnings = report.get("warnings", [])
    lines += [f"## Warnings ({len(warnings)})", ""]
    if warnings:
        lines += [f"{i}. {w}" for i, w in enumerate(warnings, 1)]
    else:
        lines.append("No warnings.")
    lines.append("")

    return "\n".join(lines)


def render_html(report: dict) -> str:
    """Render the validation report as a standalone HTML page."""
    summary = report["summary"]
    status = report["overall_status"]
    status_class = "valid" if status == "VALID" else "invalid"
    errors = report.get("errors", [])
    groups = group_errors(errors)

    def chips(values, limit=8):
        shown = "".join(f"<code>{escape(str(v))}</code>" for v in values[:limit])
        extra = len(values) - limit
        return shown + (f"<span class='more'>… and {extra} more</span>" if extra > 0 else "")

    def object_links(objects, limit=8):
        parts = []
        for obj in objects[:limit]:
            label = escape(str(obj["label"]))
            link = _link_href(obj["href"])
            parts.append(
                f"<a href='{escape(link)}'><code>{label}</code></a>" if link
                else f"<code>{label}</code>"
            )
        extra = len(objects) - limit
        return "".join(parts) + (
            f"<span class='more'>… and {extra} more</span>" if extra > 0 else ""
        )

    cards = []
    for i, g in enumerate(groups, 1):
        structural = g["object_type"] in ("Catalog", "Collection")
        meta = [f"<dt>Affects</dt><dd>{g['count']} {escape(g['object_type'].lower())}"
                f"{'s' if g['count'] != 1 else ''}</dd>"]
        if g["path"]:
            meta.append(f"<dt>Property</dt><dd><code>{escape(g['path'])}</code></dd>")
        if g["keyword"]:
            meta.append(f"<dt>Schema keyword</dt><dd><code>{escape(g['keyword'])}</code></dd>")
        if g["schema"]:
            meta.append(f"<dt>Schema</dt><dd><a href='{escape(g['schema'])}'>"
                        f"{escape(g['schema_label'] or g['schema'])}</a></dd>")
        if g["values"]:
            meta.append(f"<dt>Offending values</dt><dd>{chips(g['values'])}</dd>")
        if g["objects"]:
            meta.append(f"<dt>Objects</dt><dd>{object_links(g['objects'])}</dd>")

        raw_items = "".join(
            f"<li><pre>{escape(str(raw).rstrip())}</pre></li>" for raw in g["raws"]
        )

        cards.append(f"""
<section class="issue {'structural' if structural else ''}" id="issue-{i}">
  <h3><span class="badge {escape(g['object_type'].lower())}">{escape(g['object_type'])}</span>
      {i}. {escape(g['title'])} <span class="count">{g['count']}×</span></h3>
  <dl>{''.join(meta)}</dl>
  <p><strong>What it means:</strong> {escape(g['meaning'])}</p>
  <p><strong>Suggested fix:</strong> {escape(g['fix'])}</p>
  <details><summary>Example raw error</summary>
    <pre>{escape(g['example']['raw'].rstrip())}</pre></details>
  <details><summary>All {g['count']} raw errors</summary>
    <ol class="raws">{raw_items}</ol></details>
</section>""")

    if errors:
        rows = "".join(
            f"<tr><td class='num'>{i}</td>"
            f"<td><span class='badge {escape(g['object_type'].lower())}'>"
            f"{escape(g['object_type'])}</span></td>"
            f"<td><a href='#issue-{i}'>{escape(g['title'])}</a></td>"
            f"<td class='num'>{g['count']}</td></tr>"
            for i, g in enumerate(groups, 1)
        )
        issues_html = f"""
<h2>Issues ({len(groups)} distinct, {len(errors)} errors)</h2>
<table class="issues">
  <tr><th>#</th><th>Scope</th><th>Issue</th><th>Errors</th></tr>
  {rows}
</table>
{''.join(cards)}"""
    else:
        issues_html = "<h2>Issues</h2><p class='none'>No validation errors found. 🎉</p>"

    warnings = report.get("warnings", [])
    if warnings:
        warn_items = "".join(f"<li>{escape(str(w))}</li>" for w in warnings)
        warnings_html = f"<h2>Warnings ({len(warnings)})</h2><ol>{warn_items}</ol>"
    else:
        warnings_html = "<h2>Warnings (0)</h2><p class='none'>No warnings.</p>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>STAC Validation Report</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
         margin: 2rem auto; max-width: 62rem; padding: 0 1rem; line-height: 1.55; color: #1f2328; }}
  h1 {{ margin-bottom: 0.25rem; }}
  h3 {{ margin: 0 0 0.75rem; }}
  .meta {{ color: #57606a; font-size: 0.9rem; word-break: break-all; }}
  .status {{ display: inline-block; padding: 0.2rem 0.6rem; border-radius: 4px;
             font-weight: 600; color: #fff; }}
  .valid {{ background: #1a7f37; }}
  .invalid {{ background: #cf222e; }}
  table {{ border-collapse: collapse; margin: 1rem 0; width: 100%; }}
  th, td {{ border: 1px solid #d0d7de; padding: 0.4rem 0.8rem; text-align: left; }}
  td.num, th:last-child {{ text-align: right; font-variant-numeric: tabular-nums; }}
  .badge {{ display: inline-block; padding: 0.05rem 0.45rem; border-radius: 999px;
            font-size: 0.75rem; font-weight: 600; color: #fff; background: #57606a;
            vertical-align: middle; }}
  .badge.collection {{ background: #bc4c00; }}
  .badge.catalog {{ background: #cf222e; }}
  .badge.item {{ background: #0969da; }}
  .issue {{ border: 1px solid #d0d7de; border-left: 4px solid #0969da; border-radius: 6px;
            padding: 1rem 1.25rem; margin: 1rem 0; background: #f6f8fa; }}
  .issue.structural {{ border-left-color: #bc4c00; background: #fff8f2; }}
  .count {{ color: #57606a; font-weight: 400; font-size: 0.9rem; }}
  dl {{ display: grid; grid-template-columns: max-content 1fr; gap: 0.15rem 1rem; margin: 0 0 0.75rem; }}
  dt {{ color: #57606a; font-size: 0.85rem; }}
  dd {{ margin: 0; font-size: 0.9rem; word-break: break-word; }}
  code {{ background: #eaeef2; padding: 0.05rem 0.3rem; border-radius: 3px;
          font-size: 0.85em; margin-right: 0.25rem; display: inline-block; }}
  .more {{ color: #57606a; font-size: 0.85rem; }}
  pre {{ background: #fff; border: 1px solid #d0d7de; border-radius: 6px; padding: 0.75rem;
         overflow-x: auto; font-size: 0.8rem; line-height: 1.4; }}
  summary {{ cursor: pointer; color: #57606a; font-size: 0.85rem; margin-top: 0.4rem; }}
  .raws {{ max-height: 32rem; overflow-y: auto; padding-left: 2rem; }}
  .raws li {{ margin: 0.4rem 0; }}
  .raws pre {{ margin: 0.25rem 0; }}
  a code {{ color: inherit; }}
  ol li {{ margin-bottom: 0.5rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
           font-size: 0.85rem; white-space: pre-wrap; word-break: break-word; }}
  .none {{ color: #57606a; }}
</style>
</head>
<body>
<h1>STAC Validation Report</h1>
<p class="meta">Catalog: {escape(str(report['catalog_url']))}<br>
Generated: {escape(str(report.get('timestamp', '')))}</p>
<p><span class="status {status_class}">{status}</span></p>
<h2>Summary</h2>
<table>
  <tr><th>Metric</th><th>Count</th></tr>
  <tr><td>Catalogs validated</td><td class="num">{summary['total_catalogs']}</td></tr>
  <tr><td>Collections validated</td><td class="num">{summary['total_collections']}</td></tr>
  <tr><td>Items validated</td><td class="num">{summary['total_items']}</td></tr>
  <tr><td>Validation errors</td><td class="num">{summary['validation_errors']}</td></tr>
  <tr><td>Validation warnings</td><td class="num">{summary['validation_warnings']}</td></tr>
  <tr><td>Distinct issues</td><td class="num">{len(groups)}</td></tr>
</table>
{issues_html}
{warnings_html}
</body>
</html>
"""
