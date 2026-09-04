import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { search } from '../scripts/search-shot-vocabulary.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const db = JSON.parse(readFileSync(join(here, '..', 'references', 'shot-vocabulary.json'), 'utf8'));

test('словарь валиден и полон', () => {
  assert.ok(db.items.length >= 90);
  for (const it of db.items) {
    assert.ok(it.term && it.cat && it.effect && it.when, `пустое поле у ${it.term}`);
    assert.ok(['Видео', 'Фото', 'Оба'].includes(it.scope), it.term);
    assert.ok(['Сильно', 'Средне', 'Тонко'].includes(it.power), it.term);
  }
});

test('поиск по подстроке и фильтрам', () => {
  assert.ok(search(db.items, { query: 'orbit' }).length >= 2);
  assert.ok(search(db.items, { cat: 'Свет' }).every(i => i.cat === 'Свет'));
  assert.ok(search(db.items, { scope: 'Видео', power: 'Сильно' }).length > 0);
  assert.equal(search(db.items, { query: 'zzz-нет-такого' }).length, 0);
});
