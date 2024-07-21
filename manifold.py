import os
import requests
import json
import time

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

    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()


def get_market_by_slug(market_slug):
    """Get market information by its slug."""
    return _make_api_request("GET", f"/slug/{market_slug}")


def get_user_by_username(username):
    """Get user information by their username."""
    return _make_api_request("GET", f"/user/{username}")


def place_bet(contract_id, amount, outcome="YES", limit_prob=None, expires_at=None, dry_run=False):
    """Place a bet or limit order on a market."""
    data = {
        "contractId": contract_id,
        "amount": amount,
        "outcome": outcome,
        "limitProb": limit_prob,
        "expiresAt": expires_at,
        "dryRun": dry_run
    }
    return _make_api_request("POST", "/bet", data=data)


def cancel_limit_order(bet_id):
    """Cancel an existing limit order."""
    return _make_api_request("POST", f"/bet/cancel/{bet_id}")


def get_my_bets(limit=1000, contract_id=None):
    """Retrieve a list of the authenticated user's bets."""
    data = {"limit": limit}
    if contract_id:
        data["contractId"] = contract_id 
    return _make_api_request("GET", "/bets", data=data)


def get_market_positions(market_id, order="profit", top=None, bottom=None, user_id=None):
    """Get positions information for a market."""
    data = {"order": order}
    if top:
        data["top"] = top
    if bottom:
        data["bottom"] = bottom
    if user_id:
        data["userId"] = user_id
    return _make_api_request("GET", f"/market/{market_id}/positions", data=data)


def main():
    """Example usage of the Manifold API functions."""

    try:
        # Example 1: Get market info and place a bet
        market_slug = "will-gpt-5-be-announced-by-october-1st" 
        market = get_market_by_slug(market_slug)
        market_id = market['id']
        
        bet_result = place_bet(contract_id=market_id, amount=1, outcome="YES") 
        print("Bet placed:", bet_result)

        # Example 2: Cancel a limit order (replace with actual bet ID)
        # limit_order_id_to_cancel = "your_limit_order_id"
        # cancel_result = cancel_limit_order(limit_order_id_to_cancel) 
        # print("Cancel result:", cancel_result)

        # Example 3: Get your recent bets
        my_bets = get_my_bets(limit=5)
        print("My recent bets:", my_bets)

        # Example 4: Get market positions
        positions = get_market_positions(market_id=market_id, top=3)
        print("Top 3 positions:", positions)

    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")

if __name__ == "__main__":
    main()
