import React, {useState} from 'react'
import Login from './components/Login'
import Signup from './components/Signup'
import Dashboard from './components/Dashboard'

export default function App(){
  const [token, setToken] = useState(null)
  const [view, setView] = useState('login')
  if(!token){
    return <div className="container"><div className="card">{view==='login'?<Login onLogin={t=>setToken(t)} switch={()=>setView('signup')}/>:<Signup onSignup={t=>setToken(t)} switch={()=>setView('login')}/>}</div></div>
  }
  return <div className="container"><Dashboard token={token} /></div>
}
