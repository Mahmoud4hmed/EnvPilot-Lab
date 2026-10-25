'use client';
import {useState} from 'react';
export type Memo={id:number;title:string;archived_at:string|null};
export default function MemoEditor({initial,token}:{initial:Memo;token:string}){
  const [memo,setMemo]=useState(initial);const [draft,setDraft]=useState(initial.title);const [error,setError]=useState('');
  async function save(){
    const title=draft;setDraft('');setMemo({...memo,title});setError('');
    try{const response=await fetch(`/api/memos/${memo.id}/`,{method:'PATCH',headers:{'Content-Type':'application/json',Authorization:`Token ${token}`},body:JSON.stringify({title})});if(!response.ok)throw new Error('Save failed');setMemo(await response.json());}
    catch(e){setError(String(e));}
  }
  return <article><h2>{memo.title}</h2><label>Title<input aria-label="Title" value={draft} onChange={e=>setDraft(e.target.value)}/></label><button onClick={()=>void save()}>Save</button>{error&&<p role="alert">{error}</p>}</article>;
}
