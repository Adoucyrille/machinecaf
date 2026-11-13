
from unittest.mock import Mock

from exo.coffe_machine import MachineACafe

from exo.services import Notificateur, VerificateurQuantite



def test_commande_the_sans_sucre():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("the", 0, 0.40)

    preparateur.preparer.assert_called_once_with("T::")


def test_commande_cafe_sans_sucre():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("cafe", 0, 0.60)

    preparateur.preparer.assert_called_once_with("C::")


def test_commande_chocolat_sans_sucre():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("chocolat", 0, 0.50)

    preparateur.preparer.assert_called_once_with("H::")


def test_commande_the_avec_un_sucre():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("the", 1, 0.40)

    preparateur.preparer.assert_called_once_with("T:1:0")


def test_commande_cafe_avec_deux_sucres():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("cafe", 2, 0.60)

    preparateur.preparer.assert_called_once_with("C:2:0")


def test_commande_chocolat_avec_un_sucre():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("chocolat", 1, 0.50)

    preparateur.preparer.assert_called_once_with("H:1:0")


def test_commande_cafe_avec_montant_exact():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("cafe", 0, 0.60)

    preparateur.preparer.assert_called_once_with("C::")


def test_commande_cafe_avec_montant_insuffisant():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("cafe", 2, 0.40)

    preparateur.preparer.assert_called_once_with(
        "M:Il manque 0.20 €"
    )

def test_commande_cafe_avec_montant_superieur():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("cafe", 1, 1.00)

    preparateur.preparer.assert_called_once_with("C:1:0")

def test_commande_jus_orange():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("orange", 0, 0.60)

    preparateur.preparer.assert_called_once_with("O::")

def test_commande_cafe_extra_chaud():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("cafe", 0, 0.60, extra_chaud=True)

    preparateur.preparer.assert_called_once_with("Ch::")

def test_commande_chocolat_extra_chaud():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("chocolat", 1, 0.50, extra_chaud=True)

    preparateur.preparer.assert_called_once_with("Hh:1:0")

def test_commande_the_extra_chaud():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("the", 2, 0.40, extra_chaud=True)

    preparateur.preparer.assert_called_once_with("Th:2:0")

def test_jus_orange_ignore_extra_chaud():
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("orange", 0, 0.60, extra_chaud=True)

    preparateur.preparer.assert_called_once_with("O::")

def test_rapport_une_boisson_vendue(capsys):
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("the", 0, 0.40)
    machine.imprimer_rapport()

    resultat = capsys.readouterr()

    assert "Thé : 1" in resultat.out
    assert "Recettes totales : 0.40 €" in resultat.out


def test_rapport_plusieurs_boissons_vendues(capsys):
    preparateur = Mock()
    machine = MachineACafe(preparateur)

    machine.commander("the", 0, 0.40)
    machine.commander("cafe", 0, 0.60)
    machine.commander("chocolat", 0, 0.50)
    machine.commander("orange", 0, 0.60)

    machine.imprimer_rapport()

    resultat = capsys.readouterr()

    assert "Thé : 1" in resultat.out
    assert "Café : 1" in resultat.out
    assert "Chocolat : 1" in resultat.out
    assert "Jus d'orange : 1" in resultat.out
    assert "Recettes totales : 2.10 €" in resultat.out

def test_boisson_epuisee_envoie_un_message_et_une_notification():
    preparateur = Mock()
    verificateur = Mock(spec=VerificateurQuantite)
    notificateur = Mock(spec=Notificateur)
    verificateur.est_vide.return_value = True
    machine = MachineACafe(preparateur, verificateur, notificateur)

    machine.commander("cafe", 0, 0.60)

    preparateur.preparer.assert_called_once_with(
        "M:Boisson épuisée : un message a été envoyé au responsable"
    )
    notificateur.notifier_boisson_manquante.assert_called_once_with("cafe")


def test_boisson_disponible_ne_declenche_pas_de_notification():
    preparateur = Mock()
    verificateur = Mock(spec=VerificateurQuantite)
    notificateur = Mock(spec=Notificateur)
    verificateur.est_vide.return_value = False
    machine = MachineACafe(preparateur, verificateur, notificateur)

    machine.commander("cafe", 0, 0.60)

    preparateur.preparer.assert_called_once_with("C::")
    notificateur.notifier_boisson_manquante.assert_not_called()