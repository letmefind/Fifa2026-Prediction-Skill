# Multilingual README Help

This document provides the same practical help as the main README in 10 languages. Commands, paths, and endpoint names stay in English because they must be copied exactly.

## 1. فارسی

### معرفی

این پروژه یک موتور پیش‌بینی جام جهانی ۲۰۲۶ است. برای پیش‌بینی مسابقه، شبیه‌سازی تورنمنت، محاسبه گل‌های مورد انتظار، ساخت ورودی برای Claude/GPT و تحلیل ارزش شرط‌بندی استفاده می‌شود.

### قابلیت‌ها

- دریافت داده از CSV و اتصال آماده به StatsBomb، FiveThirtyEight SPI و API-Football
- مدل ELO با K-factor و امتیاز میزبانی قابل تنظیم
- مدل قدرت حمله/دفاع با گل و xG
- مدل Poisson همراه با Dixon-Coles برای بهتر شدن احتمال مساوی و نتایج کم‌گل
- شبیه‌سازی جام جهانی ۴۸ تیمی
- API با FastAPI، CLI و داشبورد وب
- محاسبه EV برای Polymarket و سایت‌های مشابه

### نصب

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### استفاده از CLI

```bash
python -m cli.main predict-match Brazil France
python -m cli.main predict-match Brazil France --json-output
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.50 2.38
```

### داشبورد و API

```bash
uvicorn api.main:app --reload
```

داشبورد را باز کنید:

```text
http://127.0.0.1:8000/
```

Endpointهای مهم:

- `GET /`
- `GET /teams`
- `POST /predict_match`
- `POST /simulate`
- `GET /team/{name}`
- `GET /tournament/probabilities`

### Claude Skill

مهارت Claude در این مسیر است:

```text
claude-skill/fifa2026-prediction/
```

این مهارت به Claude یاد می‌دهد چطور مدل را اجرا کند، تعداد شبیه‌سازی را از کاربر بپرسد، نتایج جدید را بررسی کند، و خروجی قابل فهم بدهد.

### شرط‌بندی و Polymarket

برای Polymarket اگر قیمت Yes برابر `0.42` باشد:

```text
Market probability = 42%
Decimal odds = 1 / 0.42 = 2.38
```

اگر مدل احتمال واقعی را `50%` بداند:

```bash
python -m cli.main betting-edge 0.50 2.38
```

EV مثبت یعنی قیمت ممکن است ارزش داشته باشد، اما کارمزد، نقدشوندگی، ترکیب تیم و ریسک مدل را بررسی کنید.

### داده‌های جدید

فایل‌های داده:

- `data/sample_matches.csv`
- `data/sample_team_ratings.csv`
- `data/sample_xg.csv`
- `data/latest_results.csv`

برای API-Football:

```bash
cp .env.example .env
# API_FOOTBALL_KEY را در .env قرار دهید
python -m cli.main refresh-latest-data
python -m cli.main latest-data-status
```

اگر مسابقه قبلاً انجام شده باشد، برنامه نتیجه واقعی را نشان می‌دهد و پیش‌بینی را به عنوان پیش‌بینی بازی مجدد نمایش می‌دهد.

### تنظیمات و تست

تنظیمات در `config/default.yaml` است. اجرای تست:

```bash
pytest
```

### هشدار

این نرم‌افزار سود شرط‌بندی را تضمین نمی‌کند. همیشه مصدومیت‌ها، ترکیب تیم، اخبار، ضرایب بازار و نقدشوندگی را بررسی کنید.

---

## 2. العربية

### المقدمة

هذا المشروع هو محرك توقعات لكأس العالم 2026. يستخدم لتوقع المباريات، محاكاة البطولة، حساب الأهداف المتوقعة، تجهيز مدخلات Claude/GPT، وتحليل القيمة المتوقعة للرهانات.

### الميزات

- إدخال بيانات من CSV واتصال جاهز بـ StatsBomb و FiveThirtyEight SPI و API-Football
- نموذج ELO مع K-factor وأفضلية ملعب قابلة للتعديل
- نموذج قوة هجومية ودفاعية باستخدام الأهداف و xG
- نموذج Poisson مع تعديل Dixon-Coles للنتائج قليلة الأهداف والتعادلات
- محاكاة بطولة من 48 فريقاً
- FastAPI و CLI ولوحة ويب
- حساب EV لـ Polymarket والأسواق المشابهة

### التثبيت

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### استخدام CLI

```bash
python -m cli.main predict-match Brazil France
python -m cli.main predict-match Brazil France --json-output
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.50 2.38
```

### لوحة التحكم و API

```bash
uvicorn api.main:app --reload
```

افتح:

```text
http://127.0.0.1:8000/
```

أهم endpoints:

- `GET /`
- `GET /teams`
- `POST /predict_match`
- `POST /simulate`
- `GET /team/{name}`
- `GET /tournament/probabilities`

### Claude Skill

مجلد المهارة:

```text
claude-skill/fifa2026-prediction/
```

تساعد Claude على تشغيل النموذج، سؤال المستخدم عن عدد المحاكاة، فحص أحدث النتائج، وتقديم شرح واضح.

### الرهانات و Polymarket

إذا كان سعر Yes في Polymarket هو `0.42`:

```text
Market probability = 42%
Decimal odds = 1 / 0.42 = 2.38
```

إذا كان احتمال النموذج `50%`:

```bash
python -m cli.main betting-edge 0.50 2.38
```

EV موجب يعني أن السعر قد يكون جيداً، لكن يجب فحص الرسوم والسيولة والتشكيلة ومخاطر النموذج.

### البيانات الحديثة

ملفات البيانات:

- `data/sample_matches.csv`
- `data/sample_team_ratings.csv`
- `data/sample_xg.csv`
- `data/latest_results.csv`

لـ API-Football:

```bash
cp .env.example .env
# ضع API_FOOTBALL_KEY في .env
python -m cli.main refresh-latest-data
python -m cli.main latest-data-status
```

إذا كانت المباراة قد لعبت بالفعل، يعرض التطبيق النتيجة المعروفة ويصنف التوقع كتوقع لمباراة إعادة مستقبلية.

### الإعدادات والاختبار

الإعدادات في `config/default.yaml`. تشغيل الاختبارات:

```bash
pytest
```

### تنبيه

هذا البرنامج لا يضمن الربح. تحقق دائماً من الإصابات، التشكيلات، الأخبار، الأسعار والسيولة.

---

## 3. Español

### Introducción

Este proyecto es un motor de predicción para la Copa Mundial FIFA 2026. Sirve para predecir partidos, simular torneos, calcular goles esperados, preparar prompts para Claude/GPT y analizar valor esperado de apuestas.

### Funciones

- Ingesta CSV y adaptadores listos para StatsBomb, FiveThirtyEight SPI y API-Football
- Modelo ELO con K-factor y ventaja local configurables
- Modelo de fuerza ofensiva/defensiva con goles y xG
- Modelo Poisson con ajuste Dixon-Coles para empates y marcadores bajos
- Simulación de torneo de 48 equipos
- FastAPI, CLI y dashboard web
- Cálculo de EV para Polymarket y mercados similares

### Instalación

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Uso CLI

```bash
python -m cli.main predict-match Brazil France
python -m cli.main predict-match Brazil France --json-output
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.50 2.38
```

### Dashboard y API

```bash
uvicorn api.main:app --reload
```

Abre:

```text
http://127.0.0.1:8000/
```

Endpoints principales:

- `GET /`
- `GET /teams`
- `POST /predict_match`
- `POST /simulate`
- `GET /team/{name}`
- `GET /tournament/probabilities`

### Claude Skill

Carpeta:

```text
claude-skill/fifa2026-prediction/
```

La skill enseña a Claude a ejecutar el modelo, preguntar el número de simulaciones, revisar resultados recientes y explicar la predicción.

### Apuestas y Polymarket

Si el precio Yes en Polymarket es `0.42`:

```text
Market probability = 42%
Decimal odds = 1 / 0.42 = 2.38
```

Si el modelo estima `50%`:

```bash
python -m cli.main betting-edge 0.50 2.38
```

EV positivo puede indicar valor, antes de comisiones, liquidez y error del modelo.

### Datos recientes

Archivos:

- `data/sample_matches.csv`
- `data/sample_team_ratings.csv`
- `data/sample_xg.csv`
- `data/latest_results.csv`

Para API-Football:

```bash
cp .env.example .env
# agrega API_FOOTBALL_KEY en .env
python -m cli.main refresh-latest-data
python -m cli.main latest-data-status
```

Si el partido ya se jugó, la app muestra el resultado conocido y marca la predicción como pronóstico de revancha futura.

### Configuración y pruebas

Configura en `config/default.yaml`. Ejecuta:

```bash
pytest
```

### Nota

El software no garantiza ganancias. Revisa lesiones, alineaciones, noticias, cuotas y liquidez.

---

## 4. Français

### Introduction

Ce projet est un moteur de prédiction pour la Coupe du Monde FIFA 2026. Il prédit les matchs, simule le tournoi, calcule les expected goals, prépare des prompts Claude/GPT et analyse la valeur attendue des paris.

### Fonctionnalités

- Ingestion CSV et adaptateurs StatsBomb, FiveThirtyEight SPI et API-Football
- Modèle ELO avec K-factor et avantage domicile configurables
- Forces offensives/défensives avec buts et xG
- Modèle Poisson avec ajustement Dixon-Coles
- Simulation d’un tournoi à 48 équipes
- FastAPI, CLI et dashboard web
- Calcul EV pour Polymarket et marchés similaires

### Installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Utilisation CLI

```bash
python -m cli.main predict-match Brazil France
python -m cli.main predict-match Brazil France --json-output
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.50 2.38
```

### Dashboard et API

```bash
uvicorn api.main:app --reload
```

Ouvrez:

```text
http://127.0.0.1:8000/
```

Endpoints:

- `GET /`
- `GET /teams`
- `POST /predict_match`
- `POST /simulate`
- `GET /team/{name}`
- `GET /tournament/probabilities`

### Claude Skill

Chemin:

```text
claude-skill/fifa2026-prediction/
```

La skill indique à Claude comment exécuter le modèle, demander le nombre de simulations, vérifier les scores récents et expliquer les résultats.

### Paris et Polymarket

Prix Yes Polymarket `0.42`:

```text
Market probability = 42%
Decimal odds = 1 / 0.42 = 2.38
```

Si le modèle donne `50%`:

```bash
python -m cli.main betting-edge 0.50 2.38
```

EV positif peut indiquer de la valeur, avant frais, liquidité et incertitude.

### Données récentes

Fichiers:

- `data/sample_matches.csv`
- `data/sample_team_ratings.csv`
- `data/sample_xg.csv`
- `data/latest_results.csv`

API-Football:

```bash
cp .env.example .env
# ajoutez API_FOOTBALL_KEY dans .env
python -m cli.main refresh-latest-data
python -m cli.main latest-data-status
```

Si un match a déjà été joué, l’application affiche le score connu puis indique que la prédiction est une prévision de revanche future.

### Configuration et tests

Paramètres dans `config/default.yaml`. Tests:

```bash
pytest
```

### Note

Ce logiciel ne garantit pas de profits. Vérifiez blessures, compositions, nouvelles, cotes et liquidité.

---

## 5. Deutsch

### Einführung

Dieses Projekt ist eine Vorhersage-Engine für die FIFA-Weltmeisterschaft 2026. Es prognostiziert Spiele, simuliert das Turnier, berechnet Expected Goals, erstellt Claude/GPT-Prompts und analysiert Wett-Expected-Value.

### Funktionen

- CSV-Daten und Adapter für StatsBomb, FiveThirtyEight SPI und API-Football
- ELO-Modell mit konfigurierbarem K-factor und Heimvorteil
- Angriffs- und Defensivstärken aus Toren und xG
- Poisson-Modell mit Dixon-Coles-Anpassung
- Simulation eines 48-Team-Turniers
- FastAPI, CLI und Web-Dashboard
- EV-Berechnung für Polymarket und ähnliche Märkte

### Installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### CLI-Nutzung

```bash
python -m cli.main predict-match Brazil France
python -m cli.main predict-match Brazil France --json-output
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.50 2.38
```

### Dashboard und API

```bash
uvicorn api.main:app --reload
```

Öffnen:

```text
http://127.0.0.1:8000/
```

Endpoints:

- `GET /`
- `GET /teams`
- `POST /predict_match`
- `POST /simulate`
- `GET /team/{name}`
- `GET /tournament/probabilities`

### Claude Skill

Pfad:

```text
claude-skill/fifa2026-prediction/
```

Die Skill zeigt Claude, wie das Modell ausgeführt wird, wie viele Simulationen gefragt werden, wie aktuelle Ergebnisse geprüft werden und wie Ergebnisse erklärt werden.

### Wetten und Polymarket

Polymarket Yes-Preis `0.42`:

```text
Market probability = 42%
Decimal odds = 1 / 0.42 = 2.38
```

Wenn das Modell `50%` schätzt:

```bash
python -m cli.main betting-edge 0.50 2.38
```

Positiver EV kann Wert anzeigen, aber Gebühren, Liquidität und Modellfehler beachten.

### Aktuelle Daten

Dateien:

- `data/sample_matches.csv`
- `data/sample_team_ratings.csv`
- `data/sample_xg.csv`
- `data/latest_results.csv`

API-Football:

```bash
cp .env.example .env
# API_FOOTBALL_KEY in .env eintragen
python -m cli.main refresh-latest-data
python -m cli.main latest-data-status
```

Wenn ein Spiel bereits gespielt wurde, zeigt die App das bekannte Ergebnis und markiert die Prognose als zukünftige Revanche-Prognose.

### Konfiguration und Tests

Konfiguration in `config/default.yaml`. Tests:

```bash
pytest
```

### Hinweis

Das Modell garantiert keinen Gewinn. Prüfe Verletzungen, Aufstellungen, Nachrichten, Quoten und Liquidität.

---

## 6. Português

### Introdução

Este projeto é um motor de previsão para a Copa do Mundo FIFA 2026. Ele prevê jogos, simula o torneio, calcula gols esperados, cria prompts para Claude/GPT e analisa valor esperado de apostas.

### Recursos

- Dados CSV e adaptadores para StatsBomb, FiveThirtyEight SPI e API-Football
- Modelo ELO com K-factor e vantagem de mando configuráveis
- Forças de ataque/defesa com gols e xG
- Modelo Poisson com ajuste Dixon-Coles
- Simulação de torneio com 48 seleções
- FastAPI, CLI e dashboard web
- EV para Polymarket e mercados similares

### Instalação

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Uso CLI

```bash
python -m cli.main predict-match Brazil France
python -m cli.main predict-match Brazil France --json-output
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.50 2.38
```

### Dashboard e API

```bash
uvicorn api.main:app --reload
```

Abra:

```text
http://127.0.0.1:8000/
```

Endpoints:

- `GET /`
- `GET /teams`
- `POST /predict_match`
- `POST /simulate`
- `GET /team/{name}`
- `GET /tournament/probabilities`

### Claude Skill

Caminho:

```text
claude-skill/fifa2026-prediction/
```

A skill ensina Claude a executar o modelo, perguntar o número de simulações, verificar resultados recentes e explicar previsões.

### Apostas e Polymarket

Preço Yes `0.42`:

```text
Market probability = 42%
Decimal odds = 1 / 0.42 = 2.38
```

Se o modelo estima `50%`:

```bash
python -m cli.main betting-edge 0.50 2.38
```

EV positivo pode indicar valor, antes de taxas, liquidez e erro do modelo.

### Dados recentes

Arquivos:

- `data/sample_matches.csv`
- `data/sample_team_ratings.csv`
- `data/sample_xg.csv`
- `data/latest_results.csv`

API-Football:

```bash
cp .env.example .env
# adicione API_FOOTBALL_KEY em .env
python -m cli.main refresh-latest-data
python -m cli.main latest-data-status
```

Se o jogo já aconteceu, o app mostra o placar conhecido e marca a previsão como previsão de revanche futura.

### Configuração e testes

Configuração em `config/default.yaml`. Testes:

```bash
pytest
```

### Nota

O modelo não garante lucro. Verifique lesões, escalações, notícias, odds e liquidez.

---

## 7. Italiano

### Introduzione

Questo progetto è un motore di previsione per la FIFA World Cup 2026. Predice partite, simula il torneo, calcola expected goals, crea prompt per Claude/GPT e analizza il valore atteso delle scommesse.

### Funzioni

- Dati CSV e adattatori per StatsBomb, FiveThirtyEight SPI e API-Football
- Modello ELO con K-factor e vantaggio casa configurabili
- Forze di attacco/difesa con gol e xG
- Modello Poisson con correzione Dixon-Coles
- Simulazione torneo a 48 squadre
- FastAPI, CLI e dashboard web
- EV per Polymarket e mercati simili

### Installazione

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Uso CLI

```bash
python -m cli.main predict-match Brazil France
python -m cli.main predict-match Brazil France --json-output
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.50 2.38
```

### Dashboard e API

```bash
uvicorn api.main:app --reload
```

Apri:

```text
http://127.0.0.1:8000/
```

Endpoints:

- `GET /`
- `GET /teams`
- `POST /predict_match`
- `POST /simulate`
- `GET /team/{name}`
- `GET /tournament/probabilities`

### Claude Skill

Percorso:

```text
claude-skill/fifa2026-prediction/
```

La skill insegna a Claude come eseguire il modello, chiedere il numero di simulazioni, verificare risultati recenti e spiegare le previsioni.

### Scommesse e Polymarket

Prezzo Yes `0.42`:

```text
Market probability = 42%
Decimal odds = 1 / 0.42 = 2.38
```

Se il modello stima `50%`:

```bash
python -m cli.main betting-edge 0.50 2.38
```

EV positivo può indicare valore, prima di commissioni, liquidità e incertezza.

### Dati recenti

File:

- `data/sample_matches.csv`
- `data/sample_team_ratings.csv`
- `data/sample_xg.csv`
- `data/latest_results.csv`

API-Football:

```bash
cp .env.example .env
# aggiungi API_FOOTBALL_KEY in .env
python -m cli.main refresh-latest-data
python -m cli.main latest-data-status
```

Se la partita è già stata giocata, l’app mostra il risultato noto e marca la previsione come previsione di rivincita futura.

### Configurazione e test

Configurazione in `config/default.yaml`. Test:

```bash
pytest
```

### Nota

Il modello non garantisce profitti. Controlla infortuni, formazioni, notizie, quote e liquidità.

---

## 8. Türkçe

### Giriş

Bu proje FIFA 2026 Dünya Kupası için bir tahmin motorudur. Maçları tahmin eder, turnuvayı simüle eder, expected goals hesaplar, Claude/GPT için prompt üretir ve bahis EV analizi yapar.

### Özellikler

- CSV verisi ve StatsBomb, FiveThirtyEight SPI, API-Football adaptörleri
- Ayarlanabilir K-factor ve ev sahibi avantajı olan ELO modeli
- Gol ve xG ile hücum/savunma gücü
- Dixon-Coles düzeltmeli Poisson modeli
- 48 takımlı turnuva simülasyonu
- FastAPI, CLI ve web dashboard
- Polymarket ve benzer marketler için EV

### Kurulum

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### CLI Kullanımı

```bash
python -m cli.main predict-match Brazil France
python -m cli.main predict-match Brazil France --json-output
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.50 2.38
```

### Dashboard ve API

```bash
uvicorn api.main:app --reload
```

Aç:

```text
http://127.0.0.1:8000/
```

Endpointler:

- `GET /`
- `GET /teams`
- `POST /predict_match`
- `POST /simulate`
- `GET /team/{name}`
- `GET /tournament/probabilities`

### Claude Skill

Yol:

```text
claude-skill/fifa2026-prediction/
```

Skill, Claude’a modeli çalıştırmayı, simülasyon sayısını sormayı, son skorları kontrol etmeyi ve tahmini açıklamayı öğretir.

### Bahis ve Polymarket

Yes fiyatı `0.42`:

```text
Market probability = 42%
Decimal odds = 1 / 0.42 = 2.38
```

Model `50%` diyorsa:

```bash
python -m cli.main betting-edge 0.50 2.38
```

Pozitif EV değer gösterebilir; komisyon, likidite ve model hatasını dikkate alın.

### Güncel veriler

Dosyalar:

- `data/sample_matches.csv`
- `data/sample_team_ratings.csv`
- `data/sample_xg.csv`
- `data/latest_results.csv`

API-Football:

```bash
cp .env.example .env
# API_FOOTBALL_KEY değerini .env içine ekleyin
python -m cli.main refresh-latest-data
python -m cli.main latest-data-status
```

Maç zaten oynandıysa, uygulama bilinen skoru gösterir ve tahmini gelecekteki rövanş tahmini olarak etiketler.

### Ayarlar ve test

Ayarlar `config/default.yaml` içindedir. Test:

```bash
pytest
```

### Not

Model kâr garantisi vermez. Sakatlıkları, kadroları, haberleri, oranları ve likiditeyi kontrol edin.

---

## 9. हिन्दी

### परिचय

यह FIFA World Cup 2026 के लिए prediction engine है। यह match prediction, tournament simulation, expected goals, Claude/GPT prompts और betting EV analysis करता है।

### Features

- CSV data और StatsBomb, FiveThirtyEight SPI, API-Football adapters
- configurable K-factor और home advantage वाला ELO model
- goals और xG से attack/defense strength
- Dixon-Coles adjustment वाला Poisson model
- 48-team tournament simulation
- FastAPI, CLI और web dashboard
- Polymarket और similar markets के लिए EV

### Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### CLI Usage

```bash
python -m cli.main predict-match Brazil France
python -m cli.main predict-match Brazil France --json-output
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.50 2.38
```

### Dashboard और API

```bash
uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

Endpoints:

- `GET /`
- `GET /teams`
- `POST /predict_match`
- `POST /simulate`
- `GET /team/{name}`
- `GET /tournament/probabilities`

### Claude Skill

Path:

```text
claude-skill/fifa2026-prediction/
```

यह skill Claude को model चलाना, simulation runs पूछना, latest scores check करना और prediction explain करना सिखाती है।

### Betting और Polymarket

Polymarket Yes price `0.42`:

```text
Market probability = 42%
Decimal odds = 1 / 0.42 = 2.38
```

अगर model probability `50%` है:

```bash
python -m cli.main betting-edge 0.50 2.38
```

Positive EV value दिखा सकता है, लेकिन fees, liquidity और model risk जरूर check करें।

### Latest Data

Files:

- `data/sample_matches.csv`
- `data/sample_team_ratings.csv`
- `data/sample_xg.csv`
- `data/latest_results.csv`

API-Football:

```bash
cp .env.example .env
# .env में API_FOOTBALL_KEY डालें
python -m cli.main refresh-latest-data
python -m cli.main latest-data-status
```

अगर match पहले ही खेला जा चुका है, app known score दिखाएगा और prediction को future rematch forecast कहेगा।

### Config और Testing

Config `config/default.yaml` में है। Test:

```bash
pytest
```

### Warning

Model profit guarantee नहीं करता। Injuries, lineups, news, odds और liquidity check करें।

---

## 10. 中文

### 介绍

这是 FIFA 2026 世界杯预测引擎。它可以预测比赛、模拟锦标赛、计算预期进球、生成 Claude/GPT 输入，并分析投注期望值。

### 功能

- CSV 数据，以及 StatsBomb、FiveThirtyEight SPI、API-Football 适配器
- 可配置 K-factor 和主场优势的 ELO 模型
- 基于进球和 xG 的进攻/防守强度
- 带 Dixon-Coles 修正的 Poisson 模型
- 48 队世界杯模拟
- FastAPI、CLI 和网页仪表盘
- Polymarket 和类似市场的 EV 计算

### 安装

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### CLI 使用

```bash
python -m cli.main predict-match Brazil France
python -m cli.main predict-match Brazil France --json-output
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.50 2.38
```

### 仪表盘和 API

```bash
uvicorn api.main:app --reload
```

打开:

```text
http://127.0.0.1:8000/
```

主要 endpoints:

- `GET /`
- `GET /teams`
- `POST /predict_match`
- `POST /simulate`
- `GET /team/{name}`
- `GET /tournament/probabilities`

### Claude Skill

路径:

```text
claude-skill/fifa2026-prediction/
```

该 skill 教 Claude 如何运行模型、询问模拟次数、检查最新比分并解释预测。

### 投注和 Polymarket

Polymarket Yes 价格 `0.42`:

```text
Market probability = 42%
Decimal odds = 1 / 0.42 = 2.38
```

如果模型概率是 `50%`:

```bash
python -m cli.main betting-edge 0.50 2.38
```

正 EV 可能表示有价值，但仍需考虑费用、流动性和模型误差。

### 最新数据

文件:

- `data/sample_matches.csv`
- `data/sample_team_ratings.csv`
- `data/sample_xg.csv`
- `data/latest_results.csv`

API-Football:

```bash
cp .env.example .env
# 在 .env 中添加 API_FOOTBALL_KEY
python -m cli.main refresh-latest-data
python -m cli.main latest-data-status
```

如果比赛已经结束，应用会先显示已知比分，并把预测标记为未来重赛预测。

### 配置和测试

配置在 `config/default.yaml`。运行测试:

```bash
pytest
```

### 注意

模型不保证盈利。请检查伤病、首发、新闻、赔率和流动性。
