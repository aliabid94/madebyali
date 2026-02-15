const fs = require('fs');
const path = require('path');
const glob = require('glob');

const hashFilePath = './static/.css-hash';

if (fs.existsSync(hashFilePath)) {
  const hashedFilename = fs.readFileSync(hashFilePath, 'utf8').trim();

  // Find all HTML files in pages directory
  const htmlFiles = ['./pages/index.html', './pages/fishwish.html', './pages/slumberparty.html'];

  htmlFiles.forEach(filePath => {
    if (fs.existsSync(filePath)) {
      let content = fs.readFileSync(filePath, 'utf8');

      // Replace CSS reference
      content = content.replace(
        /href="\/static\/styles(?:\.[a-f0-9]{8})?\.css"/g,
        `href="/static/${hashedFilename}"`
      );

      fs.writeFileSync(filePath, content);
      console.log(`Updated ${filePath} with ${hashedFilename}`);
    }
  });
}