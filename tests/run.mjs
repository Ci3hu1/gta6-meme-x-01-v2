// tests/run.mjs — node stdlib only. Usage: node tests/run.mjs
// 1. main.ts copies a scratch POST.json to the output dir (repo has no POST.json
//    yet — the post waits for approval, so the test uses a temp one outside the repo).
// 2. meme.jpg exists and is 1200x675.
import { mkdtempSync, writeFileSync, readFileSync, existsSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';

const root = new URL('..', import.meta.url).pathname;
let failures = 0;
const check = (name, ok) => {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name}`);
  if (!ok) failures++;
};

const botDir = mkdtempSync(join(tmpdir(), 'gta6v2-bot-'));
const outDir = mkdtempSync(join(tmpdir(), 'gta6v2-out-'));
const post = { url: 'https://x.com/ci3hu1/status/1234567890123456789' };
writeFileSync(join(botDir, 'POST.json'), JSON.stringify(post));
try {
  execFileSync('node', [join(root, 'main.ts')], {
    cwd: root,
    env: { ...process.env, MAKEFUN_BOT_DIR: botDir, MAKEFUN_OUTPUT_DIR: outDir },
    stdio: 'pipe',
  });
  const copied = JSON.parse(readFileSync(join(outDir, 'POST.json'), 'utf8'));
  check('main.ts copies POST.json byte-for-byte', copied.url === post.url);
} catch (err) {
  check('main.ts copies POST.json byte-for-byte', false);
  console.error(String(err.stderr ?? err));
} finally {
  rmSync(botDir, { recursive: true, force: true });
  rmSync(outDir, { recursive: true, force: true });
}

const meme = join(root, 'meme.jpg');
check('meme.jpg exists', existsSync(meme));
if (existsSync(meme)) {
  const dims = execFileSync('python3', ['-c',
    "from PIL import Image; im=Image.open('meme.jpg'); print(im.size[0], im.size[1])"],
    { cwd: root, encoding: 'utf8' }).trim();
  check(`meme.jpg is 1200x675 (got ${dims})`, dims === '1200 675');
}

if (failures) {
  console.error(`${failures} check(s) failed`);
  process.exit(1);
}
console.log('all checks passed');
