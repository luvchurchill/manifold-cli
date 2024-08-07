# Manifold CLI

A command-line interface for interacting with the Manifold Markets API.

## Requirements

* Python 3.6 or higher
* A Manifold Markets API key (go to your profile settings - account settings)

## Installation

1. Clone this repository:


2. Set your API key as an environment variable: 

`export MANIFOLD_API_KEY="your_api_key"`


You can optionally install the requests library if you don't have it already:

`pip install requests`

Usage:
`python3 cli-manifold.py <command> [options]`

Available Commands:

search-market <term>

Searches for markets by term.

Options:

--limit <number>: Maximum number of markets to return (default: 10).

get-market <slug>

Retrieves market information by its slug.

get-user <username>

Retrieves user information by username.

bet <contract_id> <amount>

Places a bet on a market.

Options:

--outcome <YES/NO>: Outcome to bet on (default: "YES").

--limit_prob <probability>: Limit probability for a limit order (optional).

--expires_at <timestamp>: Expiration timestamp for a limit order (optional).

sell <market_id> <YES/NO>

Sells shares of a market.

Options:

--shares <number>: Number of shares to sell (optional, defaults to selling all shares).

--answer_id <answer_id>: Answer ID (required for multiple choice markets).

cancel-order <bet_id>

Cancels an existing limit order.

get-bets

Retrieves a list of the authenticated user's bets.

Options:

--limit <number>: Maximum number of bets to return (default: 1000).

get-positions <market_id>

Retrieves positions information for a market.

Options:

--order <profit/shares>: Order results by profit or shares (default: "profit").

--top <number>: Get the top N positions.

--bottom <number>: Get the bottom N positions.

Examples:

Search for markets related to "AI":

`python3 cli-manifold.py search-market AI --limit 20`


Get information about a market with the slug "will-tesla-stock-go-up":

`python3 cli-manifold.py get-market will-tesla-stock-go-up`


Place a 5 manna bet on YES for the market with ID "abc123def456":

`python3 cli-manifold.py bet abc123def456 5.00`

Sell all YES shares for the market with ID "xyz789ghi012":

`python3 cli-manifold.py sell xyz789ghi012 YES`

### License

This project is licensed under the MIT License - see the LICENSE file for details.

