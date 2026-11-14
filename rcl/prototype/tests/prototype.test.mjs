import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const html=readFileSync(new URL('../index.html',import.meta.url),'utf8');
test('prototype provides essential controls',()=>{
  for(const id of ['back','hub','search','cards','empty']) assert.match(html,new RegExp('id="'+id+'"'));
});
test('prototype uses accessible native expandable cards',()=>{
  assert.match(html,/createElement\('details'\)/);
  assert.match(html,/createElement\('summary'\)/);
  assert.match(html,/<label for="search">/);
});
test('prototype uses safe text nodes rather than HTML interpolation for cards',()=>{
  assert.match(html,/s\.textContent=c\.title/);
  assert.match(html,/p\.textContent=c\.body/);
});
test('prototype includes explicit Hub navigation and safe back fallback',()=>{
  assert.match(html,/location\.assign\(config\.hubUrl\)/);
  assert.match(html,/new URL\(document\.referrer\)\.origin===location\.origin/);
});
test('prototype contains no remote runtime dependencies',()=>{
  assert.doesNotMatch(html,/<script[^>]+src="https?:/i);
  assert.doesNotMatch(html,/<link[^>]+href="https?:/i);
});
