import requests
import argparse

class ValidateMethodsAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        methods = list(dict.fromkeys(values[0].split(',')))
        if methods[0] != 'all':
            for method in methods:
                if method.lower() not in ['get','post','put','delete']:
                    parser.error(f"argument -m/--method: invalid choice(s): '{methods}' (choose from 'get', 'post', 'put', 'delete' or choose 'all')")
        else:
            methods = ['get', 'post', 'delete', 'put']
        setattr(namespace, self.dest, methods)

def error(message):

    print(message)
    exit()

def process_response(request, match_string, default_testing_length, verbose):

    response = request.text
    if match_string != None:
        for string in match_string:
            if string in response:
                print(f"[+] {request.request.method} - \"{str(string)}\" detected: {request.request.url}")

    if len(response) != default_testing_length:
        print(f"[+] {request.request.method} - Different response length: {str(len(response))} - {request.request.url} ")
    if verbose:
        print(f"[VERBOSE] {request.request.method} {str(len(response))}       {request.request.url}")
    pass

def prepare_request(methods, url, default_testing_length, verbose, ignore_ssl_verification, match_string):

    for method in methods:
        request = requests.request(method, url, verify=ignore_ssl_verification)
        process_response(request, match_string, default_testing_length, verbose)

def banner():

    print("""_____________________________________________________________________
FAPI - API endpoint fuzzer v0.1
Developed by: arcan3, TheM8thy
Last updated: 21/04/2023
_____________________________________________________________________
""")

def fapi():

    banner()

    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=64)
    parser = argparse.ArgumentParser(formatter_class=formatter)
    parser.add_argument('-u', '--url', metavar='<example url>', type=str, help='Specify the target url after the -u flag.', nargs='+', required=True)
    parser.add_argument('-w', '--wordlist', metavar='<wordlist>', type=argparse.FileType('r'), help='Specify your chosen wordlist after the -w flag.', nargs=1, required=True)
    parser.add_argument('-m', '--method', action=ValidateMethodsAction, metavar='<method>', type=str, help='Specify the desired request methods, accepted methods are get,post,put,delete.', nargs=1, required=True)
    parser.add_argument('-dl', '--default_testing_length', metavar='', type=int, help='Specify the testing length thats tested against.', default=0, nargs=1)
    parser.add_argument('-ms', '--match_string', metavar='<string>', type=str, help='Match a specific string within the response text.', nargs='+')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('-k', '--ignore_certificates', action='store_false', help='Ignore SSL certificate verification.')
    #group = parser.add_mutually_exclusive_group(required=True)
    #group.add_argument('-t', '--threading', metavar='<threads>', type=int, help='Specify number of threads to use.', nargs=1)
    #group.add_argument('-mp', '--multiprocessing', metavar='<processes>', type=int, help='Specify number of processes to use.', nargs=1)
    parser.add_argument('--version', action='version', help='Show %(prog)s version number', version='%(prog)s 0.1')
    parser._actions[0].help='Display the help options.'
    args = parser.parse_args()
    urls : list = args.url
    wordlist = args.wordlist[0]
    methods : list = args.method
    default_testing_length : int = args.default_testing_length[0] if type(args.default_testing_length) is list else args.default_testing_length
    ignore_ssl_verification = args.ignore_certificates
    match_string : list = args.match_string
    verbose : bool = args.verbose

    print(f"URL: {','.join(urls)}")
    print(f"Methods: {','.join([x.upper() for x in methods])}")

    if match_string:
        for string in match_string:
            print(f"Matching String: {string}")

    endpoints = wordlist.readlines()

    if args.verbose:
        print("Length - URL\n")
    else:
        print("\n")

    for url in urls:
        for endpoint in [x for x in endpoints if x[0].strip() not in ['#','','/']]:
            request_url = f"{url}/{endpoint.strip()}"
            prepare_request(methods, request_url, default_testing_length, verbose, ignore_ssl_verification, match_string)

fapi()
