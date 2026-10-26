---
name: Engineering
description: Skills for software development, for the tooling an agent works with, and for packs of documents. Use when the task is to build or change software (writing and changing code, building apps and taking them live, keeping a codebase's documents true to it, testing, debugging), to turn a job into a skill, to make a pack of documents an agent searches through SkillCDN, or to answer a question from one.
license: MIT
translations:
  ko:
    name: 개발
    description: 소프트웨어 개발, 에이전트가 쓰는 도구, 그리고 문서 팩을 위한 스킬입니다. 소프트웨어를 만들거나 고칠 때(코드 작성과 수정, 앱 개발과 출시, 코드베이스 문서를 사실에 맞게 유지하기, 테스트, 디버깅), 일을 스킬로 만들 때, 에이전트가 SkillCDN으로 검색하는 문서 팩을 만들 때, 또는 팩에서 질문에 답할 때 쓰세요.
metadata:
  author: skillcdn
---
# Rules for engineering skills

These add to the rules of the repository.

**Show a change before it lands.** A change to the user's code, configuration or data is shown as a diff or a plan and applied after they agree, unless they said to go ahead alone.

**A commit follows the repository's agreement.** A commit or a push lands as the agreement of the repository it lands in says (its `AGENTS.md` or `CLAUDE.md`), and on the user's word where it has none.

**Prove what is claimed.** A skill that says a change works shows the check it ran (tests, build, lint) and the result. A check that did not run is reported as not run.
