import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const dataDirectory = join(scriptDirectory, '..', 'references', 'youmind-prompts');
const remoteBase = 'https://raw.githubusercontent.com/YouMind-OpenLab/ai-image-prompts-skill/main/references';

const STALE_AFTER_HOURS = 24;

const localManifest = () => JSON.parse(readFileSync(join(dataDirectory, 'manifest.json'), 'utf8'));

async function fetchJson(file) {
  const response = await fetch(`${remoteBase}/${file}`);
  if (!response.ok) throw new Error(`Failed to fetch ${file}: HTTP ${response.status}`);
  return response.text();
}

function ageInHours(manifest) {
  return (Date.now() - Date.parse(manifest.updatedAt)) / 3_600_000;
}

async function check() {
  const manifest = localManifest();
  const hours = ageInHours(manifest);
  const stale = hours > STALE_AFTER_HOURS;
  console.log(JSON.stringify({
    updatedAt: manifest.updatedAt,
    totalPrompts: manifest.totalPrompts,
    ageHours: Number(hours.toFixed(1)),
    stale,
    hint: stale ? 'run: node scripts/update-youmind-prompts.mjs' : 'library is fresh'
  }, null, 2));
}

async function update() {
  const remoteManifestText = await fetchJson('manifest.json');
  const remoteManifest = JSON.parse(remoteManifestText);

  for (const category of remoteManifest.categories) {
    const body = await fetchJson(category.file);
    writeFileSync(join(dataDirectory, category.file), body, 'utf8');
    console.error(`updated ${category.file} (${category.count} prompts)`);
  }

  writeFileSync(join(dataDirectory, 'manifest.json'), remoteManifestText, 'utf8');
  console.log(JSON.stringify({
    updatedAt: remoteManifest.updatedAt,
    totalPrompts: remoteManifest.totalPrompts,
    categories: remoteManifest.categories.length
  }, null, 2));
}

const wantsCheck = process.argv.includes('--check');

try {
  await (wantsCheck ? check() : update());
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
