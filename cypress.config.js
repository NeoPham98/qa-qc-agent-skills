const { defineConfig } = require("cypress");
const fs = require("fs");
const path = require("path");
const http = require("http");

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // Start a tiny local http server on port 8080 for offline visits
      const server = http.createServer((req, res) => {
        res.writeHead(200, { "Content-Type": "text/html" });
        res.end("<html><body><h1>BIDV Mock Server</h1></body></html>");
      });
      server.listen(8080, "127.0.0.1");

      // Read and convert TSV to JSON fixture before running specs
      const tsvPath = path.resolve("outputs/run-customer-validate/Legacy19TestCase.generated.tsv");
      if (fs.existsSync(tsvPath)) {
        let content = fs.readFileSync(tsvPath, "utf-8");
        if (content.startsWith("\ufeff")) {
          content = content.slice(1);
        }
        const lines = content.split("\n");
        const testCases = [];
        if (lines.length >= 2) {
          const headers = lines[0].replace(/"/g, "").split("\t");
          for (let i = 1; i < lines.length; i++) {
            if (!lines[i].trim()) continue;
            const columns = lines[i].split("\t").map(col => col.replace(/^"(.*)"$/, "$1").replace(/""/g, '"'));
            const row = {};
            headers.forEach((header, idx) => {
              row[header] = columns[idx] || "";
            });
            testCases.push(row);
          }
        }
        const fixturesDir = path.resolve("cypress/fixtures");
        if (!fs.existsSync(fixturesDir)) {
          fs.mkdirSync(fixturesDir, { recursive: true });
        }
        fs.writeFileSync(path.join(fixturesDir, "testCases.json"), JSON.stringify(testCases, null, 2));
      }
    },
    supportFile: false
  }
});
