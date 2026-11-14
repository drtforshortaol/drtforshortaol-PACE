export async function initializeOffline(status){
 const root=new URL('../',import.meta.url);
 if(!('serviceWorker' in navigator)){if(status)status.textContent='Offline unavailable';return;}
 try{
  const registration=await navigator.serviceWorker.register(new URL('sw.js',root),{scope:root.pathname});
  await navigator.serviceWorker.ready;
  const required=['index.html','registry.json','environment.json','search-index.json','core/hub.js','core/hub.css','core/navigation.js','core/offline.js','core/app-contract.js','apps/rcl-component-lab/index.html','apps/rcl-component-lab/manifest.json','shared/rcl/card-search.js'];
  const complete=(await Promise.all(required.map(p=>caches.match(new URL(p,root))))).every(Boolean);
  if(status)status.textContent=complete?'Offline preview ready':'Offline preparation incomplete — retry online';
  return registration;
 }catch(error){
  if(status)status.textContent='Offline preparation failed — retry online';
  console.error('RCL preview offline preparation failed',error);
 }
}
