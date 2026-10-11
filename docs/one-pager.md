# Virtual Crew
### An agent crew for AI film production — a director's method, built as installable agent skills

**Author** Xinrui Shao · **Project** Virtual Crew (2026) · **Made for** **Demon**, a ~20-minute AIGC short (18 scenes, 210 shots)

**One line.** I built a crew of seven agent skills that carries the production paperwork for an
AI-generated film, while the director keeps the only two decisions that matter: approve the prompt,
and judge the clip.

**The problem.** A text-to-video model holds nothing in mind between shots. In a film, almost
everything is an obligation — a door that must stay the same door, a chain that must not become
handcuffs, a face that must survive a wardrobe change — and none of it survives in a prompt by
itself. So I stopped treating this as prompting and treated it as production: write the obligations
down, write them into every prompt, and check them after every take.

**What I built.** Seven skills — an orchestrator plus an asset forge, continuity supervisor, art
department, QC reviewer, line producer and ethics gate — with five templates, six Python scripts
(a script+storyboard parser, an asset extractor, a markdown→Word exporter, a prompt linter, a take
log, and the verification harness), and a fictional sanitised example project. Nothing calls a model:
the crew stops at the prompt, the report and the number; the director generates.

**What it produced on **Demon**.** A shot index of **210 shots** parsed from my own script and
storyboard; an asset document of **128 prompts** — 13 character identities, 14 variants, 76
four-direction location views (19 spaces × N/E/S/W) and 25 props — delivered as markdown and Word; a
continuity state file; prompts carrying named reverse locks; a comparison report per take; and a take
log that counts rework rounds, failure types and attribution.

**Why it is a method, not a tool.**

- **Two human gates, and only two.** Everything else is bookkeeping — which is exactly what should be automated.
- **Reverse locks.** Every prompt names what must **not** happen. About half of my rework traced back to a missing lock.
- **An empirical failure catalogue.** 15 entries, each paid for by a regenerated take, each carrying the wording that fixed it.
- **Assets before shots.** Identities pin the face in detail; variants describe only the change and copy the uploaded identity plate; locations get four directional views so a room cannot change shape when the camera turns around.

**Verification.** `make verify` — 27 checks over the parsers, the linter's severity logic, the .docx
package and the take log; exit 0 = pass. This is ad-hoc verification, not a full test suite, and it is
labelled as such.

**Links.** Repository: `<repo link>` · Case study (PDF): `docs/case-study.pdf` ·
60-second walkthrough: `<video link>`

---

**Note.** One page. Export to PDF from `docs/one-pager.docx` (or print to PDF). Fill the three
`<...>` links before submitting.
