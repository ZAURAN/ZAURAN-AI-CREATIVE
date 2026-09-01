import assert from 'node:assert/strict';
import test from 'node:test';

import { findRecipeById, listCategories, searchRecipes } from '../scripts/search-nbp-recipes.mjs';

test('lists the ten prompt categories', () => {
  const categories = listCategories();

  assert.equal(categories.length, 10);
  assert.equal(categories[0].title, 'Photorealism & Aesthetics');
});

test('finds a recipe by its canonical ID and returns the full prompt', () => {
  const result = findRecipeById('6.1');

  assert.equal(result.title, 'Composition Rescue (Smart Outpainting)');
  assert.equal(result.truncated, false);
  assert.match(result.prompt, /16:9 aspect ratio/);
});

test('rejects an unknown ID instead of returning an empty match', () => {
  assert.throws(() => findRecipeById('99.9'), /No recipe with ID/);
});

test('every recipe keeps a creator credit', () => {
  const all = searchRecipes({ limit: 70 });

  assert.equal(all.length, 70);
  assert.ok(all.every((item) => item.source && item.source.url));
});

test('restricts results to one category', () => {
  const results = searchRecipes({ category: 'Interior Design', limit: 10 });

  assert.ok(results.length > 0);
  assert.ok(results.every((item) => item.category.includes('Interior Design')));
});

test('filters by prompt format', () => {
  const results = searchRecipes({ format: 'json', limit: 20 });

  assert.ok(results.length > 0);
  assert.ok(results.every((item) => item.promptFormat === 'json'));
});

test('ranks a title match above a prompt-only match', () => {
  const results = searchRecipes({ query: 'product photography', limit: 3 });

  assert.ok(results.length > 0);
  assert.ok(/Product Photography/i.test(results[0].title));
  assert.equal(results[0].relaxed, false);
});

test('falls back to a flagged relaxed pass when no recipe matches every term', () => {
  const results = searchRecipes({ query: 'selfie quantum blockchain', limit: 3 });

  assert.ok(results.length > 0);
  assert.ok(results.every((item) => item.relaxed === true));
});

test('previews long prompts unless --full is requested', () => {
  const [preview] = searchRecipes({ query: 'cinematic keyframe', limit: 1 });
  const [full] = searchRecipes({ query: 'cinematic keyframe', limit: 1, full: true });

  assert.equal(preview.truncated, true);
  assert.equal(full.truncated, false);
  assert.ok(full.prompt.length > preview.prompt.length);
});

test('rejects a non-positive limit', () => {
  assert.throws(() => searchRecipes({ limit: 0 }), /positive integer/);
});
