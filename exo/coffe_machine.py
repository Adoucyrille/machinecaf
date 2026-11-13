class MachineACafe:
    TYPES = {
        "the": "T",
        "cafe": "C",
        "chocolat": "H",
        "orange": "O",
    }

    PRIX = {
        "the": 0.40,
        "cafe": 0.60,
        "chocolat": 0.50,
        "orange": 0.60,
    }

    NOMS = {
        "the": "Thé",
        "cafe": "Café",
        "chocolat": "Chocolat",
        "orange": "Jus d'orange",
    }

    def __init__(self, preparateur, verificateur=None, notificateur=None):
        self.preparateur = preparateur
        self.verificateur = verificateur
        self.notificateur = notificateur
        self.ventes = {}

    def commander(self, boisson, sucres=0, montant=0, extra_chaud=False):
        if self.verificateur and self.verificateur.est_vide(boisson):
            self.notificateur.notifier_boisson_manquante(boisson)
            self.preparateur.preparer(
                "M:Boisson épuisée : un message a été envoyé au responsable"
            )
            return

        prix = self.PRIX[boisson]

        if montant < prix:
            manque = prix - montant
            self.preparateur.preparer(
                f"M:Il manque {manque:.2f} €"
            )
            return

        code_boisson = self.TYPES[boisson]

        if extra_chaud and boisson != "orange":
            code_boisson += "h"

        if sucres == 0:
            message = f"{code_boisson}::"
        else:
            message = f"{code_boisson}:{sucres}:0"

        self.preparateur.preparer(message)
        self.ventes[boisson] = self.ventes.get(boisson, 0) + 1

    def imprimer_rapport(self):
        total = 0.0
        for boisson, quantite in self.ventes.items():
            print(f"{self.NOMS[boisson]} : {quantite}")
            total += self.PRIX[boisson] * quantite
        print(f"Recettes totales : {total:.2f} €")