import React, {useState, useEffect} from 'react'
import Journal from './Journal'
import PrivateAgent from './PrivateAgent'
import {listJournals} from '../api'

export default function Dashboard({token}){
  const [journals, setJournals] = useState([])
  useEffect(()=>{ fetchJournals() },[])
  async function fetchJournals(){ const res = await listJournals(token); setJournals(res || []) }
  return <div>
    <h1>Dashboard</h1>
    <div style={{display:'flex', gap:16}}>
      <div style={{flex:1}} className="card">
        <Journal token={token} onSaved={fetchJournals} />
      </div>
      <div style={{flex:1}} className="card">
        <PrivateAgent token={token} />
      </div>
    </div>
    <div style={{marginTop:16}} className="card">
      <h3>Your journal entries (ciphertext blobs)</h3>
      <ul>
        {journals.map(j=> <li key={j.id}><strong>{j.created_at}</strong> — {j.ciphertext.slice(0,60)}...</li>)}
      </ul>
    </div>
  </div>
}
