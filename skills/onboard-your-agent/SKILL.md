---
name: onboard-your-agent
description: Onboard a personal AI agent (Claude, ChatGPT, Cursor, Codex and others) to Nimble for company investment research at hedge funds. Use when the user first loads these skills, asks how to get started with Nimble for investment research, wants a free trial, needs to connect Nimble, or asks which skill to use. Shows four tiles summarizing the skills, connects Nimble following Nimble's agent setup guide (a new user creates their free account during the MCP sign-in, or at the signup page for API-key setups), then routes their research request to company-deep-research, company-fast-search, filings-media-pdfs or alt-data-at-scale.
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

The setup in Steps 2 to 5 follows Nimble's agent setup guide (https://docs.nimbleway.com/agent-onboarding.md). Follow the steps in order and do not skip ahead. Most hosts need no API key.

## Step 2: Check what is already available

While the user answers, check silently. Two surfaces reach Nimble: the MCP server and the `nimble` CLI. Probe both before installing anything. Either one working means the user is already set up.

**MCP.** If your host lists any Nimble tool, call the read-only one:

```
nimble_agents_list
```

**CLI.** If you can run shell commands, check the binary and the key together:

```bash
command -v nimble && nimble --version && nimble agents list
```

`nimble agents list` is read-only and confirms both the install and the credential in one call. The CLI reads `NIMBLE_API_KEY` from the environment. It has no OAuth support, so without that variable it cannot authenticate.

| Result | Go to |
| - | - |
| Either probe returns data | Step 6. Setup is done, do not install anything |
| A Nimble tool is listed but returns an auth error or an authorization URL | Step 4 |
| `nimble` exists but the probe fails on credentials | Fallback: API key, then Step 5 |
| Neither surface exists | Step 3 |

## Step 3: Choose a surface, then install

If you cannot run shell commands, use MCP. That is the only option.

If you can, both work, and they differ in ways that matter here:

| | MCP server | Nimble CLI |
| - | - | - |
| Authentication | OAuth in the browser, nothing to store | API key only. No `login` command, so no OAuth |
| Where results land | Through your context window | A file or a pipe |
| Cost of large results | Every token is charged to context | Write to disk and read what you need |
| Product coverage | Search, Extract, Extract Template, Map, Crawl, Agents | All of those, plus SERP, Media and Extract Jobs |
| Best for | Ordinary tool calls, and any host without a terminal | Bulk work and the products MCP does not carry |

Default to MCP, because it needs no API key. Three exceptions:

* **On Claude products, start with the Nimble plugin.** It installs the MCP connector and Nimble's skills. Those skills call the `nimble` CLI, which is a separate install (`npm i -g @nimble-way/nimble-cli` plus `NIMBLE_API_KEY`). Add the CLI only if the task needs a product MCP does not carry.
* **If the task needs SERP, Media or Extract Jobs,** install the CLI; MCP alone cannot do the job. In this repo that means downloading files in `filings-media-pdfs` and scheduled Jobs in `alt-data-at-scale`.
* **If the task is bulk retrieval,** such as an alt-data panel or a batch of filings, ask the user once whether to add the CLI. Give the reason in one sentence: large results are cheaper written to a file than passed through the context window. If they have no API key and do not want one, stay on MCP.

Do not install both without being asked. One working surface is enough.

### Install the CLI

Only where a terminal is available:

```bash
npm i -g @nimble-way/nimble-cli
```

Then set `NIMBLE_API_KEY` as described in the Fallback section, and go to Step 5. The CLI does not use OAuth, so skip Step 4.

### Install the MCP server

Pick the row that matches your host.

| Host | Command |
| - | - |
| Claude Code | `claude plugin marketplace add Nimbleway/agent-skills && claude plugin install nimble@nimble-plugin-marketplace` |
| Claude Cowork, claude.ai | Install **Nimble** from the [plugin directory](https://claude.ai/directory/plugins/nimble%40knowledge-work-plugins) |
| Cortex Code | `cortex mcp add nimble https://mcp.nimbleway.com/mcp --transport http` |
| Cursor, VS Code, other MCP clients | Add the config below, then `npx skills add Nimbleway/agent-skills -a <host>` |
| Codex Desktop | Open **Plugins**, search for **Nimble**, install it, approve OAuth, then call it in a new task with `@nimble` |
| Codex CLI | Add the Codex config below, then `npx skills add Nimbleway/agent-skills -a codex` |

The `<host>` value is your client name, for example `cursor` or `codex`.

For any client that reads a standard MCP config file:

```json
{
  "mcpServers": {
    "nimble": {
      "type": "http",
      "url": "https://mcp.nimbleway.com/mcp"
    }
  }
}
```

No `Authorization` header. The server advertises OAuth, and the first tool call starts the flow. Cursor reads `.cursor/mcp.json` for one project, or `~/.cursor/mcp.json` for all projects.

Codex CLI authenticates with an API key rather than OAuth. Add to `~/.codex/config.toml` (or a project `.codex/config.toml`):

```toml
[mcp_servers.nimble-mcp-server]
url = "https://mcp.nimbleway.com/mcp"
bearer_token_env_var = "NIMBLE_API_KEY"
```

If the variable is not set, follow the Fallback section, then go to Step 5.

Full per-client detail: https://docs.nimbleway.com/integrations/agent-skills/plugin-installation.md

### Install these investment research skills

| Host | Command |
| - | - |
| Claude Code | `claude plugin marketplace add Nimbleway/nimble-for-company-investment-research && claude plugin install nimble-investment-research@nimble-investment-research` |
| Cursor, Codex, other agents | `npx skills add Nimbleway/nimble-for-company-investment-research` |
| claude.ai | Zip each folder under `skills/` and upload it under **Customize → Skills** |

## Step 4: Authorize and create the free account

`https://mcp.nimbleway.com/mcp` runs OAuth 2.1 with PKCE. Authorization happens in the user's browser. **No API key is created, pasted or stored.**

* Claude Code: run `/mcp` and follow the prompt
* Claude Cowork, claude.ai: open **Customize → Connectors**, find **Nimble**, click **Connect**
* Cortex Code: run `cortex mcp start`
* Codex Desktop: OAuth opens in the browser as soon as the plugin installs
* Other clients: the first tool call returns an authorization URL

The user approves the scopes and, if they have no Nimble account, creates one during that same login. That is where a new user gets their free Nimble account, so there is no separate signup step on the MCP path. Tell the user this in one line so they do not sign up twice.

**If a tool returns an authorization URL instead of data:** present the URL exactly as given and stop. There is no step where the user pastes anything back to you. Wait for them to authorize, then return to Step 2 and probe again.

Never substitute a different tool while waiting. Do not fall back to a generic web fetch, a search tool or `curl`. Those return different data and hide the setup failure from the user.

## Step 5: Verify

Repeat the Step 2 probe for whichever surface you installed. Expect a successful response.

In Claude Code, `claude mcp list` also shows MCP state directly. Look for `nimble` marked `✓ Connected`. A `! Needs authentication` marker means Step 4 is incomplete.

Then confirm the setup with a real call, on the company the user named if they named one:

- MCP: `nimble_search` with query `"<company> latest 8-K"` (or `"nimble web data platform"`)
- CLI: `nimble search --query "<company> latest 8-K" --max-results 3`

Tell the user Nimble is ready and route their answer from Step 1 (Step 6).

## Fallback: API key

Use this **only** when your host cannot speak MCP or cannot complete OAuth, or when the CLI is needed. An API key is a long-lived secret, so OAuth is preferred wherever it works.

Check whether `NIMBLE_API_KEY` is already set, without printing its value:

```bash
[ -n "$NIMBLE_API_KEY" ] && echo set || echo missing
```

If it is set, use it without ever reading the value. Let the shell expand the variable and send it as a bearer token: `Authorization: Bearer $NIMBLE_API_KEY`. Store the raw key; the `Bearer` prefix belongs in the header, not in the stored value.

If it is not set:

1. A user with no Nimble account starts the free trial at **https://online.nimbleway.com/signup**, confirms their email and logs in. Open the link for them if your host can; do not fill in the form or create the account for them.
2. They create a key at **https://online.nimbleway.com/settings/api-keys** (one key per agent, with a descriptive name; it is shown only once) and set it as `NIMBLE_API_KEY` in their environment.

Never ask the user to paste the key into the chat. Never print it, and never read it into your own context: do not run `printenv NIMBLE_API_KEY`, `echo $NIMBLE_API_KEY` or any equivalent. Do not write it to a file you commit or include it in output the user might share. Full credential path: https://nimbleway.com/auth.md

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
