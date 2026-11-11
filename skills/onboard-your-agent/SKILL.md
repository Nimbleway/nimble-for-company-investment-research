---
name: onboard-your-agent
description: Onboard a personal AI agent (Claude, ChatGPT, Cursor, Codex and others) to Nimble for company investment research at hedge funds. Use when the user first loads these skills, asks how to get started with Nimble for investment research, wants a free trial, needs to connect Nimble, or asks which skill to use. Shows four tiles summarizing the skills, gets the user onto a free Nimble trial and connected, then routes their research request to company-deep-research, company-fast-search, filings-media-pdfs or alt-data-at-scale.
---

# Onboard your agent: Nimble for company investment research

You are setting up Nimble for an investment professional (analyst, PM, credit or event-driven desk, data scientist). Nimble gives you the live web as cited, structured data. Follow the steps in order.

## Step 1: Show the four tiles and ask one question

As soon as this skill loads, show the four tiles below, then ask exactly one question. Do this before any setup talk.

**How to draw the tiles.** If your host can render visual output (Claude artifacts or inline widgets, ChatGPT canvas, an HTML preview), draw a 2×2 grid of four cards: a short title, one line of what it does, one line of example. Keep it plain and compact. If not, use this markdown table:

| 🔎 **Deep research** | ⚡ **Fast search** |
| - | - |
| 13 hedge fund research agents (deep dive, catalysts, filing changes, red flags, credit, merger arb, channel checks) plus custom agents. Cited answers in about 5 to 15 minutes. | Answers in seconds from filings, IR pages, regulators and news, with dated primary-source citations. |
| *"Build a catalyst calendar for RKLB."* | *"What did NVDA's latest 8-K disclose?"* |
| 📄 **Filings, PDFs & media** | 📊 **Alt data at scale** |
| Turn 10-K exhibits, decks, credit and merger agreements into markdown; download files and webcasts to disk or S3. | Prices, reviews, jobs and store data from 800+ Extract Templates, run as batches or scheduled jobs into S3 or Databricks. |
| *"Pull the debt table from this credit agreement."* | *"Track Celsius prices at Walmart and Target daily."* |

Then ask:

> **What kind of company investment research do you want to do?** For example, a name you're underwriting, a catalyst or deal you're tracking, a borrower you're watching, or a dataset you want to build.

Keep the tiles and the question to one screen. No preamble.

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
| Claude Code | `claude plugin marketplace add Nimbleway/agent-skills && claude plugin install nimble@nimble-plugin-marketplace`, then `/mcp` to authorize |
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
| Claude Code | `claude plugin marketplace add Nimbleway/nimble-for-company-investment-research && claude plugin install nimble-investment-research@nimble-investment-research` |
| Cursor, Codex, other agents | `npx skills add Nimbleway/nimble-for-company-investment-research` |
| Claude.ai | Zip each folder under `skills/` and upload it under **Customize → Skills** |
| ChatGPT or any other agent | Add the `SKILL.md` files to the project or custom GPT instructions |

## Step 5: Verify with a real call

Run one cheap, relevant call and show the result in one line:

- MCP: `nimble_search(query="<a company the user named, or Nvidia> latest 8-K", include_domains=["sec.gov"], max_results=3)`
- CLI: `nimble search --query "Nvidia latest 8-K" --max-results 3`

Then confirm: "Nimble is connected. Here's what I can do," and route their answer from Step 1.

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

- Only public information. No paywalled, logged-in, leaked or expert-network content, which could be MNPI.
- Every value comes with its source URL and date; anything unpublished is reported as not found, not estimated.
- Analyst estimates and price targets are labeled as opinions.
- Deep research runs take minutes. You'll be told when one starts and roughly when it will finish.

## Reference

- Docs index: https://docs.nimbleway.com/llms.txt
- Agent setup (general): https://docs.nimbleway.com/agent-onboarding.md
- Credentials for agents: https://nimbleway.com/auth.md
- Pricing and usage: the Usage page in the Nimble dashboard
