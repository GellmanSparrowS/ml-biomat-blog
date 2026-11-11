import {ALLOWED} from './routes.mjs';
/* Verified PayPal PDT fulfillment. No payer information is stored or logged. */
const SITE='https://ml-biomat.com';
const ITEM='ML-BIOMAT-HTML';
export function validPayment(text,tx,now=Date.now()){
 const lines=text.trim().split(/\r?\n/);if(lines.shift()!=='SUCCESS')return false;
 const data=new URLSearchParams(lines.join('&'));
 const amount=Number(data.get('mc_gross')||data.get('payment_gross'));
 const paid=Date.parse(data.get('payment_date'));
 return data.get('txn_id')===tx && data.get('payment_status')==='Completed'
  && data.get('mc_currency')==='USD' && Number.isFinite(amount) && amount>=1
  && (data.get('item_number')===ITEM||data.get('item_number1')===ITEM)
  && data.get('test_ipn')!=='1' && Number.isFinite(paid)
  && paid<=now+300000 && paid>=now-3*86400000;
}
export class PaymentClaim {
 constructor(ctx,env){this.ctx=ctx;this.env=env}
 async fetch(request){
  const {tx,claim,page}=await request.json();
  return this.ctx.blockConcurrencyWhile(async()=>{
   const saved=await this.ctx.storage.get('claim');
   if(saved)return Response.json({ok:saved.claim===claim&&saved.page===page},{status:saved.claim===claim&&saved.page===page?200:409});
   if(!this.env.PAYPAL_PDT_TOKEN)return Response.json({ok:false},{status:503});
   let response;
   try{response=await fetch('https://www.paypal.com/cgi-bin/webscr',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams({cmd:'_notify-synch',tx,at:this.env.PAYPAL_PDT_TOKEN}),signal:AbortSignal.timeout(12000)})}
   catch{return Response.json({ok:false},{status:503})}
   if(!response.ok||!validPayment(await response.text(),tx))return Response.json({ok:false},{status:402});
   await this.ctx.storage.put('claim',{claim,page});
   await this.ctx.storage.setAlarm(Date.now()+7*86400000);
   return Response.json({ok:true});
  });
 }
 async alarm(){await this.ctx.storage.deleteAll()}
}
export default {
 async fetch(request,env){
  const url=new URL(request.url),origin=request.headers.get('Origin');
  const headers={'Access-Control-Allow-Origin':SITE,'Vary':'Origin','Cache-Control':'no-store','Content-Type':'application/json','X-Content-Type-Options':'nosniff'};
  if(url.pathname==='/health'&&request.method==='GET')return Response.json({ready:Boolean(env.PAYPAL_PDT_TOKEN&&env.PAYMENTS)},{headers});
  if(origin!==SITE)return Response.json({error:'origin'},{status:403,headers});
  if(request.method==='OPTIONS')return new Response(null,{status:204,headers:{...headers,'Access-Control-Allow-Methods':'POST','Access-Control-Allow-Headers':'Content-Type','Access-Control-Max-Age':'600'}});
  if(url.pathname!=='/verify'||request.method!=='POST')return Response.json({error:'route'},{status:404,headers});
  if(Number(request.headers.get('Content-Length')||0)>2048)return Response.json({error:'size'},{status:413,headers});
  let data;try{const raw=await request.text();if(raw.length>2048)throw Error();data=JSON.parse(raw)}catch{return Response.json({error:'input'},{status:400,headers})}
  if(!data||typeof data!=='object'||Array.isArray(data))return Response.json({error:'input'},{status:400,headers});
  const {tx,claim,page}=data;
  if(typeof tx!=='string'||!/^[A-Z0-9]{17}$/.test(tx)||typeof claim!=='string'||!/^[a-f0-9]{64}$/.test(claim)||!ALLOWED.has(page))return Response.json({error:'input'},{status:400,headers});
  const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(tx)))).map(b=>b.toString(16).padStart(2,'0')).join('');
  const result=await env.PAYMENTS.get(env.PAYMENTS.idFromName(hash)).fetch('https://claim.internal/',{method:'POST',body:JSON.stringify({tx,claim,page})});
  return new Response(await result.text(),{status:result.status,headers});
 }
};
