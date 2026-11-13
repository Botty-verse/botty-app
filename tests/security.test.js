// Run: deno test --allow-read tests/security.test.js
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { parseHTML } from 'npm:linkedom@0.18.12';
const html = readFileSync(new URL('../botty.html', import.meta.url), 'utf8');
function fn(name) {
  const match = html.match(new RegExp('  function ' + name + '\\([^]*?\\n  }'));
  if (!match) throw new Error('Missing function: ' + name);
  return match[0];
}
function assert(ok) { if (!ok) throw new Error('Assertion failed'); }
const { document } = parseHTML('<html><body></body></html>');
const context = vm.createContext({ document, location: { hash: '' }, b64dec: (s) => Buffer.from(s, 'base64url').toString('utf8'), el: () => ({}), naam: () => '<img src=x onerror=alert(1)>' });
vm.runInContext(['deelTekstVeilig', 'geldigSnapshot', 'leesGedeeld', 'vulKaart'].map(fn).join('\n'), context);
const valid = { n: 'Botty 🤖', g: 1, lt: '1 dag', sl: 'Baby', sk: 'born', gr: 1, lk: 'normaal', z: 0, w: 5, e: 100, d: 80, f: 90, gl: 90, b: 20 };
Deno.test('valid share links decode; malformed and oversized links are rejected', () => {
  context.location.hash = '#b=' + Buffer.from(JSON.stringify(valid)).toString('base64url');
  assert(context.leesGedeeld().n === valid.n);
  for (const input of [{ g: 1 }, { ...valid, e: '<img src=x>' }, null, [], { ...valid, n: 'x'.repeat(201) }]) {
    context.location.hash = '#b=' + Buffer.from(JSON.stringify(input)).toString('base64url');
    assert(context.leesGedeeld() === null);
  }
  context.location.hash = '#b=' + 'x'.repeat(4097);
  assert(context.leesGedeeld() === null);
});
Deno.test('share card fields render as text and badge names are escaped', () => {
  const attack = '<img src=x onerror=alert(1)>';
  const holder = document.createElement('div'), name = document.createElement('div'), rules = document.createElement('div');
  context.vulKaart(holder, name, rules, { ...valid, n: attack, lt: attack, sl: attack });
  assert(!name.querySelector('img') && !rules.querySelector('img'));
  assert(rules.textContent.includes(attack));
  const badge = document.createElement('div');
  badge.innerHTML = context.deelTekstVeilig(attack) + '<small>Safe formatting</small>';
  assert(!badge.querySelector('img') && badge.querySelector('small'));
  assert(!/regelsEl\.innerHTML\s*=/.test(html));
  // Each name used in the HTML badge must be escaped, in both translations.
  for (const line of html.split('\n').filter(l => /gedeeldBadge(Kan|Niet):/.test(l))) {
    assert(line.includes('deelTekstVeilig(sn)'));
    const formatter = vm.runInContext('(' + line.slice(line.indexOf('function'), line.lastIndexOf('}') + 1) + ')', context);
    badge.innerHTML = formatter(attack);
    assert(!badge.querySelector('img') && badge.querySelector('small'));

    if (line.includes('naam()')) assert(line.includes('deelTekstVeilig(naam())'));
  }
  const shared = html.slice(html.indexOf('  function toonGedeeld('), html.indexOf('// "Speel zelf"'));
  assert(!/\(s\.n \+/.test(shared));
});
