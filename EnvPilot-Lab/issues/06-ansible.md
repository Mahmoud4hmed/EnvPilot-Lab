# Exercise 6 — Complete isolated fixture automation

**Target time:** 45 minutes. **Your role:** engineer turning a partial operational recipe into repeatable configuration.

## The problem

Operations needs a predictable directory layout and agent configuration. The supplied playbook prepares only part of it. A successful command exit alone does not prove the required files, contents, and permissions exist.

The work runs locally inside the Ansible tools container and a named fixture volume. You are not configuring Windows, your WSL home, a remote host, or a cloud account.

## Before you start

Read [the shared workflow](../docs/EXERCISE_WORKFLOW.md). Inspect `ansible/playbook.yml`, `ansible/templates/agent.conf.j2`, and `ansible/verify.py`. The supplied template defines the exact output format; your task is the repeatable automation around it, not an arbitrary replacement file format.

Start by running:

```bash
python3 lab.py check 6
```

This builds the tools image and runs fixture verification. Record the first missing/incorrect artifact as baseline evidence; do not create the required paths manually on the host.

## Required layout and contents

| Path inside the fixture container | Type | Required mode |
|---|---|---|
| `/fixture/envpilot` | Directory | `0755` |
| `/fixture/envpilot/config` | Directory | `0750` |
| `/fixture/envpilot/logs` | Directory | `0750` |
| `/fixture/envpilot/config/agent.conf` | Rendered template file | `0640` |

The default variables are `service_name=envpilot-agent` and `agent_port=9100`. The default file must contain exactly these three lines, including a final newline:

```text
# Managed by Ansible
service=envpilot-agent
port=9100
```

Directory/file modes are part of the acceptance criteria, not an optional formatting preference. The configuration must derive from the supplied template and variables.

## Repeatability scenarios

After your repair, collect evidence for each run:

| Run | Required result |
|---|---|
| Apply default inputs. | Required directories/file exist with the exact contents and modes. |
| Apply the same inputs again. | Ansible recap reports `changed=0`; already-correct state is preserved. |
| Override `agent_port=9200`. | The rendered port becomes 9200, service name/layout/modes remain correct, and only the intended configuration behavior changes. |

You can invoke the playbook manually after the tools image has been built:

```bash
docker compose run --rm ansible ansible-playbook -i localhost, -c local playbook.yml
docker compose run --rm ansible ansible-playbook -i localhost, -c local playbook.yml
docker compose run --rm ansible ansible-playbook -i localhost, -c local playbook.yml -e agent_port=9200
```

Run these one at a time and save each recap. The named volume persists across containers; `--rm` removes a container, not the fixture data.

Inspect the result inside the tools container, for example:

```bash
docker compose run --rm ansible python -c "from pathlib import Path; p=Path('/fixture/envpilot/config/agent.conf'); print(p.read_text()); print(oct(p.stat().st_mode & 0o777))"
```

If the file is still missing, that inspection will fail too; it is evidence of the incomplete fixture, not a reason to inspect your host's `/fixture` path.

## Acceptance criteria

- [ ] All four paths have the required type/mode.
- [ ] The file is rendered from the supplied template with default values and exact contents/newline.
- [ ] An unchanged second run reports `changed=0`.
- [ ] The 9200 override updates the intended value without unrelated configuration changes.
- [ ] Tasks are maintainable/repeatable and operate only in the fixture; no SSH credentials, privileged access, host-service changes, or real provisioning.

## Verification and deliverables

```bash
python3 lab.py check 6
```

The verifier exercises default contents/modes, the no-change second run, the changed input, and restoration of the default port. Submit playbook/template changes as needed, inspection output, recaps for the scenarios, the final check result, and an English [engineering note](../notes/TEMPLATE.md) explaining repeatability.
