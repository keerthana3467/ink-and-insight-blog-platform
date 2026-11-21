import React, {useRef} from 'react'
export default function Editor({value,onChange}) {
  const ref=useRef(null)
  function insert(tag){
    const el=ref.current; el?.focus()
    const start=el?.selectionStart ?? value.length, end=el?.selectionEnd ?? value.length
    const selected=value.slice(start,end) || 'Your text'
    const wrap=tag==='ul'?`<ul><li>${selected}</li></ul>`:tag==='ol'?`<ol><li>${selected}</li></ol>`:tag==='blockquote'?`<blockquote>${selected}</blockquote>`:`<${tag}>${selected}</${tag}>`
    onChange(value.slice(0,start)+wrap+value.slice(end))
  }
  return <div className="editor-shell"><div className="editor-toolbar" aria-label="Text formatting">
    {[['h2','H2'],['h3','H3'],['p','P'],['strong','B'],['em','I'],['ul','• List'],['ol','1. List'],['blockquote','Quote']].map(([tag,label])=><button type="button" key={tag} onClick={()=>insert(tag)}>{label}</button>)}
    <button type="button" onClick={()=>{const url=window.prompt('Paste a link URL');if(url)onChange(value+`<a href="${url}" target="_blank" rel="noopener noreferrer">Link text</a>`)}}>Link</button>
  </div><textarea ref={ref} className="editor-input" value={value} onChange={e=>onChange(e.target.value)} placeholder="Start with a thought worth sharing…" rows="16"/></div>
}
