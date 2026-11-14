// Isolated RCL v0.4 preview only. Does not control orange or blue Hub.
const CACHE='rcl-v04-preview-20261114-a';
const ASSETS=['./','./index.html','./registry.json','./environment.json','./search-index.json','./core/hub.js','./core/hub.css','./core/navigation.js','./core/offline.js','./core/app-contract.js','./apps/rcl-component-lab/index.html','./apps/rcl-component-lab/manifest.json','./shared/rcl/card-search.js'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(ASSETS))));
self.addEventListener('activate',event=>event.waitUntil((async()=>{for(const key of await caches.keys())if(key.startsWith('rcl-v04-preview-')&&key!==CACHE)await caches.delete(key);await self.clients.claim();})()));
self.addEventListener('fetch',event=>{const url=new URL(event.request.url);if(event.request.method!=='GET'||url.origin!==self.location.origin||!url.pathname.startsWith(new URL('./',self.location.href).pathname))return;event.respondWith((async()=>{const cached=await caches.match(event.request,{ignoreSearch:true});if(cached)return cached;try{return await fetch(event.request);}catch{return new Response('Not available offline',{status:503});}})());});
