# Command/reference sheet

Use these general investigation commands to collect evidence. They do not identify the locations of intentional defects.

```bash
docker compose ps
docker compose logs --tail=100 api worker proxy provider
docker compose exec api python manage.py showmigrations
docker compose exec api python manage.py profile_queries --organization 1
docker compose exec db psql -U envpilot -d envpilot
docker compose exec redis redis-cli LLEN provision
docker compose exec worker celery -A config inspect active_queues
docker compose exec worker celery -A config inspect active
docker compose exec proxy nginx -T
docker compose exec proxy sh -c 'ps; netstat -lnt'
docker compose exec api python -c "import socket; print(socket.getaddrinfo('provider',9000))"
docker compose restart api worker
curl -i http://localhost:8090/health/
```

Direct `docker compose` commands use the base configuration. When an incident is active, include its overlay when inspecting configuration or recreating a service:
`docker compose -f compose.yaml -f infra/incidents/proxy.yaml config`.
The `lab.py` CLI automatically includes active overlays for its service-changing commands.

```bash
curl -s http://localhost:8090/api/login/ -H 'Content-Type: application/json' -d '{"username":"owner","password":"LabPass123!"}'
curl -i http://localhost:8090/api/me/ -H 'Authorization: Token REPLACE_ME'
docker compose exec db psql -U envpilot -d envpilot -c 'SELECT status,count(*) FROM lab_operation GROUP BY status;'
docker compose run --rm web npm run typecheck
```

In PowerShell, use `curl.exe` if `curl` is an alias, or run the examples from WSL2.
In psql: `\dt`, `\d lab_environment`, `EXPLAIN (ANALYZE, BUFFERS) SELECT ...;`.
Interpret sequential scans, index scans, and row estimates in context. A sequential scan can be the appropriate plan.

## Linux/systemd reference (read-only examples)

These containers do not run systemd. Host operating system changes are not required.
On a VM with systemd, useful commands include `systemctl status envpilot-worker`, `journalctl -u envpilot-worker --since '-15 min'`, `ss -lntp`, `ps aux`, and `getent hosts api`.
In this lab, use Docker logs and exec. Practice reading journal output with the samples in `infra/sample-journal.log`.

## Official documentation

- [Django queryset optimization](https://docs.djangoproject.com/en/5.2/topics/db/optimization/)
- [DRF permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [React useEffect](https://react.dev/reference/react/useEffect)
- [Ansible template module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/template_module.html)
- [Docker Compose](https://docs.docker.com/compose/)
