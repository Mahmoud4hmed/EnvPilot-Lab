import { test, expect } from '@playwright/test';
test('sign in, request provisioning, observe actual worker result', async ({page}) => {
  await page.goto('/');
  await page.getByLabel('Password').fill('LabPass123!');
  await page.getByRole('button', {name: 'Sign in', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Environments', exact: true})).toBeVisible();
  await page.getByLabel('Status', {exact: true}).selectOption('pending');
  const button = page.getByRole('button', {name: /^Provision /}).first();
  const name = (await button.innerText()).replace('Provision ', '');
  await button.click();
  // Inspect server state independently, so optimistic UI alone cannot satisfy the happy path.
  await expect.poll(async () => page.evaluate(async (envName) => {
    const login = await fetch('/api/login/', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:'mahmoud',password:'LabPass123!'})}).then(r=>r.json());
    const me = await fetch('/api/me/',{headers:{Authorization:`Token ${login.token}`}}).then(r=>r.json());
    const data = await fetch(`/api/environments/?organization=${me.memberships[0].organization}&page_size=100`,{headers:{Authorization:`Token ${login.token}`}}).then(r=>r.json());
    return data.results.find((e: {name:string})=>e.name===envName)?.status;
  }, name), {timeout:20000}).toBe('ready');
  await page.getByLabel('Status', {exact: true}).selectOption('ready');
  await expect(page.getByRole('heading', {name,exact:true})).toBeVisible();
});
