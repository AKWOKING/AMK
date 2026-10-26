/**
 * ─────────────────────────────────────────────────────────────────────────────
 * PRESTATIONS — le strict minimum déductible, rien de plus
 * ─────────────────────────────────────────────────────────────────────────────
 *
 * Le médecin n'a pas énuméré ses actes. Une seule chose est certaine, parce
 * qu'elle définit la mission décrite : il **consulte** en ophtalmologie, dans
 * plusieurs structures. Tout le reste — chirurgie, examens complémentaires,
 * champ visuel, OCT, prescription de lentilles — serait une invention.
 *
 * Pour publier une prestation : la copier ici avec sa source et sa date, puis
 * passer `status` à "confirmed" quand le médecin l'a validée. Le bloc se
 * construit à partir de cette liste ; vide, il n'affiche qu'une phrase honnête.
 */

export const services = [
  {
    id: "consultation",
    status: "reported",
    asOf: "2026-10-26",
    source: "Rôle décrit dans la demande : « itinerant consulting ophthalmologist ».",
    label: {
      fr: "Consultation ophtalmologique",
      en: "Ophthalmology consultation",
    },
    note: {
      fr: "Sur rendez-vous, dans l’un des quatre lieux de consultation.",
      en: "By appointment, at one of the four consultation locations.",
    },
  },

  /* Exemples de ce qui PEUT être ajouté — et qui n'est pas publié aujourd'hui.
  {
    id: "refraction",
    status: "unknown",
    asOf: "",
    source: "",
    label: { fr: "Réfraction et prescription de lunettes", en: "Refraction and spectacle prescription" },
    note: { fr: "", en: "" },
  },
  */
];

/** Ce qu'on affiche quand aucune prestation n'est confirmée. */
export const servicesEmptyNotice = {
  fr: "La liste des actes pratiqués sera publiée après confirmation du médecin. En cas de doute, posez la question au moment de la prise de rendez-vous.",
  en: "The list of services performed will be published once the doctor confirms it. If in doubt, ask when you request an appointment.",
};
