# Exercise 6 — Complete isolated fixture automation

Estimated time: 45 minutes (target timebox).

## Context and symptoms

Operations needs a repeatable fixture recipe inside the tools container. The playbook currently prepares only part of the required layout.

## Acceptance criteria

- Under /fixture/envpilot, create config/ and logs/ directories with mode 0750; base directory mode 0755.
- Render config/agent.conf from the supplied template, mode 0640, with service_name=envpilot-agent and agent_port default 9100.
- Exact config lines: managed comment, service=<name>, port=<port>, ending newline.
- A second unchanged run reports changed=0; overriding agent_port=9200 updates only intended config behavior.
- No host directories, SSH credentials, privileged access, or real cloud provisioning.

## Relevant checks

```bash
python lab.py check 6
docker compose run --rm ansible ansible-playbook -i localhost, -c local playbook.yml -e agent_port=9200
```

The isolated named volume persists between runs. Inspect files with docker compose run --rm ansible python -c commands, not your host /fixture path.

Deliver: working changes, regression evidence, and a short English engineering note using notes/TEMPLATE.md.
