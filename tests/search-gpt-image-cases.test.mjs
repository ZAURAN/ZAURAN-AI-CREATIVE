import assert from 'node:assert/strict';
import test from 'node:test';

import { findCaseById, searchCases } from '../scripts/search-gpt-image-cases.mjs';

test('finds a case by its canonical ID', () => {
  const result = findCaseById(1);

  assert.equal(result.id, 1);
  assert.equal(result.title, '信息图可视化设计');
});

test('filters cases by category and style', () => {
  const results = searchCases({ category: 'UI & Interfaces', styles: ['UI'] });

  assert.ok(results.length > 0);
  assert.ok(results.every((item) => item.category === 'UI & Interfaces'));
  assert.ok(results.every((item) => item.styles.includes('UI')));
});

test('searches prompt and title text without case sensitivity', () => {
  const results = searchCases({ query: 'urban metabolism atlas', limit: 3 });

  assert.ok(results.some((item) => item.id === 1));
});
