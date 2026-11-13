# Machine à café : kata TDD (Python)

Implémentation du kata Coffee Machine en TDD, avec Python, pytest et unittest.mock.
La classe `MachineACafe` traduit les commandes clients en messages pour la machine à boissons.

## Prérequis

- Python 3.14 (testé avec 3.14.3)
- Git

## Installation

```powershell
git clone []
cd coffe_machine
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Lancer les tests

```powershell
pytest
```

Résultat attendu : `18 passed`.

## Structure

```
coffe_machine/
    exo/
        coffe_machine.py   # classe MachineACafe
        services.py        #  Notificateur et VerificateurQuantite
    test/
        test_coffe_machine.py
    pytest.ini
    requirements.txt


## Étapes réalisées

1. **Préparation des boissons** : thé, café, chocolat, sucres et bâtonnet (`T:1:0`, `H::`)
2. **Prix et argent** : préparation si montant suffisant, sinon message `M:Il manque X €`
3. **Extra chaud et orange** : `Ch::`, `Hh:1:0`, `Th:2:0`, `O::`
4. **Rapport de ventes** : unités par boisson et recettes totales
5. **Épuisement** : message à la console et notification, avec deux services mockés (`Mock(spec=...)`)

Toutes les itérations sont terminées, avec 18 tests verts.

## Difficultés rencontrées

- Configuration de pytest : `pythonpath` et `testpaths` dans `pytest.ini`, noms de dossiers et de fichiers à faire correspondre aux imports
- Erreur de syntaxe (`:` oublié après `else`)
- Piège des flottants (`0.60 - 0.40`), réglé avec le formatage `:.2f`
- Constructeur élargi à l'itération 5 : valeurs par défaut `None` pour ne pas casser les anciens tests
- Piège des mocks sans contrat, résolu avec `spec`

## Limites et améliorations possibles

- Les dates du rapport ne sont pas gérées (le cas d'utilisation ne les demande pas)
- Montants en flottants : des centimes entiers seraient plus robustes
- Regrouper `TYPES`, `PRIX` et `NOMS` en un seul dictionnaire