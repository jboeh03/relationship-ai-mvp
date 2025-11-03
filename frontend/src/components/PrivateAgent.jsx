import React, {useState} from 'react'
import {deriveKey, decryptText} from '../crypto'
import {queryPrivateAgent, listJournals} from '../api'

export default function PrivateAgent({token}){
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState(null)
  const [pass, setPass] = useState('')
  async function ask(){
    // This simple prototype does not send plaintext journals to the server.
    // It sends the question and the server returns a placeholder response.
    const res = await queryPrivateAgent(token, question)
    setAnswer(res.response)
  }
  return <div>
    <h3>Private Agent</h3>
    <p>Ask a private reflection question — agent uses your private journals (when implemented).</p>
    <input placeholder="Your question..." value={question} onChange={e=>setQuestion(e.target.value)} />
    <div style={{marginTop:8}}>
      <button onClick={ask}>Ask</button>
    </div>
    {answer && <div style={{marginTop:12}} className="card"><strong>Agent:</strong><p>{answer}</p></div>}
  </div>
}
