# UI Test Design From RSD/PTTK-UI

**Original source**: `BIDV/Prompt/UI/UI_Gen_TD.txt`

## Objective

Generate full Web UI Test Design as Markmap-compatible Markdown for all screens and sequential flows in RSD/PTTK-UI.

## Source rules

- RSD provides screens, fields, buttons, grids, popups, navigation, business rules and error messages.
- PTTK-UI provides API behavior, UI-field/API mapping, response-to-UI behavior, and special interactions.
- Highlighted/red UI elements in mockup are priority scope.
- Only generate conditions for highlighted elements unless RSD/PTTK explicitly defines a rule for another element.
- Do not create screen, field, rule, message or flow outside RSD/PTTK.

## Coverage techniques

Each screen/flow should cover applicable:

- ECP.
- BVA.
- Decision Table.
- State Transition.
- Error Guessing.

## Output contract

```markdown
# <Tên file RSD>
## <Tên Function / Màn hình / Flow>
### TD_<NNN> - [<Technique>] - <UI element/rule + partition/boundary/state>
- **Steps**: <High-level UI action>
- **Expected**: <High-level UI/API/DB behavior>
```

## Prohibitions

- Do not output coverage matrix or analysis text.
- Do not write detailed numbered test steps; this is Test Design, not Test Case.
- Do not use vague text: `như trên`, `tương tự`, `data hợp lệ`, `max length OK`.
- Do not verify layout/color/responsive unless RSD/PTTK explicitly requires it.
- Assumption must appear in the Test Condition title or Expected, not hidden.
