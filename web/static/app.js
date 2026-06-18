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
  const knownResult = result.known_result;
  const alreadyPlayed =
    knownResult && knownResult.found
      ? `
        <div class="result-alert">
          <strong>Already played:</strong>
          ${knownResult.home_team} ${knownResult.home_score}-${knownResult.away_score} ${knownResult.away_team}
          <span>${knownResult.date} | ${knownResult.competition}</span>
          <p>The probabilities below are for a future rematch forecast, not the historical result.</p>
        </div>
      `
      : "";
  return `
    ${alreadyPlayed}
    <div class="prob-grid">
      <div class="prob-card">
        <span>${result.team_a} win</span>
        <strong>${percent(result.win_prob_a)}</strong>
        <button class="mini-button use-probability" data-probability="${result.win_prob_a}" type="button">Use for EV</button>
      </div>
      <div class="prob-card">
        <span>Draw</span>
        <strong>${percent(result.draw_prob)}</strong>
        <button class="mini-button use-probability" data-probability="${result.draw_prob}" type="button">Use for EV</button>
      </div>
      <div class="prob-card">
        <span>${result.team_b} win</span>
        <strong>${percent(result.win_prob_b)}</strong>
        <button class="mini-button use-probability" data-probability="${result.win_prob_b}" type="button">Use for EV</button>
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

function renderGroupMatches(matches) {
  return `
    <table class="data-table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Match</th>
          <th>Status</th>
          <th>Score</th>
          <th>Winner</th>
        </tr>
      </thead>
      <tbody>
        ${matches
          .map(
            (match) => `
              <tr>
                <td>${match.date}</td>
                <td><strong>${match.team_a}</strong> vs <strong>${match.team_b}</strong></td>
                <td><span class="pill ${match.status === "played" ? "played-pill" : ""}">${match.status}</span></td>
                <td>${match.score}</td>
                <td>${match.winner}</td>
              </tr>
            `,
          )
          .join("")}
      </tbody>
    </table>
  `;
}

function renderGroupTable(table) {
  return `
    <table class="data-table">
      <thead>
        <tr>
          <th>Rank</th>
          <th>Team</th>
          <th>Pts</th>
          <th>W</th>
          <th>D</th>
          <th>L</th>
          <th>GF</th>
          <th>GA</th>
          <th>GD</th>
        </tr>
      </thead>
      <tbody>
        ${table
          .map(
            (row) => `
              <tr>
                <td>${row.rank}</td>
                <td><strong>${row.team}</strong></td>
                <td>${row.points}</td>
                <td>${row.wins}</td>
                <td>${row.draws}</td>
                <td>${row.losses}</td>
                <td>${row.goals_for}</td>
                <td>${row.goals_against}</td>
                <td>${row.goal_difference}</td>
              </tr>
            `,
          )
          .join("")}
      </tbody>
    </table>
  `;
}

function renderOneGroup(group) {
  return `
    <div class="group-card">
      <h3>Group ${group.group}</h3>
      <p class="muted">Winner: <strong>${group.winner}</strong> | Runner-up: <strong>${group.runner_up}</strong> | Third: <strong>${group.third_place}</strong></p>
      ${renderGroupMatches(group.matches)}
      ${renderGroupTable(group.table)}
    </div>
  `;
}

function renderGroups(result, selectedGroup) {
  const groups =
    selectedGroup === "ALL"
      ? Object.values(result.groups)
      : [result.groups[selectedGroup]];
  const thirdRows = result.third_place_ranking.slice(0, 12);
  const warning = result.fixture_status && result.fixture_status.warning
    ? `
      <div class="result-alert">
        <strong>Fixture warning:</strong>
        <p>${result.fixture_status.warning}</p>
      </div>
    `
    : "";
  return `
    ${warning}
    ${groups.map(renderOneGroup).join("")}
    <div class="group-card">
      <h3>Best Third-Place Ranking</h3>
      <p class="muted">Top 8 third-place teams are projected to reach the Round of 32.</p>
      ${renderGroupTable(thirdRows.map((row, index) => ({ ...row, rank: index + 1 })))}
    </div>
    <div class="score-cloud">
      <span class="pill">Round of 32 qualifiers: ${result.qualified_round_of_32.length}</span>
      <span class="pill">Projected champion: ${result.knockout_projection.champion}</span>
    </div>
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

function renderLatestStatus(status) {
  const latestDate = status.latest_match_date || "None loaded";
  const apiText = [
    status.football_data_api_configured ? "Football-Data" : null,
    status.api_football_configured ? "API-Football" : null,
  ]
    .filter(Boolean)
    .join(", ");
  return `
    <div class="status-grid">
      <div class="status-item">
        <span>Latest matches merged</span>
        <strong>${status.latest_matches_loaded}</strong>
      </div>
      <div class="status-item">
        <span>Total matches in model</span>
        <strong>${status.total_matches_in_model}</strong>
      </div>
      <div class="status-item">
        <span>Latest match date</span>
        <strong>${latestDate}</strong>
      </div>
      <div class="status-item">
        <span>API feeds configured</span>
        <strong>${apiText || "Local CSV only"}</strong>
      </div>
    </div>
    <p class="muted">Latest results improve future-match predictions by updating ELO and attack/defense strengths before the model runs.</p>
  `;
}

async function loadLatestStatus() {
  const element = document.querySelector("#latestStatus");
  try {
    const status = await requestJson("/data/latest_status");
    element.className = "result-block";
    element.innerHTML = renderLatestStatus(status);
  } catch (error) {
    renderError(element, error);
  }
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

document.querySelector("#refreshLatest").addEventListener("click", async () => {
  const element = document.querySelector("#latestStatus");
  setLoading(element, "Refreshing latest score/result data and rebuilding the model...");
  try {
    const status = await requestJson("/data/refresh_latest", { method: "POST" });
    element.className = "result-block";
    element.innerHTML = renderLatestStatus(status);
  } catch (error) {
    renderError(element, error);
  }
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

document.querySelector("#matchResult").addEventListener("click", (event) => {
  const button = event.target.closest(".use-probability");
  if (!button) return;
  document.querySelector("#modelProb").value = Number(button.dataset.probability).toFixed(3);
  document.querySelector("#evResult").className = "result-block muted";
  document.querySelector("#evResult").textContent = "Model probability copied. Add market odds, then calculate EV.";
  document.querySelector("#modelProb").scrollIntoView({ behavior: "smooth", block: "center" });
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

document.querySelector("#groupForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const element = document.querySelector("#groupResult");
  const selectedGroup = document.querySelector("#groupSelect").value;
  setLoading(element, "Refreshing latest results and predicting group stage...");
  try {
    const result = await requestJson("/groups/predictions?refresh=true");
    element.className = "result-block";
    element.innerHTML = renderGroups(result, selectedGroup);
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
loadLatestStatus();
