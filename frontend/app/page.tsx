'use client';
import { useState } from 'react';
import Dashboard from '../components/Dashboard';
import { api, Membership } from '../lib/api';

export default function Home() {
  const [username, setUsername] = useState('mahmoud');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [memberships, setMemberships] = useState<Membership[]>([]);
  const [org, setOrg] = useState(0);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  async function login(e: React.FormEvent) {
    e.preventDefault(); setBusy(true); setError('');
    try {
      const response = await fetch('/api/login/', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({username, password})});
      if (!response.ok) throw new Error('Login failed. Check your demo credentials.');
      const body: {token: string} = await response.json();
      const me = await api<{memberships: Membership[]}>('/api/me/', body.token);
      setToken(body.token); setMemberships(me.memberships); setOrg(me.memberships[0]?.organization || 0);
    } catch (e) {setError(String(e));} finally {setBusy(false);}
  }
  return <main><header><div><p className="eyebrow">ENGINEERING WORKBENCH / LOCAL LAB</p><h1>EnvPilot<span> Lab</span></h1></div><p>Temporary environments.<br/>Real engineering decisions.</p></header>
    {!token ? <form onSubmit={login}><h2>Welcome back</h2><p>Sign in with a fictional lab account.</p><label>Username<input value={username} onChange={e => setUsername(e.target.value)} autoComplete="username" /></label><label>Password<input type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="current-password" /></label><button disabled={busy}>{busy ? 'Signing in…' : 'Sign in'}</button>{error && <p role="alert">{error}</p>}</form> : <>
      <nav><label>Organization <select aria-label="Organization" value={org} onChange={e => setOrg(Number(e.target.value))}>{memberships.map(m => <option key={m.organization} value={m.organization}>{m.name} · {m.role}</option>)}</select></label><button onClick={() => {setToken(''); setPassword('');}}>Sign out</button></nav>
      {org ? <Dashboard token={token} organization={org} role={memberships.find(m => m.organization === org)?.role || 'viewer'} /> : <p>No organization memberships.</p>}
    </>}
    <footer>Fictional data · Local Docker stack · Read START_HERE.md to begin</footer>
  </main>;
}
