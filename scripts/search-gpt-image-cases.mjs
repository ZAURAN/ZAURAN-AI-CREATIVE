import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const dataPath = join(scriptDirectory, '..', 'references', 'gpt-image-2-cases.json');
const library = JSON.parse(readFileSync(dataPath, 'utf8'));

const normalize = (value) => String(value ?? '').trim().toLocaleLowerCase();
const asList = (value) => Array.isArray(value) ? value : value ? [value] : [];

function matchesAll(values, expected) {
  const normalizedValues = new Set(values.map(normalize));
  return expected.every((item) => normalizedValues.has(normalize(item)));
}

export function findCaseById(id) {
  const numericId = Number(id);
  const found = library.cases.find((item) => item.id === numericId);

  if (!found) throw new Error(`No case with ID ${id}.`);
  return { ...found, styles: [...found.styles], scenes: [...found.scenes] };
}

export function searchCases({ query = '', category, styles, scenes, limit = 5 } = {}) {
  const normalizedQuery = normalize(query);
  const requestedStyles = asList(styles).filter(Boolean);
  const requestedScenes = asList(scenes).filter(Boolean);
  const normalizedCategory = normalize(category);
  const numericLimit = Number(limit);

  if (!Number.isInteger(numericLimit) || numericLimit < 1) {
    throw new Error('limit must be a positive integer.');
  }

  return library.cases
    .filter((item) => !normalizedCategory || normalize(item.category) === normalizedCategory)
    .filter((item) => matchesAll(item.styles, requestedStyles))
    .filter((item) => matchesAll(item.scenes, requestedScenes))
    .filter((item) => {
      if (!normalizedQuery) return true;
      const searchable = [item.title, item.category, item.prompt, ...item.styles, ...item.scenes]
        .map(normalize)
        .join('\n');
      return searchable.includes(normalizedQuery);
    })
    .slice(0, numericLimit)
    .map((item) => ({ ...item, styles: [...item.styles], scenes: [...item.scenes] }));
}

function parseArguments(args) {
  const options = { styles: [], scenes: [] };

  for (let index = 0; index < args.length; index += 1) {
    const flag = args[index];
    const value = args[index + 1];

    if (flag === '--id') options.id = value;
    else if (flag === '--query') options.query = value;
    else if (flag === '--category') options.category = value;
    else if (flag === '--style') options.styles.push(value);
    else if (flag === '--scene') options.scenes.push(value);
    else if (flag === '--limit') options.limit = value;
    else if (flag === '--help') return { help: true };
    else throw new Error(`Unknown argument: ${flag}`);

    if (flag !== '--help') index += 1;
  }

  return options;
}

function usage() {
  return [
    'Search the 523-case GPT-Image-2 prompt library (zauran_ai_creative snapshot).',
    '',
    'Examples:',
    '  node scripts/search-gpt-image-cases.mjs --id 1',
    '  node scripts/search-gpt-image-cases.mjs --category "Charts & Infographics" --style Infographic --limit 3',
    '  node scripts/search-gpt-image-cases.mjs --query "product packaging" --scene Commerce --limit 5',
    '',
    'Filters combine with AND. Repeating --style or --scene requires every listed tag.'
  ].join('\n');
}

function main() {
  const options = parseArguments(process.argv.slice(2));
  if (options.help) {
    console.log(usage());
    return;
  }

  const results = options.id ? [findCaseById(options.id)] : searchCases(options);
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
