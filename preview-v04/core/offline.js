export async function initializeOffline(status){
 const root=new URL('../',import.meta.url);
 if(!('serviceWorker' in navigator)){if(status)status.textContent='Offline unavailable';return;}
 try{
  const registration=await navigator.serviceWorker.register(new URL('sw.js',root),{scope:root.pathname});
  await navigator.serviceWorker.ready;
  // Installation only succeeds after every required preview asset is cached.
  if(status)status.textContent='Offline preview ready';
  return registration;
 }catch(error){
  if(status)status.textContent='Offline preparation failed — retry online';
  console.error('RCL preview offline preparation failed',error);
 }
}
