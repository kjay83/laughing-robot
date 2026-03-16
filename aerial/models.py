from django.db import models

class Player(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(default='AUCUN',max_length=200,blank=True)
    alias = models.CharField(default='AUCUN',max_length=200,blank=True)
    email = models.EmailField(default='aucun@fail.com',max_length=200,blank=True)
    money = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom}"
    
    def initialize(self,starting_money):
        self.money = starting_money
    
    def receive(self,amount):
        self.money += amount
    
    def pay(self,amount):
        self.money -= amount
