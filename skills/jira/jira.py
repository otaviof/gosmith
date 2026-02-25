#!/usr/bin/env python3

"""
Fetch a Jira ticket and convert to markdown.

Usage: jira.py TICKET-KEY [--comments N]
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
_SECTION_SEP_RE = re.compile(r"^-{10,}.*[A-Za-z].*-{10,}$")
_DESC_SEP_RE = re.compile(r"^-{10,}.*[Dd]escription.*-{10,}$")
_COMMENT_SEP_RE = re.compile(r"^-{10,}.*[Cc]omment.*-{10,}$")
_FOOTER_RE = re.compile(r"^View this issue on Jira:")
_STATUS_RE = re.compile(r"\s{2}\S+\s+(.+?)\s{2,}\u231b")


def jira_to_md(text: str) -> str:
    """Convert remaining Jira wiki markup that survives --plain rendering."""
    # {{text}} → `text` (inline code) — handles multi-line spans too.
    text = re.sub(r"\{\{(.+?)\}\}", r"`\1`", text, flags=re.DOTALL)

    # Admonition blocks: {tag}...{tag} → blockquote with label.
    for tag, label in [
        ("note", "Note"),
        ("warning", "Warning"),
        ("tip", "Tip"),
        ("info", "Info"),
    ]:
        pattern = re.compile(r"\{" + tag + r"\}(.*?)\{" + tag + r"\}", re.DOTALL)
        text = pattern.sub(r"> **" + label + r":** \1", text)
        # Handle unpaired (orphan) opening tags.
        text = text.replace("{" + tag + "}", f"> **{label}:** ")

    # {code}...{code}, {noformat} → fenced code blocks.
    text = re.sub(r"\{code(:[^}]*)?\}", "```", text)
    text = text.replace("{noformat}", "```")

    # [text|url] → [text](url) (Jira link format).
    text = re.sub(r"\[([^|]*)\|([^]]*)\]", r"[\1](\2)", text)

    return text


def join_paragraphs(raw_lines: list[str]) -> str:
    """Join wrapped lines into proper paragraphs.

    The jira-cli wraps text at column width.  This function joins consecutive
    non-blank lines, keeping structural elements (headings, separators, table
    rows, code fences) on their own lines while merging prose and bullet
    continuations.
    """
    standalone_re = re.compile(r"^(#{1,6}\s|```|-{3,})")
    table_row_re = re.compile(r"^.+\|.+$")
    table_cont_re = re.compile(r"^\|")
    block_start_re = re.compile(r"^([•\-*+]\s|\d+\.\s|>)")

    result: list[str] = []
    buf: list[str] = []

    def flush() -> None:
        if buf:
            result.append(" ".join(buf))
            buf.clear()

    for line in raw_lines:
        if not line.strip():
            flush()
            result.append("")
        elif (
            standalone_re.match(line)
            or table_row_re.match(line)
            or table_cont_re.match(line)
        ):
            flush()
            result.append(line)
        elif block_start_re.match(line):
            flush()
            buf.append(line)
        else:
            buf.append(line)

    flush()
    return "\n".join(result)


def strip_ansi(raw: str) -> list[str]:
    """Strip ANSI escape codes and trim each line."""
    return [_ANSI_RE.sub("", line).strip() for line in raw.splitlines()]


def trim_blank_edges(lines: list[str]) -> list[str]:
    """Remove leading and trailing blank lines from a list."""
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def extract_title(lines: list[str], fallback: str) -> str:
    """Return the first ``# heading`` text, or *fallback*."""
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    return fallback


def extract_link(lines: list[str]) -> str:
    """Return the last URL found in *lines* (typically the Jira link)."""
    for line in reversed(lines):
        m = re.search(r"https://\S+", line)
        if m:
            return m.group(0)
    return ""


def extract_status(lines: list[str]) -> str:
    """Parse the status from the first non-blank metadata line."""
    for line in lines:
        if line.strip():
            m = _STATUS_RE.search(line)
            return m.group(1) if m else "Unknown"
    return "Unknown"


def extract_section(
    lines: list[str],
    start_re: re.Pattern[str],
    stop_re: re.Pattern[str] | None = None,
) -> list[str]:
    """Return lines between *start_re* and the next named separator / footer."""
    result: list[str] = []
    capturing = False
    for line in lines:
        if start_re.match(line):
            capturing = True
            continue
        if not capturing:
            continue
        if _SECTION_SEP_RE.match(line) and "|" not in line:
            break
        if _FOOTER_RE.match(line):
            break
        if stop_re and stop_re.match(line):
            continue
        result.append(line)
    return trim_blank_edges(result)


def die(msg: str) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_args(argv: list[str]) -> tuple[str, str | None]:
    """Parse CLI arguments and return ``(key, comments_n)``."""
    args = list(argv)
    if not args:
        die("Usage: jira.py TICKET-KEY [--comments N]")

    key = args.pop(0)
    if not re.match(r"^[A-Z]+-[0-9]+$", key):
        die(f"Invalid ticket key '{key}'. Expected format: PROJ-123")

    comments_n: str | None = None
    while args:
        if args[0] == "--comments":
            args.pop(0)
            if not args:
                die("--comments requires a number")
            comments_n = args.pop(0)
        else:
            die(f"Unknown argument '{args[0]}'")

    return key, comments_n


def fetch_ticket(key: str, comments_n: str | None = None) -> str:
    """Run ``jira issue view`` and return raw stdout."""
    if not shutil.which("jira"):
        die("Jira ('jira') CLI not found. " +
            "Install: https://github.com/ankitpokhrel/jira-cli")

    cmd = ["jira", "issue", "view", key, "--plain"]
    if comments_n is not None:
        cmd += ["--comments", comments_n]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        die(f"Failed to fetch {key}: {result.stderr.strip()}")
    return result.stdout


def write_markdown(
    path: str,
    *,
    title: str,
    status: str,
    link: str,
    body: str,
    comments: str,
) -> None:
    """Write the final markdown file with YAML frontmatter."""
    yaml_title = title.replace('"', '\\"')
    with open(path, "w") as f:
        f.write("---\n")
        f.write(f'Title: "{yaml_title}"\n')
        f.write(f"Status: {status}\n")
        if link:
            f.write(f"Link: {link}\n")
        if comments:
            f.write("Comments: true\n")
        f.write("---\n\n")
        f.write(f"# `{title}`\n\n")
        f.write(body)
        f.write("\n")
        if comments:
            f.write("\n## Comments\n\n")
            f.write(comments)
            f.write("\n")


def main() -> None:
    key, comments_n = parse_args(sys.argv[1:])

    raw = fetch_ticket(key, comments_n)
    lines = strip_ansi(raw)

    title = extract_title(lines, fallback=key)
    link = extract_link(lines)
    status = extract_status(lines)

    body_lines = extract_section(lines, _DESC_SEP_RE)
    body = jira_to_md(join_paragraphs(body_lines))

    comments_body = ""
    if comments_n is not None:
        skip_re = re.compile(r"^Use --comments")
        comment_lines = extract_section(lines, _COMMENT_SEP_RE, stop_re=skip_re)
        if comment_lines:
            comments_body = jira_to_md(join_paragraphs(comment_lines))

    output_file = f"{key}.md"
    write_markdown(
        output_file,
        title=title,
        status=status,
        link=link,
        body=body,
        comments=comments_body,
    )
    print(f"Created {output_file}")


if __name__ == "__main__":
    main()
