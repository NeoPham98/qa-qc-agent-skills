Feature: API schema validation for domestic payment

  @TD_P2_001_TC_001
  Scenario: TD_P2_001_TC_001 rejects missing amount field
    Given the domestic payment API endpoint POST /payments/domestic is available
    And the request body contains customerId "CCTG0001" and beneficiaryAccount "970400000001"
    When the client submits the request without the amount field
    Then the API response status is 400
    And the response contains errorCode "AMOUNT_REQUIRED"
