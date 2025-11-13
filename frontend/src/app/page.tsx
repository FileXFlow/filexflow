import Uploader from "../components/Uploader";
export default function Page(){ return <main style={{maxWidth:820,margin:'40px auto',padding:16}}>
  <h1 style={{fontSize:28,fontWeight:700}}>Convert your files in seconds</h1>
  <p style={{opacity:.7}}>PDF ↔ Word/Excel/CSV/HTML/JPG • Pay per file or subscribe monthly</p>
  <Uploader/>
</main> }
