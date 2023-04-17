const fs = require('fs');
const toc = require('markdown-toc');

const inputFile = 'README.md';

fs.readFile(inputFile, 'utf8', (err, data) => {
  if (err) {
    console.error(`Error reading file: ${err}`);
    process.exit(1);
  }

  const updatedData = toc.insert(data);
  fs.writeFile(inputFile, updatedData, (err) => {
    if (err) {
      console.error(`Error writing file: ${err}`);
      process.exit(1);
    }
    console.log('Table of Contents updated successfully.');
  });
});
