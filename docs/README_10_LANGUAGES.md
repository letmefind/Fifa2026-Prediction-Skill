# Multilingual Quick Help

This file explains how to use the FIFA 2026 Prediction Engine in 10 languages.

Core commands are the same in every language:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Open the web dashboard:

```text
http://127.0.0.1:8000/
```

CLI examples:

```bash
python -m cli.main predict-match Brazil France
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.50 2.38
```

---

## 1. فارسی

این پروژه یک موتور پیش‌بینی جام جهانی ۲۰۲۶ است. می‌توانید احتمال برد، مساوی، گل‌های مورد انتظار، شبیه‌سازی تورنمنت و ارزش شرط‌بندی را محاسبه کنید.

روش استفاده:

1. وابستگی‌ها را نصب کنید.
2. سرور را با `uvicorn api.main:app --reload` اجرا کنید.
3. داشبورد را در `http://127.0.0.1:8000/` باز کنید.
4. در بخش `Predict a Match` دو تیم را انتخاب کنید.
5. احتمال‌های مدل را ببینید: برد تیم اول، مساوی، برد تیم دوم.
6. برای شرط‌بندی، همان احتمال را در بخش `Expected Value Calculator` وارد کنید.

مثال:

```text
Brazil win = 35.6% یعنی Model Probability = 0.356
Polymarket Yes price = 0.42 یعنی Decimal Odds = 1 / 0.42 = 2.38
```

نکته مهم: این ابزار سود شرط‌بندی را تضمین نمی‌کند. همیشه مصدومیت‌ها، ترکیب تیم، ضرایب بازار و نقدشوندگی را بررسی کنید.

---

## 2. العربية

هذا المشروع هو محرك توقعات لكأس العالم 2026. يمكنك حساب احتمالات الفوز، التعادل، الأهداف المتوقعة، محاكاة البطولة، والقيمة المتوقعة للرهانات.

طريقة الاستخدام:

1. ثبّت المتطلبات.
2. شغّل الخادم باستخدام `uvicorn api.main:app --reload`.
3. افتح لوحة التحكم على `http://127.0.0.1:8000/`.
4. اختر فريقين في قسم `Predict a Match`.
5. استخدم احتمالات النموذج: فوز الفريق الأول، التعادل، فوز الفريق الثاني.
6. للرهانات، أدخل الاحتمال المناسب في `Expected Value Calculator`.

مثال:

```text
Brazil win = 35.6% يعني Model Probability = 0.356
Polymarket Yes price = 0.42 يعني Decimal Odds = 2.38
```

تنبيه: النتائج تقديرات نموذجية وليست ضماناً للربح.

---

## 3. Español

Este proyecto es un motor de predicción para la Copa Mundial FIFA 2026. Calcula probabilidades de partido, goles esperados, simulaciones del torneo y valor esperado para apuestas.

Cómo usarlo:

1. Instala las dependencias.
2. Ejecuta `uvicorn api.main:app --reload`.
3. Abre `http://127.0.0.1:8000/`.
4. En `Predict a Match`, elige dos equipos.
5. Lee las probabilidades del modelo: victoria del equipo A, empate, victoria del equipo B.
6. Para apuestas, copia esa probabilidad en `Expected Value Calculator`.

Ejemplo:

```text
Brazil win = 35.6% -> Model Probability = 0.356
Polymarket Yes price = 0.42 -> Decimal Odds = 1 / 0.42 = 2.38
```

Aviso: el modelo no garantiza ganancias. Revisa lesiones, alineaciones, cuotas y liquidez.

---

## 4. Français

Ce projet est un moteur de prédiction pour la Coupe du Monde FIFA 2026. Il calcule les probabilités de match, les expected goals, les simulations du tournoi et la valeur attendue des paris.

Utilisation:

1. Installez les dépendances.
2. Lancez `uvicorn api.main:app --reload`.
3. Ouvrez `http://127.0.0.1:8000/`.
4. Dans `Predict a Match`, choisissez deux équipes.
5. Utilisez les probabilités du modèle: victoire équipe A, nul, victoire équipe B.
6. Pour les paris, utilisez cette probabilité dans `Expected Value Calculator`.

Exemple:

```text
Brazil win = 35.6% -> Model Probability = 0.356
Polymarket Yes price = 0.42 -> Decimal Odds = 2.38
```

Attention: ce logiciel fournit des estimations, pas des profits garantis.

---

## 5. Deutsch

Dieses Projekt ist eine Vorhersage-Engine für die FIFA-Weltmeisterschaft 2026. Es berechnet Spielwahrscheinlichkeiten, Expected Goals, Turniersimulationen und Expected Value für Wetten.

Verwendung:

1. Installiere die Abhängigkeiten.
2. Starte `uvicorn api.main:app --reload`.
3. Öffne `http://127.0.0.1:8000/`.
4. Wähle zwei Teams unter `Predict a Match`.
5. Nutze die Modellwahrscheinlichkeiten: Team A gewinnt, Unentschieden, Team B gewinnt.
6. Für Wetten trägst du die passende Wahrscheinlichkeit in `Expected Value Calculator` ein.

Beispiel:

```text
Brazil win = 35.6% -> Model Probability = 0.356
Polymarket Yes price = 0.42 -> Decimal Odds = 2.38
```

Hinweis: Das Modell garantiert keinen Gewinn. Prüfe Verletzungen, Aufstellungen, Marktpreise und Liquidität.

---

## 6. Português

Este projeto é um motor de previsão para a Copa do Mundo FIFA 2026. Ele calcula probabilidades de jogo, gols esperados, simulações do torneio e valor esperado para apostas.

Como usar:

1. Instale as dependências.
2. Execute `uvicorn api.main:app --reload`.
3. Abra `http://127.0.0.1:8000/`.
4. Em `Predict a Match`, escolha dois times.
5. Leia as probabilidades do modelo: vitória do time A, empate, vitória do time B.
6. Para apostas, use essa probabilidade em `Expected Value Calculator`.

Exemplo:

```text
Brazil win = 35.6% -> Model Probability = 0.356
Polymarket Yes price = 0.42 -> Decimal Odds = 2.38
```

Aviso: o modelo não garante lucro. Verifique lesões, escalações, odds e liquidez.

---

## 7. Italiano

Questo progetto è un motore di previsione per la FIFA World Cup 2026. Calcola probabilità di partita, expected goals, simulazioni del torneo e valore atteso per le scommesse.

Come usarlo:

1. Installa le dipendenze.
2. Avvia `uvicorn api.main:app --reload`.
3. Apri `http://127.0.0.1:8000/`.
4. In `Predict a Match`, scegli due squadre.
5. Usa le probabilità del modello: vittoria squadra A, pareggio, vittoria squadra B.
6. Per le scommesse, inserisci quella probabilità in `Expected Value Calculator`.

Esempio:

```text
Brazil win = 35.6% -> Model Probability = 0.356
Polymarket Yes price = 0.42 -> Decimal Odds = 2.38
```

Nota: il modello non garantisce profitti. Controlla infortuni, formazioni, quote e liquidità.

---

## 8. Türkçe

Bu proje FIFA 2026 Dünya Kupası için bir tahmin motorudur. Maç olasılıkları, beklenen goller, turnuva simülasyonları ve bahis için beklenen değer hesaplar.

Kullanım:

1. Bağımlılıkları kurun.
2. `uvicorn api.main:app --reload` komutunu çalıştırın.
3. `http://127.0.0.1:8000/` adresini açın.
4. `Predict a Match` bölümünde iki takım seçin.
5. Model olasılıklarını kullanın: takım A kazanır, beraberlik, takım B kazanır.
6. Bahis için bu olasılığı `Expected Value Calculator` alanına girin.

Örnek:

```text
Brazil win = 35.6% -> Model Probability = 0.356
Polymarket Yes price = 0.42 -> Decimal Odds = 2.38
```

Uyarı: Model kâr garantisi vermez. Sakatlıkları, kadroları, oranları ve likiditeyi kontrol edin.

---

## 9. हिन्दी

यह प्रोजेक्ट FIFA World Cup 2026 के लिए prediction engine है। यह match probabilities, expected goals, tournament simulation और betting expected value निकालता है।

कैसे उपयोग करें:

1. dependencies install करें।
2. `uvicorn api.main:app --reload` चलाएँ।
3. `http://127.0.0.1:8000/` खोलें।
4. `Predict a Match` में दो teams चुनें।
5. model probabilities देखें: Team A win, Draw, Team B win।
6. betting के लिए वही probability `Expected Value Calculator` में डालें।

Example:

```text
Brazil win = 35.6% -> Model Probability = 0.356
Polymarket Yes price = 0.42 -> Decimal Odds = 2.38
```

Warning: यह model profit guarantee नहीं करता। injuries, lineups, odds और liquidity जरूर check करें।

---

## 10. 中文

这个项目是 FIFA 2026 世界杯预测引擎。它可以计算比赛胜平负概率、预期进球、锦标赛模拟结果和投注期望值。

使用方法:

1. 安装依赖。
2. 运行 `uvicorn api.main:app --reload`。
3. 打开 `http://127.0.0.1:8000/`。
4. 在 `Predict a Match` 选择两支球队。
5. 查看模型概率: A 队获胜、平局、B 队获胜。
6. 如果用于投注，把对应概率填入 `Expected Value Calculator`。

示例:

```text
Brazil win = 35.6% -> Model Probability = 0.356
Polymarket Yes price = 0.42 -> Decimal Odds = 2.38
```

注意: 模型不能保证盈利。请检查伤病、首发阵容、市场赔率和流动性。
