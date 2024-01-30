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
git clone https://github.com/IrtsaDevelopment/Steganopy.git
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
python Steganopy.py [-h] [-v VALUES] [-t TEXT] [-f FILE] [-o OUTPUT] [-k KEY] source action
```
If installed with **PIP**:
```
steganopy [-h] [-v VALUES] [-t TEXT] [-f FILE] [-o OUTPUT] [-k KEY] source action
```
<br />

Utilize `-h` or `--help` parameter for additional help.
```
positional arguments:
  source                Picture source location.
  action                Specifies whether to be encrypting or decrypting.

options:
  -h, --help            show this help message and exit
  -v VALUES, --values VALUES
                        Values used for encryption. (default: rgb)
  -t TEXT, --text TEXT  Text to be added when encrypting is selected for "action" argument. (default: None)
  -f FILE, --file FILE  File location of text to be added when encrypting is selected for "action" argument. (default:
                        None)
  -o OUTPUT, --output OUTPUT
                        Specifies output file name. (default: None)
  -e ENCODING, --encoding ENCODING
                        Specifies the base the information is to be or is encoded in. (default: binary)
  -k KEY, --key KEY     Specifies key to use for xor operation. (default: None)
```
#### Additional Notes: 
- The `-t` or `-f` option is necessary if the `action` argument is set to **e** or **encrypt**
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
steganopy exampleimage.png e -t "test text" -v r

- Will only utilize the red values in the image to put the information in.
```
```
steganopy exampleimage.png e -t "test text" -o "newname"

- Will output the file with the name "newname" instead of the default name of the original filename with -steganopy appended to it.
```
```
steganopy exampleimage.png e -f exampletext.txt

- Will get text from the exampletext.txt file to use.
```
```
steganopy exampleimage.png e -e trinary

- Will encode the information in base 3 (trinary) instead of the default of binary.
```
```
steganopy exampleimage-steganopy.png d -v r

- When decrypting, the values used in encryption must be the same, otherwise errors may be thrown.
```
```
steganopy exampleimage-steganopy.png d -v r -o test

- When decrypting, you can also use the -o --output argument to have the information be outputed into the a text document with the specified name.
```
