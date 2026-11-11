---
name: onboard-your-agent
description: Onboard a personal AI agent (Claude, ChatGPT, Cursor, Codex and others) to Nimble for company investment research at hedge funds. Use when the user first loads these skills, asks how to get started with Nimble for investment research, wants a free trial, needs to connect Nimble, or asks which skill to use. Shows a benchmark chart and five tiles (four use cases to test Nimble's APIs in the user's AI, plus integrating the APIs into their stack), gets the user onto a free Nimble trial and connected, then routes their research request to company-deep-research, company-fast-search, filings-media-pdfs or alt-data-at-scale.
---

# Onboard your agent: Nimble for company investment research

You are setting up Nimble for an investment professional (analyst, PM, credit or event-driven desk, data scientist). Nimble gives you the live web as cited, structured data. Follow the steps in order.

## Step 1: Show the benchmark chart, the five tiles and ask one question

As soon as this skill loads, show the benchmark chart, then the five tiles below it, then ask exactly one question. Do this before any setup talk.

### 1a. Benchmark chart (above the tiles)

Plot the six providers from Nimble's public Finance Use-Case Benchmark v2 (all eight finance jobs, 40 tasks, November 2026; source: [`benchmark/README.md`](../../benchmark/README.md)) as a scatter chart:

- **x axis:** cost per run (USD), starting at $0.
- **y axis:** "F1 accuracy + coverage" (the benchmark's combined score), from 0.3 to 0.65.
- **Points:** one per provider, each labeled with its name. Nimble in an accent color, the others in one neutral color.
- **Title:** "F1 accuracy + coverage vs. cost per run". **Caption:** "Finance Use-Case Benchmark v2, 40 tasks, November 2026. Higher and further left is better."

| Provider | F1 accuracy + coverage | Cost per run (USD) |
| - | - | - |
| Nimble | 0.594 | 0.45 |
| Claude Opus 5.5 | 0.583 | 0.79 |
| GPT-6.1 Sol | 0.513 | 0.64 |
| Exa | 0.455 | 0.48 |
| Parallel | 0.418 | 0.54 |
| Firecrawl | 0.388 | 0.36 |

Use exactly these numbers; never round them up or add providers. If your host can render visual output (Claude artifacts or inline widgets, ChatGPT canvas, an HTML preview), draw the chart there (inline SVG or Chart.js), compact, about 300px tall. If it cannot, show the table above under the title, with Nimble's row in bold.

### 1b. The five tiles

The tiles say what they are: the user is testing Nimble's APIs on real investment research use cases, right here in their own AI. Each tile names the Nimble API behind it. The fifth tile is for taking those APIs into the user's own stack.

**How to draw the tiles.** Put this line above the tiles: **"Test Nimble's APIs on these use cases, right here in your AI."** If your host can render visual output, draw a 2×2 grid of four cards, each with a short title, the Nimble API it tests, one line of what it does and one example, and below the grid one full-width fifth card with a link. Keep it plain and compact. If not, use this markdown:

| 🔎 **Deep research** · *Web Search Agents API* | ⚡ **Fast search** · *Search + Extract APIs* |
| - | - |
| 13 hedge fund research agents (deep dive, catalysts, filing changes, red flags, credit, merger arb, channel checks) plus custom agents. Cited answers in about 5 to 15 minutes. | Answers in seconds from filings, IR pages, regulators and news, with dated primary-source citations. |
| *"Underwrite Duolingo long on paid subscriber growth."* | *"What did NVDA's latest 8-K disclose?"* |
| 📄 **Filings, PDFs & media** · *Extract file parsing + Media API* | 📊 **Alt data at scale** · *Extract Templates + Jobs API* |
| Turn 10-K exhibits, decks, credit and merger agreements into markdown; download files and webcasts to disk or S3. | Prices, reviews, jobs and store data from 800+ Extract Templates, run as batches or scheduled jobs into S3 or Databricks. |
| *"Pull the debt table from this credit agreement."* | *"Track Celsius prices at Walmart and Target daily."* |

> 🔌 **Integrate Nimble's APIs into your stack.** Like what you see? Call the same APIs from your own apps, agents and warehouse (MCP server, SDK and CLI, Databricks and Snowflake apps): **https://docs.nimbleway.com/integrations/overview**

Then ask:

> **What kind of company investment research do you want to test?** For example, a name you're underwriting, a catalyst or deal you're tracking, a borrower you're watching, or a dataset you want to build. Or try: *"Underwrite Duolingo long on paid subscriber growth."*

Keep the chart, the tiles and the question to one screen. No preamble.

## Step 2: Check whether Nimble is already connected

While the user answers, check silently. Either surface working means setup is done; skip to Step 5.

- **MCP:** if any Nimble tool is listed, call the read-only `nimble_agents_list`.
- **CLI:** if you can run shell commands: `command -v nimble && nimble --version && nimble agents list`. The CLI reads `NIMBLE_API_KEY` from the environment.

| Result | Next |
| - | - |
| Either probe returns data | Step 5 |
| A Nimble tool returns an auth error or an authorization URL | Step 4 |
| Nothing is installed and the user has no Nimble account | Step 3 |
| Nothing is installed but the user has an account | Step 4 |

## Step 3: Start the free trial

If the user has no Nimble account, this comes first. Say it in two or three lines:

> Nimble has a free trial, and signing up takes about two minutes.
> 1. Open **https://online.nimbleway.com/signup** and create an account with your work email.
> 2. Confirm your email, then log in to the dashboard.
> Tell me when you're in and I'll connect it.

Open the link for them if your host can. Do not fill in the form, create the account or confirm the email for them. Wait for them to confirm, then go to Step 4.

On hosts that use OAuth (most MCP clients), the user can also create the account during the first authorization in Step 4; mention it so they do not sign up twice.

## Step 4: Connect Nimble to this agent

Default to the MCP server: it uses OAuth, so no API key is created, pasted or stored. Pick the row for your host:

| Host | How |
| - | - |
| Claude Code | Nothing extra to install: this plugin (`nimble-investment-research`) bundles the Nimble MCP server. Run `/mcp`, pick **nimble** and authorize. If the plugin isn't installed yet, install it first (see **Install these skills** below) |
| Claude.ai / Claude Desktop / Cowork | Install **Nimble** from the plugin directory, or add a custom connector at `https://mcp.nimbleway.com/mcp` under **Customize → Connectors**, then **Connect** |
| ChatGPT | Settings → Apps & Connectors → add a custom connector with URL `https://mcp.nimbleway.com/mcp` (requires developer mode on some plans), then sign in |
| Cursor, VS Code, other MCP clients | Add `{"mcpServers": {"nimble": {"type": "http", "url": "https://mcp.nimbleway.com/mcp"}}}`; the first tool call starts OAuth |
| Codex Desktop | Plugins → search **Nimble** → install and approve OAuth |
| Codex CLI | In `~/.codex/config.toml`: `[mcp_servers.nimble-mcp-server]`, `url = "https://mcp.nimbleway.com/mcp"`, `bearer_token_env_var = "NIMBLE_API_KEY"` |

**When the CLI or API is also needed.** The MCP server covers Search, Extract, Extract Templates, Map, Crawl and Web Search Agents. Parsing PDFs, downloading media, template batches and Extract Jobs need the CLI or REST API (`filings-media-pdfs`, `alt-data-at-scale`). If the user's task needs those and the host has a terminal, ask once whether to add the CLI and say why in one sentence:

```bash
npm i -g @nimble-way/nimble-cli
```

Then the user creates a key at **https://online.nimbleway.com/settings/api-keys** (one key per agent, named for it) and sets `NIMBLE_API_KEY` in their shell profile or secret manager.

**Credential safety.** Never ask the user to paste the key into the chat. Never print it (`echo $NIMBLE_API_KEY`, `printenv`) or write it to a file that could be committed or shared. Check it exists with `[ -n "$NIMBLE_API_KEY" ] && echo set || echo missing` and let the shell expand it in an `Authorization: Bearer $NIMBLE_API_KEY` header.

If a tool returns an authorization URL, show it exactly as given and wait. Do not fall back to a generic web search or fetch tool while waiting; that hides the setup problem and returns different data.

**Install these skills** so the agent can route requests:

| Host | Command |
| - | - |
| Claude Code | `claude plugin marketplace add Nimbleway/nimble-for-company-investment-research && claude plugin install nimble-investment-research@nimble-investment-research` (this one plugin is all Claude Code needs: skills and the Nimble MCP server) |
| Cursor, Codex, other agents | `npx skills add Nimbleway/nimble-for-company-investment-research` |
| Claude.ai | Zip each folder under `skills/` and upload it under **Customize → Skills** |
| ChatGPT or any other agent | Add the `SKILL.md` files to the project or custom GPT instructions |

## Step 5: Verify with a real call

The test prompt is **"Underwrite Duolingo long on paid subscriber growth."** Use it unless the user already named their own company or thesis in Step 1; then use theirs in the same shape ("Underwrite <company> <long or short> on <thesis>").

Run one fast, cheap call with the test prompt and show the answer in one or two lines with its citations:

- MCP: `nimble_search(query="Underwrite Duolingo long on paid subscriber growth", include_answer=true, max_results=3)`
- CLI: `nimble search --query "Underwrite Duolingo long on paid subscriber growth" --include-answer --max-results 3`

Then confirm: "Nimble is connected. That was Search, in seconds." Offer the full version of the same prompt as the next step: a `company-deep-research` run with `hf-fundamental-deep-dive` (about 5 to 15 minutes), for example "Do a fundamental deep dive on Duolingo (DUOL, duolingo.com) for a long/short fund testing a long thesis on paid subscriber growth and pricing power." Then route their answer from Step 1.

## Step 6: Route the request to a skill

| What the user said | Skill | First move |
| - | - | - |
| A single fact, date, person, filing or page ("who", "when", "what did the 8-K say") | `company-fast-search` | One scoped Search, then Extract the primary page |
| A name to underwrite, a thesis to test, a short idea, management credibility | `company-deep-research` | `hf-fundamental-deep-dive`, `hf-forensic-red-flags` or `hf-management-track-record` |
| What's coming up, what changed | `company-deep-research` | `hf-catalyst-calendar`, `hf-filing-changes` |
| A pending merger (merger arb) | `company-deep-research` | `hf-deal-terms`, then `hf-deal-tracker` |
| A borrower, a loan, a bond, distress | `company-deep-research` | `hf-credit-profile`, then `hf-credit-early-warning` |
| Customers, suppliers, competitors, government revenue | `company-deep-research` | `hf-customer-supplier-map`, `hf-competitor-momentum`, `hf-government-contracts` |
| "What does the web show today versus last quarter" for one question | `company-deep-research` | `hf-channel-check` |
| Anything else that needs many sources | `company-deep-research` | Build a custom Web Search Agent (section 5 of that skill) |
| Using Nimble's APIs from their own code, agents, pipelines or warehouse | None | Link https://docs.nimbleway.com/integrations/overview and help them pick a path (MCP server, plugin and skills, SDK and CLI, Databricks or Snowflake) |
| A PDF, deck, agreement, spreadsheet, webcast or image | `filings-media-pdfs` | Extract with `file_parsing_options`, or Media download |
| A panel of prices, reviews, postings or locations over time | `alt-data-at-scale` | Find the Extract Template, pilot 20 to 50 inputs, then batch or schedule a Job |

If the answer spans more than one (common), start with the fastest piece that unblocks the rest and say what comes next. For example: fast search to pin the entity and latest filing, then a deep research run, then an alt-data panel to keep watching.

By strategy, the usual starting points:

- **Fundamental long/short:** fundamental deep dive → catalyst calendar → channel check or an alt-data panel on the key KPI.
- **Event-driven / merger arb:** deal terms → deal tracker on a schedule → fast search for each new filing.
- **Credit / distressed:** credit file → early-warning log since the last review → parse the credit agreement.
- **Quant / data science:** alt-data panels via Extract Jobs into S3 or Databricks, with entity maps to tickers.
- **Activist:** forensic screen, management track record, proxy (DEF 14A) parsing.

## Ground rules to state once

Say these once during onboarding, briefly, then apply them silently:

- Only public information. No paywalled, logged-in, leaked or expert-network content, which could be MNPI. A paywalled page is never the only source for a value.
- Every value comes with its source URL and date; anything unpublished is reported as not found, not estimated. Date windows stay windows, and problems that were cured are labeled cured, not live.
- Analyst estimates and price targets are labeled as opinions.
- Deep research runs take minutes. You'll be told when one starts and roughly when it will finish.

## Reference

- Docs index: https://docs.nimbleway.com/llms.txt
- Agent setup (general): https://docs.nimbleway.com/agent-onboarding.md
- Credentials for agents: https://nimbleway.com/auth.md
- Pricing and usage: the Usage page in the Nimble dashboard
