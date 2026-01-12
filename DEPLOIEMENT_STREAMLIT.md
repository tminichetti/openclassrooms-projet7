# Guide de Déploiement Streamlit Cloud

Ce guide explique comment déployer l'interface Streamlit sur Streamlit Cloud (gratuit).

---

## 🚀 Étapes de Déploiement

### 1. Préparer le Repository GitHub

✅ **Vérifier que ces fichiers sont présents** :
- `api/streamlit_app.py` ✓
- `api/requirements-streamlit.txt` ✓
- `.streamlit/config.toml` ✓

✅ **Commit et push sur GitHub** :

```bash
git add .
git commit -m "Add Streamlit interface with user feedback"
git push origin main
```

### 2. Créer l'Application sur Streamlit Cloud

1. **Aller sur** [share.streamlit.io](https://share.streamlit.io)
2. **Se connecter** avec ton compte GitHub
3. **Cliquer sur** "New app"
4. **Remplir le formulaire** :
   - **Repository** : `ton-username/openclassrooms-projet7`
   - **Branch** : `main`
   - **Main file path** : `api/streamlit_app.py`
   - **App URL** : Choisir un nom (ex: `airparadis-sentiment`)

5. **Cliquer sur** "Advanced settings..."

### 3. Configurer les Secrets

Dans "Advanced settings" → Onglet "Secrets", ajouter :

```toml
# URL de ton API Heroku (remplacer par la tienne)
API_URL = "https://ton-api.herokuapp.com"

# Application Insights (optionnel - pour le monitoring)
# APPINSIGHTS_CONNECTION_STRING = "InstrumentationKey=xxx;..."
```

**Important** : Remplace `https://ton-api.herokuapp.com` par l'URL réelle de ton API déployée sur Heroku.

### 4. Déployer !

Cliquer sur **"Deploy!"**

L'app sera disponible sur : `https://ton-nom-app.streamlit.app`

⏱️ Le déploiement prend 2-3 minutes.

---

## 🔧 Configuration Post-Déploiement

### Vérifier que tout fonctionne

1. **Accéder à l'URL de l'app**
2. **Dans la sidebar**, vérifier :
   - ✅ Status API : "API en ligne"
   - ✅ Modèle chargé
3. **Tester une prédiction** :
   - Entrer un tweet
   - Cliquer sur "Analyser"
   - Vérifier que le résultat s'affiche
4. **Tester le feedback** :
   - Cliquer sur "Prédiction incorrecte"
   - Corriger le sentiment
   - Vérifier le message de confirmation

### Si l'API n'est pas accessible

**Erreur** : "❌ API inaccessible"

**Solutions** :
1. Vérifier que l'API Heroku est bien déployée
2. Vérifier l'URL dans les secrets Streamlit Cloud
3. Vérifier que l'API accepte les requêtes CORS (déjà configuré dans `app.py`)

Pour modifier les secrets :
1. Dans Streamlit Cloud, aller dans ton app
2. Menu hamburger → **"Settings"**
3. Onglet **"Secrets"**
4. Modifier `API_URL`
5. Sauvegarder → L'app redémarre automatiquement

---

## 🔄 Mises à Jour

### Redéploiement automatique

Streamlit Cloud redéploie automatiquement à chaque push sur GitHub :

```bash
# Faire des modifications
git add .
git commit -m "Update Streamlit interface"
git push origin main

# L'app se redéploie automatiquement (1-2 min)
```

### Redéploiement manuel

1. Aller dans Streamlit Cloud
2. Cliquer sur les 3 points → **"Reboot app"**

---

## 📊 Monitoring

### Logs de l'application

Pour voir les logs en temps réel :
1. Dans Streamlit Cloud, ouvrir ton app
2. Menu hamburger → **"Manage app"**
3. Onglet **"Logs"**

Utile pour débugger !

### Analytics

Streamlit Cloud fournit des analytics de base :
- Nombre de visiteurs
- Nombre de sessions
- Durée moyenne

Accessible dans **"Manage app"** → **"Analytics"**

---

## 🎓 Pour le Livrable OpenClassrooms

### URLs à fournir

```
API REST (Heroku) : https://ton-api.herokuapp.com
Documentation API : https://ton-api.herokuapp.com/docs
Interface Streamlit : https://ton-app.streamlit.app
```

### Captures d'écran à inclure

1. **Page d'accueil Streamlit** avec un tweet analysé
2. **Section de validation** avec les boutons
3. **Message de confirmation** après feedback
4. **Mode batch** avec graphiques
5. **Paramètres Streamlit Cloud** montrant l'URL et la config

### Démonstration pour la soutenance

**Scénario suggéré** :

1. **Montrer l'API** (`/docs`) :
   - "Voici la documentation Swagger de l'API"
   - Tester un endpoint directement

2. **Montrer Streamlit** :
   - "Voici l'interface conviviale pour les équipes marketing"
   - Taper : "This flight was terrible, lost my luggage!"
   - Analyser → Voir la prédiction
   - Si incorrect, cliquer sur "Prédiction incorrecte"
   - Corriger → Voir le message Application Insights

3. **Montrer le mode batch** :
   - Upload d'un CSV avec 10 tweets
   - Voir les statistiques et graphiques
   - Télécharger les résultats

4. **Expliquer l'architecture** :
   - "L'interface Streamlit appelle l'API REST"
   - "Les feedbacks sont envoyés à Azure pour amélioration continue"

---

## 🔒 Sécurité

### Fichiers à NE PAS commit

Ajouter au `.gitignore` :

```
# Secrets Streamlit
.streamlit/secrets.toml

# Fichiers locaux
.env
*.env
```

### Bonnes pratiques

✅ Utiliser les secrets Streamlit Cloud pour les clés
✅ Ne jamais commit `secrets.toml`
✅ Utiliser des variables d'environnement
✅ Limiter les requêtes (déjà fait : max 100 tweets batch)

---

## 🆘 Troubleshooting

### Erreur : "ModuleNotFoundError"

**Cause** : Dépendance manquante

**Solution** :
1. Vérifier `api/requirements-streamlit.txt`
2. Ajouter la dépendance manquante
3. Commit et push
4. Streamlit redéploie automatiquement

### Erreur : "Can't connect to API"

**Cause** : URL de l'API incorrecte ou API down

**Solution** :
1. Tester l'API directement : `curl https://ton-api.herokuapp.com/health`
2. Si OK, vérifier les secrets Streamlit Cloud
3. Si KO, vérifier le déploiement Heroku de l'API

### L'app est lente

**Causes possibles** :
1. API Heroku en mode "sleep" (gratuit)
2. Requêtes batch trop volumineuses
3. Pas de caching

**Solutions** :
1. Attendre que l'API se réveille (30 sec)
2. Limiter à 50 tweets par batch
3. Ajouter du caching dans Streamlit (optionnel)

### "App is over quota"

**Cause** : Streamlit Cloud gratuit a des limites (rare)

**Solution** : Attendre que le quota se réinitialise (mensuel)

---

## 📚 Ressources

- [Documentation Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Deploying apps](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Secrets management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

---

## ✅ Checklist Finale

Avant la soutenance, vérifier :

- [ ] API Heroku déployée et accessible
- [ ] Streamlit Cloud déployé et accessible
- [ ] Les deux communiquent correctement
- [ ] Le feedback fonctionne (au moins en mode local)
- [ ] Screenshots prêts
- [ ] URLs documentées
- [ ] Démonstration testée

**Tout est prêt pour la soutenance ! 🎉**
