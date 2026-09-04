#!/usr/bin/env node
// Поиск по словарю кино-терминов (references/shot-vocabulary.json).
// Использование:
//   node scripts/search-shot-vocabulary.mjs --query "orbit"            # подстрока по термину/фразе/эффекту/когда
//   node scripts/search-shot-vocabulary.mjs --cat "Движение камеры"     # фильтр по категории
//   node scripts/search-shot-vocabulary.mjs --scope Видео --power Сильно
//   node scripts/search-shot-vocabulary.mjs --cats                      # список категорий
//   node scripts/search-shot-vocabulary.mjs --json                      # вывод JSON вместо таблицы
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const db = JSON.parse(readFileSync(join(here, '..', 'references', 'shot-vocabulary.json'), 'utf8'));

const args = process.argv.slice(2);
const opt = {};
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '--help' || a === '-h') { help(); process.exit(0); }
  if (a === '--cats' || a === '--json') { opt[a.slice(2)] = true; continue; }
  if (a.startsWith('--')) { opt[a.slice(2)] = args[++i] ?? ''; }
}

function help() {
  console.log(readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').filter(l => l.startsWith('//')).map(l => l.slice(3)).join('\n'));
}

export function search(items, { query, cat, scope, power } = {}) {
  const q = (query ?? '').toLowerCase().trim();
  return items.filter(it =>
    (!cat || it.cat.toLowerCase() === cat.toLowerCase()) &&
    (!scope || it.scope === scope) &&
    (!power || it.power === power) &&
    (!q || [it.term, it.phrase ?? '', it.effect, it.when].join(' ').toLowerCase().includes(q))
  );
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  if (opt.cats) {
    const counts = {};
    for (const it of db.items) counts[it.cat] = (counts[it.cat] ?? 0) + 1;
    for (const [c, n] of Object.entries(counts)) console.log(`${c} — ${n}`);
    process.exit(0);
  }
  const res = search(db.items, opt);
  if (opt.json) { console.log(JSON.stringify(res, null, 2)); process.exit(0); }
  if (!res.length) { console.log('Ничего не найдено.'); process.exit(0); }
  for (const it of res) {
    console.log(`• ${it.term}  [${it.cat} · ${it.scope} · ${it.power}]`);
    if (it.phrase) console.log(`  phrase: ${it.phrase}`);
    console.log(`  что делает: ${it.effect}`);
    console.log(`  когда: ${it.when}`);
  }
  console.log(`\n${res.length} из ${db.items.length}`);
}
