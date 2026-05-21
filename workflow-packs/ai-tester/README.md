# AI Tester Workflow Pack

This workflow pack adds a cognition-first layer before the existing QA output generation flow.

## Goal

The AI tester must act like a tester, not a direct input-to-output converter:

```text
source / prompt
-> knowledge setup
-> input understanding
-> knowledge cooking
-> reasoning / brainstorming
-> tester planning
-> existing output generation
-> validation / review / approval
-> reflection / memory update
```

## Rule

Do not call final output skills directly from raw input. Existing output skills are reused after cognition artifacts pass the cognition gate.

## Main routes

- `source_to_knowledge`
- `source_to_understanding`
- `understanding_to_cooked_knowledge`
- `cooked_knowledge_to_strategy`
- `strategy_to_outputs`
- `review_to_memory_update`

## Current status

This pack is a skeleton for implementation. It defines routes, stages, policies, contracts, and review gates. Deterministic validators for cognition artifacts can be implemented after the contracts are approved.
