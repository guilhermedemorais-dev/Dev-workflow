# Upstream Agent Skills

Use this reference when the coding environment supports Agent Skills.

## Official GSAP AI Skills

Repository:

- https://github.com/greensock/gsap-skills

The official repository provides skills for:

- `gsap-core`
- `gsap-timeline`
- `gsap-scrolltrigger`
- `gsap-plugins`
- `gsap-utils`
- `gsap-react`
- `gsap-performance`
- framework-specific guidance

The upstream project documents compatibility with Codex and other skill-capable coding agents.

Install with the skills CLI when the environment allows it:

```bash
npx skills add https://github.com/greensock/gsap-skills --all
```

For Codex, the upstream documentation also describes copying skills into the Codex skill directory.

### Delegation Rule

If these official skills are available, load the relevant official GSAP skill before writing/reviewing GSAP API details. `cinematic-web-standard` remains responsible for the wider scrollytelling architecture, media pipeline, renderer decisions, accessibility, and QA.

Do not copy stale GSAP examples into this skill when the official upstream skill can provide current API guidance.

## Optional Scrollytelling Skill Ecosystem

Community project:

- https://github.com/kenzofujimoto/agent-skills

Relevant skills listed by that project include:

- `motion-site-builder`
- `scroll-world-browser`

Treat these as optional inspiration/companion skills, not as a dependency or source of truth for this standard.

A separate community project also exists at:

- https://github.com/olbboy/motion-site-builder

Do not automatically install third-party agent skills into production workflows. Review their instructions and supply-chain implications first.

## Why This Skill Still Exists

The official GSAP skills teach GSAP correctly. This skill adds the Dev-workflow-specific engineering layer around them:

- renderer decision gates
- 2D cinematic media pipeline
- frame extraction/manifest/budget scripts
- scrollytelling scene contracts
- mobile/reduced-motion requirements
- MCP/browser QA guidance
- Dev-workflow handoff artifacts
