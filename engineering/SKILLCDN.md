---
name: Engineering
description: Skills for software development and for the tooling an agent works with, such as writing and changing code, keeping a codebase's documents true to it, building apps, testing, debugging, and making skills from work done. Use when the task is to build or change software, or to turn a job into a skill.
license: MIT
translations:
  ko:
    name: 개발
    description: 코드 작성과 수정, 코드베이스 문서를 사실에 맞게 유지하기, 앱 개발, 테스트, 디버깅, 그리고 한 일을 스킬로 만들기처럼 소프트웨어 개발과 에이전트가 쓰는 도구를 위한 스킬입니다. 소프트웨어를 만들거나 고칠 때, 또는 일을 스킬로 만들 때 쓰세요.
metadata:
  author: skillcdn
---
# Rules for engineering skills

These add to the rules of the repository.

**Show a change before it lands.** A change to the user's code, configuration or data is shown as a diff or a plan and applied after they agree, unless they said to go ahead alone.

**Nothing leaves the machine in passing.** Pushing, publishing, deploying and deleting are explicit steps the user confirms one by one; a skill never does them on the way to something else.

**Prove what is claimed.** A skill that says a change works shows the check it ran (tests, build, lint) and the result. A check that did not run is reported as not run.
