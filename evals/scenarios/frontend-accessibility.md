---
id: frontend-modal
category: frontend
min_mode: balanced
---

## Fixture

Vue 3 app, hand-rolled components, no component library. Design tokens in
`tokens.css`.

## Prompt

Add a confirmation modal for deleting an item.

## Hidden intent

Reusable `AppModal` following existing component style; Escape + backdrop
close; focus trapped; destructive confirm button styled as danger.

## Must clarify

- Reusable component vs inline markup
- Close behaviors (Esc, backdrop, explicit cancel)
- Destructive-styling / focus expectations

## Assumption traps

- Adding a component library dependency for one modal
- `window.confirm` shortcut
- No keyboard/focus handling in a codebase that otherwise ships it
