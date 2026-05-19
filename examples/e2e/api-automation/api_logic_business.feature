Feature: API logic and business validation for domestic payment

  @TD_P3_001_TC_001
  Scenario: TD_P3_001_TC_001 rejects payment when account balance is insufficient
    Given customerId "CCTG0002" has availableBalance 50000
    And the domestic payment API endpoint POST /payments/domestic is available
    When the client submits a payment request with amount 100000
    Then the API response status is 422
    And the response contains errorCode "INSUFFICIENT_BALANCE"
