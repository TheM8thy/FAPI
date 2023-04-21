# Fuzz API (FAPI) - A fuzzer for API's
**Developed by:** arcan3, TheM8thy
**Version**: 0.1
**Last updated:** 17/04/2023
**Status**: Active Development

### About FAPI
FAPI is an API endpoint fuzzer, once a wordlist has been selected it'll send a request to each possible endpoint using various request methods (POST, GET, PUT and DELETE) and then look for differences within the responses.

### Usage Example
`console[~/fapi/]: python3 fapi.py -u https://api.target.com/api/ -w /opt/wordlists/api-endpoints.txt -m get,post -dl 2 -ms parameter`


### Help Output
```
usage: fapi.py [-h] -u <example url> [<example url> ...] -w <wordlist> -m <method> [-dl]
               [-ms <string> [<string> ...]] [-v] [-k] [--version]

options:
  -h, --help                                                    Display the help options.
  -u <example url> [<example url> ...], --url <example url> [<example url> ...]
                                                                Specify the target url after the -u
                                                                flag.
  -w <wordlist>, --wordlist <wordlist>                          Specify your chosen wordlist after the
                                                                -w flag.
  -m <method>, --method <method>                                Specify the desired request methods,
                                                                accepted methods are
                                                                get,post,put,delete or all.
  -dl , --default_testing_length                                Specify the testing length thats tested
                                                                against.
  -ms <string> [<string> ...], --match_string <string> [<string> ...]
                                                                Match a specific string within the
                                                                response text.
  -v, --verbose                                                 Verbose mode
  -k, --ignore_certificates                                     Ignore SSL certificate verification.
  --version                                                     Show fapi.py version number

```
