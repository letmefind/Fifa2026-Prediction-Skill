const percent = (value) => `${(Number(value) * 100).toFixed(1)}%`;
const number = (value, digits = 2) => Number(value).toFixed(digits);

const state = {
  teams: [],
};

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }
  return response.json();
}

function setLoading(element, message) {
  element.className = "result-block muted";
  element.innerHTML = message;
}

function renderError(element, error) {
  element.className = "result-block negative";
  element.textContent = `Error: ${error.message}`;
}

function topScores(distribution, limit = 5) {
  return Object.entries(distribution)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit);
}

function renderBars(items, key, formatter = percent) {
  const max = Math.max(...items.map((item) => Number(item[key])), 0.01);
  return `
    <div class="bar-list">
      ${items
        .map((item) => {
          const value = Number(item[key]);
          const width = Math.max((value / max) * 100, 2);
          return `
            <div class="bar-row">
              <strong>${item.team}</strong>
              <div class="bar"><span style="width:${width}%"></span></div>
              <span>${formatter(value)}</span>
            </div>
          `;
        })
        .join("")}
    </div>
  `;
}

function renderMatch(result) {
  const scores = topScores(result.score_distribution);
  return `
    <div class="prob-grid">
      <div class="prob-card">
        <span>${result.team_a} win</span>
        <strong>${percent(result.win_prob_a)}</strong>
      </div>
      <div class="prob-card">
        <span>Draw</span>
        <strong>${percent(result.draw_prob)}</strong>
      </div>
      <div class="prob-card">
        <span>${result.team_b} win</span>
        <strong>${percent(result.win_prob_b)}</strong>
      </div>
    </div>
    <div class="score-cloud">
      <span class="pill">xG ${result.team_a}: ${number(result.expected_goals_a)}</span>
      <span class="pill">xG ${result.team_b}: ${number(result.expected_goals_b)}</span>
      ${scores.map(([score, probability]) => `<span class="pill">${score} ${percent(probability)}</span>`).join("")}
    </div>
    ${renderBars(
      [
        { team: result.team_a, probability: result.win_prob_a },
        { team: "Draw", probability: result.draw_prob },
        { team: result.team_b, probability: result.win_prob_b },
      ],
      "probability",
    )}
  `;
}

function renderSimulation(result) {
  const rows = result.probabilities.slice(0, 12);
  return `
    <table class="data-table">
      <thead>
        <tr>
          <th>Team</th>
          <th>Win WC</th>
          <th>Final</th>
          <th>Semis</th>
          <th>R32</th>
        </tr>
      </thead>
      <tbody>
        ${rows
          .map(
            (row) => `
              <tr>
                <td><strong>${row.team}</strong></td>
                <td>${percent(row.win_world_cup)}</td>
                <td>${percent(row.reach_final)}</td>
                <td>${percent(row.reach_semis)}</td>
                <td>${percent(row.round_of_32)}</td>
              </tr>
            `,
          )
          .join("")}
      </tbody>
    </table>
    ${renderBars(rows.slice(0, 8), "win_world_cup")}
  `;
}

function calculateEv(modelProb, marketOdds) {
  const impliedProb = 1 / marketOdds;
  const expectedValue = modelProb * (marketOdds - 1) - (1 - modelProb);
  const edge = modelProb - impliedProb;
  const label = expectedValue > 0.02 ? "undervalued" : expectedValue < -0.02 ? "overvalued" : "fair";
  return { impliedProb, expectedValue, edge, label };
}

function renderEv(result) {
  const statusClass = result.expectedValue >= 0 ? "positive" : "negative";
  return `
    <div class="prob-grid">
      <div class="prob-card">
        <span>Implied probability</span>
        <strong>${percent(result.impliedProb)}</strong>
      </div>
      <div class="prob-card">
        <span>Expected value</span>
        <strong class="${statusClass}">${number(result.expectedValue, 3)}</strong>
      </div>
      <div class="prob-card">
        <span>Label</span>
        <strong class="${statusClass}">${result.label}</strong>
      </div>
    </div>
    <p class="muted">Edge versus market: ${percent(result.edge)}. This excludes limits, bookmaker margin, stale prices, and lineup risk.</p>
  `;
}

async function loadTeams() {
  state.teams = await requestJson("/teams");
  const options = state.teams.map((team) => `<option value="${team}">${team}</option>`).join("");
  document.querySelector("#teamA").innerHTML = options;
  document.querySelector("#teamB").innerHTML = options;
  document.querySelector("#teamA").value = state.teams.includes("Brazil") ? "Brazil" : state.teams[0];
  document.querySelector("#teamB").value = state.teams.includes("France") ? "France" : state.teams[1];
}

document.querySelector("#swapTeams").addEventListener("click", () => {
  const teamA = document.querySelector("#teamA");
  const teamB = document.querySelector("#teamB");
  [teamA.value, teamB.value] = [teamB.value, teamA.value];
});

document.querySelector("#matchForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const element = document.querySelector("#matchResult");
  setLoading(element, "Calculating match probabilities...");
  try {
    const result = await requestJson("/predict_match", {
      method: "POST",
      body: JSON.stringify({
        team_a: document.querySelector("#teamA").value,
        team_b: document.querySelector("#teamB").value,
        neutral: document.querySelector("#neutral").checked,
      }),
    });
    element.className = "result-block";
    element.innerHTML = renderMatch(result);
  } catch (error) {
    renderError(element, error);
  }
});

document.querySelector("#simulateForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const element = document.querySelector("#simulationResult");
  setLoading(element, "Running tournament simulation...");
  try {
    const result = await requestJson("/simulate", {
      method: "POST",
      body: JSON.stringify({ runs: Number(document.querySelector("#runs").value) }),
    });
    element.className = "result-block";
    element.innerHTML = renderSimulation(result);
  } catch (error) {
    renderError(element, error);
  }
});

document.querySelector("#evForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const element = document.querySelector("#evResult");
  const modelProb = Number(document.querySelector("#modelProb").value);
  const marketOdds = Number(document.querySelector("#marketOdds").value);
  element.className = "result-block";
  element.innerHTML = renderEv(calculateEv(modelProb, marketOdds));
});

loadTeams().catch((error) => renderError(document.querySelector("#matchResult"), error));
