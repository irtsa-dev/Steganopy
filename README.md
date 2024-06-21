![PyPI](https://img.shields.io/pypi/v/idev-steganopy) ![Python](https://img.shields.io/pypi/pyversions/idev-steganopy)
# **Steganopy**
A [**python**](https://www.python.org) script for hiding text into images (**steganography**).
<br />
<br />
<br />
<br />
​<br />
# Installation
With `git` [GitHub](https://github.com):
```
git clone https://github.com/irtsa-dev/Steganopy.git
```
With `pip` [PyPi](https://pypi.org/project/idev-steganopy/)
```
pip install idev-steganopy
```
<br />
<br />
<br />
<br />
<br />
<br />

# Usage
<br />
<br />

### Within the CMD/Terminal
If installed with **GIT**:
```
python steganopy.py [-h] {encrypt,decrypt} ...
```
If installed with **PIP**:
```
steganopy [-h] {encrypt,decrypt} ...
```
<br />

Utilize `-h` or `--help` parameter for additional help.
```
usage: steganopy [-h] {encrypt,decrypt} ...

positional arguments:
  {encrypt,decrypt}

options:
  -h, --help         show this help message and exit
```
```
usage: steganopy encrypt [-h] [-t TEXT] [-f FILE] [-v VALUES] [-e ENCODING] [-k KEY] [-o OUTPUT] source

positional arguments:
  source                Picture source location.

options:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text to be added for encryption (cannot be used with --file).
  -f FILE, --file FILE  File location of text to be added when encrypting (cannot be used with --text).
  -v VALUES, --values VALUES
                        Values to be used for encryption.
  -e ENCODING, --encoding ENCODING
                        Specifies the base the information is to be encoded in.
  -k KEY, --key KEY     Specifies key to use for xor operation.
  -o OUTPUT, --output OUTPUT
                        Specifies output file name.
```
```
usage: steganopy decrypt [-h] [-v VALUES] [-e ENCODING] [-k KEY] [-o OUTPUT] source

positional arguments:
  source                Picture source location.

options:
  -h, --help            show this help message and exit
  -v VALUES, --values VALUES
                        Values to be used for decryption.
  -e ENCODING, --encoding ENCODING
                        Specifies the base the information is encoded in.
  -k KEY, --key KEY     Specifies key to use for xor operation.
  -o OUTPUT, --output OUTPUT
                        Specifies output file name.
```
#### Additional Notes: 
- The following are accepted file extensions: `png`, `jpg`, `webp`, `jpeg`
- The following are accepted encoding bases: `binary`, `trinary`, `quaternary`, `quinary`, `senary`, `septenary`, `octal`, `nonal`
<br />
<br />
<br />
<br />
<br />
<br />

# Examples
```
steganopy encrypt exampleimage.png -t "test text" -v r

- Will only utilize the red values in the image to put the information in.
```
```
steganopy encrypt exampleimage.png -t "test text" -o "newname"

- Will output the file with the name "newname" instead of the default name of the original filename with -steganopy appended to it.
```
```
steganopy encrypt exampleimage.png -f exampletext.txt

- Will get text from the exampletext.txt file to use.
```
```
steganopy encrypt exampleimage.png -e trinary

- Will encode the information in base 3 (trinary) instead of the default of binary.
```
```
steganopy decrypt exampleimage-steganopy.png -v r

- When decrypting, the values used in encryption must be the same, otherwise errors may be thrown.
```
```
steganopy decrypt exampleimage-steganopy.png -v r -o test

- When decrypting, you can also use the -o --output argument to have the information be outputed into the a text document with the specified name.
```
