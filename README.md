# Forensic Data Visualization — iPhone Activity Timeline

Ce dépôt propose un script d'analyse et une représentation graphique interactive des données d'extraction téléphonique issues de pièces à conviction rendues publiques dans le cadre d'une procédure judiciaire.

L'objectif principal de ce projet est de transformer un journal d'événements bruts (logs système, messages, données de santé, navigation) en une chronologie lisible, exploitable et synthétique.

---

## 📌 Méthodologie & Traitement des Données

1. **Normalisation & Catégorisation** : Les entrées brutes de l'extraction ont été nettoyées et regroupées en **7 ensembles fonctionnels** (Logs système, Réseau Wi-Fi, Capteurs Santé, Navigation Web, Photos & Géolocalisation, Messages, Appels & Agenda) afin d'offrir une vision thématique claire.
2. **Combinaison Temporelle** : Alignement de l'ensemble des données sur un axe temporel continu pour révéler les séquences d'activité, les simultanéités et les phases d'inactivité.
3. **Restitution Interactive (Plotly)** : Génération d'une interface web autonome permettant une exploration dynamique.

---

## 📊 Fonctionnalités de la Timeline Interactive

La visualisation générée (`timeline.html`) offre plusieurs leviers d'analyse :

* **Survol d'éléments (Tooltips)** : Affiche instantanément les détails contextuels de chaque événement au passage de la souris (nature de l'entrée, participants, direction, contenu).
* **Filtrage dynamique** : Possibilité de masquer ou d'isoler des groupes d'activités spécifiques en cliquant sur la légende.
* **Navigation temporelle** : Outils de zoom, dézoom et sélection de fenêtres horaires ciblées pour étudier des intervalles précis.

---

## 🚀 Utilisation

### Prérequis
* Python 3.8+
* `pandas`
* `plotly`
* `openpyxl`

### Exécution du script
```bash
python timeline_forensic.py nom_du_fichier.xlsx
