"""
Improved Ticker Extractor with Expanded False Positive Filtering
Enhanced with common conversational words and regulatory terms
Updated March 2026 — added GME-era Reddit jargon and common false positives
identified from 2.5M mention dataset analysis.
"""
import re

class ImprovedTickerExtractor:
    """Extract stock tickers from text with better false positive filtering"""
    
    def __init__(self):
        self.blacklist = {
            # Single letters (except valid tickers)
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            
            # Common words/abbreviations
            'CEO', 'CFO', 'CTO', 'COO', 'ETF', 'IPO', 'NYSE', 'NASDAQ',
            'USA', 'NYC', 'FOR', 'AND', 'THE', 'BUT', 'NOT', 'YOU', 'ARE',
            'WAS', 'HIS', 'HER', 'ITS', 'OUR', 'THEIR', 'HAS', 'HAD', 'CAN',
            'MAY', 'WILL', 'DID', 'GET', 'GOT', 'NOW', 'NEW', 'OLD', 'BEST',
            'GOOD', 'BAD', 'BIG', 'TOP', 'ALL', 'ONE', 'TWO', 'MANY', 'SOME',
            'TO', 'DO', 'WHAT', 'WHY', 'HOW', 'WHO', 'WHEN', 'THAT', 'THIS',
            'THEN', 'THAN', 'THEM', 'THEY', 'THERE', 'THESE', 'THOSE',
            'US', 'UK', 'RRSP', 'FCF', 'DTE',
            
            # Common conversational words
            'HERE', 'START', 'RED', 'THINK', 'WIKI', 'SHARE', 'VIEWS', 
            'GUYS', 'ABOUT', 'MOVED', 'HAPPENED', 'SUDDENLY', 'KNOWLEDGE',
            'DISCUSS', 'WELCOME', 'HELLO', 'PLEASE', 'THANK', 'THANKS',
            'KNOW', 'MAKE', 'MADE', 'TAKE', 'SAID', 'SAYS', 'WOULD',
            'COULD', 'SHOULD', 'WANT', 'NEED', 'LIKE', 'LOOK', 'LOOKS',
            'GOING', 'DOES', 'DOING', 'DONE', 'COME', 'CAME', 'GONE',
            'SEEN', 'GIVE', 'GAVE', 'TOLD', 'TELL', 'KEEP', 'LEFT',
            'FELT', 'FIND', 'FOUND', 'CALL', 'ASKED', 'WORK', 'WORKS',
            'SEEM', 'SEEMS', 'HELP', 'HELPS', 'SHOW', 'SHOWS', 'TRYING',
            'MEANS', 'MEANT', 'READ', 'READS', 'NICE', 'HOPE', 'STOP',
            'BUY', 'SELL', 'LONG', 'SHORT', 'WAIT', 'MOVE', 'MOVES',
            
            # Reddit/Internet slang
            'WSB', 'DD', 'YOLO', 'FD', 'ER', 'IMO', 'IMHO', 'FOMO',
            'ATH', 'ATL', 'HOLD', 'HODL', 'MOON', 'EDIT', 'TLDR', 'ELI',
            
            # Financial/trading terms that aren't tickers
            'PUT', 'CALL', 'LEAP', 'OTM', 'ITM', 'IV', 'PE', 'EPS', 'EBITDA',
            'ROI', 'YTD', 'QOQ', 'YOY', 'EOD', 'AH', 'PM', 'EV',
            
            # Technical indicators
            'RSI', 'MACD', 'SMA', 'EMA', 'ATR', 'ADX', 'CCI', 'ROC', 'MFI',
            'OBV', 'VWAP', 'STOCH', 'PSAR', 'SAR', 'DMI', 'TRIX',
            
            # Economic indicators
            'GDP', 'CPI', 'PPI', 'PCE', 'NFP', 'PMI', 'ISM', 'VIX', 'DXY',
            'QE', 'ZIRP', 'NIRP', 'FOMC', 'ECB', 'BOJ', 'PBOC',
            
            # Indices & abbreviations
            'SP', 'DOW', 'DJ', 'NQ', 'RUT', 'SPX', 'NDX', 'DJI', 'RUI',
            
            # Currencies & commodities
            'USD', 'EUR', 'GBP', 'JPY', 'CHF', 'AUD', 'CAD', 'CNY', 'INR',
            'BTC', 'ETH', 'XRP', 'SOL', 'DOGE', 'SHIB',
            'GOLD', 'OIL', 'GAS', 'CRUDE', 'WTI', 'BRENT',
            
            # Financial structure terms
            'FTA', 'MOU', 'SPO', 'APO', 'ATM', 'SPAC', 'PIPE',
            'LBO', 'MBO', 'RTO', 'DCF', 'NPV', 'IRR', 'WACC',
            
            # Regulatory bodies
            'SEC', 'FTC', 'FCC', 'FDA', 'EPA', 'FBI', 'CIA', 'DOJ', 'IRS',
            'FINRA', 'POTUS', 'SCOTUS', 'CBOE', 'CFTC', 'OCC',
            'ESMA', 'CIRO', 'ASIC', 'FCA', 'IIROC', 'SEBI', 'BAFIN',
            'AMF', 'CONSOB', 'CSSF', 'FMA', 'DFSA',
            
            # Time/date related
            'EST', 'PST', 'GMT', 'UTC', 'JAN', 'FEB', 'MAR',
            'APR', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',
            'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN',
            
            # Common abbreviations
            'AI', 'ML', 'IT', 'HR', 'PR', 'IR', 'AR', 'VR', 'API', 'SDK',
            'SEO', 'FAQ', 'FYI', 'ASAP', 'BTW', 'ETA', 'TBA', 'TBD',
            
            # Media/news
            'WSJ', 'NYT', 'CNN', 'BBC', 'CNBC', 'FOX', 'MSNBC',
            
            # Generic business terms
            'LLC', 'INC', 'LTD', 'CORP', 'GROUP', 'HOLDINGS',
            
            # Numbers/math
            'ZERO', 'TEN', 'HUNDRED', 'MILLION', 'BILLION',
            
            # Directions/positions
            'UP', 'DOWN', 'HIGH', 'LOW', 'ABOVE', 'BELOW', 'NEAR', 'FAR',
            
            # Common Reddit mentions that aren't stocks
            'DYOR', 'NFA', 'LMAO', 'ROFL', 'WTF', 'OMG', 'FML', 'SMH',
            'LOL', 'LMFAO', 'GTFO', 'STFU', 'FWIW',
            
            # Misc common words
            'GREAT', 'JUST', 'ONLY', 'VERY', 'MUCH', 'MORE', 'LESS', 'MOST',
            'FIRST', 'LAST', 'NEXT', 'EACH', 'BOTH', 'FEW', 'OTHER', 'NEVER',
            'ALWAYS', 'OFTEN', 'MAYBE', 'BEEN', 'BEING', 'STILL', 'ALSO',
            'BACK', 'INTO', 'OVER', 'UNDER', 'AFTER', 'BEFORE',
            'DURING', 'UNTIL', 'WHILE', 'WHERE', 'WHICH', 'WHOM', 'WHOSE',
            'YES', 'NO', 'OKAY',
            
            # Academic/formal
            'PHD', 'MBA', 'CPA', 'CFA', 'DDS', 'ESQ', 'JD',
            
            # Tech terms
            'CLOUD', 'DATA', 'CODE', 'APP', 'WEB', 'NET', 'TECH', 'BOT',
            'HTTP', 'HTTPS', 'WWW', 'HTML', 'CSS', 'SQL', 'JSON', 'XML',
            
            # WSB-specific jargon
            'GUH', 'STONK', 'TENDIES', 'BAGHOLDER', 'DIAMOND', 'PAPER',
            'ROCKET', 'BRRRR', 'PRINTER', 'JPOW',
            
            # Historical events
            'WWI', 'WWII', 'WW',
            
            # Misc false positives
            'BELOW', 'LIST', 'EBT', 'TF', 'DM', 'OA', 'UMADA', 'BRAVO',
            'DSCR', 'VFIAX', 'VFSUX', 'EIA', 'RDDT',
            
            # Market structure terms
            'ATS', 'ECN', 'MTF', 'OTC', 'NBBO', 'SIP', 'TICK', 'LOT',
            'BID', 'ASK', 'MID', 'TWAP',
            
            # Price/rate related
            'APY', 'APR', 'RATE', 'RATES', 'YIELD', 'PIPS',
            
            # Medical/pharma terms
            'COVID', 'CDC', 'NIH',
            
            # Trading platforms
            'TRADE', 'ETRADE', 'ROBIN', 'HOOD',
            
            # Generic product terms
            'CBD', 'THC', 'WEED', 'POT',

            # ── NEW: GME-era Reddit jargon (identified from 2.5M dataset) ────
            # These appeared in top tickers but are NOT stocks:

            # GME/Superstonk movement terms
            'DRS',      # Direct Registration System — GME shareholder movement
            'MOASS',    # Mother Of All Short Squeezes — WSB slogan
            'DTCC',     # Depository Trust & Clearing Corporation — not a stock
            'NSCC',     # National Securities Clearing Corporation
            'PFOF',     # Payment For Order Flow — industry term
            'SHRG',     # Sometimes used as shorthand, unreliable
            'FTD',      # Failure To Deliver — market mechanic term
            'SI',       # Short Interest — metric, not ticker (also Singapore)
            'CTB',      # Cost To Borrow — options term
            'HTB',      # Hard To Borrow — options term
            'SLD',      # Sold — past tense verb picked up as ticker

            # Ambiguous 2-letter terms from dataset
            'IS',       # Too common as English word
            'RH',       # Robinhood app reference, not RH Inc stock
            'RC',       # Ryan Cohen (GME chairman) — person not ticker
            'DFV',      # DeepFuckingValue — WSB user, not a ticker
            'PP',       # common abbreviation
            'OP',       # "original poster" on Reddit
            'GG',       # "good game" — gaming slang used in WSB
            'GL',       # "good luck"
            'HL',       # ambiguous
            'MS',       # ambiguous — Morgan Stanley sometimes but mostly noise
            'CS',       # ambiguous — Credit Suisse sometimes but mostly noise
            'GO',       # common word
            'HI',       # greeting
            'NO',       # common word
            'OK',       # common word
            'SO',       # common word
            'IF',       # common word
            'AS',       # common word
            'AT',       # common word
            'BY',       # common word
            'IN',       # common word
            'OF',       # common word
            'ON',       # common word
            'OR',       # common word
            'BE',       # common word
            'AN',       # common word
            'MY',       # common word
            'HE',       # common word
            'ME',       # common word
            'WE',       # common word
            'IT',       # common word (also IT sector abbreviation)

            # Additional Reddit/finance slang
            'BTFD',     # Buy The F***ing Dip
            'BTFP',     # Bank Term Funding Program (Fed facility, not a stock)
            'HTF',      # High Time Frame (trading term)
            'LTF',      # Low Time Frame
            'HTM',      # Held To Maturity (accounting term)
            'AFS',      # Available For Sale (accounting term)
            'MBS',      # Mortgage Backed Securities
            'CDO',      # Collateralized Debt Obligation
            'CDS',      # Credit Default Swap
            'HFT',      # High Frequency Trading
            'PFOF',     # Payment For Order Flow
            'NMS',      # National Market System
            'REG',      # Regulation — common abbreviation
            'SUB',      # Subreddit reference
            'MOD',      # Moderator reference
            'FAQ',      # Frequently Asked Questions
            'PSA',      # Public Service Announcement
            'TIL',      # Today I Learned
            'AMA',      # Ask Me Anything
            'ETA',      # Estimated Time of Arrival
            'EOW',      # End of Week
            'EOM',      # End of Month
            'EOY',      # End of Year
            'YE',       # Year End
            'QE',       # Quantitative Easing (already above, kept for clarity)
            'TA',       # Technical Analysis
            'FA',       # Fundamental Analysis
            'PA',       # Price Action
            'PB',       # Price to Book
            'PS',       # Price to Sales — also common abbreviation
            'PEG',      # Price/Earnings to Growth ratio
            'NAV',      # Net Asset Value
            'AUM',      # Assets Under Management
            'MER',      # Management Expense Ratio
            'TER',      # Total Expense Ratio
            'VGT',      # This IS a real ETF — remove from blacklist if needed
        }

        # Remove VGT from blacklist — it's a real Vanguard ETF
        self.blacklist.discard('VGT')
        
        # Known valid single-letter tickers
        self.valid_single_letters = {'F', 'C'}  # Ford, Citigroup
        
        # Pattern to match potential tickers
        self.ticker_pattern = re.compile(r'\b[A-Z]{1,5}\b')
    
    def extract_tickers(self, text):
        if not text:
            return set()
        
        potential_tickers = self.ticker_pattern.findall(text)
        
        valid_tickers = set()
        for ticker in potential_tickers:
            if ticker in self.blacklist:
                continue
            if len(ticker) == 1 and ticker not in self.valid_single_letters:
                continue
            if all(c in 'AEIOU' for c in ticker):
                continue
            valid_tickers.add(ticker)
        
        return valid_tickers
    
    def is_likely_ticker(self, ticker):
        if not ticker or len(ticker) > 5:
            return False
        if ticker in self.blacklist:
            return False
        if len(ticker) == 1 and ticker not in self.valid_single_letters:
            return False
        if all(c in 'AEIOU' for c in ticker):
            return False
        return True


def extract_tickers(text):
    extractor = ImprovedTickerExtractor()
    return extractor.extract_tickers(text)


if __name__ == "__main__":
    extractor = ImprovedTickerExtractor()
    print(f"Blacklist contains {len(extractor.blacklist)} terms\n")
    
    test_texts = [
        "I bought AAPL and TSLA yesterday. TO THE MOON!",
        "DRS your shares for MOASS! RC is the man!",
        "GME is the play, RH is screwing us with PFOF",
        "The RSI indicator shows oversold conditions on GME",
        "NVDA and AMD both look good this quarter",
        "IS this the way? RC says DRS everything",
    ]
    
    print("Testing updated extractor:\n")
    for text in test_texts:
        tickers = extractor.extract_tickers(text)
        print(f"Input:   {text}")
        print(f"Tickers: {tickers}\n")