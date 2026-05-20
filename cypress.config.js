const { defineConfig } = require("cypress");
const fs = require("fs");
const path = require("path");

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
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
    baseUrl: "http://sit-deposit.apps.uat2ttptnhs.ldapudtest.com", // Fallback URL
    supportFile: false
  }
});
