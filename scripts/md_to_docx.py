#!/usr/bin/env python3
"""
md_to_docx.py — turn a markdown document into a Word .docx the director can copy prompts out of.

    md_to_docx.py IN.md [OUT.docx]

Stdlib only (no python-docx): a .docx is a zip of XML parts, and this writes the four that matter.
Handles: # / ## / ### headings, paragraphs, - list items, > quotes, **bold**, and simple pipe tables.
"""

import html
import os
import re
import sys
import zipfile

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="SimSun"/>
<w:sz w:val="21"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>
<w:pPr><w:spacing w:after="80" w:line="300" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>
<w:pPr><w:outlineLvl w:val="0"/><w:spacing w:before="240" w:after="120"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>
<w:pPr><w:outlineLvl w:val="1"/><w:spacing w:before="200" w:after="100"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="27"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>
<w:pPr><w:outlineLvl w:val="2"/><w:spacing w:before="160" w:after="80"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/>
<w:pPr><w:ind w:left="360"/></w:pPr><w:rPr><w:i/><w:color w:val="444444"/></w:rPr></w:style>
</w:styles>"""


def esc(t):
    return html.escape(t, quote=False)


INLINE = re.compile(r"\*\*(.+?)\*\*|\*([^*\n]+?)\*")


def runs(text):
    """**bold** → bold runs; *italic* → italic runs; everything else plain."""
    out, pos = [], 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            out.append(f'<w:r><w:t xml:space="preserve">{esc(text[pos:m.start()])}</w:t></w:r>')
        if m.group(1) is not None:
            out.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{esc(m.group(1))}</w:t></w:r>')
        else:
            out.append(f'<w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{esc(m.group(2))}</w:t></w:r>')
        pos = m.end()
    if pos < len(text):
        out.append(f'<w:r><w:t xml:space="preserve">{esc(text[pos:])}</w:t></w:r>')
    return "".join(out) or '<w:r><w:t xml:space="preserve"></w:t></w:r>'


def para(text, style=None):
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{ppr}{runs(text)}</w:p>"


def table(rows):
    width = max(len(r) for r in rows)
    body = []
    for row in rows:
        cells = []
        for c in (row + [""] * (width - len(row)))[:width]:
            cells.append(f"<w:tc><w:tcPr><w:tcW w:w=\"{int(9000 / width)}\" w:type=\"dxa\"/></w:tcPr>{para(c)}</w:tc>")
        body.append("<w:tr>" + "".join(cells) + "</w:tr>")
    borders = ("<w:tblBorders>" + "".join(
        f'<w:{s} w:val="single" w:sz="4" w:color="AAAAAA"/>' for s in
        ("top", "left", "bottom", "right", "insideH", "insideV")) + "</w:tblBorders>")
    return f"<w:tbl><w:tblPr>{borders}</w:tblPr>{''.join(body)}</w:tbl>"


def convert(md_path, docx_path):
    lines = open(md_path, encoding="utf-8").read().split("\n")
    body, i = [], 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.startswith("|") and i + 1 < len(lines) and set(lines[i + 1].replace("|", "").strip()) <= set("-: "):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not set(lines[i].replace("|", "").strip()) <= set("-: "):
                    rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            body.append(table(rows) if rows else "")
            continue
        if ln.startswith("### "):
            body.append(para(ln[4:], "Heading3"))
        elif ln.startswith("## "):
            body.append(para(ln[3:], "Heading2"))
        elif ln.startswith("# "):
            body.append(para(ln[2:], "Heading1"))
        elif ln.startswith("> "):
            body.append(para(ln[2:], "Quote"))
        elif ln.startswith("- "):
            body.append(para("• " + ln[2:]))
        elif ln.strip() in ("---", ""):
            body.append("")
        else:
            body.append(para(ln))
        i += 1

    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           "<w:body>" + "".join(body) +
           '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
           '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/></w:sectPr>'
           "</w:body></w:document>")

    with zipfile.ZipFile(docx_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/document.xml", doc)
    return docx_path


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".docx"
    out = convert(src, dst)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
