---
source_path: Prompt/API/Gen Script/api_method_header_validation_example.txt
source_role: api_prompt
canonical_status: reference
redaction_status: unredacted
---
@API @ExampleAI

Feature: Schema Validation

  Background:
    And Set environment "Group_Account.properties"
    Given Set data link TestLink
      | TestLinkIntegration  | buildName          | planName          | flatformName | testProjectName       | user          | tag       | TL_Key       |
      | @testLinkIntegration | @testLinkBuildName | @testLinkPlanName | API          | enter_testProjectName | @testLinkUser | enter_tag | @testLinkKey |

    #API config
    Given user sets API URL <Base_API_URL> and <API_EndPoint>
      | Base_API_URL      | API_EndPoint       |
      | @AD_4_0_0_BaseURL | @AD_Min_Val_Submit |

    And user sets API JSON Body
      | jsonBody     |
      | #minVal.json |

  Scenario Outline: Protocol validation

    And user sets API headers
      | Content-Type     | Authorization           |
      | application/json | Bearer {{access_token}} |
    When user sends "<Method>" request and saves response as "response"
      """
      jsonBody
      """

    And verify status code match "<httpStatusCode>"
    Then user verifies response "response" against the expected values below
      | code   |
      | <code> |

    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples:
      | Method | httpStatusCode | code |
      | GET    | ==400          | 107  |
    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples:
      | Method | httpStatusCode | code |
      | PUT    | ==400          | 107  |
    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples:
      | Method | httpStatusCode | code |
      | DELETE | ==400          | 107  |

  Scenario Outline: Authorization missing

    And user sets API headers
      | Content-Type     |
      | application/json |

    When user sends "POST" request and saves response as "response"
      """
      jsonBody
      """

    And verify status code match "<httpStatusCode>"
    Then user verifies response "response" against the expected values below
      | code   |
      | <code> |

    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples:
      | httpStatusCode | code |
      | ==400          | 107  |

  Scenario Outline: Authorization validation

    And user sets API headers
      | Content-Type     | Authorization   |
      | application/json | <Authorization> |

    When user sends "POST" request and saves response as "response"
      """
      jsonBody
      """

    And verify status code match "<httpStatusCode>"
    Then user verifies response "response" against the expected values below
      | code   |
      | <code> |

    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples: empty
      | Authorization | httpStatusCode | code |
      |               | ==400          | 107  |
    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples: not valid
      | Authorization | httpStatusCode | code |
      | not_valid     | ==400          | 107  |
    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples: expired
      | Authorization | httpStatusCode | code |
      | expired       | ==400          | 107  |
    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples: permission denied
      | Authorization     | httpStatusCode | code |
      | permission_denied | ==400          | 107  |

  Scenario Outline: Content-Type validation

    And user sets API headers
      | Content-Type   | Authorization           |
      | <Content-Type> | Bearer {{access_token}} |
    When user sends "POST" request and saves response as "response"
      """
      jsonBody
      """

    And verify status code match "<httpStatusCode>"

    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples: text/plain
      | Content-Type | httpStatusCode |
      | text/plain   | ==415          |
    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples:
      | Content-Type        | httpStatusCode |
      | multipart/form-data | ==415          |

  Scenario Outline: Content-Type missing

    And user sets API headers
      | Authorization           |
      | Bearer {{access_token}} |
    When user sends "POST" request and saves response as "response"
      """
      jsonBody
      """

    And verify status code match "<httpStatusCode>"


    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples:
      | httpStatusCode |
      | ==415          |

  Scenario Outline: 'custom-header' missing

    #missing custom header on data table, the other headers are complete
    And user sets API headers
      | Authorization           |
      | Bearer {{access_token}} |
    When user sends "POST" request and saves response as "response"
      """
      jsonBody
      """

    And verify status code match "<httpStatusCode>"

    @TD_P1_xxx_TC_xxx @Prefix-xxx
    Examples:
      | httpStatusCode |
      | ==400          |

