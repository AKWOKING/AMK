/* UNI-LABO v2 · LES LIENS WHATSAPP QUI PARLENT LA LANGUE DU VISITEUR — écrit le 24/09/2026.

   Pourquoi CE bloc existe, et pourquoi il est séparé des deux autres :
   les deux blocs repris mot pour mot de la version précédente portent la fiche vivante, l'état
   d'ouverture et la bascule de langue — c'est le contrat, on n'y touche pas. Ce troisième bloc ajoute
   une chose que la version précédente ne savait pas faire, et il le fait sans élargir ce contrat.

   Le problème, tel qu'il se voyait : un visiteur qui lit la page en anglais clique « Ask the price » et
   envoie… une phrase française. Le laboratoire est bilingue, mais choisir la langue de quelqu'un d'autre
   n'est pas notre travail. (Le formulaire, lui, compose déjà son message dans la langue de la page :
   c'est le bloc repris qui s'en occupe.)

   La règle de la maison, tenue : **le HTML porte toujours un lien réel et utilisable** — le lien
   français, parce que c'est la langue du laboratoire et celle de son personnel. Sans JavaScript, un
   visiteur écrit en français. Avec JavaScript, s'il lit la page en anglais, le lien se réécrit en
   anglais. Rien n'est inventé : le numéro est écrit ici, les deux messages viennent des attributs
   `data-fr-text` / `data-en-text` posés par le constructeur. */
(function () {
  var NUM = '237696139819';
  function build(text) {
    return 'https://wa.me/' + NUM + '?text=' + encodeURIComponent(text);
  }
  function paint() {
    var en = document.documentElement.getAttribute('data-lang') === 'en';
    var links = [].slice.call(document.querySelectorAll('a[data-wa][data-fr-text]'));
    links.forEach(function (a) {
      var text = a.getAttribute(en ? 'data-en-text' : 'data-fr-text');
      if (text) a.setAttribute('href', build(text));
    });
  }
  paint();
  ['btn-fr', 'btn-en'].forEach(function (id) {
    var b = document.getElementById(id);
    if (b) b.addEventListener('click', function () { setTimeout(paint, 0); });
  });
})();
