import React, {useState} from 'react'
import {login} from '../api'

export default function Login({onLogin, switch: switchToSignup}){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  async function doLogin(){
    const res = await login(email, password)
    if(res.access_token) onLogin(res.access_token)
    else alert('Login failed')
  }
  return <div>
    <h2>Login</h2>
    <input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
    <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
    <div style={{marginTop:8}}>
      <button onClick={doLogin}>Login</button>
      <button style={{marginLeft:8}} onClick={switchToSignup}>Sign up</button>
    </div>
  </div>
}
