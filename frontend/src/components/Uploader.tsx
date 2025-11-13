'use client';
import { useState } from 'react';
import { uploadAndConvert } from "../lib/api";

type Kind = 'pdf2docx'|'pdf2xlsx'|'pdf2csv'|'pdf2pptx'|'pdf2html'|'pdf2jpg'|'jpg2pdf'|'docx2pdf'|'xlsx2pdf'|'pptx2pdf'|'html2pdf';

export default function Uploader(){
  const [kind, setKind] = useState<Kind>('pdf2docx');
  const [busy, setBusy] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState<string>();

  const acceptFor = (k: Kind) => k.startsWith('pdf2') ? 'application/pdf'
    : k==='jpg2pdf' ? 'image/jpeg'
    : k==='docx2pdf' ? '.docx,application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    : k==='xlsx2pdf' ? '.xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    : k==='pptx2pdf' ? '.pptx,application/vnd.openxmlformats-officedocument.presentationml.presentation'
    : k==='html2pdf' ? '.html,text/html' : '*/*';

  async function onSelect(e: React.ChangeEvent<HTMLInputElement>){
    const f = e.target.files?.[0]; if(!f) return;
    setBusy(true); setDownloadUrl(undefined);
    try{
      const blob = await uploadAndConvert(f, kind);
      const url = URL.createObjectURL(blob);
      setDownloadUrl(url);
    }catch(err:any){
      alert(err?.message || 'Error converting file.');
    }finally{ setBusy(false); }
  }

  return (<div style={{marginTop:16}}>
    <div style={{display:'flex',flexWrap:'wrap',gap:8,marginBottom:12}}>
      {(['pdf2docx','pdf2xlsx','pdf2csv','pdf2pptx','pdf2html','pdf2jpg','jpg2pdf','docx2pdf','xlsx2pdf','pptx2pdf','html2pdf'] as Kind[]).map(k=> (
        <button key={k} onClick={()=>setKind(k)} style={{padding:'6px 10px',border:'1px solid #e5e7eb',borderRadius:8,background:k===kind?'#111':'#fff',color:k===kind?'#fff':'#111'}}>
          {k.replace('2', ' → ').toUpperCase()}
        </button>
      ))}
    </div>
    <label style={{display:'block',border:'2px dashed #e5e7eb',borderRadius:12,padding:24,textAlign:'center',cursor:'pointer'}}>
      <input type="file" accept={acceptFor(kind)} style={{display:'none'}} onChange={onSelect}/>
      {busy ? 'Processing…' : 'Drag & drop or click to upload'}
    </label>
    {downloadUrl && <a download href={downloadUrl} style={{display:'block',marginTop:12,textDecoration:'underline'}}>Download converted file</a>}
  </div>);
}
