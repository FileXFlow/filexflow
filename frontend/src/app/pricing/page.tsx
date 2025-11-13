export default function Pricing(){
  function payPerFile(){ window.location.href="LEMON_ONE_OFF_URL"; }
  function subscribe(){ window.location.href="LEMON_SUBSCRIPTION_URL"; }
  return (<main style={{maxWidth:820,margin:'40px auto',padding:16}}>
    <h1 style={{fontSize:28,fontWeight:700}}>Pricing</h1>
    <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16}}>
      <div style={{border:'1px solid #e5e7eb',borderRadius:12,padding:16}}>
        <h2>Pay per file</h2>
        <p>$0.50 per file (up to 10 pages)</p>
        <button onClick={payPerFile}>Buy now</button>
      </div>
      <div style={{border:'1px solid #e5e7eb',borderRadius:12,padding:16}}>
        <h2>Monthly</h2>
        <p>$9.99/month • 400 pages included</p>
        <button onClick={subscribe}>Subscribe</button>
      </div>
    </div>
  </main>);
}