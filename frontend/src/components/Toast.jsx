import React, { useEffect } from 'react'
export default function Toast({message,onClose}) {
  useEffect(() => { if(message) { const t=setTimeout(onClose,3400); return ()=>clearTimeout(t) } },[message,onClose])
  if(!message) return null
  return <div className="toast-note" role="status"><i className="bi bi-check-circle-fill me-2"></i>{message}<button onClick={onClose} aria-label="Close"><i className="bi bi-x"></i></button></div>
}
