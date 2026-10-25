import { test, expect } from '@playwright/test';
test('choose a demo role, request provisioning, observe actual worker result', async ({page}) => {
  await page.goto('/');
  await page.getByLabel('Role',{exact:true}).selectOption('owner');
  await expect(page.getByRole('heading', {name: 'Environments', exact: true})).toBeVisible();
  await page.getByLabel('Status', {exact: true}).selectOption('pending');
  const button = page.getByRole('button', {name: /^Provision /}).first();
  const name = (await button.innerText()).replace('Provision ', '');
  await button.click();
  // Inspect server state independently, so optimistic UI alone cannot satisfy the happy path.
  await expect.poll(async () => page.evaluate(async (envName) => {
    const login = await fetch('/api/login/', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:'owner',password:'LabPass123!'})}).then(r=>r.json());
    const me = await fetch('/api/me/',{headers:{Authorization:`Token ${login.token}`}}).then(r=>r.json());
    const data = await fetch(`/api/environments/?organization=${me.memberships[0].organization}&page_size=100`,{headers:{Authorization:`Token ${login.token}`}}).then(r=>r.json());
    return data.results.find((e: {name:string})=>e.name===envName)?.status;
  }, name), {timeout:20000}).toBe('ready');
  await page.getByLabel('Status', {exact: true}).selectOption('ready');
  await expect(page.getByRole('heading', {name,exact:true})).toBeVisible();
});

test('selected role survives guide navigation and page reload',async({page})=>{
  await page.goto('/');
  await page.getByLabel('Role',{exact:true}).selectOption('viewer');
  await expect(page.getByLabel('Organization',{exact:true})).toContainText('Team Alpha · viewer');
  await page.getByRole('link',{name:'Start Day 1 →',exact:true}).click();
  await expect(page.getByRole('heading',{level:1})).toContainText('DAY 1');
  await page.getByRole('link',{name:'Dashboard',exact:true}).click();
  await expect(page.getByLabel('Role',{exact:true})).toHaveValue('viewer');
  await page.reload();
  await expect(page.getByLabel('Organization',{exact:true})).toContainText('Team Alpha · viewer');
  await expect(page.getByLabel('Password')).toHaveCount(0);
  await expect(page.getByRole('button',{name:/^Provision /})).toHaveCount(0);
});
