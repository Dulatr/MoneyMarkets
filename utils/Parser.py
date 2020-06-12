import argparse as ap

def Parse(*args):
    parser = ap.ArgumentParser(prog="money",description="A toolkit for retrieving CNN Money Market webpage data.")

    # File arguments
    suppress = parser.add_argument("--suppress","-s",action="store_true",help="Write data as file to /<program_directory>/data/*.json")

    # Data arguments
    app = parser.add_argument("app",default=["stock"],nargs='*',help="Return story/stock/currency data from webpages (Default is stock).")
    img = parser.add_argument("--image","-i",dest='img',action="store_true",help="Return image data from speficied app.")

    # Format arguments
    _format = parser.add_argument("--format",'-f',nargs=1,default='json',help="Write data to stdout or a file in specified format (Default is json). See docs for valid types.")

    collection = ap.Namespace()  
    if not(args is None):
        collection = parser.parse_args(*args)
    else:
        collection = parser.parse_args()
    
    if len(collection.app) > 3:
        raise ap.ArgumentError(app,f"Too many applications listed. {len(collection.app)} found, expected at most 3.")
    for application_listed in collection.app:
        if not(application_listed in {'story', 'stock', 'currency'}):
            raise ap.ArgumentError(app,f"'{application_listed}' not a valid application process."+
                "\nCheck documentation or type 'money -h' for help.")
    
    if not(collection.format in {'txt','json','table'}):
        raise ap.ArgumentError(_format,f"'{collection.format}' not a valid stdout format. Expected 'txt','json' or 'table'.")

    return collection