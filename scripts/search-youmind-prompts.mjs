import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const dataDirectory = join(scriptDirectory, '..', 'references', 'youmind-prompts');

const PREVIEW_LENGTH = 220;

const normalize = (value) => String(value ?? '').trim().toLocaleLowerCase();

function loadManifest() {
  return JSON.parse(readFileSync(join(dataDirectory, 'manifest.json'), 'utf8'));
}

function categoryFiles(requested) {
  const manifest = loadManifest();
  if (!requested) return manifest.categories;

  const wanted = normalize(requested);
  const matched = manifest.categories.filter((category) =>
    normalize(category.slug) === wanted ||
    normalize(category.title) === wanted ||
    normalize(category.title).includes(wanted) ||
    normalize(category.slug).includes(wanted));

  if (matched.length === 0) {
    const known = manifest.categories.map((category) => category.slug).join(', ');
    throw new Error(`Unknown category "${requested}". Known slugs: ${known}`);
  }
  return matched;
}

function readCategory(category) {
  const prompts = JSON.parse(readFileSync(join(dataDirectory, category.file), 'utf8'));
  return prompts.map((prompt) => ({ ...prompt, category: category.title, categorySlug: category.slug }));
}

function scorePrompt(prompt, terms) {
  const title = normalize(prompt.title);
  const description = normalize(prompt.description);
  const content = normalize(prompt.content);

  let score = 0;
  let matchedTerms = 0;

  for (const term of terms) {
    let termScore = 0;
    if (title.includes(term)) termScore += 3;
    if (description.includes(term)) termScore += 2;
    if (content.includes(term)) termScore += 1;
    if (termScore > 0) matchedTerms += 1;
    score += termScore;
  }

  return { score, matchedTerms };
}

function shape(prompt, full) {
  const content = full || prompt.content.length <= PREVIEW_LENGTH
    ? prompt.content
    : `${prompt.content.slice(0, PREVIEW_LENGTH)}…`;

  return {
    id: prompt.id,
    title: prompt.title,
    category: prompt.category,
    categorySlug: prompt.categorySlug,
    description: prompt.description,
    needReferenceImages: Boolean(prompt.needReferenceImages),
    sampleImage: prompt.sourceMedia?.[0] ?? null,
    galleryUrl: `https://youmind.com/nano-banana-pro-prompts?id=${prompt.id}`,
    truncated: !full && prompt.content.length > PREVIEW_LENGTH,
    content
  };
}

export function findPromptById(id) {
  const numericId = Number(id);
  for (const category of loadManifest().categories) {
    const found = readCategory(category).find((prompt) => prompt.id === numericId);
    if (found) return shape(found, true);
  }
  throw new Error(`No prompt with ID ${id}.`);
}

export function searchPrompts({ query = '', category, limit = 5, full = false, referenceImages } = {}) {
  const numericLimit = Number(limit);
  if (!Number.isInteger(numericLimit) || numericLimit < 1) {
    throw new Error('limit must be a positive integer.');
  }

  const terms = normalize(query).split(/\s+/).filter(Boolean);
  const seen = new Set();
  const pool = categoryFiles(category)
    .flatMap(readCategory)
    .filter((prompt) => referenceImages === undefined || Boolean(prompt.needReferenceImages) === referenceImages)
    .filter((prompt) => !seen.has(prompt.id) && seen.add(prompt.id));

  if (terms.length === 0) {
    return { relaxed: false, matches: pool.slice(0, numericLimit).map((prompt) => shape(prompt, full)) };
  }

  const scored = pool
    .map((prompt) => ({ prompt, ...scorePrompt(prompt, terms) }))
    .filter((entry) => entry.matchedTerms > 0)
    .sort((a, b) => b.matchedTerms - a.matchedTerms || b.score - a.score);

  const strict = scored.filter((entry) => entry.matchedTerms === terms.length);
  const relaxed = strict.length === 0 && scored.length > 0;
  const selected = (strict.length === 0 ? scored : strict).slice(0, numericLimit);

  return { relaxed, matches: selected.map((entry) => shape(entry.prompt, full)) };
}

function parseArguments(args) {
  const options = {};

  for (let index = 0; index < args.length; index += 1) {
    const flag = args[index];

    if (flag === '--help') return { help: true };
    if (flag === '--categories') { options.categories = true; continue; }
    if (flag === '--full') { options.full = true; continue; }
    if (flag === '--needs-ref') { options.referenceImages = true; continue; }
    if (flag === '--no-ref') { options.referenceImages = false; continue; }

    const value = args[index + 1];
    if (value === undefined) throw new Error(`Missing value for ${flag}`);

    if (flag === '--id') options.id = value;
    else if (flag === '--query') options.query = value;
    else if (flag === '--category') options.category = value;
    else if (flag === '--limit') options.limit = value;
    else throw new Error(`Unknown argument: ${flag}`);

    index += 1;
  }

  return options;
}

function usage() {
  return [
    'Search the YouMind community prompt library (15k+ prompts, 11 use-case categories).',
    '',
    'Examples:',
    '  node scripts/search-youmind-prompts.mjs --categories',
    '  node scripts/search-youmind-prompts.mjs --query "cyberpunk avatar" --category profile-avatar --limit 3',
    '  node scripts/search-youmind-prompts.mjs --query "product white background" --category ecommerce-main-image --no-ref',
    '  node scripts/search-youmind-prompts.mjs --id 32503',
    '',
    'Flags:',
    '  --query <text>     space-separated terms; all must match (falls back to partial, sets relaxed:true)',
    '  --category <slug>  restrict to one category (omit to search all 11)',
    '  --limit <n>        max results, default 5',
    '  --full             print the full prompt instead of a 220-char preview',
    '  --needs-ref        only prompts that require reference images',
    '  --no-ref           only prompts that work without reference images',
    '  --id <n>           fetch one prompt by id (always full)',
    '  --categories       print the manifest (slugs, titles, counts, updatedAt)',
    '',
    'Never open the JSON files directly — they total ~46 MB.'
  ].join('\n');
}

function main() {
  const options = parseArguments(process.argv.slice(2));

  if (options.help) { console.log(usage()); return; }
  if (options.categories) { console.log(JSON.stringify(loadManifest(), null, 2)); return; }
  if (options.id) { console.log(JSON.stringify(findPromptById(options.id), null, 2)); return; }

  console.log(JSON.stringify(searchPrompts(options), null, 2));
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
