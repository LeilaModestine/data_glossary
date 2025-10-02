import re, sys, pathlib

README = pathlib.Path("README.md")
text = README.read_text(encoding="utf-8")

start_tag = "<!-- GLOSSARY:START -->"
end_tag = "<!-- GLOSSARY:END -->"

start = text.find(start_tag)
end = text.find(end_tag)
if start == -1 or end == -1 or end < start:
    sys.exit(0)  # pas de bloc, pas d'action

block = text[start+len(start_tag):end].strip("\n")
lines = [l for l in block.splitlines() if l.strip()]

# On conserve l'entête (1re et 2e lignes) puis on trie le reste
header = lines[:2]
rows = lines[2:]

def key(line: str):
    # clé de tri = première cellule (English Term), insensible à la casse/espaces
    cells = [c.strip() for c in line.strip("|").split("|")]
    return cells[0].casefold()

rows_sorted = sorted(rows, key=key)

new_block = "\n".join(header + rows_sorted)
new_text = text[:start+len(start_tag)] + "\n" + new_block + "\n" + text[end:]

if new_text != text:
    README.write_text(new_text, encoding="utf-8")
