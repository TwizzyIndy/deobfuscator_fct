"""
The code below is a deobfuscator for python code obfuscated by freecodingtools.org
https://freecodingtools.org/py-obfuscator

by TwizzyIndy (https://github.com/TwizzyIndy) - 2024 Oct
"""

import zlib
import base64
import re
import argparse


def extractReverseBase64(fileContent: str):
    # get a string between (b' and '))
    search = re.search(r"\(b'(.*?)'\)\)", fileContent)
    if search is not None:
        reversedB64 = search.group(0)

        reversedB64 = reversedB64[3:-3]
        return reversedB64

def deofuscate(reversedBase64):
    # Python obfuscation by freecodingtools.org
    base64Str = reversedBase64[::-1]
    plain = zlib.decompress(base64.b64decode(base64Str))
    plainText = plain.decode('utf-8')

    count = 0

    foundPlainPython = False

    while True:
        if plainText.startswith('\n#'):
            break

        if plainText.startswith('import '):
            foundPlainPython = True
            break

        # get base64 string between two single quotes
        search = re.search(r"'(.*?)'", plainText)
        if search is not None:
            base64StrRev = search.group(0)

            base64Str = base64StrRev[::-1]

            compressBytes = base64.b64decode(base64Str)

            count += 1

            plainText = zlib.decompress(compressBytes)

            plainText = plainText.decode('utf-8')
            
            print(f'count: {count}')
        else:
            break

    print('last line')
    
    if plainText.startswith('\n#'):
       plainText = extractReverseBase64(plainText)
       deofuscate(plainText)
    
    if foundPlainPython:
        open('deobfuscated.py', 'w').write(plainText)

    print('done')

def main():
    argparser = argparse.ArgumentParser(
        description='Deobfuscate obfuscated python code generated by freecodingtools.org by TwizzyIndy')

    argparser.add_argument('file', help='Path to the obfuscated python file')

    args = argparser.parse_args()

    with open(args.file, 'r') as f:
        pyFile = f.read()

        reversedB64 = extractReverseBase64(pyFile)

        deofuscate(reversedB64)


if __name__ == '__main__':
    main()