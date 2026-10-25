'use client';
import { useEffect, useRef, useState } from 'react';
import Dashboard from '../components/Dashboard';
import { Membership } from '../lib/api';
import Link from 'next/link';
import LabOrientation from '../components/LabOrientation';

const roles=[['owner','Owner · Team Alpha'],['developer','Developer · Team Alpha'],['viewer','Viewer · Team Alpha'],['other_owner','Owner · Team Beta'],['dual','Developer · both teams'],['outsider','Outsider · no memberships']] as const;
const preferenceKey='envpilot.demo-selection.v1';
type Session={username:string;token:string;memberships:Membership[]};
function saveSelection(role:string,organization:number) {
  try {localStorage.setItem(preferenceKey,JSON.stringify({role,organization}));} catch { /* Storage may be disabled; switching still works. */ }
}

export default function Home() {
  const [role,setRole]=useState('owner');
  const [session,setSession]=useState<Session|null>(null);
  const [hydrated,setHydrated]=useState(false);
  const [org, setOrg] = useState(0);
  const [error, setError] = useState('');
  const [busy,setBusy]=useState(true);
  const [retry,setRetry]=useState(0);
  const preferredOrg=useRef(0);
  useEffect(()=>{
    try {
      const saved=JSON.parse(localStorage.getItem(preferenceKey)||'null');
      if (saved && roles.some(([value])=>value===saved.role)) {
        setRole(saved.role);
        preferredOrg.current=Number.isInteger(saved.organization)?saved.organization:0;
      }
    } catch { /* Ignore invalid or unavailable local preferences. */ }
    setHydrated(true);
  },[]);
  useEffect(()=>{
    if (!hydrated) return;
    const controller=new AbortController();
    setBusy(true);setError('');setSession(null);
    void (async()=>{
      try {
        const response=await fetch('/api/demo-session/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({role}),signal:controller.signal});
        if (!response.ok) throw new Error('Demo role unavailable. Check that the local lab is running and demo role switching is enabled.');
        const body:Session=await response.json();
        if (controller.signal.aborted) return;
        const organization=body.memberships.find(m=>m.organization===preferredOrg.current)?.organization||body.memberships[0]?.organization||0;
        setSession(body);setOrg(organization);saveSelection(role,organization);
      } catch(e) {if (!controller.signal.aborted) setError(String(e));}
      finally {if (!controller.signal.aborted) setBusy(false);}
    })();
    return ()=>controller.abort();
  },[role,hydrated,retry]);
  function switchRole(value:string) {
    setSession(null);setBusy(true);preferredOrg.current=0;setRole(value);saveSelection(value,0);
  }
  return <main><header><div><p className="eyebrow">ENGINEERING WORKBENCH / LOCAL LAB</p><h1>EnvPilot<span> Lab</span></h1></div><div className="header-guide"><p>Investigate. Repair. Verify.</p><Link href="/guide">Lab guide & exercises ↗</Link></div></header>
    <div className="product-layout"><LabOrientation/>
      <nav className="demo-role-controls" aria-label="Demo workspace controls">
        <label>Role<select aria-label="Role" value={role} onChange={e=>switchRole(e.target.value)}>{roles.map(([value,label])=><option key={value} value={value}>{label}</option>)}</select></label>
        {session && session.memberships.length>0 && <label>Organization<select aria-label="Organization" value={org} onChange={e=>{const value=Number(e.target.value);setOrg(value);preferredOrg.current=value;saveSelection(role,value);}}>{session.memberships.map(m=><option key={m.organization} value={m.organization}>{m.name} · {m.role}</option>)}</select></label>}
        <p className="role-note">Local demo · switch roles without signing in. Your selection is remembered on this browser.</p>
      </nav>
      {busy && <p role="status">Opening demo workspace…</p>}
      {error && <div><p role="alert">{error}</p><button onClick={()=>setRetry(value=>value+1)}>Retry</button></div>}
      {session && !busy && <>
        {org>0 && <p className="workspace-caption">Demo product workspace · {session.memberships.find(m=>m.organization===org)?.name}. Inspect the cards below while working through your current exercise.</p>}
        {org ? <Dashboard key={session.username} token={session.token} organization={org} role={session.memberships.find(m=>m.organization===org)?.role||'viewer'}/> : <p>This demo account has no organization memberships. Select another role to explore a workspace.</p>}
      </>}
    </div>
    <footer>Fictional data · Local Docker stack · <Link href="/guide">Open the lab guide</Link></footer>
  </main>;
}
