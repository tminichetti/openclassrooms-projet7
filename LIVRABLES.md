Livrables

L’API de prédiction du score, qui expose le “Modèle sur mesure avancé”, déployée sur un service Cloud , qui recevra en entrée un tweet et retournera le sentiment associé au tweet prédit par le modèle (lien vers l’API sur le Cloud).
L’ensemble des scripts pour réaliser les trois approches (classique, modèle sur mesure avancé, modèle avancé BERT).
Ce livrable intégrera la gestion des expérimentations avec l’outil MLFlow (tracking des expérimentations, enregistrement des modèles)
Un dossier, géré via un outil de versioning de code contenant :
Le ou les notebooks des modélisations, intégrant via MLFlow le tracking d’expérimentations et le stockage centralisé des modèles
Le code permettant de déployer le modèle sous forme d'API
Pour l’API, un fichier introductif permettant de comprendre l'objectif du projet et le découpage des dossiers, et un fichier listant les packages utilisés seront présents dans le dossier
Une interface de test de l’API (notebook ou application Streamlit), exécutée en local, qui permet la saisie d’un tweet, affiche la prédiction, demande une validation à l’utilisateur de la pertinence de la prédiction, et envoie une trace au service Application Insight en cas de non validation
Un article de blog de 1500 à 2000 mots environ (+ copies écrans) contenant :
Une présentation synthétique et une comparaison des trois approches (“Modèle sur mesure simple” et “Modèle sur mesure avancé”, “Modèle avancé BERT”)
La démarche orientée MLOps mise en oeuvre :
principes MLOps,
étapes mises en oeuvre : tracking, stockage model, gestion version, tests unitaires, déploiement,
y compris le suivi de la performance en production : traces et alertes sur Azure Application Insight, ainsi qu’une présentation d’une démarche qui pourrait être mise en oeuvre pour l’analyse de ces statistiques et l’amélioration du modèle dans le temps.
Un support de présentation (type PowerPoint) de votre démarche méthodologique, des résultats des différents modèles élaborés via la mise en oeuvre d’expérimentations MLFlow et de sa visualisation via l’UI (User Interface) de MLFlow, et de la mise en production d’un modèle avancé. Il sera également formalisé :
Des copies écran des commits, du dossier Github (+ lien vers ce dossier)de l’exécution des tests unitaires, qui sont les preuves qu’un pipeline de déploiement continu a permis de déployer l’API,
Des copies écran du suivi de performance sur Azure Application Insight et du déclenchement d’alerte, qui sont les preuves d’un suivi de la performance du modèle en production
