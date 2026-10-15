"""Tests de l'API. Lancer : pytest -q"""
import pandas as pd
import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)

HISTORIQUE = [{"mois": f"2025-{m:02d}", "prix": 240 + 3 * m} for m in range(1, 13)]
DEMANDE = {
    "produit": "Millet", "marche": "Ouahigouya", "region": "NORD",
    "prix_national_lag1": 265.0,
    "historique": HISTORIQUE + [{"mois": "2026-01", "prix": 279.0}],
}


def test_sante():
    r = client.get("/sante")
    assert r.status_code == 200
    assert r.json()["statut"] == "ok"


def test_performance_expose_les_baselines():
    """Un service honnête publie ses baselines, pas seulement son meilleur score."""
    r = client.get("/performance")
    assert r.status_code == 200
    corps = r.json()
    for h in ("1", "3", "6", "12"):
        methodes = corps["horizons"][h]["methodes"]
        assert {"modele", "persistance", "saisonnier_12"} <= set(methodes)
        assert "MAE" in methodes["persistance"]


def test_prevision_nominale():
    r = client.post("/prevision", json=DEMANDE)
    assert r.status_code == 200, r.text
    corps = r.json()
    assert len(corps["previsions"]) == 4
    assert corps["dernier_prix_connu"] == 279.0
    for p in corps["previsions"]:
        assert p["valeur_recommandee"] > 0
        assert p["horizon_mois"] in (1, 3, 6, 12)
    # la méthode recommandée à court terme doit être la persistance (résultat mesuré)
    court = next(p for p in corps["previsions"] if p["horizon_mois"] == 1)
    assert court["methode_recommandee"] == "persistance"


def test_mois_non_consecutifs_rejetes():
    mauvais = dict(DEMANDE)
    mauvais["historique"] = DEMANDE["historique"][:6] + DEMANDE["historique"][7:]
    r = client.post("/prevision", json=mauvais)
    assert r.status_code == 422


def test_historique_trop_court_rejete():
    mauvais = dict(DEMANDE, historique=HISTORIQUE[:5])
    assert client.post("/prevision", json=mauvais).status_code == 422


def test_produit_inconnu_rejete():
    mauvais = dict(DEMANDE, produit="Riz")
    assert client.post("/prevision", json=mauvais).status_code == 422


def test_prix_absurde_rejete():
    mauvais = dict(DEMANDE)
    mauvais["historique"] = [{"mois": p["mois"], "prix": -5} for p in DEMANDE["historique"]]
    assert client.post("/prevision", json=mauvais).status_code == 422


def test_alerte():
    r = client.post("/alerte", json=DEMANDE)
    assert r.status_code == 200, r.text
    corps = r.json()
    assert 0.0 <= corps["probabilite_flambee"] <= 1.0
    assert corps["decision"] in {"alerte", "vigilance normale"}
    assert corps["performance_modele"]["pr_auc"] is not None


def test_reproductibilite():
    """Deux appels identiques doivent donner exactement le même résultat."""
    a = client.post("/prevision", json=DEMANDE).json()
    b = client.post("/prevision", json=DEMANDE).json()
    assert a == b
