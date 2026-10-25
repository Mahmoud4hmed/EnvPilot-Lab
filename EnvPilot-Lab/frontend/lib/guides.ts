export const guides = [
  {slug: 'start', title: 'Start here', file: 'START_HERE.md', group: 'Getting started'},
  {slug: 'day-1', title: 'Day 1 · backend and operations', file: 'DAY_1.md', group: 'Getting started'},
  {slug: 'day-2', title: 'Day 2 · frontend, automation and mock', file: 'DAY_2.md', group: 'Getting started'},
  {slug: 'exercise-1', title: '1 · API correctness and tenant isolation', file: 'issues/01-api.md', group: 'Exercises'},
  {slug: 'exercise-2', title: '2 · PostgreSQL and ORM performance', file: 'issues/02-database.md', group: 'Exercises'},
  {slug: 'exercise-3', title: '3 · Reliable asynchronous provisioning', file: 'issues/03-provisioning.md', group: 'Exercises'},
  {slug: 'exercise-4', title: '4 · Linux and Docker incidents', file: 'issues/04-incidents.md', group: 'Exercises'},
  {slug: 'exercise-5', title: '5 · React and TypeScript behavior', file: 'issues/05-frontend.md', group: 'Exercises'},
  {slug: 'exercise-6', title: '6 · Ansible automation', file: 'issues/06-ansible.md', group: 'Exercises'},
  {slug: 'exercise-7', title: '7 · Applied AI and RAG', file: 'issues/07-assistant.md', group: 'Exercises'},
  {slug: 'api', title: 'API contract', file: 'docs/API_CONTRACT.md', group: 'Reference'},
  {slug: 'architecture', title: 'Architecture and repository map', file: 'docs/ARCHITECTURE.md', group: 'Reference'},
  {slug: 'commands', title: 'Command cheat sheet', file: 'docs/CHEATSHEET.md', group: 'Reference'},
  {slug: 'notes', title: 'Engineering notes template', file: 'notes/TEMPLATE.md', group: 'Reference'},
  {slug: 'rubric', title: 'Training rubric', file: 'RUBRIC.md', group: 'Reference'},
  {slug: 'verification', title: 'Setup verification', file: 'VERIFICATION.md', group: 'Reference'},
] as const;

export function guideHref(file: string, href: string): string | undefined {
  if (/^(https?:|mailto:|#)/.test(href)) return href;
  const [target, fragment] = href.split('#', 2);
  const segments = [...file.split('/').slice(0, -1), ...target.split('/')];
  const resolved: string[] = [];
  for (const segment of segments) {
    if (segment === '..') resolved.pop();
    else if (segment && segment !== '.') resolved.push(segment);
  }
  const guide = guides.find(item => item.file === resolved.join('/'));
  return guide ? `/guide/${guide.slug}${fragment ? '#' + fragment : ''}` : undefined;
}
