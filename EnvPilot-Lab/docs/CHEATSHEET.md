# Command/reference sheet

الأوامر دي أدوات تحقيق عامة، مش مواقع العيوب.

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

عند وجود incident، direct `docker compose` للتشخيص بس بيستخدم base config. أضف الـactive overlay يدويًا لأي config inspection/recreation:
`docker compose -f compose.yaml -f infra/incidents/proxy.yaml config`.
الـCLI `lab.py` بيضيف الـoverlays النشطة تلقائيًا للـmutations.

```bash
curl -s http://localhost:8090/api/login/ -H 'Content-Type: application/json' -d '{"username":"mahmoud","password":"LabPass123!"}'
curl -i http://localhost:8090/api/me/ -H 'Authorization: Token REPLACE_ME'
docker compose exec db psql -U envpilot -d envpilot -c 'SELECT status,count(*) FROM lab_operation GROUP BY status;'
docker compose run --rm web npm run typecheck
```

في PowerShell استخدم `curl.exe` لو curl alias، أو نفّذ الأمثلة من WSL2.
في psql: `\dt`, `\d lab_environment`, `EXPLAIN (ANALYZE, BUFFERS) SELECT ...;`.
افهم sequential scan/index scan والـrow estimates؛ مش كل sequential scan مشكلة.

## Linux/systemd reference (read-only examples)

الـcontainers هنا مش مشغّلة systemd، ومش مطلوب تغيّر host OS.
على VM فيها systemd ممكن تستخدم `systemctl status envpilot-worker`, `journalctl -u envpilot-worker --since '-15 min'`, `ss -lntp`, `ps aux`, `getent hosts api`.
في المعمل استخدم Docker logs/exec؛ samples في `infra/sample-journal.log` للتدريب على قراءة journal.

## Official documentation

- [Django queryset optimization](https://docs.djangoproject.com/en/5.2/topics/db/optimization/)
- [DRF permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [React useEffect](https://react.dev/reference/react/useEffect)
- [Ansible template module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/template_module.html)
- [Docker Compose](https://docs.docker.com/compose/)
