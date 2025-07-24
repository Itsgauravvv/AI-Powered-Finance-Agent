from nsepython import nse_eq

def get_stock_market_overview(symbol: str) -> dict:
    """
    Provides a market overview for a given NSE stock symbol.
    Includes current price, market cap, 52-week high/low, and P/E ratio.
    """
    try:
        data = nse_eq(symbol)
        if not data or 'priceInfo' not in data:
            return {"error": f"Could not retrieve data for symbol {symbol}. It might be an invalid symbol."}

        price_info = data.get('priceInfo', {})
        security_info = data.get('securityInfo', {})
        info = data.get('info', {})
        metadata = data.get('metadata', {})
        
        market_cap_str = "Data unavailable"
        last_price = price_info.get('lastPrice')
        issued_size = security_info.get('issuedSize')

        if last_price is not None and issued_size is not None:
            market_cap_value = (last_price * issued_size) / 10_000_000
            market_cap_str = f"{market_cap_value:,.2f}"

        return {
            "Symbol": info.get('symbol'),
            "Company Name": info.get('companyName'),
            "Current Price": price_info.get('lastPrice'),
            "Change": price_info.get('change'),
            "% Change": price_info.get('pChange'),
            "52 Week High": price_info.get('weekHighLow', {}).get('max'),
            "52 Week Low": price_info.get('weekHighLow', {}).get('min'),
            "Market Cap (Cr)": market_cap_str,
            "P/E Ratio": metadata.get('pdSymbolPe'),
        }
    except Exception as e:
        return {"error": f"An error occurred while fetching stock overview for {symbol}: {e}"}

stock_analyst_tools = [get_stock_market_overview]