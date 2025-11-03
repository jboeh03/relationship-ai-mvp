export const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function signup(email,password){
  const res = await fetch(API_BASE + '/signup', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({email,password})})
  return res.json()
}

export async function login(username,password){
  const res = await fetch(API_BASE + '/token', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({username,password})})
  return res.json()
}

export async function saveJournal(token, ciphertext, iv){
  const res = await fetch(API_BASE + '/journals', {method:'POST', headers:{'content-type':'application/json', 'authorization':'Bearer '+token}, body: JSON.stringify({ciphertext, iv})})
  return res.json()
}

export async function listJournals(token){
  const res = await fetch(API_BASE + '/journals', {method:'GET', headers:{'authorization':'Bearer '+token}})
  return res.json()
}

export async function queryPrivateAgent(token, question){
  const res = await fetch(API_BASE + '/agent/private', {method:'POST', headers:{'content-type':'application/json', 'authorization':'Bearer '+token}, body: JSON.stringify({question})})
  return res.json()
}
