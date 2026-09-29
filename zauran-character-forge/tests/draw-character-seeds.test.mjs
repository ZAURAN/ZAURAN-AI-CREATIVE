import assert from 'node:assert/strict';
import test from 'node:test';

import { db, draw, stage } from '../scripts/draw-character-seeds.mjs';

const { categories } = db;

test('same seed gives the same sets', () => {
  assert.deepEqual(draw(categories, { seed: 42 }), draw(categories, { seed: 42 }));
});

test('each set has one item from every category', () => {
  const { sets } = draw(categories, { count: 2, seed: 7 });

  for (const set of sets) {
    assert.deepEqual(Object.keys(set), Object.keys(categories));
    for (const [id, value] of Object.entries(set)) assert.ok(categories[id].items.includes(value));
  }
});

test('sets in one draw do not repeat an item within a category', () => {
  const { sets } = draw(categories, { count: 5, seed: 1 });
  const occupations = sets.map((s) => s.occupation);

  assert.equal(new Set(occupations).size, 5);
});

test('--only limits the categories', () => {
  const { sets } = draw(categories, { only: ['talisman', 'palette'], seed: 3 });

  assert.deepEqual(Object.keys(sets[0]), ['talisman', 'palette']);
});

test('rejects an unknown category and a bad count', () => {
  assert.throws(() => draw(categories, { only: ['nope'] }), /Unknown category/);
  assert.throws(() => draw(categories, { count: 0 }), /positive integer/);
});

test('seed list has no duplicate items', () => {
  for (const [id, c] of Object.entries(categories)) {
    assert.equal(new Set(c.items).size, c.items.length, id);
  }
});

test('stages name only existing categories', () => {
  for (const [id, list] of Object.entries(db.stages)) {
    assert.deepEqual(Object.keys(draw(categories, { only: stage(id), seed: 5 }).sets[0]), list);
  }
  assert.throws(() => stage('nope'), /Unknown stage/);
});

test('contradictions do not name a job that clashes with the occupation seed', () => {
  const jobs = /мясник|врач|инженер|переговорщик|спасатель|работа/;
  assert.deepEqual(categories.contradiction.items.filter((x) => jobs.test(x)), []);
});
