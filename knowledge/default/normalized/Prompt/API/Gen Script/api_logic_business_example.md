---
source_path: Prompt/API/Gen Script/api_logic_business_example.txt
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
    And user sets API headers
      | Content-Type     | Authorization           | Connection |
      | application/json | Bearer {{access_token}} | keep-alive |
    And user sets API JSON Body
      | jsonBody     |
      | #minVal.json |

  Scenario Outline: [Test case summary] - #If Test case has database verification step
    Given user connects to DB
      | hostname        | port        | serviceName        | username        | password        |
      | @nmsbl_hostname | @nmsbl_port | @nmsbl_serviceName | @nmsbl_username | @nmsbl_password |

    When user sends "POST" request and saves response as "response"
      | field1   | field2   | field3   |
      | <field1> | <field2> | <field3> |

    And verify status code match "<httpStatusCode>"
    Then user verifies response "response" against the expected values below
      | code   | message   | response1   | response2   | response3   |
      | <code> | <message> | <response1> | <response2> | <response3> |

    And user query and save as "DTTD_TRANS_LOG"
      | query                                  |
      | select * from DTTD_TRANS_LOG where ... |
    Then user verifies SQL response "DTTD_TRANS_LOG" against the expected values below
      | column1   | column2   | column2   |
      | <column1> | <column2> | <column2> |

    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples:
      | field1 | field2 | field3 | response1 | response2 | response3 | httpStatusCode | code | message | column1   | column2   | column2   |
      | value1 | value2 | value3 | response1 | response2 | response3 | ==200          | 0    | SUCCESS | column1   | column2   | column2   |

  Scenario Outline: [Test case summary] - #If Test case has not database verification step

    When user sends "POST" request and saves response as "response"
      | field1   | field2   | field3   |
      | <field1> | <field2> | <field3> |

    And verify status code match "<httpStatusCode>"
    Then user verifies response "response" against the expected values below
      | code   | message   | response1   | response2   | response3   |
      | <code> | <message> | <response1> | <response2> | <response3> |

    @TD_P2_xxx_TC_xxx @Prefix-xxx
    Examples:
      | field1 | field2 | field3 | response1 | response2 | response3 | httpStatusCode | code | message |
      | value1 | value2 | value3 | response1 | response2 | response3 | ==200          | 0    | SUCCESS |
