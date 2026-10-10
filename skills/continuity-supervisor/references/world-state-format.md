# World-state format (three layers)

The state file exists to guarantee one thing: **when you re-describe a character in every prompt (which you must, because the model has no memory), you describe the same thing every time.**

## Layer 1 — identity (never changes)

Age, body type, hair, permanent marks (scars), permanent wardrobe cues, the likeness assets, the voice asset. Written once per character per film.

## Layer 2 — variant (changes with story events)

An "appearance instance": outfit, body state (dry / soaked / beaten / bound), restraints, carried props, plus the **canonical wardrobe paragraph** — one paragraph to paste verbatim into prompts — and the list of reference plates to attach.

Variant changes happen for exactly three reasons:

1. change of place → different outfit
2. an event changes the body → new variant layered on the previous one
3. a prop is gained or lost

Every change is logged as a transition: `after <shot id>: <character> → V<nn>`.

## Layer 3 — state_by_shot (position and facing)

Where a character physically is at the end of a shot, which way they face, what is in their hands. Written back **only after the director approves the clip**.

```yaml
characters:
  <character_id>:
    identity:
      age: ""
      body: ""
      hair: ""
      permanent_marks: []
      likeness_assets: []
      voice_assets: []
    variants:
      V01_<slug>:
        wardrobe_paragraph: "…paste verbatim into prompts…"   # canonical
        body_state: ""
        restraints: ""
        props_held: []
        attach_assets: []
        used_in: [sc1, sc2]
    state_by_shot:
      sc1-shot11: {variant: V01_<slug>, position: "", facing: "", hands: ""}
```

## Rules

- The wardrobe paragraph is **verbatim**: identical wording in every prompt, never re-invented.
- Restraints, wounds and props carry a standing rule, e.g. *"coiled many times around both wrists, loose end hanging; not handcuffs, no shackle, no lock; never disappears, never loosens"*.
- Restraints/血/水 need a truthfulness clause: what it is, and what it is not (a chain is not handcuffs; soaked clothes are water, not blood).
- Set facts that have drifted before get promoted into `must_not_drift` for that scene, and the corresponding prompt block becomes mandatory for every shot in that room.

## Scene entries

Per scene: name, time, interior/exterior, `established_facts` (door form, floor, furniture count, light), `must_not_drift` (the ones that have burned you), and — where relevant — a boundary note (a scene that is not depicted at all, only recorded as an event).

## Props

Per prop: holder, condition, and a standing rule. A prop's condition change is a continuity fact (a bag that is soaked stays soaked; a bowl that was on the table cannot vanish from the next shot in that room).

## Why so pedantic

Because this is where AI filmmaking actually fails. Every entry in this file came from a shot that had to be regenerated: a door that turned into a double door, a chain that became handcuffs, a prop that disappeared mid-shot, a wardrobe that changed between two shots in the same room.
