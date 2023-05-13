# pylint: disable=line-too-long,C0114

import argparse
import sys
import requests
import threading

thread_responses = []

def validatemethod(value):
    r"""Validates the methods passed into the script via the -m parameter
    """

    methods = list(dict.fromkeys(value.split(',')))
    if methods[0] == 'all':
        return ['get', 'post', 'delete', 'put']
    for method in methods:
        if method.lower() not in ['get','post','put','delete']:
            raise argparse.ArgumentTypeError(f"argument -m/--method: invalid choice(s): '{methods}' (choose from 'get', 'post', 'put', 'delete' or choose 'all')")
    return methods

def formatter(prog):
    r"""Formats the help display of the script to have a certain width
    """

    return argparse.HelpFormatter(prog, max_help_position=64)

def error(message):
    r"""Is called whenever an error is handled by the script

    :param message: Error message to be printed.
    """

    print(message)
    sys.exit()

def chunk_list(list_to_chunk : list, num_chunks : int):
    r"""Splits a list into a given number of chunks up

    :param list_to_chunk: The list to be chunked.
    :param num_chunks: The number of chunks.
    """
    return [list_to_chunk[x:x+len(list_to_chunk)//num_chunks if len(list_to_chunk)//num_chunks > 1 else x+num_chunks] for x in range(0, len(list_to_chunk), len(list_to_chunk)//num_chunks if len(list_to_chunk)//num_chunks > 1 else num_chunks)]


def process_response(request, match_string, default_testing_length, verbose):
    r"""Processes the response of the selected method and print it out

    :param request: The request's:class:`Response <Response>` object.
    :param default_testing_length: The default_testing_length that is tested against.
    :param verbose: Enable/disable verbose output.
    :param match_string: The string to match within the response text.
    """

    response = request.text
    if match_string is not None:
        for string in match_string:
            if string in response:
                print(f"[+] {request.request.method} - \"{str(string)}\" detected: {request.request.url}")

    if len(response) != default_testing_length:
        print(f"[+] {request.request.method} - Different response length: {str(len(response))} - {request.request.url} ")
    if verbose:
        print(f"[VERBOSE] {request.request.method} {str(len(response))}       {request.request.url}")

def prepare_request(methods : list, url : str, match_string : str, timeout : float, default_testing_length : int, verbose : bool, ignore_ssl_verification : bool):
    r"""Prepare the requests to be sent

    :param methods: The methods set for the current URL.
    :param url: The current URL to be reqquested.
    :param default_testing_length: The default_testing_length that is tested against.
    :param verbose: Enable/disable verbose output.
    :param timeout: The amount of seconds after a request times out.
    :param ignore_ssl_verification: Ignore SSL verification.
    :param match_string: The string to match within the response text.
    """

    for method in methods:
        try:
            request = requests.request(method, url, timeout=timeout, verify=ignore_ssl_verification)
            process_response(request, match_string, default_testing_length, verbose)
        except requests.ConnectTimeout:
            print(f"[Verbose] {method} - Connection timed out - {url}")

def banner() -> None:
    r"""Prints the banner at the start of the script
    """

    print("""_____________________________________________________________________
FAPI - API endpoint fuzzer v0.1
Developed by: arcan3, TheM8thy
Last updated: 27/04/2023
_____________________________________________________________________
""")

def thread_request(methods : list, url : str, endpoints : list, match_string : str, timeout : float, default_testing_length : int, verbose : bool, ignore_ssl_verification : bool, thread_num : int):
    
    global thread_responses

    for endpoint in endpoints:
        for method in methods:
            try:
                request = requests.request(method, f"{url}/{endpoint.strip()}", timeout=timeout, verify=ignore_ssl_verification)
                thread_responses[thread_num].append(request)
            except requests.ConnectTimeout:
                print(f"[Verbose] {method} - Connection timed out - {url}")

def fapi():
    r"""Main function
    """

    global thread_responses

    banner()

    parser = argparse.ArgumentParser(formatter_class=formatter)
    parser.add_argument('-u', '--url', metavar='<example url>', type=str, help='Specify the target url after the -u flag.', nargs='+', required=True)
    parser.add_argument('-w', '--wordlist', metavar='<wordlist>', type=argparse.FileType('r'), help='Specify your chosen wordlist after the -w flag.', nargs=1, required=True)
    parser.add_argument('-m', '--method', metavar='<method>', type=validatemethod, help='Specify the desired request methods, accepted methods are get,post,put,delete.', nargs=1, required=True)
    parser.add_argument('-dl', '--default_testing_length', metavar='', type=int, help='Specify the testing length thats tested against.', default=0, nargs=1)
    parser.add_argument('-ms', '--match_string', metavar='<string>', type=str, help='Match a specific string within the response text.', nargs='+')
    parser.add_argument('-t', '--timeout', metavar='<seconds>', type=float, help='Specify the amount of seconds before a request times out, defaults to 5', default=5)
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('-k', '--ignore_certificates', action='store_false', help='Ignore SSL certificate verification.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-th', '--threading', metavar='<threads>', type=int, help='Specify number of threads to use.', nargs=1)
    group.add_argument('-mp', '--multiprocessing', metavar='<processes>', type=int, help='Specify number of processes to use.', nargs=1)
    parser.add_argument('--version', action='version', help='Show %(prog)s version number', version='%(prog)s 0.1')
    parser._actions[0].help='Display the help options.' # pylint: disable=W0212
    args = parser.parse_args()

    urls : list = args.url
    wordlist = args.wordlist[0]
    methods : list = args.method[0]
    default_testing_length : int = args.default_testing_length[0] if isinstance(args.default_testing_length,list) else args.default_testing_length
    match_string : list = args.match_string
    timeout : float = args.timeout
    verbose : bool = args.verbose
    ignore_certificates : bool = args.ignore_certificates
    thread_num : int = args.threading

    print(f"URL: {','.join(urls)}")
    print(f"Methods: {','.join([x.upper() for x in methods])}")

    if match_string:
        for string in match_string:
            print(f"Matching String: {string}")

    endpoints = wordlist.readlines()

    if verbose:
        print("Length - URL\n")
    else:
        print("\n")

    endpoints = [x for x in endpoints if x[0].strip() not in ['#','','/']]

    print(args)

    if thread_num:
        threads = []
        thread_responses = [ [] for _ in range(thread_num[0]) ]
        chunked_list = chunk_list(endpoints, thread_num[0])
        for current_thread in range(thread_num[0]):
            thread = threading.Thread(target=thread_request, args=(methods, urls[0], chunked_list[current_thread], match_string, timeout, default_testing_length, verbose, ignore_certificates, current_thread))
            threads.append(thread)
            thread.start()
    else:
        for url in urls:
            for endpoint in endpoints:
                request_url = f"{url}/{endpoint.strip()}"
                prepare_request(methods, request_url, match_string, timeout, default_testing_length, verbose, ignore_certificates)

fapi()
print(thread_responses)