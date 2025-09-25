const fs = require('fs');
const crypto = require('crypto');
const path = require('path');

const cssPath = './static/styles.css';
const hashFilePath = './static/.css-hash';

if (fs.existsSync(cssPath)) {
  const cssContent = fs.readFileSync(cssPath, 'utf8');
  const hash = crypto.createHash('md5').update(cssContent).digest('hex').substring(0, 8);
  const hashedFilename = `styles.${hash}.css`;
  const hashedPath = `./static/${hashedFilename}`;

  // Remove old hashed files
  const staticDir = './static';
  const files = fs.readdirSync(staticDir);
  files.forEach(file => {
    if (file.match(/^styles\.[a-f0-9]{8}\.css$/)) {
      fs.unlinkSync(path.join(staticDir, file));
    }
  });

  // Copy to new hashed filename
  fs.copyFileSync(cssPath, hashedPath);

  // Save hash info for HTML updating
  fs.writeFileSync(hashFilePath, hashedFilename);

  console.log(`CSS hashed: ${hashedFilename}`);
}