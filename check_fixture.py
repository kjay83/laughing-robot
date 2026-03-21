import json

with open('aerial/fixtures/complet_v2.json') as f:
    data = json.load(f)

print("=== Vérification du fixture ===\n")

# Chercher les objets CompagnieAerienne
compagnies = [obj for obj in data if obj['model'] == 'aerial.compagnieaerienne']
print(f"Nombre de CompagnieAerienne: {len(compagnies)}")

for obj in compagnies:
    print(f"\nCompagnieAerienne pk={obj['pk']}:")
    print(f"  Champs: {list(obj['fields'].keys())}")
    if 'player' in obj['fields']:
        print(f"  ⚠️  ERREUR: Contient 'player' au lieu de 'proprietaire'")
        print(f"      Valeur: {obj['fields']['player']}")
    if 'proprietaire' in obj['fields']:
        print(f"  ✓ OK: Contient 'proprietaire'")
        print(f"    Valeur: {obj['fields']['proprietaire']}")
