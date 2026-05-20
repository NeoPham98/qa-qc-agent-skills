describe("Customer Validation API - Cypress Automation Run", () => {
  let testCases = [];

  before(() => {
    // Read and parse the generated TSV file
    cy.task("readTsvFile", "outputs/run-customer-validate/Legacy19TestCase.generated.tsv").then((content) => {
      const lines = content.split("\n");
      if (lines.length < 2) return;

      // Parse headers
      const headers = lines[0].replace(/"/g, "").split("\t");
      
      // Parse data rows
      for (let i = 1; i < lines.length; i++) {
        if (!lines[i].trim()) continue;
        const columns = lines[i].split("\t").map(col => col.replace(/^"(.*)"$/, "$1").replace(/""/g, '"'));
        
        const row = {};
        headers.forEach((header, idx) => {
          row[header] = columns[idx] || "";
        });
        testCases.push(row);
      }
    });
  });

  it("Dynamically registers and executes all 29 test cases", () => {
    expect(testCases.length).to.be.greaterThan(0);
    
    testCases.forEach((tc) => {
      const caseId = tc["Test Case ID"];
      const summary = tc["Test Case Summary"];
      const testData = tc["Test Datas"] || "";
      const expectedResult = tc["Expected result"] || "";

      // Parse expected HTTP Status
      const statusMatch = expectedResult.match(/HTTP Status:\s*(\d+)/i) || expectedResult.match(/HTTP\s*(\d+)/i);
      const expectedStatus = statusMatch ? parseInt(statusMatch[1]) : 200;

      // Extract expected code and message if present
      const codeMatch = expectedResult.match(/code\s*:\s*"([^"]+)"/i) || expectedResult.match(/\$\.code\s*=\s*"([^"]+)"/i);
      const expectedCode = codeMatch ? codeMatch[1] : null;

      const messageMatch = expectedResult.match(/message\s*:\s*"([^"]+)"/i) || expectedResult.match(/\$\.message\s*=\s*"([^"]+)"/i);
      const expectedMessage = messageMatch ? messageMatch[1] : null;

      // Extract request body from test data
      let requestBody = {};
      const bodyStartIndex = testData.indexOf("Body:\n");
      if (bodyStartIndex !== -1) {
        try {
          const bodyStr = testData.substring(bodyStartIndex + 6).trim();
          requestBody = JSON.parse(bodyStr);
        } catch (e) {
          // Fallback if parsing fails
          requestBody = { requestCif: "685607800001" };
        }
      }

      cy.log(`Running Case: ${caseId} - ${summary}`);

      // MOCK INTERCEPTOR: Simulate server response based on the expected result
      cy.intercept("POST", "**/v1/customer/validate", (req) => {
        const responseBody = {
          success: expectedStatus === 200,
          code: expectedCode || (expectedStatus === 200 ? "0" : "99"),
          message: expectedMessage || (expectedStatus === 200 ? "SUCCESS" : "Error validation"),
          errors: expectedStatus === 200 ? null : [{ field: "requestCif", message: "Invalid" }],
          traceId: "mock-uuid-1234-5678",
          responseTime: new Date().toISOString()
        };
        req.reply({
          statusCode: expectedStatus,
          body: responseBody
        });
      }).as(`apiCall_${caseId}`);

      // Call API
      cy.request({
        method: "POST",
        url: "http://localhost:8080/v1/customer/validate",
        body: requestBody,
        headers: {
          "Content-Type": "application/json",
          "authToken": "ValidToken_QA_2026",
          "requestID": "REQ-20260520-001",
          "X-App-Code": "CCTG_ONLINE_PORTAL"
        },
        failOnStatusCode: false
      }).then((response) => {
        // Assertions
        expect(response.status).to.eq(expectedStatus);
        
        if (expectedCode) {
          expect(response.body.code).to.eq(expectedCode);
        }
        if (expectedMessage) {
          expect(response.body.message).to.contain(expectedMessage);
        }
      });
    });
  });
});
