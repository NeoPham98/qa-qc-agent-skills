# API Automation Feature Contract

This contract defines runtime validation rules for API automation Gherkin `.feature` outputs.

## Required Gherkin shape

- File must contain one `Feature:` line.
- File must contain at least one `Scenario:` or `Scenario Outline:`.
- Step lines must use only `Given`, `When`, `Then`, `And`, or `But`.
- Scenario tags or scenario text must reference concrete testcase ids when testcase ids are in scope.

## Phase-specific testcase filtering

- `api_method_header_validation.feature` must include only `TD_P1_*` testcase ids.
- `api_validation.feature` must include only `TD_P2_*` testcase ids.
- `api_logic_business.feature` must include only `TD_P3_*` testcase ids.

## Content rules

- Do not use placeholder-only values such as `valid data`, `invalid data`, `TODO`, `TBD`, `như trên`, or `tương tự` when concrete values are expected.
- Do not invent SQL/schema/internal field markers unless present in the testcase or source input.
- Do not mix Method/Header, Schema/Validation, and Logic/Business testcase ids in the same phase-specific output.
- Do not reference raw sample paths in runtime output.
