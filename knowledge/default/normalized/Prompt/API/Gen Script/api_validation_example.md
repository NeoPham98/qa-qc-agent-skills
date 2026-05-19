---
source_path: Prompt/API/Gen Script/api_validation_example.txt
source_role: api_prompt
canonical_status: reference
redaction_status: unredacted
---
@API @AutoDeposit_4_0_0 @MinVal

Feature: Schema Validation

  Background:
    And Set environment "Auto_Deposit_4_0_0.properties"
    Given Set data link TestLink
      | TestLinkIntegration  | buildName          | planName          | flatformName | testProjectName       | user          | tag       | TL_Key       |
      | @testLinkIntegration | @testLinkBuildName | @testLinkPlanName | API          | enter_testProjectName | @testLinkUser | enter_tag | @testLinkKey |

    #API config
    Given user sets API URL <Base_API_URL> and <API_EndPoint>
      | Base_API_URL      | API_EndPoint       |
      | @AD_4_0_0_BaseURL | @AD_Min_Val_Submit |
    And user sets API headers
      | Content-Type     | Authorization           | Connection |
      | application/json | Bearer {{access_token}} | keep-alive |
    And user sets API JSON Body
      | jsonBody     |
      | #minVal.json |

  Scenario Outline: Field Missing Validation
    And delete "<field>" in jsonBody
    When user sends "POST" request and saves response as "response"
      """
      jsonBody
      """

    Then user verifies response "response" against the expected values below
      | code   | message   |
      | <code> | <message> |
    And verify status code match "<httpStatusCode>"

    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples:
      | field     | httpStatusCode | code | message                      |
      | $.transId | ==400          | 105  | Validate Field Request Error |
    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples:
      | field    | httpStatusCode | code | message                      |
      | $.acctNo | ==400          | 105  | Validate Field Request Error |
    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples:
      | field      | httpStatusCode | code | message                      |
      | $.cdMinVal | ==400          | 105  | Validate Field Request Error |

  Scenario Outline: Field 'replaceField' Empty Validation
    When user sends "POST" request and saves response as "response"
      | replaceField |
      |              |

    Then user verifies response "response" against the expected values below
      | code   | message   |
      | <code> | <message> |
    And verify status code match "<httpStatusCode>"

    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples:
      | httpStatusCode | code | message                      |
      | ==400          | 105  | Validate Field Request Error |

  Scenario Outline: Field 'replaceField' with wrong type
    When user sends "POST" request and saves response as "response"
      | replaceField   |
      | <replaceField> |

    Then user verifies response "response" against the expected values below
      | code   | message   |
      | <code> | <message> |
    And verify status code match "<httpStatusCode>"

    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples: text
      | replaceField | httpStatusCode | code | message                      |
      | abcxyz       | ==400          | 105  | Validate Field Request Error |
    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples: negative number
      | replaceField | httpStatusCode | code | message                      |
      | -1000        | ==400          | 105  | Validate Field Request Error |
    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples: decimal number
      | replaceField | httpStatusCode | code | message                      |
      | 1.5          | ==400          | 105  | Validate Field Request Error |
    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples: array
      | replaceField | httpStatusCode | code | message                      |
      | ["abc"]      | ==400          | 105  | Validate Field Request Error |
    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples: boolean
      | replaceField | httpStatusCode | code | message                      |
      | true         | ==400          | 105  | Validate Field Request Error |
    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples: special character
      | replaceField | httpStatusCode | code | message                      |
      | ~            | ==400          | 105  | Validate Field Request Error |
      | ^            | ==400          | 105  | Validate Field Request Error |
      | <            | ==400          | 105  | Validate Field Request Error |
      | >            | ==400          | 105  | Validate Field Request Error |
      | #            | ==400          | 105  | Validate Field Request Error |
      | '            | ==400          | 105  | Validate Field Request Error |
      | )            | ==400          | 105  | Validate Field Request Error |
      | (            | ==400          | 105  | Validate Field Request Error |

  Scenario Outline: Field 'replaceField' with max length
    When user sends "POST" request and saves response as "response"
      | replaceField   |
      | <replaceField> |

    Then user verifies response "response" against the expected values below
      | code   | message   |
      | <code> | <message> |
    And verify status code match "<httpStatusCode>"

    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples: max length N characters of text
      | replaceField          | httpStatusCode | code | message |
      | randomStringLength(N) | ==200          | 0    | SUCCESS |
    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples: max length N+1 characters of text
      | replaceField            | httpStatusCode | code | message                      |
      | randomStringLength(N+1) | ==400          | 105  | Validate Field Request Error |
    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples: max length N characters of number
      | replaceField       | httpStatusCode | code | message |
      | randomNumLength(N) | ==200          | 0    | SUCCESS |
    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples: max length N+1 characters of number
      | replaceField         | httpStatusCode | code | message                      |
      | randomNumLength(N+1) | ==400          | 105  | Validate Field Request Error |


