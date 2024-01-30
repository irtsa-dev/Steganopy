#Imports
import argparse

from os import path
from PIL import Image
from tqdm import tqdm
from PyTermColor.Color import printColor






#Parser Declarations
SteganopyParser = argparse.ArgumentParser(description="", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

SteganopyParser.add_argument('source', help = 'Picture source location.')
SteganopyParser.add_argument('action', help = 'Specifies whether to be encrypting or decrypting.')

SteganopyParser.add_argument('-v', '--values', help = 'Values used for encryption.', default = 'rgb')
SteganopyParser.add_argument('-t', '--text', help = 'Text to be added when encrypting is selected for "action" argument.')
SteganopyParser.add_argument('-f', '--file', help = 'File location of text to be added when encrypting is selected for "action" argument.')
SteganopyParser.add_argument('-o', '--output', help = 'Specifies output file name.')
SteganopyParser.add_argument('-e', '--encoding', help = 'Specifies the base the information is to be or is encoded in.', default = 'binary')
SteganopyParser.add_argument('-k', '--key', type = int,  help = 'Specifies key to use for xor operation.')






#Functions
def error(errorType: str, value: str):
    print('\n')
    printColor(errorType, 'red', end = ': ')
    printColor(value, 'lightyellow')
    quit()



def baseConvert(number: int, base: int):
    if number == 0: return '0'
    
    digits = []
    while number:
        digits.append(int(number % base))
        number //= base
    return ''.join([str(i) for i in digits[::-1]])


def expandKey(key: int, length: int, base: int) -> str:
    if key < 2: error('ValueError', 'Argument "key" must be greater than 2.')
    while len(baseConvert(key, base)) < length: key *= key
    return baseConvert(key, base)[0:length]



def testArgument(argument: str, value: str):
    AcceptedArguments = {'action' : ('e', 'encrypt', 'd', 'decrypt'), 'values' : ('r', 'g', 'b'), 'encoding' : ('binary', 'trinary', 'quaternary', 'quinary', 'senary', 'septenary', 'octal', 'nonal')}
    if argument in AcceptedArguments and value:
        if argument == 'values':
            for value in list(value):
                if value not in AcceptedArguments[argument]: error('KeyError', 'Invalid value for argument "values".')
        else:
            if value not in AcceptedArguments[argument]: error('KeyError', 'Invalid value for argument "' + argument + '".')



def imageInformation(filePath: str) -> bool:
    AcceptedFileExtensions = ('png', 'webp', 'jpg', 'jpeg')
    if not path.isfile(filePath): error('FileNotFoundError', filePath)
    if filePath.split('.')[-1] not in AcceptedFileExtensions: error('ValueError', 'Invalid File Extension')

    iname = path.splitext(path.basename(filePath))[0]
    ipath = path.dirname(path.abspath(filePath))
    return (True, iname, ipath)



def getEncodingInformation(base: str):
    Values = ('binary', 'trinary', 'quaternary', 'quinary', 'senary', 'septenary', 'octal', 'nonal')
    EncodingFills = (8, 6, 4, 4, 4, 3, 3, 3)
    EncodingLengthFills = (16, 11, 8, 7, 7, 6, 6, 6)
    EncodingBases = (2, 3, 4, 5, 6, 7, 8, 9)

    return EncodingFills[Values.index(base)], EncodingLengthFills[Values.index(base)], EncodingBases[Values.index(base)]






#Main
def main():
    print('\n')
    Arguments = vars(SteganopyParser.parse_args())
    for argument in Arguments: testArgument(argument, Arguments[argument])
    if Arguments['text'] is not None and Arguments['file'] is not None: error('ValueError', 'Cannot have "file" and "text" arguments both be in use.')
    Indexes = [{'r' : 0, 'g' : 1, 'b' : 2}.get(i) for i in Arguments['values']]

    fileTest = imageInformation(Arguments['source'])
    imageName, imagePath = fileTest[1], fileTest[2]
    encodingFill, encodingLengthFill, encodingBase = getEncodingInformation(Arguments['encoding'])


    try:
        imageData = Image.open(Arguments['source'], 'r')
        width, height = imageData.size
        imageData = list(imageData.getdata())
        for i in tqdm(range(len(imageData)), desc = 'Preparing Image: '): imageData[i] = list(imageData[i])
    except KeyboardInterrupt: raise KeyboardInterrupt
    except Exception as exception: error('RuntimeError', 'Could not Prepare Image.\n' + str(exception))


    
    match Arguments['action'][0]:
        case 'e':
            try:
                if Arguments['file']:
                    if not path.isfile(Arguments['file']): error('FileNotFoundError', Arguments['file'])
                    with open(Arguments['file'], 'r', errors = 'ignore') as f: Arguments['text'] = ''.join(f.readlines())
                        
                information = []
                for i in tqdm(range(len(Arguments['text'])), desc = 'Encoding Information: '): information.append(baseConvert(ord(Arguments['text'][i]), encodingBase).zfill(encodingFill))
            except KeyboardInterrupt: raise KeyboardInterrupt
            except Exception as exception: error('RuntimeError', 'Could not Encode Information.\n' + str(exception))


            if Arguments['key'] is not None:
                try:
                    information = list(''.join(information))
                    key = expandKey(Arguments['key'], len(information), encodingBase)
                    
                    for i in tqdm(range(len(key)), desc = 'Encrypting Information: '): information[i] = str(int(information[i]) ^ int(key[i]))
                except KeyboardInterrupt: raise KeyboardInterrupt
                except Exception as exception: error('RuntimeError', 'Could not Encrypt Information.\n' + str(exception))
            information = list(baseConvert(int(len(''.join(information)) / encodingFill), encodingBase).zfill(encodingLengthFill) + ''.join(information))


            try:
                c, p = 0, 0
                for i in tqdm(range(len(information)), desc = 'Inserting Information: '):
                    if p > len(Indexes) - 1: 
                        p = 0
                        c += 1

                    pixel = str(imageData[c][Indexes[p]])[-1] + information[i]
                    imageData[c][Indexes[p]] = int(''.join(pixel))
                    p += 1
            except KeyboardInterrupt: raise KeyboardInterrupt
            except Exception as exception: error('RuntimeError', 'Could not Insert Information.\n' + str(exception))


            try:
                if Arguments['output']: newImagePath = imagePath + '\\' + Arguments['output'] + '.png'
                else: newImagePath = imagePath + '\\' + imageName + '-steganopy.png'
                
                newImageData = []
                for i in tqdm(range(len(imageData)), desc = 'Saving Image: '): newImageData.extend(imageData[i])
                    
                imageFormat = {3 : 'RGB', 4 : 'RGBA'}.get(len(imageData[0]))
                newImage = Image.frombytes(imageFormat, (width, height), bytes(newImageData))
                newImage.save(newImagePath)
            except KeyboardInterrupt: raise KeyboardInterrupt
            except Exception as exception: return ('Could not Save Image.', exception)

            
            print('\n')
            printColor('Image Successfully Saved: ', 'green', end = '')
            print(newImagePath)
        


        case 'd':
            try:
                newImageData = []
                for i in tqdm(range(len(imageData)), desc = 'Extracting Values: '):
                    pixel = imageData[i]
                    for v in Indexes: newImageData.append(list(str(pixel[v]))[-1])
            except KeyboardInterrupt: raise KeyboardInterrupt
            except Exception as exception: error('RuntimeError', 'Could not Extract Values.\n' + str(exception))


            try:
                information = []
                length = int(''.join([str(i) for i in newImageData[:encodingLengthFill]]), encodingBase)
                for i in tqdm(range(length * encodingFill), desc = 'Collecting Necessary Values: '): information.append(newImageData[encodingLengthFill + i])
            except KeyboardInterrupt: raise KeyboardInterrupt
            except Exception as exception: error('RuntimeError', 'Could not Collect Necessary Values.\n' + str(exception))


            if Arguments['key']:
                try:
                    key = expandKey(Arguments['key'], length * encodingFill, encodingBase)
                    for i in tqdm(range(len(key)), desc = 'Decrypting Information: '): information[i] = str(int(information[i]) ^ int(key[i]))
                except KeyboardInterrupt: raise KeyboardInterrupt
                except Exception as exception: error('RuntimeError', 'Could not Decrypt Information.\n' + str(exception))


            try:
                decodedInformation = []
                for i in tqdm(range(0, len(information), encodingFill), desc = 'Decoding Information: '): decodedInformation.append(chr(int(''.join(information[i:i + encodingFill]), encodingBase)))
            except KeyboardInterrupt: raise KeyboardInterrupt
            except Exception as exception: error('RuntimeError', 'Could not Decode Information.\n' + str(exception))


            print('\n)
            if Arguments['output']:
                try:
                    outputPath = imagePath + '\\' + Arguments['output'] + '.txt'
                    with open(outputPath, 'w+', errors = 'ignore') as f: f.write(''.join(decodedInformation))
                    printColor('Information Output: ', 'green', end = '')
                    print(outputPath)
                except KeyboardInterrupt: raise KeyboardInterrupt
                except Exception as exception: error('RuntimeError', 'Could not Save Information to Output File.\n' + str(exception))
            
                else:
                printColor('Information Found: ', 'green', end = '')
                print(''.join(decodedInformation))






if __name__ == '__main__': main()
