# Testing: one check, three layers

The test structure every repository made with this pack has: one command that proves a commit, tests in three layers with a place and a name each, and continuous integration that runs the same command. Read when a repository is set up, when its first test is written, and when a new kind of test is added.

## The check

- One command runs everything a commit must pass, in the order that fails fastest: the format check, the lint, the type check, the unit tests, and the build where the stack builds. It is named `check` in the stack's task runner (`npm run check`, `pnpm check`, `make check`, `just check`, `uv run poe check`), listed first and in bold in the agreement's command table, and run before every commit.
- It is green from the first commit. Where code exists, the first commit carries one real test of it, of a pure function or of the entry point starting and answering, so that the check proves something from day one. An empty folder has no code to test, and no code is written to have something to test: its check runs the format check, the lint and the type check over the skeleton, and the test runner with its own option for an empty suite (`vitest run --passWithNoTests`; pytest's exit status 5, no tests collected, taken as a pass by the script), and the agreement's Testing section says that the first feature starts with its test. A repository that holds no code yet runs the content check of "By stack".
- A check that needs something the machine may lack (a database, a browser) says what to start and fails when it is missing; it never skips silently. Where the machine's runtime is not the one the repository pins, the check is run on what is there and the report names both versions. A layer that cannot run in the check (end-to-end, below) has its own command and its own job in continuous integration.
- The check never calls a live third-party service and never needs a secret. What a test needs from outside is a recorded or invented fixture.

## The layers

| Layer | What it proves | Where it lives | Runs |
|---|---|---|---|
| Unit | A function or a module, alone: no network, no database, no clock it does not inject; fast | Next to the code it tests, named after it (`price.ts` and `price.test.ts`; `price.py` and `test_price.py` under `tests/` where the stack expects it there) | In the check, on every commit |
| Integration | A module against the real dependency it talks to: the database engine the product uses, a local emulator of the platform, a queue, a file store | Next to the code as `*.int.test.ts`, or `tests/integration/` where the stack keeps tests apart | In the check when the dependency starts locally with one command (a compose file, the platform's local mode), else as `test:int` with its own job |
| End-to-end | A person's path through the running product: a page opened, a form sent, a result seen, in a real browser or a real client | `e2e/` at the root, one file per journey | `test:e2e`, before a release and as its own job in continuous integration; few, for the paths that earn money or lose data |

The rules the agreement's Testing section carries: what is outside the product's control is mocked, and the database never, nor swapped for another engine; a bug fix starts with a test that fails for the bug; every parser of outside input has hostile cases; time, randomness and identifiers are injected; fixtures are invented, with no real customer, person, account or address.

## By stack

The repository's framework decides first: when a scaffold or the framework's own guide names a test runner and a linter, those are taken. Otherwise, the default per stack, each at the version its registry lists as current on the day of setup (`npm view <package> version`, `pip index versions <package>`, `go list -m -versions`), never a remembered number:

| Stack | Unit and integration | Lint and format | Types | End-to-end |
|---|---|---|---|---|
| TypeScript on Node.js | Vitest | Biome, or ESLint and Prettier where the framework scaffolds them; Biome formats Markdown and JSON too, so the documents the setup writes are formatted with it once before the first check | `tsc --noEmit` | Playwright |
| Python | pytest | Ruff (`ruff check`, `ruff format --check`) | Pyright or mypy | Playwright for Python |
| Go | `go test ./...` | `gofmt -l` (empty output), `go vet ./...` | The compiler | A test binary against the running service |
| Rust | `cargo test` | `cargo fmt --check`, `cargo clippy -- -D warnings` | The compiler | A test binary against the running service |
| Content only (documents, data, skills), or no code yet | A script that validates what the repository holds: every local link of the Markdown resolves, front-matter parses, data files match their schema; written in the language of the machine's runtime with no dependency (`node scripts/check.mjs`). A pack in the SkillCDN Format (a `SKILLCDN.md` at its root) also runs the indexer's own reading, `npx @skillcdn/cli@latest check`, always with `@latest`: a bare `npx` runs the copy its cache holds, which may read by older rules (SkillCDN 0.6, checked 2026-11) | The script | None | None |

A stack the table lacks gets the same shape: one `check`, unit tests next to the code, and the agreement's command table saying which command does what.

## Versions

Every version the setup writes is found on the day, never remembered:

- **The runtime.** Node.js: the newest release whose `lts` is not `false` in `https://nodejs.org/dist/index.json`, its major in `.node-version` and `engines`, unless a tool the repository uses needs a later minor (`npm view <package> engines`). Python: the newest stable minor its tools support, from `https://www.python.org/downloads/` or `uv python list`, in `.python-version`. Go: the newest stable from `https://go.dev/dl/?mode=json`, in `go.mod`. Rust: `stable` in `rust-toolchain.toml`.
- **Packages.** The registry's current version (`npm view <package> version`, `pip index versions <package>`, `go list -m -versions <module>`), written as the package manager writes it and locked by its lockfile.
- **Continuous integration's actions.** Each action's newest release, `gh api repos/<owner>/<action>/releases/latest --jq .tag_name`, referenced by its major tag (`actions/checkout@v<major>`), as the action's own README shows.

## Continuous integration

- `.github/workflows/check.yml` (or the git host's equivalent) runs the check on every push and every pull request, on the runtime version the repository pins, with the package manager's frozen install.
- A layer outside the check is a job of its own in the same workflow, so that a red end-to-end run is seen without blocking the unit tests' signal.
- A red run on the main branch is the first thing to fix, before new work.
- Continuous integration holds no secret the check needs; a job that deploys is the deploy skill's, and is added by it.

## What the agreement says about tests

The agreement's Testing section (agreement.md) carries the repository's own version of this page in four to six lines: the runner, where each layer lives, the commands, what is never mocked, and the rule that a bug fix starts with a failing test. It links nothing outside the repository, so that it holds wherever the repository is cloned.
