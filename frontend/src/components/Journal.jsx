import React, {useState} from 'react'
import {deriveKey, encryptText, decryptText} from '../crypto'
import {saveJournal} from '../api'

export default function Journal({token, onSaved}){
  const [pass, setPass] = useState('')
  const [text, setText] = useState('')
  async function save(){
    if(!pass){ alert('Enter passphrase to derive key (client-side only)'); return }
    const key = await deriveKey(pass)
    const {ciphertext, iv} = await encryptText(key, text)
    await saveJournal(token, ciphertext, iv)
    setText(''); onSaved && onSaved()
  }
  return <div>
    <h3>Private Journal (client-side encrypted)</h3>
    <p>Enter a passphrase (not sent to server) to encrypt your entry locally.</p>
    <input placeholder="passphrase (local only)" value={pass} onChange={e=>setPass(e.target.value)} />
    <textarea placeholder="write your journal..." rows={6} value={text} onChange={e=>setText(e.target.value)} />
    <div style={{marginTop:8}}>
      <button onClick={save}>Save encrypted entry</button>
    </div>
  </div>
}
