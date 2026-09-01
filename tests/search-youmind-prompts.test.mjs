import assert from 'node:assert/strict';
import test from 'node:test';

import { findPromptById, searchPrompts } from '../scripts/search-youmind-prompts.mjs';

test('finds a prompt by its canonical ID and returns the full content', () => {
  const result = findPromptById(12601);

  assert.equal(result.id, 12601);
  assert.equal(result.truncated, false);
  assert.ok(result.content.length > 220);
});

test('restricts results to one category', () => {
  const { matches } = searchPrompts({ query: 'thumbnail', category: 'youtube-thumbnail', limit: 5 });

  assert.ok(matches.length > 0);
  assert.ok(matches.every((item) => item.categorySlug === 'youtube-thumbnail'));
});

test('requires every query term before falling back to a relaxed match', () => {
  const strict = searchPrompts({ query: 'cyberpunk neon portrait', limit: 3 });

  assert.equal(strict.relaxed, false);
  assert.ok(strict.matches.length > 0);
});

test('filters on reference-image requirement', () => {
  const { matches } = searchPrompts({ query: 'portrait', referenceImages: false, limit: 10 });

  assert.ok(matches.length > 0);
  assert.ok(matches.every((item) => item.needReferenceImages === false));
});

test('returns no matches instead of a relaxed flag when nothing hits', () => {
  const result = searchPrompts({ query: 'qqqzzzxyzzy', limit: 3 });

  assert.equal(result.relaxed, false);
  assert.deepEqual(result.matches, []);
});

test('truncates the prompt preview unless full output is requested', () => {
  const preview = searchPrompts({ query: 'isometric', limit: 1 });
  const full = searchPrompts({ query: 'isometric', limit: 1, full: true });

  assert.ok(preview.matches[0].content.length <= 221);
  assert.equal(full.matches[0].truncated, false);
});
