// src/api.js

// Use Vercel environment variable VITE_BACKEND_URL, fallback to localhost
export const API_BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

// Debug: confirm correct URL in console
console.log("API_BASE is", API_BASE)

// Centralized fetch wrapper
async function request(endpoint, options) {
  const res = await fetch(API_BASE + endpoint, options)
  if (!res.ok) {
    const errorText = await res.text()
    throw new Error(`API request to ${endpoint} failed: ${errorText}`)
  }
  return res.json()
}

// Signup
export async function signup(email, password) {
  return request('/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
}

// Login
export async function login(username, password) {
  return request('/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
}

// Save journal entry
export async function saveJournal(token, ciphertext, iv) {
  return request('/journals', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token,
    },
    body: JSON.stringify({ ciphertext, iv }),
  })
}

// List journal entries
export async function listJournals(token) {
  return request('/journals', {
    method: 'GET',
    headers: { 'Authorization': 'Bearer ' + token },
  })
}

// Query private AI agent
export async function queryPrivateAgent(token, question) {
  return request('/agent/private', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token,
    },
    body: JSON.stringify({ question }),
  })
}
