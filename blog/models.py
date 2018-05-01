from django.db import models





class Categorie(models.Model):
    nom = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.nom


# Create your models here.
class Article(models.Model):
    titre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True)
    auteur = models.CharField(max_length=42)
    contenu = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de parution")
    """
    About Foreign Keys -- 
    Comment the foreign key reference in videodata and run the makemigrations and migrate
    Add the model in admins.py and make a new entry in table
    Now uncomment the foreign key reference and provide a default=1 .Run make migrations and migrate
    Remove the default=1 in foreign key field.
    """
    categorie = models.ForeignKey('Categorie',on_delete=models.PROTECT)
    def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.titre

class Moteur(models.Model):
    nom = models.CharField(max_length=25)
    def __str__(self):
        return self.nom

class Voiture(models.Model):
    nom = models.CharField(max_length=25)
    moteur = models.OneToOneField(Moteur,on_delete=models.PROTECT)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom

class Vendeur(models.Model):
    nom = models.CharField(max_length=30)
    produits = models.ManyToManyField(Produit, through='Offre')

    def __str__(self):
        return self.nom

class Offre(models.Model):
    prix = models.IntegerField()
    produit = models.ForeignKey(Produit,on_delete=models.PROTECT)
    vendeur = models.ForeignKey(Vendeur,on_delete=models.PROTECT)

    def __str__(self):
        return "{0} vendu par {1}".format(self.produit, self.vendeur)