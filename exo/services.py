from abc import ABC, abstractmethod


class Notificateur(ABC):
    @abstractmethod
    def notifier_boisson_manquante(self, boisson):
        ...


class VerificateurQuantite(ABC):
    @abstractmethod
    def est_vide(self, boisson):
        ...