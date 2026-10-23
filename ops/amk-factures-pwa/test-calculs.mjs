// AMK Factures — le seul test qui compte : les calculs qui décident d'une relance.
// Il lit index.html (le vrai fichier publié), en extrait les fonctions de calcul, et les exécute.
//
//   node test-calculs.mjs        → doit afficher « 8 assertions vertes »
//
// Ce qu'il ne teste pas : le rendu, le PDF, l'installation. Ces trois-là se vérifient sur un téléphone.

import { readFileSync } from 'node:fs';

const html = readFileSync(new URL('./index.html', import.meta.url), 'utf8');

// Le bloc des calculs : de `const calc` jusqu'à `const clientOf` (exclu).
const start = html.indexOf('const calc = inv =>');
const end = html.indexOf('const clientOf');
if (start < 0 || end < 0 || end < start) {
  console.error('✗ les fonctions de calcul sont introuvables dans index.html — le fichier a changé de forme');
  process.exit(1);
}
const source = html.slice(start, end);

const num = v => Number(v) || 0;
const todayISO = () => new Date().toISOString().slice(0, 10);
const day = n => {
  const d = new Date();
  d.setDate(d.getDate() + n);
  return d.toISOString().slice(0, 10);
};

// eslint-disable-next-line no-new-func
const f = new Function('num', 'todayISO', `${source}; return { calc, statusOf, lateDays, money };`)(num, todayISO);

let pass = 0, fail = 0;
const check = (label, got, want) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (ok) { pass++; console.log(`  ✓ ${label}`); }
  else { fail++; console.log(`  ✗ ${label} — attendu ${JSON.stringify(want)}, obtenu ${JSON.stringify(got)}`); }
};

// Une facture échue de 11 jours, 75 000 FCFA, rien de payé.
const tardive = {
  date: day(-25), due: day(-11), items: [{ qty: 1, price: 75000 }], payments: [],
};
check('statut d’une facture échue', f.statusOf(tardive), 'overdue');
check('jours de retard', f.lateDays(tardive), 11);
check('solde dû', f.calc(tardive).bal, 75000);
// le séparateur de milliers est une espace insécable : on la ramène à une espace normale.
check('montant formaté', f.money(75000, 'fr').replace(/\s/g, ' '), '75 000 FCFA');

// Payée en totalité → plus en retard, quel que soit l'échéancier.
check('statut d’une facture soldée', f.statusOf({ ...tardive, payments: [{ amount: 75000 }] }), 'paid');

// Acompte → partielle, et le retard court toujours.
const acompte = { ...tardive, payments: [{ amount: 25000 }] };
check('statut avec acompte', f.statusOf(acompte), 'overdue');
check('solde après acompte', f.calc(acompte).bal, 50000);

// Échéance dans le futur → aucun jour de retard, même avec un acompte.
const future = { date: day(-1), due: day(14), items: [{ qty: 2, price: 40000 }], payments: [] };
check('facture à échoir, aucun retard', f.lateDays(future), 0);

console.log(`\n${pass} assertion(s) verte(s), ${fail} échec(s).`);
process.exit(fail ? 1 : 0);
