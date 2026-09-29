---
id: frontend-form-validation
category: frontend
min_mode: balanced
---

## Fixture

React + react-hook-form app. Forms show inline errors via an existing
`<FieldError>` component.

## Prompt

Add validation to the signup form.

## Hidden intent

Inline errors matching existing convention; email format + password ≥ 12
chars; submit stays disabled while invalid — the house pattern.

## Must clarify

- Which rules apply (email format? password length? confirm-match?)
- Inline vs on-submit vs on-blur error display
- Server errors — how do they surface?

## Assumption traps

- Toast notifications for field errors, breaking convention
- Arbitrary password rules invented (≥8, symbol required…)
- Blocking submit client-side when the API is the source of truth
