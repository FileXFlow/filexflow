export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
export async function uploadAndConvert(file: File, kind: string){
  const form = new FormData();
  form.append("file", file);
  form.append("kind", kind);
  const res = await fetch(`${API_BASE}/convert`, { method: "POST", body: form });
  if(!res.ok){ throw new Error(await res.text()); }
  return res.blob();
}
export function openOneOffCheckout(){ window.location.href = "LEMON_ONE_OFF_URL"; }
export function openSubscriptionCheckout(){ window.location.href = "LEMON_SUBSCRIPTION_URL"; }
