// Raster previews of hand-authored SVGs. This does not author slide content.
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const packages = process.env.CODEX_NODE_MODULES || path.join(process.env.USERPROFILE, '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const sharp = require(path.join(packages, 'sharp'));
const source = path.join(root, 'presentation/plc_defense_ppt169_20261026/svg_output');
const target = path.join(root, 'presentation/rendered');
fs.mkdirSync(target, {recursive: true});
(async () => {
  for (const file of fs.readdirSync(source).filter(n => n.endsWith('.svg')).sort()) {
    if (process.argv[2] && !file.startsWith(process.argv[2])) continue;
    const output = path.join(target, file.slice(0,2) + '.png');
    await sharp(path.join(source,file), {density:144}).resize(1280,720).png().toFile(output);
    console.log(output);
  }
})();
