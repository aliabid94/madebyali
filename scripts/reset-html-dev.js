const fs = require('fs');

// Reset HTML files to use non-hashed CSS for development
const htmlFiles = ['./pages/index.html', './pages/fishwish.html', './pages/slumberparty.html'];

htmlFiles.forEach(filePath => {
  if (fs.existsSync(filePath)) {
    let content = fs.readFileSync(filePath, 'utf8');

    // Replace any hashed CSS reference with the standard styles.css
    content = content.replace(
      /href="\/static\/styles(?:\.[a-f0-9]{8})?\.css"/g,
      `href="/static/styles.css"`
    );

    fs.writeFileSync(filePath, content);
    console.log(`Reset ${filePath} to use styles.css`);
  }
});