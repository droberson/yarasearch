#!/usr/bin/env python3

""" yarasearch.py -- by Daniel Roberson @dmfroberson 10/2017

This searches a file or directory for files with positive hits to
pre-defined yara rules.


The MIT License

Copyright (c) 2017 Daniel Roberson

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

import os
import sys
import argparse
import yara
import magic


def main():
    """yarasearch.py entry point"""

    description = "example: ./yarasearch.py --path /mnt/smb --rules rules.d/"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-p",
                        "--path",
                        default="/mnt",
                        help="File or directory to scan")
    parser.add_argument("-r",
                        "--rules",
                        default="/etc/yarasearch.rules.d",
                        help="File or directory containing yara rules")
    parser.add_argument("-t",
                        "--timeout",
                        type=int,
                        default=60,
                        required=False,
                        help="Seconds to analyze a file before timing out")
    args = parser.parse_args()

    print("[+] yarasearch.py -- by Daniel Roberson")
    print()

    if not os.path.isdir(args.rules): # Read single rule file
        try:
            rules = yara.compile(args.rules)
        except yara.SyntaxError as err:
            print("[-] Syntax error in rule file %s: %s" % (args.path, err))
            print("[-] Exiting.")
            return os.EX_USAGE
    else: # Read every file in the directory as rules
        print("[-] Directory support not implemented yet")
        return os.EX_USAGE

    print("[+] Scanning files in %s" % args.path)
    filecount = 0
    hits = 0

    for root, _, files in os.walk(args.path):
        for filename in files:
            filecount += 1
            try_file = os.path.join(root, filename)

            m = magic.open(magic.NONE)
            m.load()
            magic_type = m.file(try_file)
            m.close()

            try:
                matches = rules.match(try_file, timeout=args.timeout)
                if matches:
                    hits += 1
                    print("  [+] %s" % os.path.realpath(try_file))
                    print("      Matches rule: %s" % str(matches).strip("[]"))
                    print("      File type:    %s" % magic_type)
            except yara.TimeoutError:
                print("  [-] %s" % os.path.realpath(try_file))
                print("      Timed out after %d seconds" % args.timeout)
                print("      File type: %s" % magic_type)

    print()
    print("[+] %d files scanned, %d hits." % (filecount, hits))

    return os.EX_OK


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("[-] Caught ^C. Exiting.")
        sys.exit(os.EX_USAGE)
