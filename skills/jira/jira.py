#!/usr/bin/env python3

"""
Fetch a Jira ticket and convert to markdown.

Usage: jira.py TICKET-KEY [--comments N]
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from typing import Any


def adf_to_markdown(node: dict[str, Any], context: dict[str, Any] | None = None) -> str:
    """Convert Atlassian Document Format (ADF) to markdown.

    Args:
        node: ADF node (dict with type, content, attrs, marks, text fields)
        context: Optional context for tracking state (list depth, table mode, etc.)

    Returns:
        Markdown string
    """
    if context is None:
        context = {"list_depth": 0, "in_table": False}

    node_type = node.get("type", "")
    content = node.get("content", [])
    attrs = node.get("attrs", {})
    text = node.get("text", "")
    marks = node.get("marks", [])

    # Text nodes with marks
    if node_type == "text":
        result = text
        # Apply marks in order: code, strong, em, link, etc.
        for mark in marks:
            mark_type = mark.get("type", "")
            if mark_type == "code":
                result = f"`{result}`"
            elif mark_type == "strong":
                result = f"**{result}**"
            elif mark_type == "em":
                result = f"*{result}*"
            elif mark_type == "link":
                href = mark.get("attrs", {}).get("href", "")
                result = f"[{result}]({href})"
            elif mark_type == "strike":
                result = f"~~{result}~~"
        return result

    # Block elements
    if node_type == "doc":
        return "".join(adf_to_markdown(child, context) for child in content)

    elif node_type == "paragraph":
        if context.get("in_list_item"):
            # Don't add extra newlines inside list items
            return "".join(adf_to_markdown(child, context) for child in content)
        return "".join(adf_to_markdown(child, context) for child in content) + "\n\n"

    elif node_type == "heading":
        level = attrs.get("level", 1)
        heading_text = "".join(adf_to_markdown(child, context) for child in content)
        return f"{'#' * level} {heading_text}\n\n"

    elif node_type == "codeBlock":
        language = attrs.get("language", "")
        code_text = "".join(adf_to_markdown(child, context) for child in content)
        # Ensure code block ends with newline before closing backticks
        if code_text and not code_text.endswith("\n"):
            code_text += "\n"
        return f"```{language}\n{code_text}```\n\n"

    elif node_type == "bulletList":
        context["list_depth"] += 1
        result = "".join(adf_to_markdown(child, context) for child in content)
        context["list_depth"] -= 1
        return result + ("\n" if context["list_depth"] == 0 else "")

    elif node_type == "orderedList":
        context["list_depth"] += 1
        # Save previous counter if exists (for nested lists)
        prev_counter = context.get("list_counter")
        context["list_counter"] = attrs.get("order", 1)
        result = "".join(adf_to_markdown(child, context) for child in content)
        # Restore previous counter or remove it
        if prev_counter is not None:
            context["list_counter"] = prev_counter
        else:
            context.pop("list_counter", None)
        context["list_depth"] -= 1
        return result + ("\n" if context["list_depth"] == 0 else "")

    elif node_type == "listItem":
        indent = "  " * (context["list_depth"] - 1)
        context["in_list_item"] = True
        item_content = "".join(adf_to_markdown(child, context) for child in content)
        context["in_list_item"] = False

        # Determine bullet style
        if "list_counter" in context:
            bullet = f"{context['list_counter']}."
            context["list_counter"] += 1
        else:
            bullet = "-"

        # Handle multi-paragraph list items
        lines = item_content.strip().split("\n\n")
        if len(lines) > 1:
            first = f"{indent}{bullet} {lines[0]}\n"
            rest = "\n\n".join(f"{indent}  {line}" for line in lines[1:])
            return first + rest + "\n"
        return f"{indent}{bullet} {item_content.strip()}\n"

    elif node_type == "blockquote":
        quoted = "".join(adf_to_markdown(child, context) for child in content)
        # Prefix each line with >
        lines = quoted.strip().split("\n")
        return "\n".join(f"> {line}" for line in lines) + "\n\n"

    elif node_type == "rule":
        return "---\n\n"

    elif node_type == "table":
        context["in_table"] = True
        rows = [adf_to_markdown(child, context) for child in content]
        context["in_table"] = False

        # Build markdown table
        if not rows:
            return ""

        # First row is header, add separator after it
        result = rows[0]
        # Count columns from first row
        col_count = rows[0].count("|") - 1
        result += "| " + " | ".join(["---"] * col_count) + " |\n"
        result += "".join(rows[1:])
        return result + "\n"

    elif node_type == "tableRow":
        cells = [adf_to_markdown(child, context) for child in content]
        return "| " + " | ".join(cells) + " |\n"

    elif node_type in ("tableHeader", "tableCell"):
        return "".join(adf_to_markdown(child, context) for child in content).strip()

    elif node_type == "hardBreak":
        return "\n"

    elif node_type == "panel":
        # Jira panels (info, warning, note, etc.) -> blockquotes
        panel_type = attrs.get("panelType", "info")
        panel_content = "".join(adf_to_markdown(child, context) for child in content)
        label = panel_type.capitalize()
        lines = panel_content.strip().split("\n")
        result = f"> **{label}:** {lines[0]}\n" if lines else f"> **{label}:**\n"
        for line in lines[1:]:
            result += f"> {line}\n"
        return result + "\n"

    # Default: process children
    return "".join(adf_to_markdown(child, context) for child in content)


def extract_comments(raw_data: dict[str, Any], limit: int | None = None) -> str:
    """Extract and format comments from raw Jira API response."""
    comments_data = raw_data.get("fields", {}).get("comment", {}).get("comments", [])

    if not comments_data:
        return ""

    if limit is not None:
        comments_data = comments_data[:limit]

    result = []
    for comment in comments_data:
        author = comment.get("author", {}).get("displayName", "Unknown")
        created = comment.get("created", "")[:10]  # Just the date part
        body = comment.get("body", {})

        if body and body.get("type") == "doc":
            body_md = adf_to_markdown(body)
            result.append(f"**{author}** ({created}):\n\n{body_md}")

    return "\n---\n\n".join(result)


def die(msg: str) -> None:
    """Print error and exit."""
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_args(argv: list[str]) -> tuple[str, int | None]:
    """Parse CLI arguments and return (key, comments_limit)."""
    args = list(argv)
    if not args:
        die("Usage: jira.py TICKET-KEY [--comments N]")

    key = args.pop(0)
    if not re.match(r"^[A-Z]+-[0-9]+$", key):
        die(f"Invalid ticket key '{key}'. Expected format: PROJ-123")

    comments_n: int | None = None
    while args:
        if args[0] == "--comments":
            args.pop(0)
            if not args:
                die("--comments requires a number")
            try:
                comments_n = int(args.pop(0))
            except ValueError:
                die(f"Invalid number for --comments: {args[0]}")
        else:
            die(f"Unknown argument '{args[0]}'")

    return key, comments_n


def fetch_ticket(key: str) -> dict[str, Any]:
    """Fetch ticket data from Jira CLI and return parsed JSON."""
    if not shutil.which("jira"):
        die(
            "jira CLI not found. "
            "Install: https://github.com/ankitpokhrel/jira-cli"
        )

    cmd = ["jira", "issue", "view", key, "--raw"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        die(f"Failed to fetch {key}: {result.stderr.strip()}")

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        die(f"Failed to parse Jira response: {e}")


def main() -> None:
    """Main entry point."""
    key, comments_limit = parse_args(sys.argv[1:])

    raw_data = fetch_ticket(key)
    fields = raw_data.get("fields", {})

    # Extract metadata
    title = fields.get("summary", key)
    status = fields.get("status", {}).get("name", "Unknown")

    # Build proper browse link
    self_link = raw_data.get("self", "")
    if self_link:
        # Extract base URL and replace API path with browse
        base_url = self_link.split("/rest/api/")[0]
        link = f"{base_url}/browse/{key}"
    else:
        link = f"https://jira.example.com/browse/{key}"

    # Convert description from ADF to markdown
    description = fields.get("description", {})
    if description and description.get("type") == "doc":
        body = adf_to_markdown(description).strip()
    else:
        body = "No description available."

    # Extract comments if requested
    comments_body = ""
    if comments_limit is not None:
        comments_body = extract_comments(raw_data, comments_limit)

    # Write output
    print(f"---")
    print(f'title: "{title.replace('"', '\\"')}"')
    print(f"status: {status}")
    print(f"link: {link}")
    if comments_body:
        print("comments: true")
    print(f"---\n")
    print(f"# {title}\n")
    print(body)

    if comments_body:
        print(f"\n## Comments\n")
        print(comments_body)


if __name__ == "__main__":
    main()