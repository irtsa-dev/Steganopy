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
```
python Steganopy.py [-h] [-v VALUES] [-i INFORMATION] [-o OUTPUT] [-k KEY] source action
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
  -i INFORMATION, --information INFORMATION
                        Information to be added when encrypting is selected for "action" argument. (default: None)
  -o OUTPUT, --output OUTPUT
                        Specifies output file name. (default: None)
  -k KEY, --key KEY     Specifies key to use for xor operation. (default: None)
```
#### Additional Notes: 
- The `-i` option is necessary if the `action` argument is set to **e** or **encrypt**
- The following are accepted file extensions: `png`, `jpg`, `webp`, `jpeg`
<br />
<br />
<br />
<br />
<br />
<br />

# Examples
```
python Steganopy.py exampleimage.png e -i "test text" -v r

- Will only utilize the red values in the image to put the information in.
```
```
python Steganopy.py exampleimage.png e -i "test text" -o "newname"

- Will output the file with the name "newname" instead of the default name of the original filename with -steganopy appended to it.
```
```
python Steganopy.py exampleimage-steganopy.png d -v r

- When decrypting, the values used in encryption must be the same, otherwise errors may be thrown.
```
