import argparse as ap

def Parse(*args):
    # Top parser
    parser = ap.ArgumentParser(prog="money",description="A toolkit for retrieving CNN Money Market webpage data.")
    
    # Application parsers
    subParser = parser.add_subparsers(dest='app',help="Application to be executed.")
    storyParser = subParser.add_parser('story',help="The money markets story application.",description="Retrieve story data from Money Markets webpage.")  
    stockParser = subParser.add_parser('stock',help="The money makets stock application.",description="This application retrieves stock data.")
    currencyParser = subParser.add_parser('money',help="The money markets currency application.",description="This application returns currency information for a specified denomination. The default behavior is to print out the valuation of top 7 currencies listed on the page.")
    
    status = parser.add_argument("--status",action="store_true",help="Check the status to the url used by a specified app. Returns ('Ok','Not connected') for ok status code and last updated time if available.")

    # File arguments
    suppress = parser.add_argument("-s","--suppress",action="store_true",help="Suppress stdout. Write data as file to /<program_directory>/data/*.<format> (Default format is json).")

    # Data arguments
    img = parser.add_argument("-i","--image",dest='img',action="store_true",help="Return image data from speficied app.")

    # Format arguments
    _format = parser.add_argument('-f',"--format",nargs=1,default=['json'],help="Write data to stdout or a file in specified format (Default is json). See docs for valid types.")

    # Stock arguments
    overview = stockParser.add_argument('--overview',action="store_true",help='Return market overview data containing top 3 indexes for US.')
    keystats = stockParser.add_argument('--key-stats',dest="keystats",action="store_true",help="Returns top 30 DOW Jones index data.")
    hot = stockParser.add_argument('--hot',action='store_true',help="Returns the hot stocks: Most Active, Gainers, Losers.")
    USindex = stockParser.add_argument('--US-index','--US','-U',dest="usindex",nargs=1,default=None,help="Add a specific US index to output.")
    
    # Story arguments
    frontpage = storyParser.add_argument('--front-page',dest="frontpage",action='store_true',help="Return the front page news story headliners.")
    investing = storyParser.add_argument('--investing',action='store_true',help="Return the top investing story headliners.")
    expanded = storyParser.add_argument('-e',dest='indices',nargs=2,help="Expand each story within start and end index and return the full article.")
    
    # Money arguments
    _from = currencyParser.add_argument("base",type=str,help="Base currency.")
    _to = currencyParser.add_argument("to",type=str,help="Currency to convert to.")
    amount = currencyParser.add_argument("--amount",'-a',dest="amt",default=1.0,nargs=1,type=float,help="Amount of base currency to convert. Default 1 base currency unit.")

    collection = ap.Namespace()  
    if not(args is None):
        collection = parser.parse_args(*args)
    else:
        collection = parser.parse_args()
    
    if not(collection.format[0] in {'txt','json','table'}):
        raise ap.ArgumentError(_format,f"'{collection.format}' not a valid stdout format. Expected 'txt','json' or 'table'.")
    
    if collection.app is None:
        raise ap.ArgumentError(subParser,"Application is required. See 'money -h' for usage.")
    
    return collection