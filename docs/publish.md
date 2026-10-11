# Publishing this repo (checklist for the day you make a GitHub account)

Everything here is ready; this file is just the sequence. Nothing in it touches private project data.

## 0 · Before you push — sanity check

```
cd ~/Desktop/virtual-crew
make lint && make verify      # expect: py_compile ok + ALL PASS (31 checks)
git status                    # expect: clean
```

Confirm the figures are present: `ls docs/figures/` should list `step1-agent-shot-prompt.jpg`,
`step2-agent-qc-report.jpg`, `step3-agent-comparison.jpg`, `step4-terminal-verify.jpg`.

## 1 · Create the repository

- Sign in at github.com → **New repository**
- Name: `virtual-crew` · Description and topics: copy from `docs/github-metadata.md`
- **Do not** tick "Add a README / .gitignore / licence" — this repo already has them
- Visibility: **Private** first. Flip it to Public **before submitting the link** (Settings → General
  → Danger zone → Change visibility).

## 2 · Push (one of two ways)

**A. With the `gh` CLI** (needs `brew install gh` and one `gh auth login`):

```
cd ~/Desktop/virtual-crew
gh repo create virtual-crew --private --source=. --remote=origin --push
```

**B · Without `gh`** — after creating the empty repo, copy its URL and:

```
cd ~/Desktop/virtual-crew
git remote add origin <the URL github shows you>
git branch -M main
git push -u origin main
```

## 3 · Set the repo page up

- About (right-hand side): paste the description from `docs/github-metadata.md`; add the topics list
- Social preview image (optional): a still of the pipeline works better than a logo
- Release (optional but nice): tag `v0.1.0`, notes are drafted in `docs/github-metadata.md`

## 4 · Sanity check as a stranger

Open the repo in a private browser window (not logged in) and read the first screen: title, one-line
pitch, the four screenshots, the crew table, `make verify`. If the images do not load, the paths in
`README.md` are wrong — they must be `docs/figures/...`.

## 5 · What deliberately is NOT here

- The real film's script, storyboard, generated clips and asset document — those stay in the project
  folder, never in the repository
- Application paperwork (work statement, any document written for an admissions file)
- Any API key, absolute path from the machine that built this, or personal contact detail
