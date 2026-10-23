# Install StoryEra

## 1. Download the skill

Clone the repository or download its source ZIP from GitHub:

```sh
git clone https://github.com/kmsmohamedansar/storyera.git
```

The installable folder is `storyera/skills/storyera/` inside the downloaded repository. Copy the **whole folder**, including its references and license. Cloning alone does not activate the skill. Before copying, check for an existing destination and preserve customizations; do not nest a second `storyera/` folder inside an installation.

## 2. Choose your host and scope

| Local setup | Codex | Claude Code |
| --- | --- | --- |
| One novel project | `your-novel/.agents/skills/storyera/` | `your-novel/.claude/skills/storyera/` |
| Across your projects | `~/.agents/skills/storyera/` | `~/.claude/skills/storyera/` |

For either host, the chosen destination should contain `SKILL.md`, `LICENSE`, `references/`, and `agents/` directly. Choose one scope per host to avoid duplicate installations.

### Codex

Clone the repository and copy the entire `skills/storyera/` folder into your novel project's `.agents/skills/`. The result should be `your-novel/.agents/skills/storyera/SKILL.md`.

Use the guarded command in the [README](../README.md#quick-start-in-codex). Check existing installations before copying; avoid nesting `storyera/storyera/` or overwriting customizations. To update, compare folders and preserve your changes before deliberately replacing the skill.

Codex scans `.agents/skills/` from the working directory to the repository root. For personal use across projects, the documented user location is `~/.agents/skills/storyera/`. Changes are normally detected automatically; restart if the skill does not appear. See [official OpenAI guidance](https://learn.chatgpt.com/docs/build-skills), checked October 23, 2026.

### Claude Code

Copy `skills/storyera/` into `.claude/skills/` inside the novel project, or into `~/.claude/skills/` for personal use across local projects. The resulting entrypoint is `.claude/skills/storyera/SKILL.md` or `~/.claude/skills/storyera/SKILL.md`.

Start Claude Code in the manuscript project and invoke:

```text
/storyera Audit chapters/01.md through chapters/08.md in order.
Cite continuity issues and suggest repairs. Do not modify the manuscript.
```

These local locations and the slash-command invocation follow [Claude Code's official skills documentation](https://code.claude.com/docs/en/skills), checked October 23, 2026. This is a standalone skill: no plugin manifest, marketplace registration or plugin installation is required. `agents/openai.yaml` is optional Codex display metadata; the core skill instructions and references are shared.

The saved behavioral tests in this repository used Codex. Claude Code setup is documented from its official guidance, but an actual Claude Code run has not been recorded. These local instructions do not describe installation into Claude.ai, Cowork or cloud-only sessions.

## 3. Verify discovery and run an audit

Open a new chat in the manuscript project. In Codex, invoke `$storyera`; in Claude Code, invoke `/storyera`. You can also ask the agent to locate and read the installed `SKILL.md`. If it cannot find it, provide its actual path and check the directory structure. Restart the host if needed. A successful copy alone does not prove the host loaded it.

Codex example:

```text
Use $storyera to audit chapters/01.md through chapters/08.md in order.
Cite continuity issues and suggest repairs. Do not modify the manuscript.
```

The skill requires no Python environment or API key. Your agent host must be able to read the chapters under its own permissions and data settings.

## What runs when you invoke it?

StoryEra is a playbook, not a separate AI model or a background agent. Your existing Codex or Claude Code model reads the skill instructions and your chapters, builds a cited fact ledger, checks later explanations, and returns classified findings with proposed repairs. You still need your normal access to the chosen host. Python utilities in this repository validate saved reports during development; they do not perform the literary audit.

## Other hosts

Install the **entire** skill folder with your Agent Skills host's documented mechanism. Core instructions require no host-specific tools or MCP server. `agents/openai.yaml` is optional Codex metadata; other hosts may ignore it. This project does not claim every host has been tested.

The folder follows the [Agent Skills specification](https://agentskills.io/specification). This is not a published marketplace plugin; cloning does not install it automatically.

## Remove

Remove only the installation you created after checking its path. Keep manuscript files and audit reports. The package installs no background service, database or host configuration.

## Upgrading from Canonkeeper

The skill is now named `storyera`. If you installed `canonkeeper`, preserve any local customizations, remove that old skill folder deliberately, and install the complete `skills/storyera/` folder. Invoke `$storyera` afterward. Avoid keeping both installations active unless you intentionally want both versions. The GitHub repository is now [kmsmohamedansar/storyera](https://github.com/kmsmohamedansar/storyera).
