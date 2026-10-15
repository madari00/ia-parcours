"""Tests de l'API. Lancer : pytest -q

Ces tests sautent automatiquement si fastapi n'est pas installé.
"""
import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)

DOSSIER_VALIDE = {
    "age": 38, "revenu_mensuel_fcfa": 175000, "montant_credit_fcfa": 500000,
    "duree_mois": 12, "anciennete_client_mois": 30, "nb_credits_precedents": 3,
    "score_mobile_money": 62, "secteur": "commerce", "ville": "Ouagadougou",
}


def test_sante():
    r = client.get("/sante")
    assert r.status_code == 200
    assert r.json()["statut"] == "ok"


def test_prediction_nominale():
    r = client.post("/predire", json=DOSSIER_VALIDE)
    assert r.status_code == 200
    corps = r.json()
    assert 0.0 <= corps["probabilite_defaut"] <= 1.0
    assert corps["decision"] in {"accord", "refus"}
    assert "seuil_utilise" in corps


def test_age_invalide_rejete():
    mauvais = {**DOSSIER_VALIDE, "age": 12}
    assert client.post("/predire", json=mauvais).status_code == 422


def test_montant_negatif_rejete():
    mauvais = {**DOSSIER_VALIDE, "montant_credit_fcfa": -1000}
    assert client.post("/predire", json=mauvais).status_code == 422


def test_champ_manquant_rejete():
    incomplet = {k: v for k, v in DOSSIER_VALIDE.items() if k != "score_mobile_money"}
    assert client.post("/predire", json=incomplet).status_code == 422


def test_secteur_inconnu_ne_plante_pas():
    """Le modèle doit encaisser une modalité jamais vue (handle_unknown='ignore')."""
    autre = {**DOSSIER_VALIDE, "secteur": "transport"}
    assert client.post("/predire", json=autre).status_code == 200
