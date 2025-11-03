// Simple WebCrypto helpers: derive key from passphrase, encrypt/decrypt with AES-GCM
const enc = new TextEncoder()
const dec = new TextDecoder()

export async function deriveKey(passphrase, salt = 'relationship-ai-salt'){
  const pwKey = await window.crypto.subtle.importKey('raw', enc.encode(passphrase), 'PBKDF2', false, ['deriveKey'])
  return await window.crypto.subtle.deriveKey({name:'PBKDF2', salt: enc.encode(salt), iterations: 200000, hash:'SHA-256'}, pwKey, {name:'AES-GCM', length:256}, true, ['encrypt','decrypt'])
}

function abToBase64(buf){
  return btoa(String.fromCharCode(...new Uint8Array(buf)))
}
function base64ToAb(s){
  const bin = atob(s); const arr = new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) arr[i]=bin.charCodeAt(i); return arr.buffer
}

export async function encryptText(key, plaintext){
  const iv = window.crypto.getRandomValues(new Uint8Array(12))
  const ct = await window.crypto.subtle.encrypt({name:'AES-GCM', iv}, key, enc.encode(plaintext))
  return {ciphertext: abToBase64(ct), iv: abToBase64(iv)}
}

export async function decryptText(key, ciphertext_b64, iv_b64){
  const ct = base64ToAb(ciphertext_b64)
  const iv = base64ToAb(iv_b64)
  const pt = await window.crypto.subtle.decrypt({name:'AES-GCM', iv: new Uint8Array(iv)}, key, ct)
  return dec.decode(pt)
}
