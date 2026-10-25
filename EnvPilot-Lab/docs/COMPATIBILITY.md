# Version choices and official compatibility evidence

Verified against official documentation and package metadata during construction, 2026-10-25.
Direct Python dependencies are exact-pinned in backend/requirements.txt; full Linux runtime lock in backend/requirements.lock.
Frontend dependencies are exact-pinned in package.json and npm transitive versions/integrity are pinned by package-lock.json.
Images use explicit release tags (not latest). OS package rebuilds can still change bytes; this is a local teaching repository, not a reproducible supply-chain build.

| Component | Choice / rationale |
|---|---|
| Python | 3.13.14; compatible with Django 5.2, Celery 5.6, Ansible 2.21 |
| Django | 5.2.18 LTS, extended support to April 2028 |
| DRF | 3.18.3, supports Django 5.2 and Python 3.13 |
| Celery / Redis client | 5.6.3 / 6.4.0; Kombu Redis extra requires redis-py <6.5 |
| PostgreSQL | 17.11, supported series; psycopg 3.3.6 |
| Redis server | 7.4.11; familiar broker, append-only persistence |
| Next / React | 16.4.3 / 19.3.1; TypeScript 5.9.3 |
| Node | 24.13.1 LTS, exceeds Next minimum 20.9 |
| Ansible core | 2.21.5; Python 3.12–3.14 control-node support |
| Nginx | 1.30.6 local reverse proxy |
| UI harness | Vitest 5.0.5, jsdom 26.1.0, Playwright 1.58.2 with matching browser image |

Sources: [Django supported releases](https://www.djangoproject.com/download/), [Django Python matrix](https://docs.djangoproject.com/en/5.2/faq/install/), [DRF requirements](https://www.django-rest-framework.org/), [Celery stable](https://docs.celeryq.dev/en/stable/getting-started/introduction.html), [Next installation](https://nextjs.org/docs/app/getting-started/installation), [Ansible maintenance matrix](https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html), [PostgreSQL support policy](https://www.postgresql.org/support/versioning/).

Role context only: [EasyEnv public senior engineer role](https://easyenv.io/careers/senior-software-engineer). Its published technology mix informed scope; no access to or claim about their assessment questions.
