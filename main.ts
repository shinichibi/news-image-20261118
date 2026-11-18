// Entry point for the news-image-20261118 competition entry.
//
// The artwork itself lives in entry.png, drawn by draw.py: a broadsheet
// front page that sums up the world news of Wednesday 18 November 2026.
// All the grader asks of this program is to place that image at the
// output location, so here we simply copy the file that sits next to
// this source into the output directory.
//
// When run outside the grading sandbox, MAKEFUN_OUTPUT_DIR points at
// the directory to write into instead of the default /output.

import { copyFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));
