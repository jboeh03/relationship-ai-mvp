import React, {useState} from 'react'
import {signup} from '../api'

export default function Signup({onSignup, switch: switchToLogin}){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  async function doSignup(){
    const res = await signup(email, password)
    if(res.access_token) onSignup(res.access_token)
    else alert('Signup failed: '+(res.detail||JSON.stringify(res)))
  }
  return <div>
    <h2>Sign up</h2>
    <input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
    <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
    <div style={{marginTop:8}}>
      <button onClick={doSignup}>Create account</button>
      <button style={{marginLeft:8}} onClick={switchToLogin}>Back to login</button>
    </div>
  </div>
}
