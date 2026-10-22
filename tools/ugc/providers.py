# -*- coding: utf-8 -*-
"""Fournisseurs de clips IA — couche mince, honnête, hors ligne par défaut.

Le moteur `ugc.py` ne sait pas qui fabrique un plan : il reçoit un fichier. Cette
couche sert à *produire* ce fichier quand on a une clé, et à *refuser proprement*
quand on n'en a pas. Aucun appel réseau n'est tenté sans clé.

État réel de ce sandbox (mesuré le 22/10/2026) : seuls github, npm et pypi sont
joignables. `generativelanguage.googleapis.com` et `api.heygen.com` ne le sont pas.
Donc même avec une clé, ces appels doivent tourner **sur le poste de King ou en CI**,
pas ici. C'est écrit dans le code, pas seulement dans la doc.

    python3 tools/ugc/providers.py            # état + prix
    python3 tools/ugc/providers.py quote 8    # devis pour 8 s
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

# Tarifs Gemini API vérifiés sur ai.google.dev/gemini-api/docs/pricing (oct. 2026),
# en dollars par seconde de vidéo AVEC audio.
VEO = {
    "lite":     {"720p": 0.05, "1080p": 0.08},
    "fast":     {"720p": 0.10, "1080p": 0.12, "4k": 0.30},
    "standard": {"720p": 0.40, "1080p": 0.40, "4k": 0.60},
}

PROVIDERS = {
    "veo": {
        "name": "Google Veo 3.1 (Gemini API)",
        "key": "GEMINI_API_KEY",
        "produces": "clip 9:16 avec audio synchronisé, 4/6/8 s, 24 fps",
        "why": "la seule voie « qualité Flow » pilotable dans un pipeline ; Flow n'a pas d'API",
        "cost": "0,64 $ (Lite 1080p) · 0,96 $ (Fast 1080p) · 3,20 $ (Standard) pour 8 s",
        "host": "generativelanguage.googleapis.com",
    },
    "heygen": {
        "name": "HeyGen (Avatar V)",
        "key": "HEYGEN_API_KEY",
        "produces": "présentateur qui parle, audio fourni ou généré, fond vert ou image",
        "why": "identité stable sur un long script ; ~0,10 à 1,16 $ la vidéo de 30 s",
        "cost": "29 $/mois d'abonnement",
        "host": "api.heygen.com",
    },
    "hedra": {
        "name": "Hedra (Character-3)",
        "key": "HEDRA_API_KEY",
        "produces": "une photo + une voix -> tête parlante animée",
        "why": "le meilleur moyen d'animer une seule image de nous, sans tournage",
        "cost": "~20 $/mois",
        "host": "api.hedra.com",
    },
    "fal": {
        "name": "fal.ai (Wan 2.2 / InfiniteTalk / MuseTalk hébergés)",
        "key": "FAL_KEY",
        "produces": "modèles ouverts exécutés à distance : image->vidéo, lip-sync",
        "why": "les mêmes poids libres que sur un GPU local, sans GPU local",
        "cost": "à la seconde de calcul, quelques centimes par clip",
        "host": "queue.fal.run",
    },
}


def env(key: str) -> str | None:
    v = os.environ.get(key, "").strip()
    return v or None


def quote(seconds: float, tier: str = "fast", res: str = "1080p") -> float:
    return round(seconds * VEO[tier][res], 4)


def status() -> list[dict]:
    out = []
    for pid, p in PROVIDERS.items():
        out.append({**p, "id": pid, "ready": bool(env(p["key"]))})
    return out


def print_status():
    print("fournisseur                          clé              état")
    print("-" * 78)
    for s in status():
        state = "prête" if s["ready"] else f"manquante ({s['key']})"
        print(f"{s['name'][:36]:<36} {s['key']:<20} {state}")
    print()
    print("Devis 8 s (clip unique, audio inclus) :")
    for tier in ("lite", "fast", "standard"):
        print(f"  Veo {tier:<9} {quote(8, tier):>6.2f} $")
    print()
    print("Rappel : de ce sandbox, api.google/heygen/fal ne sont pas joignables.")
    print("Les appels ci-dessous doivent tourner sur un poste ou en CI.")


def _post(url: str, payload: dict, headers: dict) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def generate_veo(prompt: str, out: str, tier: str = "fast", res: str = "1080p",
                 seconds: int = 8, image: str | None = None) -> str:
    """Veo 3.1 via Gemini API. Long-running : on lance, on interroge, on télécharge."""
    key = env("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY absente — rien n'est tenté, aucun faux succès.")
    if seconds not in (4, 6, 8):
        raise ValueError("Veo n'accepte que 4, 6 ou 8 secondes")
    if res in ("1080p", "4k") and seconds != 8:
        raise ValueError("1080p et 4K exigent 8 s")

    model = f"veo-3.1-{tier}-generate-preview"
    payload = {"instances": [{"prompt": prompt}],
               "parameters": {"aspectRatio": "9:16", "resolution": res,
                              "durationSeconds": seconds}}
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model}:predictLongRunning?key={key}")
    op = _post(url, payload, {})
    name = op.get("name")
    while True:
        time.sleep(10)
        with urllib.request.urlopen(
                f"https://generativelanguage.googleapis.com/v1beta/{name}?key={key}",
                timeout=120) as r:
            op = json.loads(r.read().decode())
        if op.get("done"):
            break
    uri = (op["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"])
    with urllib.request.urlopen(uri if "key=" in uri else f"{uri}&key={key}", timeout=300) as r, \
            open(out, "wb") as f:
        f.write(r.read())
    return out


def generate_heygen(script: str, avatar_id: str, voice_id: str, out: str,
                    width: int = 1080, height: int = 1920) -> str:
    key = env("HEYGEN_API_KEY")
    if not key:
        raise RuntimeError("HEYGEN_API_KEY absente — rien n'est tenté.")
    payload = {"video_inputs": [{
        "character": {"type": "avatar", "avatar_id": avatar_id, "avatar_style": "normal"},
        "voice": {"type": "text", "input_text": script, "voice_id": voice_id},
        "background": {"type": "color", "value": "#0A1220"},
    }], "dimension": {"width": width, "height": height}}
    res = _post("https://api.heygen.com/v2/video/generate", payload, {"X-Api-Key": key})
    vid = res["data"]["video_id"]
    while True:
        time.sleep(15)
        with urllib.request.urlopen(urllib.request.Request(
                f"https://api.heygen.com/v1/video_status.get?video_id={vid}",
                headers={"X-Api-Key": key}), timeout=60) as r:
            st = json.loads(r.read().decode())["data"]
        if st["status"] == "completed":
            with urllib.request.urlopen(st["video_url"], timeout=300) as r, open(out, "wb") as f:
                f.write(r.read())
            return out
        if st["status"] == "failed":
            raise RuntimeError(f"HeyGen a échoué : {st.get('error')}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "quote":
        s = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
        for tier in ("lite", "fast", "standard"):
            print(f"Veo 3.1 {tier:<9} {s:>4.0f} s -> {quote(s, tier):.2f} $")
    else:
        print_status()
