import re #module pour les rejects
import string #récup tout les symboles et ponctuations 
from pathlib import Path


from tinydb import TinyDB, where, table

class User:
    #on créer un attribut pour la sauvergarde puis on lui indique le chemin du dossier courant
    DB = TinyDB(Path(__file__).resolve().parent / 'db.json', indent=4) 

    def __init__(self, first_name: str, last_name: str, phone_number: str="", address: str=""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def __repr__(self): #permet d'avoir une representation de la classe sur comment recréer cet objet print(repr(User))
        return f"User{self.first_name}, {self.last_name}"

    def __str__(self):
        return f"{self.full_name }\n{self.phone_number}\n{self.address}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def db_instance(self) -> table.Document:
        return User.DB.get((where('first_name') == self.first_name) & (where('last_name') == self.last_name))

    def _checks(self):
        self._check_phone_number()
        self._check_names

    def _check_phone_number(self):
        # [+()\s]* l'étoile * pour enlever plusieurs fois le même element \s pour les espaces
        phone_number = re.sub(r"[+()\s]*", "", self.phone_number)

        if len(phone_number) < 10 or not phone_number.isdigit(): #Vérification de la validité du numéro de telephone
           raise ValueError(f"Numéro de téléphone invalide") # on lève une erreur
    
    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError("Le prénom et le nom de famille ne peuvent pas être vides.")

        special_characters = string.punctuation + string.digits

        for character in self.first_name + self.last_name:
            if character in special_characters:
                raise ValueError(f"Nom invalide : {self.full_name}")

    def exists(self):
      return bool(self.db_instance)  #retourne true si on a un dico avec des infos
      
    def delete(self) -> list[int]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id]) #doc_id recup l'ID en fonction d'une clé
        return [] #si la liste est vide car si on utilise le script avec une boucle on itère pas sur un none

    def save(self, validate_data: bool=False) -> int: #récup un bool et retourne un int
        if validate_data:
            self._checks()
        
        if self.exists():
            return -1 #retourne -1 car l(utilisateur s'attend a un int
        else:
            return User.DB.insert(self.__dict__) #self.__dict__ insert un dico avec les attributs ^résents dans la classe


def get_all_users():
    return [User(**user) for user in User.DB.all()]
    # ** unpacking on récup la clé comme nom paramètre et la valeur comme la valeur du paramètre


if __name__ =="__main__":
    margaux = User("Margaux", "Verdier")
    print(margaux.delete())
    