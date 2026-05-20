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

      // Register custom task to read TSV file at runtime
      on("task", {
        readTsvFile(filePath) {
          const absolutePath = path.resolve(filePath);
          if (!fs.existsSync(absolutePath)) {
            throw new Error(`File not found: ${absolutePath}`);
          }
          const content = fs.readFileSync(absolutePath, "utf-8");
          return content;
        }
      });
    },
    supportFile: false
  }
});
