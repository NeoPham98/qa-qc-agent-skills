Feature: API method and header validation for domestic payment

  @TD_P1_001_TC_001
  Scenario: TD_P1_001_TC_001 validates POST method and JSON content type
    Given the domestic payment API endpoint POST /payments/domestic is available
    And the request header Content-Type is application/json
    When the client submits a payment request with customerId "CCTG0001" and amount 100000
    Then the API response status is 200
    And the response contains resultCode "00"
