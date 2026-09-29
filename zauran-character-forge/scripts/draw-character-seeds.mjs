#!/usr/bin/env node
// Случайные зацепки для персонажей (references/character-seeds.json).
// Модель сама выбирает самое вероятное — отсюда штампы. Скрипт тянет случайно.
// Использование:
//   node scripts/draw-character-seeds.mjs                      # 3 набора, все категории
//   node scripts/draw-character-seeds.mjs --count 5            # 5 наборов
//   node scripts/draw-character-seeds.mjs --stage concept --count 8   # этап концептов: занятие, противоречие, талисман, тайна
//   node scripts/draw-character-seeds.mjs --stage concept-any          # то же + природа персонажа (не только человек)
//   node scripts/draw-character-seeds.mjs --stage look --count 1       # этап внешности и одежды
//   node scripts/draw-character-seeds.mjs --only occupation,contradiction,talisman
//   node scripts/draw-character-seeds.mjs --seed 42            # повторить прошлый результат
//   node scripts/draw-character-seeds.mjs --cats               # список категорий и этапов
//   node scripts/draw-character-seeds.mjs --json               # вывод JSON
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
export const db = JSON.parse(readFileSync(join(here, '..', 'references', 'character-seeds.json'), 'utf8'));

function mulberry32(a) {
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Внутри одного вызова наборы не повторяют пункт категории, пока пункты не кончились.
export function draw(categories, { count = 3, seed, only } = {}) {
  const ids = only?.length ? only : Object.keys(categories);
  for (const id of ids) if (!categories[id]) throw new Error(`Unknown category: ${id}`);
  if (!Number.isInteger(count) || count < 1) throw new Error('count must be a positive integer');
  const s = seed ?? Math.floor(Math.random() * 2 ** 31);
  const rnd = mulberry32(s);
  const shuffled = Object.fromEntries(ids.map((id) => {
    const a = [...categories[id].items];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(rnd() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return [id, a];
  }));
  const sets = Array.from({ length: count }, (_, n) =>
    Object.fromEntries(ids.map((id) => [id, shuffled[id][n % shuffled[id].length]])));
  return { seed: s, sets };
}

export function stage(id) {
  if (!db.stages[id]) throw new Error(`Unknown stage: ${id}`);
  return db.stages[id];
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const args = process.argv.slice(2);
  const opt = {};
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--help' || a === '-h') {
      console.log(readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').filter((l) => l.startsWith('//')).map((l) => l.slice(3)).join('\n'));
      process.exit(0);
    }
    if (a === '--cats' || a === '--json') { opt[a.slice(2)] = true; continue; }
    if (a.startsWith('--')) opt[a.slice(2)] = args[++i] ?? '';
  }
  const { categories } = db;
  if (opt.cats) {
    for (const [id, c] of Object.entries(categories)) console.log(`${id} — ${c.title} (${c.items.length})`);
    for (const [id, list] of Object.entries(db.stages)) console.log(`--stage ${id}: ${list.join(', ')}`);
    process.exit(0);
  }
  const res = draw(categories, {
    count: opt.count === undefined ? 3 : Number(opt.count),
    seed: opt.seed === undefined ? undefined : Number(opt.seed),
    only: opt.stage ? stage(opt.stage) : opt.only?.split(',').map((x) => x.trim()).filter(Boolean),
  });
  if (opt.json) { console.log(JSON.stringify(res, null, 2)); process.exit(0); }
  res.sets.forEach((set, n) => {
    console.log(`Набор ${n + 1}`);
    for (const [id, v] of Object.entries(set)) console.log(`  ${categories[id].title}: ${v}`);
    console.log('');
  });
  console.log(`seed: ${res.seed} (повторить: --seed ${res.seed})`);
}
