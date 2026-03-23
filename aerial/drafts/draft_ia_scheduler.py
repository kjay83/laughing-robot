from django.utils import timezone
from datetime import timedelta

class Enterprise(models.Model):
    name = models.CharField(max_length=100)
    cash_flow = models.DecimalField(max_digits=10, decimal_places=2)
    last_update_time = models.DateTimeField(default=timezone.now())

def update_enterprise_cash_flow():
    # Récupérer toutes les entreprises à mettre à jour
    enterprises = Enterprise.objects.all()

    # Mettre à jour le cash flow de chaque entreprise
    for enterprise in enterprises:
        # Calculer la variation du cash flow en fonction du temps écoulé
        time_since_last_update = timezone.now() - enterprise.last_update_time
        cash_flow_variation = calculate_cash_flow_variation(enterprise, time_since_last_update)

        # Mettre à jour le cash flow de l'entreprise
        enterprise.cash_flow += cash_flow_variation
        enterprise.last_update_time = timezone.now()
        enterprise.save()

def calculate_cash_flow_variation(enterprise, time_since_last_update):
    # Logique de calcul de la variation du cash flow en fonction du temps écoulé
    # Par exemple, vous pouvez utiliser une formule de génération de cash flow continue
    return time_since_last_update.total_seconds() / 3600 * enterprise.cash_flow_rate

# Planifier la tâche pour mettre à jour le cash flow des entreprises à intervalles réguliers
schedule.every(1).hour.do(update_enterprise_cash_flow)

# Exécuter la tâche planifiée
while True:
    schedule.run_pending()
    time.sleep(1)