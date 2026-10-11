# GitHub repo metadata (copy-paste)

## About — short description (≤350 characters)

```
An agent crew for AI film production: seven skills that turn a script and storyboard into a
verifiable shot pipeline — asset extraction with four-way location views, continuity state, prompt QC
against an empirically collected failure catalogue, and per-shot rework accounting. Generation stays
in the director's hands.
```

## Topics

```
ai-film, aigc, text-to-video, agent-skills, prompt-engineering, film-production,
continuity, storyboard, video-generation, qc, hermes-agent, claude-skills
```

## Website field (optional)

Point it at the portfolio case study once it is rendered as a PDF, or leave the field empty.

## First release note (Releases → Draft a new release, tag v0.1.0)

```
v0.1.0 — first public cut of the crew.

- seven skills: virtual-crew (orchestrator) + asset-forge, continuity-supervisor, art-department,
  qc-reviewer, line-producer, ethics-gate
- templates: asset document, prompt skeleton, watch-list, comparison report, world-state
- scripts: build_project, extract_assets, md_to_docx, prompt_lint, shot_log (+ verify_scripts)
- docs: portfolio case study; example project (fictional, sanitised) under examples/the-visitor
- verification: `make verify` — 25 checks, exit 0 = pass
```

## Repository settings worth setting

- Description: see About above. Topics: see list above.
- Licence: the repo is dual-licensed — put "MIT (code) / CC BY-NC 4.0 (docs)" in the About licence
  dropdown notes if your UI allows a custom value; otherwise pick "View licence" and link to `LICENSE`.
- Visibility: keep private until the film is released; flip to public when you decide (nothing in the
  repo needs to change — see `.gitignore` for what was kept out from the first commit).
- Social preview image: optional — a still of the pipeline diagram works better than a logo.
