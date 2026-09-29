"""Check every skill in the repo: frontmatter name matches the folder, description fits the 1024-char limit, JSON files parse."""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
errors = []
skills = {root / 'SKILL.md': 'zauran-ai-creative'}
skills.update({p: p.parent.name for p in root.glob('zauran-*/SKILL.md')})
for path, expected in skills.items():
    text = path.read_text(encoding='utf-8')
    front = re.match(r'---\n(.*?)\n---\n', text.replace('\r\n', '\n'), re.S)
    if not front:
        errors.append(f'{path}: no frontmatter'); continue
    name = re.search(r'^name: (.+)$', front.group(1), re.M)
    desc = re.search(r'^description: "(.*)"$', front.group(1), re.M)
    if not name or name.group(1).strip() != expected:
        errors.append(f'{path}: name must be {expected}')
    if not desc or not desc.group(1) or len(desc.group(1)) > 1024:
        errors.append(f'{path}: description missing or over 1024 chars')
for path in root.rglob('*.json'):
    if '.git' in path.parts:
        continue
    try:
        json.loads(path.read_text(encoding='utf-8-sig'))
    except ValueError as e:
        errors.append(f'{path}: {e}')
print('\n'.join(errors) or f'{len(skills)} skills OK')
sys.exit(1 if errors else 0)
