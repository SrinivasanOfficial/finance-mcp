from mcp.server.fastmcp import FastMCP
from typing import Optional
import requests

mcp = FastMCP("Finance-MCP")

BASE_URL = "https://global-market-api.onrender.com/"


@mcp.tool()
def get_stocks(
    category: str,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    order: Optional[str] = "asc"
):
    """
    Fetch stock lists based on performance or activity.

    Use this tool when the user asks about:
    - top gaining stocks
    - top losing stocks
    - most active / high volume stocks
    - stock lists with sorting or limits

    Categories:
    - most_active → high trading volume stocks
    - top_gainers → stocks with highest positive price change
    - top_losers → stocks with highest negative price change

    Parameters:
    - category (required): one of [most_active, top_gainers, top_losers]
    - limit (optional): number of stocks to return (e.g., 5, 10)
    - sort (optional): field to sort by (e.g., price, volume, change_percent)
    - order (optional): sorting order → "asc" or "desc" (default: asc)

    Examples:
    - "Show top 5 gainers"
    - "List most active stocks sorted by volume"
    - "Give top losers sorted by price descending"
    """

    CATEGORY_MAP = {
        "most_active": "stocks/most-active",
        "trending": "stocks/trending-now/",
        "top_gainers": "stocks/top-gainers",
        "top_losers": "stocks/top-losers",
        "52_week_gainers": "stocks/52-week-gainers",
        "small_captial_stocks": "stocks/small-cap-stocks",
        "large_captial_stocks": "stocks/large-cap-stocks",
        "most_expensive_stocks": "stocks/most-expensive-stocks",
        "over_sold_stocks": "stocks/oversold-stocks",
        "pink_sheet_stocks": "stocks/pink-sheet-stocks",
        "overbought_stocks": "stocks/overbought-stocks",
        "all_time_high_stocks": "stocks/all-time-high-stocks",
        "unusual_volume_stocks": "stocks/unusual-volume-stocks",
        "highest_beta_stocks": "stocks/highest-beta-stocks",
    }

    category = category.lower()

    if category not in CATEGORY_MAP:
        return {
            "error": "Invalid category",
            "allowed": list(CATEGORY_MAP.keys())
        }
    url = BASE_URL + CATEGORY_MAP[category]

    params = {}

    if limit is not None:
        params["limit"] = limit

    if sort:
        params["sort"] = sort

    if order and order.lower() in ["asc", "desc"]:
        params["order"] = order.lower()

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": "Failed to fetch stock data",
            "details": str(e)
        }
