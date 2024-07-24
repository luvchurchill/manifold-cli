import os
import requests
import json
import argparse

API_BASE_URL = "https://api.manifold.markets/v0"
API_KEY = os.environ.get("MANIFOLD_API_KEY")

if API_KEY is None:
    raise ValueError("MANIFOLD_API_KEY environment variable not set.")


def _make_api_request(method, endpoint, data=None):
    headers = {
        "Authorization": f"Key {API_KEY}",
        "Content-Type": "application/json"
    }
    url = f"{API_BASE_URL}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=headers, params=data)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    response.raise_for_status()
    return response.json()

def search_market(term, limit=10):
    """Search for a market by term and return a list of matching markets."""
    data = {"term": term, "limit": limit}
    return _make_api_request("GET", "/search-markets", data=data)

def get_market_by_slug(market_slug):
    """Get market information by its slug."""
    return _make_api_request("GET", f"/slug/{market_slug}")


def get_user_by_username(username):
    """Get user information by their username."""
    return _make_api_request("GET", f"/user/{username}")


def place_bet(contract_id, amount, outcome="YES", limit_prob=None, expires_at=None):
    """Place a bet or limit order on a market."""
    data = {
        "contractId": contract_id,
        "amount": amount,
        "outcome": outcome
    }
    if limit_prob is not None:
        data["limitProb"] = limit_prob
    if expires_at is not None:
        data["expiresAt"] = expires_at

    # print("Request Data:", json.dumps(data, indent=4)) 
    return _make_api_request("POST", "/bet", data=data)


def cancel_limit_order(bet_id):
    """Cancel an existing limit order."""
    return _make_api_request("POST", f"/bet/cancel/{bet_id}")


def get_my_bets(limit=1000):
    """Retrieve a list of the authenticated user's bets."""
    return _make_api_request("GET", "/bets", data={"limit": limit})


def get_market_positions(market_id, order="profit", top=None, bottom=None):
    """Get positions information for a market."""
    data = {"order": order}
    if top:
        data["top"] = top
    if bottom:
        data["bottom"] = bottom
    return _make_api_request("GET", f"/market/{market_id}/positions", data=data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manifold CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search Market
    parser_search_market = subparsers.add_parser("search-market", help="Search for a market")
    parser_search_market.add_argument("term", type=str, help="Search term for the market")
    parser_search_market.add_argument("--limit", type=int, default=10, help="Maximum number of markets to return")

    # Get market by slug
    parser_get_market = subparsers.add_parser("get-market", help="Get market by slug")
    parser_get_market.add_argument("slug", type=str, help="Market slug")

    # Get user by username
    parser_get_user = subparsers.add_parser("get-user", help="Get user by username")
    parser_get_user.add_argument("username", type=str, help="Username")

    # Place bet
    parser_place_bet = subparsers.add_parser("bet", help="Place a bet")
    parser_place_bet.add_argument("contract_id", type=str, help="Contract ID")
    parser_place_bet.add_argument("amount", type=float, help="Bet amount")
    parser_place_bet.add_argument("--outcome", type=str, default="YES", choices=["YES", "NO"], help="Bet outcome (YES/NO)")
    parser_place_bet.add_argument("--limit_prob", type=float, help="Limit probability (optional)")
    parser_place_bet.add_argument("--expires_at", type=int, help="Expiration timestamp (optional)")

    # Cancel limit order
    parser_cancel_order = subparsers.add_parser("cancel-order", help="Cancel a limit order")
    parser_cancel_order.add_argument("bet_id", type=str, help="Bet ID")

    # Get my bets
    parser_get_bets = subparsers.add_parser("get-bets", help="Get my bets")
    parser_get_bets.add_argument("--limit", type=int, default=1000, help="Maximum number of bets to retrieve")

    # Get market positions
    parser_get_positions = subparsers.add_parser("get-positions", help="Get market positions")
    parser_get_positions.add_argument("market_id", type=str, help="Market ID")
    parser_get_positions.add_argument("--order", type=str, default="profit", choices=["profit", "shares"], help="Order by profit or shares")
    parser_get_positions.add_argument("--top", type=int, help="Get top N positions")
    parser_get_positions.add_argument("--bottom", type=int, help="Get bottom N positions")

    args = parser.parse_args()

    try:
        if args.command == "search-market":
            markets = search_market(args.term, args.limit)
            print(json.dumps(markets, indent=4))
        elif args.command == "get-market":
            market = get_market_by_slug(args.slug)
            print(json.dumps(market, indent=4))
        elif args.command == "get-user":
            user = get_user_by_username(args.username)
            print(json.dumps(user, indent=4)) 
        elif args.command == "bet":
            bet_result = place_bet(args.contract_id, args.amount, args.outcome, args.limit_prob, args.expires_at)
            print(json.dumps(bet_result, indent=4))
        elif args.command == "cancel-order":
            cancel_result = cancel_limit_order(args.bet_id)
            print(json.dumps(cancel_result, indent=4))
        elif args.command == "get-bets":
            my_bets = get_my_bets(args.limit)
            print(json.dumps(my_bets, indent=4))
        elif args.command == "get-positions":
            positions = get_market_positions(args.market_id, args.order, args.top, args.bottom)
            print(json.dumps(positions, indent=4))
        else:
            parser.print_help()
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")