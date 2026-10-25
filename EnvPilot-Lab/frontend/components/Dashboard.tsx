'use client';
import { useEffect, useState } from 'react';
import { api, Environment, Page, Operation } from '../lib/api';

export default function Dashboard({token, organization, role}: {token: string; organization: number; role: string}) {
  const [rows, setRows] = useState<Environment[]>([]);
  const [error, setError] = useState('');
  const [status, setStatus] = useState('');
  const [notice, setNotice] = useState('');
  async function load() {
    try {
      const page = await api<Page>(`/api/environments/?organization=${organization}&status=${status}`, token);
      setRows(page.results);
    } catch (e) { setError(String(e)); }
  }
  useEffect(() => { void load(); }, [organization, status]);
  async function provision(row: Environment) {
    try {
      await api<Operation>(`/api/environments/${row.id}/provision/`, token, {method: 'POST', headers: {'Idempotency-Key': crypto.randomUUID()}, body: JSON.stringify({scenario: 'success'})});
      setRows(old => old.map(env => env.id === row.id ? {...env, status: 'ready'} : env));
      setNotice('Environment ready');
    } catch (e) { setError(String(e)); }
  }
  return <section aria-label="Environment dashboard">
    <div className="toolbar"><h2>Environments</h2><label>Status <select aria-label="Status" value={status} onChange={e => setStatus(e.target.value)}>
      <option value="">All</option>{['pending', 'provisioning', 'ready', 'failed'].map(s => <option key={s}>{s}</option>)}
    </select></label><button onClick={() => void load()}>Refresh</button></div>
    {error && <p role="alert">{error}</p>}{notice && <p role="status">{notice}</p>}
    <div className="grid">{rows.map(row => <article key={row.id}>
      <span className={'badge ' + row.status}>{row.status}</span><h3>{row.name}</h3>
      <p>{row.project_name}</p><p>{row.latest_event}</p>
      <small>Resource: {row.provider_id || 'awaiting provider'}</small>
      {row.status === 'pending' && role !== 'viewer' && <button onClick={() => void provision(row)}>Provision {row.name}</button>}
    </article>)}</div>
  </section>;
}
