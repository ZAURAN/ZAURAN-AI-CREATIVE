import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const dataPath = join(scriptDirectory, '..', 'nano-banana-pro', 'recipes.json');
const library = JSON.parse(readFileSync(dataPath, 'utf8'));

const PREVIEW_LENGTH = 320;

const normalize = (value) => String(value ?? '').trim().toLocaleLowerCase();
const asList = (value) => (Array.isArray(value) ? value : value ? [value] : []);

function shape(item, { full = false } = {}) {
  const prompt = full || item.prompt.length <= PREVIEW_LENGTH
    ? item.prompt
    : `${item.prompt.slice(0, PREVIEW_LENGTH)}…`;

  return {
    id: item.id,
    category: item.category,
    title: item.title,
    description: item.description,
    promptFormat: item.promptFormat,
    prompt,
    truncated: prompt !== item.prompt,
    source: item.source,
    images: [...item.images]
  };
}

export function listCategories() {
  return library.categories.map((item) => ({ ...item }));
}

export function findRecipeById(id) {
  const found = library.recipes.find((item) => item.id === String(id).trim());

  if (!found) throw new Error(`No recipe with ID ${id}. Use --categories to list sections.`);
  return shape(found, { full: true });
}

export function searchRecipes({ query = '', category, format, limit = 5, full = false } = {}) {
  const terms = asList(query).join(' ').split(/\s+/).map(normalize).filter(Boolean);
  const normalizedCategory = normalize(category);
  const normalizedFormat = normalize(format);
  const numericLimit = Number(limit);

  if (!Number.isInteger(numericLimit) || numericLimit < 1) {
    throw new Error('limit must be a positive integer.');
  }

  const scored = library.recipes
    .filter((item) => {
      if (!normalizedCategory) return true;
      return normalize(item.category).includes(normalizedCategory)
        || String(item.categoryNumber) === normalizedCategory;
    })
    .filter((item) => !normalizedFormat || normalize(item.promptFormat) === normalizedFormat)
    .map((item) => {
      const title = normalize(item.title);
      const description = normalize(item.description);
      const prompt = normalize(item.prompt);
      let score = 0;
      let matchedAll = true;

      for (const term of terms) {
        const inTitle = title.includes(term);
        const inDescription = description.includes(term);
        const inPrompt = prompt.includes(term);

        if (!inTitle && !inDescription && !inPrompt) matchedAll = false;
        if (inTitle) score += 3;
        if (inDescription) score += 2;
        if (inPrompt) score += 1;
      }

      return { item, score, matchedAll };
    });

  const strict = scored.filter((entry) => entry.matchedAll && (terms.length === 0 || entry.score > 0));
  const relaxed = terms.length > 0 && strict.length === 0
    ? scored.filter((entry) => entry.score > 0)
    : [];
  const chosen = strict.length > 0 || terms.length === 0 ? strict : relaxed;

  return chosen
    .sort((a, b) => b.score - a.score || a.item.index - b.item.index)
    .slice(0, numericLimit)
    .map((entry) => ({ ...shape(entry.item, { full }), relaxed: relaxed.length > 0 }));
}

function parseArguments(args) {
  const options = {};

  for (let index = 0; index < args.length; index += 1) {
    const flag = args[index];
    const value = args[index + 1];

    if (flag === '--id') options.id = value;
    else if (flag === '--query') options.query = value;
    else if (flag === '--category') options.category = value;
    else if (flag === '--format') options.format = value;
    else if (flag === '--limit') options.limit = value;
    else if (flag === '--full') { options.full = true; continue; }
    else if (flag === '--categories') { options.categories = true; continue; }
    else if (flag === '--help') return { help: true };
    else throw new Error(`Unknown argument: ${flag}`);

    index += 1;
  }

  return options;
}

function usage() {
  return [
    'Search the 70-recipe Awesome Nano Banana Pro prompt library (zauran_ai_creative snapshot).',
    '',
    'Examples:',
    '  node scripts/search-nbp-recipes.mjs --categories',
    '  node scripts/search-nbp-recipes.mjs --id 2.16 --full',
    '  node scripts/search-nbp-recipes.mjs --query "product photography" --limit 3',
    '  node scripts/search-nbp-recipes.mjs --category "Interior Design" --full',
    '  node scripts/search-nbp-recipes.mjs --query selfie --format json',
    '',
    'Terms combine with AND; if nothing matches every term, a scored relaxed pass runs',
    'and results carry "relaxed": true. Prompts are previewed at 320 chars unless --full.',
    'Every recipe keeps its original creator in "source" — carry that credit when reusing.'
  ].join('\n');
}

function main() {
  const options = parseArguments(process.argv.slice(2));

  if (options.help) {
    console.log(usage());
    return;
  }

  if (options.categories) {
    console.log(JSON.stringify(listCategories(), null, 2));
    return;
  }

  const results = options.id ? [findRecipeById(options.id)] : searchRecipes(options);
  console.log(JSON.stringify(results, null, 2));
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  try {
    main();
  } catch (error) {
    console.error(error.message);
    console.error(`\n${usage()}`);
    process.exitCode = 1;
  }
}
