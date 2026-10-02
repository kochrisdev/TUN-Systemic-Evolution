import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { Review } from '../.review-build/review/src/Review.js';

const base = new URL('../', import.meta.url);
const read = relative => readFile(new URL(relative, base), 'utf8');

export async function renderReport(report) {
  if (report?.schemaVersion !== 'tun-family-demo/0.1' || report.before?.schemaVersion !== 'tun-family-review/0.1' ||
      report.after?.schemaVersion !== 'tun-family-review/0.1' || report.before.caseId !== report.after.caseId) {
    throw new Error('Unsupported or mismatched family report. Generate a report with the family demo.');
  }
  const [tokens, components, layout] = await Promise.all([
    read('vendor/design/styles/tun.css'), read('vendor/design/packages/react/src/styles.css'), read('review/layout.css'),
  ]);
  const css = tokens + '\n' + components.replace("@import './tokens.css';", '') + '\n' + layout;
  const markup = renderToStaticMarkup(createElement(Review, { report }));
  return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'">' +
    '<title>TUN Evolution — Family integration review</title><style>' + css + '</style></head><body>' + markup + '</body></html>\n';
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const [input, output] = process.argv.slice(2);
  if (!input || !output) throw new Error('Usage: npm run review:render -- input.json new-output.html');
  const report = JSON.parse(await readFile(input, 'utf8'));
  await writeFile(output, await renderReport(report), { encoding: 'utf8', flag: 'wx' });
  process.stdout.write(`Created read-only report: ${output}\n`);
}
