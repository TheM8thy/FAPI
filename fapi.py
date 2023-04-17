import requests
import argparse

class ValidateMethodsAction(argparse.Action):
        
    def __call__(self, parser, namespace, values, option_string=None):
        methods = list(dict.fromkeys(values[0].split(',')))
        if methods != 'all':
            for method in methods:
                if method.lower() not in ['get','post','put','delete']:
                    parser.error(f"argument -m/--method: invalid choice(s): '{methods}' (choose from 'get', 'post', 'put', 'delete' or choose 'all')")
        setattr(namespace, self.dest, methods)

def error(message):
    print(message)
    exit()

def do_get(url, default_testing_length, verbose):
    new_get_request = requests.get(url)
    get_response = new_get_request.text
    if len(get_response) > default_testing_length:
        print(f"GET - {str(len(get_response))} - {url} ")
    if verbose:
        print(str(len(get_response)) + "       " + url + " - GET")
    pass

def do_post(url, default_testing_length, verbose):
    new_post_request = requests.post(url, data="")
    post_response = new_post_request.text
    if len(post_response) > default_testing_length:
        print(f"POST - {str(len(post_response))} - {url}")
    if verbose:
        print(str(len(post_response)) + "       " + url + " - POST")
    pass

def do_put(url, default_testing_length, verbose):
    new_put_request = requests.put(url, data="")
    put_response = new_put_request.text
    if len(put_response) > default_testing_length:
        print(f"PUT - {str(len(put_response))} - {url}")
    if verbose:
        print(str(len(put_response)) + "       " + url + " - PUT")

def do_delete(url, default_testing_length, verbose):
    new_delete_request = requests.delete(url)
    delete_response = new_delete_request.text
    if len(delete_response) > default_testing_length:
        print(f"DELETE - {str(len(delete_response))} - {url}")
    if verbose:
        print(str(len(delete_response)) + "       " + url + " - DELETE")

def prepare_request(methods, url, default_testing_length, verbose):

    for method in methods:
        match method.lower():
            case 'get':
                do_get(url, default_testing_length, verbose)
            case 'post':
                do_post(url, default_testing_length, verbose)
            case 'put':
                do_put(url, default_testing_length, verbose)
            case 'delete':
                do_delete(url, default_testing_length, verbose)
            case 'all':
                do_all()
            case _:
                error(f"Fatal error, Invalid request method specified '{method}'")

def banner():
    print("""_____________________________________________________________________
Fuzz API (FAPI) v0.1
Developed by: arcan3, TheM8thy
Last updated: 17/04/2023
_____________________________________________________________________
""")

def fapi():

    banner()

    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=64)
    parser = argparse.ArgumentParser(formatter_class=formatter)
    parser.add_argument('-u', '--url', metavar='<example url>', type=str, help='Specify the target url after the -u flag.', nargs='+', required=True)
    parser.add_argument('-w', '--wordlist', metavar='<wordlist>', type=argparse.FileType('r'), help='Specify your chosen wordlist after the -w flag.', nargs=1, required=True)
    parser.add_argument('-m', '--method', action=ValidateMethodsAction, metavar='<method>', type=str, help='Specify the desired request methods, accepted methods are get,post,put,delete or all.', nargs=1, required=True)
    parser.add_argument('-dl', '--default_testing_length', metavar='', type=int, help='Specify the testing length thats tested against.', default=0, nargs=1)
    parser.add_argument('-ms', '--match_string', metavar='<string>', type=str, help='Match a specific string within the response text.', nargs='+')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--threading', metavar='<threads>', type=int, help='Specify number of threads to use.', nargs=1)
    group.add_argument('-mp', '--multiprocessing', metavar='<processes>', type=int, help='Specify number of processes to use.', nargs=1)
    parser.add_argument('--version', action='version', help='Show %(prog)s version number', version='%(prog)s 0.1')
    parser._actions[0].help='Display the help options.'
    args = parser.parse_args()
    urls : list = args.url
    wordlist = args.wordlist[0]
    methods : list = args.method
    default_testing_length : int = args.default_testing_length[0] if type(args.default_testing_length) is list else args.default_testing_length
    match_string : list = args.match_string
    verbose : bool = args.verbose
    

    print(f"URL: {','.join(urls)}")
    print(f"Methods: {','.join([x.upper() for x in methods])}")
    #print(args)

    if match_string:
        for string in match_string:
            print(f"Matching String: {string}")

    endpoints = wordlist.readlines()
 
    if args.verbose:
        print("Length - URL")

    for url in urls:
        for endpoint in [x for x in endpoints if x[0].strip() not in ['#','','/']]:
            request_url = f"{url}/{endpoint.strip()}"
            prepare_request(methods, request_url, default_testing_length, verbose)

fapi()
