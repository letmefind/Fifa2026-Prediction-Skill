const TEAMS = [
  "Argentina", "France", "Spain", "England", "Brazil", "Germany", "Portugal",
  "Netherlands", "Belgium", "USA", "Mexico", "Iran", "Japan", "Morocco",
  "Croatia", "Colombia", "Switzerland", "South Korea", "Canada", "Uruguay",
];

const SAMPLE_MATCH = {
  team_a: "Brazil",
  team_b: "France",
  win_prob_a: 0.46,
  draw_prob: 0.27,
  win_prob_b: 0.27,
  expected_goals_a: 1.54,
  expected_goals_b: 1.18,
  score_distribution: { "1-0": 0.11, "1-1": 0.12, "2-1": 0.1, "0-1": 0.09, "2-2": 0.07 },
};

const SAMPLE_DATE = {
  date: "2026-06-18",
  match_count: 4,
  matches: [
    { group: "A", team_a: "Czechia", team_b: "South Africa", status: "predicted", score: "2-1", winner: "Czechia", win_prob_a: 0.41, draw_prob: 0.28, win_prob_b: 0.31, decimal_odds_a: 2.44, decimal_odds_draw: 3.57, decimal_odds_b: 3.23, expected_goals_a: 1.48, expected_goals_b: 1.22 },
    { group: "B", team_a: "Canada", team_b: "Qatar", status: "predicted", score: "1-0", winner: "Canada", win_prob_a: 0.36, draw_prob: 0.29, win_prob_b: 0.35, decimal_odds_a: 2.78, decimal_odds_draw: 3.45, decimal_odds_b: 2.86, expected_goals_a: 1.23, expected_goals_b: 1.22 },
    { group: "B", team_a: "Switzerland", team_b: "Bosnia and Herzegovina", status: "predicted", score: "1-0", winner: "Switzerland", win_prob_a: 0.43, draw_prob: 0.28, win_prob_b: 0.29, decimal_odds_a: 2.33, decimal_odds_draw: 3.57, decimal_odds_b: 3.45, expected_goals_a: 1.38, expected_goals_b: 1.15 },
    { group: "K", team_a: "Uzbekistan", team_b: "Colombia", status: "predicted", score: "0-1", winner: "Colombia", win_prob_a: 0.19, draw_prob: 0.25, win_prob_b: 0.56, decimal_odds_a: 5.26, decimal_odds_draw: 4.0, decimal_odds_b: 1.79, expected_goals_a: 0.95, expected_goals_b: 1.42 },
  ],
};

const percent = (v) => `${(Number(v) * 100).toFixed(1)}%`;
const number = (v, d = 2) => Number(v).toFixed(d);

function sampleNotice() {
  return `<span class="sample-tag">Sample data — not a live prediction</span>`;
}

function renderMatch(result) {
  const scores = Object.entries(result.score_distribution)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([score, p]) => `<span class="pill">${score} ${percent(p)}</span>`)
    .join("");

  return `
    ${sampleNotice()}
    <div class="prob-grid">
      <div class="prob-card"><span>${result.team_a} win</span><strong>${percent(result.win_prob_a)}</strong></div>
      <div class="prob-card"><span>Draw</span><strong>${percent(result.draw_prob)}</strong></div>
      <div class="prob-card"><span>${result.team_b} win</span><strong>${percent(result.win_prob_b)}</strong></div>
    </div>
    <div class="score-cloud" style="display:flex;flex-wrap:wrap;gap:8px;margin-top:16px;">
      <span class="pill">xG ${result.team_a}: ${number(result.expected_goals_a)}</span>
      <span class="pill">xG ${result.team_b}: ${number(result.expected_goals_b)}</span>
      ${scores}
    </div>
  `;
}

function renderDate(result) {
  return `
    ${sampleNotice()}
    <p class="muted"><strong>${result.date}</strong> · ${result.match_count} matches (illustration only)</p>
    <table class="data-table">
      <thead>
        <tr>
          <th>Group</th><th>Match</th><th>Status</th><th>Score</th>
          <th>Win A</th><th>Draw</th><th>Win B</th><th>Odds A</th><th>Odds D</th><th>Odds B</th>
        </tr>
      </thead>
      <tbody>
        ${result.matches.map((m) => `
          <tr>
            <td>${m.group}</td>
            <td><strong>${m.team_a}</strong> vs <strong>${m.team_b}</strong></td>
            <td><span class="pill">${m.status}</span></td>
            <td>${m.score}</td>
            <td>${percent(m.win_prob_a)}</td>
            <td>${percent(m.draw_prob)}</td>
            <td>${percent(m.win_prob_b)}</td>
            <td>${number(m.decimal_odds_a)}</td>
            <td>${number(m.decimal_odds_draw)}</td>
            <td>${number(m.decimal_odds_b)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}

function fillTeams() {
  const options = TEAMS.map((t) => `<option value="${t}">${t}</option>`).join("");
  document.querySelector("#teamA").innerHTML = options;
  document.querySelector("#teamB").innerHTML = options;
  document.querySelector("#teamA").value = "Brazil";
  document.querySelector("#teamB").value = "France";
}

function wireDemo() {
  fillTeams();

  document.querySelector("#refreshLatest").addEventListener("click", () => {
    document.querySelector("#latestStatus").innerHTML = `
      ${sampleNotice()}
      <div class="result-alert">
        <strong>Refresh is disabled in this demo.</strong>
        <p>On GitHub Pages there is no Python server to fetch API-Football results or rebuild the ELO / Poisson model.</p>
      </div>
    `;
  });

  document.querySelector("#matchForm").addEventListener("submit", (e) => {
    e.preventDefault();
    document.querySelector("#matchResult").innerHTML = renderMatch({
      ...SAMPLE_MATCH,
      team_a: document.querySelector("#teamA").value,
      team_b: document.querySelector("#teamB").value,
    });
  });

  document.querySelector("#dateForm").addEventListener("submit", (e) => {
    e.preventDefault();
    document.querySelector("#dateResult").innerHTML = renderDate(SAMPLE_DATE);
  });

  document.querySelector("#groupForm").addEventListener("submit", (e) => {
    e.preventDefault();
    document.querySelector("#groupResult").innerHTML = `
      ${sampleNotice()}
      <p class="muted">Group ${document.querySelector("#groupSelect").value} preview — install the full app for live group tables and qualifiers.</p>
      ${renderDate({ ...SAMPLE_DATE, match_count: 2, matches: SAMPLE_DATE.matches.slice(0, 2) })}
    `;
  });

  document.querySelector("#simulateForm").addEventListener("submit", (e) => {
    e.preventDefault();
    document.querySelector("#simulationResult").innerHTML = `
      ${sampleNotice()}
      <table class="data-table">
        <thead><tr><th>Team</th><th>Win WC</th><th>Final</th></tr></thead>
        <tbody>
          <tr><td><strong>Spain</strong></td><td>14.2%</td><td>24.1%</td></tr>
          <tr><td><strong>Argentina</strong></td><td>13.8%</td><td>23.4%</td></tr>
          <tr><td><strong>France</strong></td><td>12.5%</td><td>21.0%</td></tr>
          <tr><td><strong>Brazil</strong></td><td>11.1%</td><td>19.2%</td></tr>
        </tbody>
      </table>
    `;
  });

  document.querySelector("#latestStatus").innerHTML = `
    ${sampleNotice()}
    <p class="muted">Static demo — no live CSV or API connection on GitHub Pages.</p>
  `;
}

wireDemo();
