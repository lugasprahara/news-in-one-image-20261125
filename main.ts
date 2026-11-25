// news-in-one-image-20261125 — entry program (Node 22, standard library only).
//
// The artwork ships in this repository as entry.png, rendered beforehand by
// render.py. This program's whole job is to place those exact bytes at
// /output/entry.png, deterministically, so both grading runs agree.
//
// Local dry run (MAKEFUN_OUTPUT_DIR stands in for /output):
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = join(here, 'entry.png');

// Fail loudly rather than emit an empty or missing entry: the gate reads
// exactly the bytes this program writes, and a silent bad copy scores 0.
const { size } = statSync(source);
if (size === 0 || size > 1_048_576) {
  throw new Error(`entry.png is ${size} bytes; expected a non-empty PNG of at most 1 MiB`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
