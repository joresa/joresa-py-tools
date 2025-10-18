import re
from typing import List, Tuple
import html

# Simple parser and formatter for rule card entries.
# Input is free-form lines; we attempt to detect sections, bullets, and IDs (hex hashes at end).

ID_RE = re.compile(r"\b[0-9a-f]{6,40}\b", re.IGNORECASE)


def parse_lines(text: str) -> List[str]:
    # Normalize line endings and split; remove empty lines at ends
    raw_lines = [ln.rstrip() for ln in text.replace('\r', '').split('\n')]
    lines = []
    for ln in raw_lines:
        # preserve leading tabs (used for explicit hierarchy input)
        mtabs = re.match(r'^(\t*)', ln)
        tabs = mtabs.group(1) if mtabs else ''
        body = ln[len(tabs):]
        # remove common bullet markers and list prefixes (•, -, *, ·, digits.) from body
        body = re.sub(r"^([\u2022\u00B7\-\*]|\d+\.)\s+", "", body)
        # also remove leading bullet characters with no space
        body = re.sub(r"^[\u2022\u00B7\-\*]+", "", body).strip()
        # collapse multiple spaces in body
        body = re.sub(r"\s+", " ", body)
        lines.append(tabs + body.rstrip())
    # drop leading/trailing empty lines
    while lines and lines[0].strip() == '':
        lines.pop(0)
    while lines and lines[-1].strip() == '':
        lines.pop()
    return lines


def format_bulleted(lines: List[str]) -> str:
    # Join lines into bullets; detect already-bulleted and preserve indentation if present
    out = []
    for ln in lines:
        if ln.strip().startswith('-') or ln.strip().startswith('*'):
            out.append(ln.strip())
        else:
            out.append('- ' + ln.strip())
    return '\n'.join(out)


def format_indented(lines: List[str]) -> str:
    # kept for backward compatibility, alias to hierarchical
    return format_hierarchical(lines)


def format_hierarchical(lines: List[str]) -> str:
    """Parse lines into boards -> categories -> cards -> rules and render with tabs.

    Improved logic:
    - For each input line, split on '->' into parts.
    - Map left-to-right: if a part contains [brackets], treat it as a board title.
      Otherwise, map parts to board/category/card/rule depending on availability.
    - Reuse existing boards/categories/cards when titles match (merge nodes) so multiple lines populate the same hierarchy.
    """

    def find_or_create_board(boards, title):
        for b in boards:
            if b.get('title') == title:
                return b
        nb = {'title': title, 'categories': []}
        boards.append(nb)
        return nb

    def find_or_create_category(board, title):
        for c in board['categories']:
            if c.get('title') == title:
                return c
        nc = {'title': title, 'cards': []}
        board['categories'].append(nc)
        return nc

    def find_or_create_card(category, title):
        for c in category['cards']:
            if c.get('title') == title:
                return c
        nc = {'title': title, 'rules': []}
        category['cards'].append(nc)
        return nc

    boards = []
    # detect if input uses explicit tabs
    uses_tabs = any(l.startswith('\t') for l in lines)
    if uses_tabs:
        # indentation-based parsing
        current_board = None
        current_cat = None
        current_card = None
        last_rule = None
        for ln in lines:
            if not ln.strip():
                continue
            tabs = len(re.match(r'^(\t*)', ln).group(1))
            text = ln.lstrip('\t').strip()

            # detect lines that are only an ID or an arrow + ID (e.g. '-> f65ef7e8' or 'f65ef7e8')
            id_only_match = re.match(r'^(?:->\s*)?([0-9a-fA-F]{6,40})\s*$', text)
            if id_only_match:
                id_val = id_only_match.group(1)
                # attach to the last parsed rule if present
                if last_rule is not None:
                    last_rule['id'] = id_val
                elif current_card is not None:
                    # otherwise attach to the current card title
                    current_card['title'] = (current_card.get('title') or '') + ' -> ' + id_val
                # consumed this line
                continue

            # Extract inline ID at end of line if present
            inline_m = re.search(r'->\s*([0-9a-f]{6,40})$', text, re.IGNORECASE)
            inline_id = ''
            if inline_m:
                inline_id = inline_m.group(1)
                # remove trailing '-> id' from text
                text = re.sub(r'->\s*' + re.escape(inline_id) + r'\s*$', '', text).strip()

            if tabs == 0:
                current_board = find_or_create_board(boards, text)
                current_cat = None
                current_card = None
                last_rule = None
                continue

            if current_board is None:
                current_board = find_or_create_board(boards, None)

            if tabs == 1:
                current_cat = find_or_create_category(current_board, text)
                current_card = None
                last_rule = None
                continue

            if tabs == 2:
                # If the line contains '->', treat it as a rule under the current category/card.
                if '->' in ln:
                    if current_cat is None:
                        current_cat = find_or_create_category(current_board, None)
                    if current_card is None:
                        current_card = find_or_create_card(current_cat, None)
                    # text already has inline id removed; use it as rule text
                    current_card['rules'].append({'text': text, 'id': inline_id})
                    last_rule = current_card['rules'][-1]
                else:
                    # card title; if inline_id present, attach to title
                    if current_cat is None:
                        current_cat = find_or_create_category(current_board, None)
                    current_card = find_or_create_card(current_cat, text)
                    if inline_id:
                        current_card['title'] = (current_card.get('title') or '') + ' -> ' + inline_id
                    last_rule = None
                continue

            # tabs >= 3: treat as rule under current card
            if tabs >= 3:
                if current_cat is None:
                    current_cat = find_or_create_category(current_board, None)
                if current_card is None:
                    current_card = find_or_create_card(current_cat, None)
                current_card['rules'].append({'text': text, 'id': inline_id})
                last_rule = current_card['rules'][-1]
                continue

        # rendering below will use boards list
        pass
    else:
        # path-based parsing (existing logic)
        i = 0
        L = len(lines)

        # First, pre-process to remove empty lines already done by parse_lines
        while i < L:
            s = lines[i].strip()
            i += 1
            if not s:
                continue

            # If the line contains '->', treat as path that may include board/category/card/rule
            if '->' in s:
                parts = [p.strip() for p in s.split('->') if p.strip()]
                # try to extract ID from the last part if present
                last_part = parts[-1]
                m = ID_RE.search(last_part)
                rule_id = m.group(0) if m else ''
                # If the last part is just an ID token (flat path like 'A -> B -> C -> id'),
                # remove that token from parts so it can be attached to the preceding element
                if rule_id and ID_RE.fullmatch(last_part):
                    parts = parts[:-1]
                     
                # Find a board part if present (prefer part that contains brackets)
                board_title = None
                board_index = None
                for idx, p in enumerate(parts):
                    if re.search(r"\[.+\]", p):
                        board_title = p
                        board_index = idx
                        break
                # If the first part looks like a board (starts with capital words and contains bracket), prefer it
                if board_title is None and parts:
                    # If the first part contains the word 'Screen' or 'Panel' or contains brackets, treat as board
                    if re.search(r"Screen|Panel|Dashboard|Menu", parts[0], re.IGNORECASE) or re.search(r"\[.+\]", parts[0]):
                        board_title = parts[0]
                        board_index = 0

                if board_title is None:
                    # fallback: use existing last board or create an unnamed board
                    if boards:
                        board = boards[-1]
                    else:
                        board = find_or_create_board(boards, None)
                    start_idx = 0
                else:
                    board = find_or_create_board(boards, board_title)
                    start_idx = board_index + 1 if board_index is not None else 1

                # Map remaining parts to category, card, and rule text
                remaining = parts[start_idx:]
                # Ensure we have at least a category container
                if not remaining:
                    # nothing else on the line, continue
                    continue

                # category = remaining[0] (if exists)
                cat_title = remaining[0] if len(remaining) >= 1 else None
                category = find_or_create_category(board, cat_title)

                # card = remaining[1] if exists
                if len(remaining) >= 2:
                    card_title = remaining[1]
                    card = find_or_create_card(category, card_title)
                    # rule text is remaining[2:] joined
                    if len(remaining) >= 3:
                        rule_text = ' -> '.join(remaining[2:])
                    else:
                        rule_text = ''
                else:
                    # no explicit card; create anonymous card to hold rule
                    card = find_or_create_card(category, None)
                    rule_text = remaining[1] if len(remaining) >= 2 else ''

                # attach rule
                if rule_text == '':
                    # if rule_text is empty but we detected a trailing id, attach the id to the card title
                    if rule_id:
                        card['title'] = (card.get('title') or '') + ' -> ' + rule_id
                    else:
                        # fallback: try to derive a sensible rule_text from the last part
                        rt = parts[-1]
                        if not ID_RE.fullmatch(rt):
                            card['rules'].append({'text': rt, 'id': ''})
                else:
                    # strip any trailing id from rule_text
                    if rule_id and rule_text.endswith(rule_id):
                        rule_text = rule_text[: -len(rule_id)].rstrip(' -')
                    card['rules'].append({'text': rule_text, 'id': rule_id})
                continue

            # If line does not contain '->', it is likely a board or category/card title
            if re.search(r"\[.+\]", s):
                # board line
                find_or_create_board(boards, s)
                continue

            # Non-arrow, non-board lines: try to attach to last board as category or card
            if not boards:
                board = find_or_create_board(boards, None)
            else:
                board = boards[-1]

            # If last category missing or last category already has cards, create new category
            if not board['categories'] or (board['categories'] and board['categories'][-1].get('cards')):
                cat = find_or_create_category(board, s)
            else:
                # otherwise treat as card title under last category
                cat = board['categories'][-1]
                find_or_create_card(cat, s)

    # Render with tabs: Board\n\tCategory\n\t\tCard\n\t\t\tRule -> ID
    out = []
    for b in boards:
        if b.get('title'):
            out.append(b['title'])
        for cat in b.get('categories', []):
            if cat.get('title'):
                out.append('\t' + cat['title'])
            for card in cat.get('cards', []):
                if card.get('title'):
                    out.append('\t\t' + card['title'])
                for rule in card.get('rules', []):
                    if rule.get('id'):
                        out.append('\t\t\t' + rule['text'] + ' -> ' + rule['id'])
                    else:
                        out.append('\t\t\t' + rule['text'])
        out.append('')

    while out and out[-1].strip() == '':
        out.pop()
    return '\n'.join(out)


def format_jira_html(lines: List[str]) -> str:
    """Return HTML suitable for pasting into Jira (IDs wrapped in <strong>), preserving indentation.

    Converts the hierarchical plain-text output into HTML by replacing leading tabs with
    visual indentation and wrapping detected IDs with <strong> tags. Uses block-level
    elements and CSS-based padding for responsive wrapping rather than non-breaking spaces.
    """
    # helper: insert <wbr> into long uninterrupted tokens so browsers and Jira can wrap
    def insert_wbr(s: str, maxlen: int = 80) -> str:
        parts = s.split(' ')
        outp = []
        for p in parts:
            if len(p) > maxlen:
                # chunk the token inserting <wbr>
                chunks = [p[i:i+maxlen] for i in range(0, len(p), maxlen)]
                outp.append('<wbr>'.join(chunks))
            else:
                outp.append(p)
        return ' '.join(outp)

    # Produce hierarchical plain text first (reuses existing logic)
    hier = format_hierarchical(lines)
    out_lines = []
    for ln in hier.splitlines():
        # count leading tabs to compute indentation
        mt = re.match(r'^(\t*)', ln)
        tabs = len(mt.group(1)) if mt else 0
        content = ln.lstrip('\t')
        # escape HTML special chars in content
        esc = html.escape(content)
        # wrap trailing IDs with <strong>
        esc = re.sub(r'->\s*([0-9a-f]{6,40})', r'-> <strong>\1</strong>', esc, flags=re.IGNORECASE)
        # insert <wbr> into very long tokens so Jira/editor can wrap long lines
        esc = insert_wbr(esc, maxlen=60)
        # Use CSS padding for indentation so lines can wrap responsively
        indent_rem = tabs * 1.25
        out_lines.append(f'<div style="padding-left:{indent_rem}rem;white-space:normal;word-break:break-word;overflow-wrap:break-word;">{esc}</div>')

    # Container: full width and allow wrapping
    container_style = 'width:100%;white-space:normal;word-break:break-word;overflow-wrap:break-word;'
    return f'<div style="{container_style}">' + ''.join(out_lines) + '</div>'


def format_rulecard(text: str, fmt: str) -> str:
    lines = parse_lines(text)
    if fmt == 'bulleted':
        return format_bulleted(lines)
    elif fmt in ('indented', 'hierarchical'):
        return format_hierarchical(lines)
    elif fmt == 'jira_html':
        return format_jira_html(lines)
    else:
        return text
