# 🧠 Health-IA-ETL – Pipeline de Données HealthAI Coach

**Pipeline ETL (Extract, Transform, Load)** de la plateforme HealthAI Coach, développé en **Python**. Ce service prend en charge l'extraction de fichiers (CSV, JSON et XLSX), leur transformation et leur chargement dans la base de données.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Google Drive](https://img.shields.io/badge/Google_Drive_API-4285F4?logo=googledrive&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

---

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Architecture](#architecture)
- [Stack technologique](#stack-technologique)
- [Logique ETL](#logique-etl)
- [Installation et Déploiement](#installation-et-déploiement)
- [Configuration Google Drive](#configuration-google-drive)
- [Initialisation du service Google Drive](#initialisation-du-service-google-drive)
- [Troubleshooting](#troubleshooting)
- [Documentation supplémentaire](#documentation-supplémentaire)

---

## Vue d'ensemble

Cette version du pipeline ETL permet l’import et le traitement automatisé des données de santé, avec intégration Google Drive pour la récupération automatique des fichiers.

Il prend en entrée des fichiers **CSV, JSON et XLSX**, les nettoie, les formate, et les envoie vers une base de données.

**Point d'entrée recommandé** :  
Le repository [Health-IA-Workspace](https://github.com/GroupMSPR/Health-IA-Workspace) qui orchestre l'ensemble du projet.

---

## Architecture

### Structure du projet

```text
Health-IA-ETL/
├── handlers/                    # Gestionnaires de traitement de fichiers et DB
│   ├── csvHandler.py            # Traitement des fichiers CSV
│   ├── dbHandler.py             # Connexion et insertion en Base de Données
│   ├── excelHandler.py          # Traitement des fichiers Excel (.xlsx)
│   └── jsonHandler.py           # Traitement des fichiers JSON
├── utils/                       # Outils et utilitaires
│   ├── dataframeFormatter.py    # Nettoyage et formatage des données (Pandas)
│   ├── driveHelper.py           # Interactions avec l'API Google Drive
│   └── fileManager.py           # Gestion des fichiers téléchargés et archivage
├── .env.example                 # Exemple de variables d'environnement
├── Aptfile                      # Dépendances système Linux
├── config.py                    # Configuration globale de l'ETL
├── docker-compose.yml           # Orchestration Docker
├── Dockerfile                   # Fichier de construction de l'image Docker
├── file-format.txt              # Documentation sur les formats de données attendus
├── main.py                      # Point d'entrée principal du script ETL
└── requirements.txt             # Dépendances Python (pip)
```

---

### Diagramme de flux

```text
Google Drive (ToImport)
    ↓ (API Drive)
Téléchargement local (fileManager)
    ↓
Détection du format (handlers : CSV, JSON, Excel)
    ↓
Transformation & Nettoyage (dataframeFormatter)
    ↓
Insertion Base de Données (dbHandler)
    ↓
Google Drive (Déplacement vers Archive / Error + Log)
```

---

## Stack technologique

### Données & Scripting

- **Langage** : Python 3
- **Manipulation de données** : Pandas
- **Formats supportés** : `.csv`, `.json`, `.xlsx`

### Cloud & API

- **Fournisseur de fichiers** : Google Drive API (OAuth 2.0)

### DevOps

- **Containerization** : Docker
- **Orchestration** : Docker Compose
- **Dépendances système** : Aptfile

---

## 📂 Logique ETL

L'arborescence Google Drive permet d'organiser les flux.  
Les fichiers à traiter doivent être déposés dans :

```text
ETL/ToImport/
```

Après traitement :

- ✅ `ETL/Archive/` → fichiers importés avec succès (nom enrichi avec date/heure)
- ❌ `ETL/Error/` → fichiers ayant rencontré une erreur
- 📝 `ETL/Log/` → détails des erreurs rencontrées lors du processus

---

## 📥 Installation et Déploiement

### Prérequis

- Python 3.10+ (pour exécution locale)
- Docker Desktop (recommandé)
- Un compte Google Cloud Console (pour l'API Drive)

---

### 1. Préparation de l'environnement

#### Cloner le projet

```bash
git clone https://github.com/GroupMSPR/Health-IA-ETL.git
cd Health-IA-ETL
```

---

#### Créer l’arborescence des dossiers dans Google Drive

```text
ETL/
├─ Log/
├─ Archive/
├─ ToImport/
└─ Error/
```

---

#### Mettre en place le fichier `.env`

```bash
cp .env.example .env
```

Remplir les variables avec vos informations (voir `.env.example`).

Optionnel : vous pouvez convertir le token Drive en Base64 et le mettre directement dans la variable :

```env
GOOGLE_TOKEN_PICKLE=
```

---

### 2. Déploiement (Au choix)

#### Option A : Avec Docker (Recommandé)

```bash
docker compose up -d
```

---

#### Option B : En local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'ETL
python main.py
```

---

## 🔑 Configuration Google Drive

Pour que l'ETL puisse interagir avec Google Drive, vous devez configurer des identifiants API :

1. Aller sur **Google Cloud Console → Credentials**
2. Créer un **OAuth 2.0 Client ID**
3. Ajouter un **Client Secret** et télécharger le fichier JSON fourni
4. Renommer ce fichier en :

```text
credentials.json
```

5. Placer ce fichier à la racine du projet

---

## ⚙️ Initialisation du service Google Drive

Pour la première connexion (si vous n'utilisez pas la variable d'environnement Base64) :

1. Décommenter le code dans la fonction `get_drive_service`
   du fichier :

```text
utils/driveHelper.py
```

2. Lancer le projet :

```bash
python main.py
```

3. Une fenêtre Google s’ouvrira pour autoriser votre compte

Cela générera automatiquement un fichier :

```text
token.pickle
```

à la racine du projet afin d’authentifier les futures connexions sans intervention manuelle.

Vous pouvez ensuite :

- laisser le code décommenté
- ou le remettre commenté selon votre stratégie de renouvellement du token

---

## Troubleshooting

### Erreur "Token has been expired or revoked"

#### Problème

Le fichier `token.pickle` n'est plus valide.

#### Solution

1. Supprimez le fichier `token.pickle`
2. Décommentez la fonction dans `driveHelper.py`
3. Relancez le script en local :

```bash
python main.py
```

4. Reconnectez votre compte Google via le navigateur

---

### Le script ne trouve pas le dossier "ToImport"

#### Problème

Les identifiants de dossiers (Folder IDs) Google Drive ne correspondent pas.

#### Solution

Assurez-vous que :

- les variables d'environnement
- ou la configuration dans `config.py`

contiennent bien les **ID exacts** des dossiers Google Drive (présents dans l’URL du navigateur) et non leurs noms textuels.

---

### Problème de connexion à la base de données

#### Problème

L'ETL n'arrive pas à insérer les données.

#### Solution

Vérifiez :

- les variables d'environnement de base de données dans le `.env`
- que le Backend est bien lancé
- que les conteneurs Docker sont sur le même réseau si applicable

---

## 📚 Documentation supplémentaire

- [Python Documentation](https://docs.python.org/3/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Google Drive API Documentation](https://developers.google.com/drive)
- [Docker Documentation](https://docs.docker.com/)

---

## 👥 Équipe

Développeurs MSPR :

- Ilan
- Anthony
- Diana

---

## 🔗 Liens

- **Organization** : GroupMSPR
- **Workspace** : Health-IA-Workspace
- **Backend** : Health-IA-Backend
- **Frontend** : Health-IA-Frontend
- **FastAPI** : Health-IA-FastAPI
- **Grafana** : Health-IA-Grafana

---

Dernière mise à jour : 28 mai 2026
