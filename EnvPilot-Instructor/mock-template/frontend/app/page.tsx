'use client';
import {useState} from 'react';
import MemoEditor,{Memo} from '../components/MemoEditor';
export default function Home(){
  const [token,setToken]=useState('');const [rows,setRows]=useState<Memo[]>([]);const [error,setError]=useState('');
  const [username,setUsername]=useState('owner');const [password,setPassword]=useState('');
  async function login(e:React.FormEvent){e.preventDefault();setError('');try{
    const response=await fetch('/api/login/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username,password})});
    if(!response.ok)throw new Error('Login failed');const body=await response.json();setToken(body.token);
    const memos=await fetch('/api/memos/',{headers:{Authorization:`Token ${body.token}`}});if(!memos.ok)throw new Error(`Memo service returned ${memos.status}`);setRows(await memos.json());
  }catch(e){setError(String(e));}}
  return <main><h1>EnvPilot · Handover memos</h1><p>Independent assessment workspace</p>{!token?<form onSubmit={login}><label>Username<input value={username} onChange={e=>setUsername(e.target.value)}/></label><label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)}/></label><button>Sign in</button></form>:rows.map(row=><MemoEditor key={row.id} initial={row} token={token}/>)}{error&&<p role="alert">{error}</p>}</main>;
}
