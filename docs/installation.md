# Install StoryEra

## One manuscript project

Clone the repository and copy the entire `skills/storyera/` folder into your novel project's `.agents/skills/`. The result should be `your-novel/.agents/skills/storyera/SKILL.md`.

Use the guarded command in the [README](../README.md#quick-start). Check existing installations before copying; avoid nesting `storyera/storyera/` or overwriting customizations. To update, compare folders and preserve your changes before deliberately replacing the skill.

Codex scans `.agents/skills/` from the working directory to the repository root. For personal use across projects, the documented user location is `~/.agents/skills/storyera/`. Changes are normally detected automatically; restart if the skill does not appear. See [official OpenAI guidance](https://learn.chatgpt.com/docs/build-skills), checked October 23, 2026.

## Verify discovery

Open a new chat in the manuscript project and invoke `$storyera`, or ask the agent to locate and read the installed `SKILL.md`. If it cannot find it, provide its actual path and check the directory structure. A successful copy alone does not prove the host loaded it.

The skill requires no Python environment or API key. Your agent host must be able to read the chapters under its own permissions and data settings.

## Other hosts

Install the **entire** skill folder with your Agent Skills host's documented mechanism. Core instructions require no host-specific tools or MCP server. `agents/openai.yaml` is optional Codex metadata; other hosts may ignore it. This project does not claim every host has been tested.

The folder follows the [Agent Skills specification](https://agentskills.io/specification). This is not a published marketplace plugin; cloning does not install it automatically.

## Remove

Remove only the installation you created after checking its path. Keep manuscript files and audit reports. The package installs no background service, database or host configuration.

## Upgrading from Canonkeeper

The skill is now named `storyera`. If you installed `canonkeeper`, preserve any local customizations, remove that old skill folder deliberately, and install the complete `skills/storyera/` folder. Invoke `$storyera` afterward. Avoid keeping both installations active unless you intentionally want both versions. The GitHub repository is now [kmsmohamedansar/storyera](https://github.com/kmsmohamedansar/storyera).
