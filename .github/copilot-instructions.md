# Copilot Instructions for laughing-robot

## Project Overview

**Type**: Django airline management game simulator  
**Language**: Python 3.x + Django 6.0.3  
**Database**: SQLite3 (db.sqlite3)  
**Main Config**: `employe_project/` (Django project settings)  
**French**: Project uses French language for models and comments

## Environment Setup

### Virtual Environment
- **Location**: `faiz1/` (Windows venv)
- **Activation**: `.\faiz1\Scripts\activate.ps1` (PowerShell)
- **Activation**: `faiz1\Scripts\activate.bat` (Command Prompt)

### Key Commands

```bash
# Activate environment
.\faiz1\Scripts\activate.ps1

# Start development server
python manage.py runserver

# Run Django shell
python manage.py shell

# Create migrations
python manage.py makemigrations [app_name]

# Apply migrations
python manage.py migrate

# Reset all data
python manage.py flush

# Load fixture data
python manage.py loaddata app_name/fixtures/fixture_name.json

# Export data to fixture
python manage.py dumpdata app_name.Model1 app_name.Model2 --indent 4 > app_name/fixtures/output.json

# Admin panel
Navigate to http://localhost:8000/admin
Admin: admin / admin
```

## Project Structure

### Django Apps

#### 1. `aerial/` - Core Aviation System
**Purpose**: Routes, cities, distances, aircraft models, airlines  
**Key Models**:
- `Pays`: Countries
- `Ville`: Cities (with hub capability)
- `Trajet`: Routes/Paths
- `DistanceEntreDeuxVilles`: Distances between cities
- `Player`: Game players
- `Entreprise`: Base enterprise (multi-table inheritance)
- `CompagnieAerienne`: Airline companies (extends Entreprise)
- `Banque`: Banks (extends Entreprise)
- `Fabricant`: Aircraft manufacturers
- `modeleAvion`: Aircraft models
- `Avion`: Individual aircraft
- `Hub`: Airline headquarters/hubs
- `LigneAerienne`: Airline routes with aircraft assignments

**Design Patterns**:
- Multi-table inheritance: `Entreprise` -> `CompagnieAerienne`/`Banque`
- ForeignKey reverse relations with `related_name` for easy traversal
- ManyToMany for route segments: `Trajet.etapes` -> `DistanceEntreDeuxVilles`

#### 2. `employe/` - Employee Management
**Status**: Under development (placeholder app)

#### 3. `gmax_km/` - Distance/KM handling
**Purpose**: Utilities for distance calculations  
**Features**: Custom context processor `version_renderer`

### Data Files

#### Fixtures
- `aerial/fixtures/complet_v2.json` - Base data (countries, cities, distances, routes, players, manufacturers, aircraft models)
- `aerial/fixtures/test_companies_aeriennes3.json` - Test data with airline companies

## Django ORM Quirks & Gotchas

### RelatedManager Iteration
```python
# NO - RelatedManager not directly iterable
for enterprise in player.entreprises:
    print(enterprise.nom)

# YES - Use .all()
for enterprise in player.entreprises.all():
    print(enterprise.nom)

# Company airplane access
company = CompagnieAerienne.objects.get(pk=1)
for airplane in company.avions.all():  # Need .all()
    print(airplane.nom_court)
```

### Indexing QuerySets
```python
# NO - Cannot subscript RelatedManager directly
player.entreprises[0].nom

# YES - Use .all() first
player.entreprises.all()[0].nom
```

### Filtering Foreign Keys
```python
# Correct syntax: use __pk or _id
Avion.objects.filter(modele__pk=1)
Avion.objects.filter(modele_id=1)

# Wrong syntax:
# Avion.objects.filter(modele=modeleAvion__pk=1)  # ✗
```

### First/Last Access
```python
# Correct: use parentheses (it's a method)
player.entreprises.first().nom

# Wrong: no parentheses
# player.entreprises.first.nom  # ✗
```

## Multi-Table Inheritance Notes

The `Entreprise` model uses Django's multi-table inheritance:
- Base class: `Entreprise` (contains shared fields like nom, abbreviation, proprietaire, cash)
- Child classes: `CompagnieAerienne`, `Banque`
- Each child auto-creates implicit OneToOneField to parent (`entreprise_ptr`)
- Access: Use `CompagnieAerienne.objects.get()` directly; Django handles the JOIN

**Migration caveat**: Adding a non-nullable field to child class may require default values or nullable fields initially.

## Database Schema

### Key Relationships
```
Player (1) ──→ (M) Entreprise ──→ (1) Pays [français/congolais]
                 ├─→ CompagnieAerienne
                 └─→ Banque

Entreprise (1) ──→ (M) Hub (1) ──→ Ville
Hub (1) ──→ (M) LigneAerienne (1) ──→ Trajet

LigneAerienne (M) ──→ (M) Avion

Avion (M) ──→ (1) CompagnieAerienne
Avion (M) ──→ (1) modeleAvion
modeleAvion (M) ──→ (1) Fabricant

Trajet (M) ──→ (M) DistanceEntreDeuxVilles
DistanceEntreDeuxVilles (2x M) ──→ (1) Ville
```

## Admin Credentials
- **Username**: admin
- **Password**: admin
- **Access**: http://localhost:8000/admin

## File Language Notes
- Models, comments, and fixtures use **French**: `nom`, `abbreviation`, `prenom`, `peut_etre_hub`, `km_parcourus`
- Follow same conventions when adding fields
- Maintain French in docstrings when describing business logic

## Future Development Areas

- [ ] CompagnieAerienne operations (full CRUD)
- [ ] Avion fleet management
- [ ] LigneAerienne scheduling
- [ ] employe app completion
- [ ] Game mechanics (money, operations, maintenance)

## Common Error Solutions

| Error | Cause | Fix |
|-------|-------|-----|
| `'RelatedManager' object is not iterable` | Trying to iterate on RelatedManager directly | Add `.all()` before loop |
| `'RelatedManager' object is not subscriptable` | Trying to index RelatedManager | Use `.all()[n]` |
| `FieldDoesNotExist: has no field named 'X'` | Model field name mismatch (especially after refactoring) | Check field definition in models.py |
| Migration conflicts with ForeignKey in inheritance | Adding non-nullable field to inherited model | Use `null=True, blank=True` or provide default |
