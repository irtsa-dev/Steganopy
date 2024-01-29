#Imports
import argparse

from os import path
from PIL import Image
from tqdm import tqdm
from PyTermColor.Color import printColor






#Extra Functions
def pri(x: int = 1): print('\n' * x)


def baseConvert(number: int, base: int):
    if number == 0: return '0'
    digits = []
    
    while number:
        digits.append(int(number % base))
        number //= base
    return ''.join([str(i) for i in digits[::-1]])


def expandKey(key: int, length: int, base: int) -> str:
    while len(baseConvert(key, base)) < length: key *= key
    return baseConvert(key, base)[0:length]






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





#Global Variables
Arguments = vars(SteganopyParser.parse_args())
AcceptedArguments = {'action' : ('e', 'encrypt', 'd', 'decrypt'), 'values' : ('r', 'g', 'b'), 'encoding' : ('binary', 'trinary', 'quaternary', 'quinary', 'senary', 'septenary', 'octal', 'nonal')}
AcceptedFileExtensions = ('png', 'webp', 'jpg', 'jpeg')
EncodingFills = (8, 6, 4, 4, 4, 3, 3, 3)
EncodingLengthFills = (16, 11, 8, 7, 7, 6, 6, 6)
EncodingBases = (2, 3, 4, 5, 6, 7, 8, 9)






#Primary Function Section
def primary():
    for argument in Arguments:
        if argument in AcceptedArguments:

            argValue = Arguments[argument]
            if argument == 'values': argValue = list(argValue)
            else: argValue = [argValue]

            for value in argValue:
                if value not in AcceptedArguments[argument]:
                    raise ValueError('Invalid argument passed for "' + argument + '". Accepted values are: ' + ', '.join(AcceptedArguments[argument]))

    pri()
    if not path.isfile(Arguments['source']): return 'File not Found.'
    if Arguments['source'].split('.')[-1] not in AcceptedFileExtensions: return 'Invalid File Extension.'
    encodingFill = EncodingFills[AcceptedArguments['encoding'].index(Arguments['encoding'])]
    encodingLengthFill = EncodingLengthFills[AcceptedArguments['encoding'].index(Arguments['encoding'])]
    encodingBase = EncodingBases[AcceptedArguments['encoding'].index(Arguments['encoding'])]


    try:
        imageName = path.splitext(path.basename(Arguments['source']))[0]
        imagePath = path.dirname(path.abspath(Arguments['source']))
        imageData = Image.open(Arguments['source'], 'r')
        width, height = imageData.size
        imageData = list(imageData.getdata())
        for i in tqdm(range(len(imageData)), desc = 'Preparing Image: '): imageData[i] = list(imageData[i])
    except KeyboardInterrupt: return False
    except Exception as exception: return ('Could not Prepare Image.', exception)

    match Arguments['action'][0]:
        case 'e':
            try:
                if Arguments['file'] is not None and Arguments['text'] is not None: return 'Cannot have "file" and "text" arguments both be in use.'

                if Arguments['file']:
                    if not path.isfile(Arguments['file']): return 'File not Found.'
                    with open(Arguments['file'], 'r', errors = 'ignore') as f: Arguments['text'] = ''.join(f.readlines())
                        
                information = []
                for i in tqdm(range(len(Arguments['text'])), desc = 'Encoding Information: '): information.append(baseConvert(ord(Arguments['text'][i]), encodingBase).zfill(encodingFill))
            except KeyboardInterrupt: return False
            except Exception as exception: return ('Could not Encode Information.', exception)


            if Arguments['key'] is not None:
                if Arguments['key'] < 2: return 'Argument "key" is too small of a value.'
                try:
                    information = list(''.join(information))
                    key = expandKey(Arguments['key'], len(information), encodingBase)
                    for i in tqdm(range(len(key)), desc = 'Encrypting Information: '): information[i] = str(int(information[i]) ^ int(key[i]))
                except KeyboardInterrupt: return False
                except Exception as exception: return ('Could not Encrypt Information.', exception)
            information = list(baseConvert(int(len(''.join(information)) / encodingFill), encodingBase).zfill(encodingLengthFill) + ''.join(information))


            try:
                c, p = 0, 0
                Indexes = [{'r' : 0, 'g' : 1, 'b' : 2}.get(i) for i in Arguments['values']]
                for i in tqdm(range(len(information)), desc = 'Inserting Information: '):
                    if p > len(Indexes) - 1: 
                        p = 0
                        c += 1

                    pixel = list(str(imageData[c][Indexes[p]]))
                    pixel[-1] = information[i]
                    imageData[c][Indexes[p]] = int(''.join(pixel))
                    p += 1
            except KeyboardInterrupt: return False
            except Exception as exception: return ('Could not Insert Information.', exception)


            try:
                if Arguments['output'] is None: newImagePath = imagePath + '\\' + imageName + '-steganopy.png'
                else: newImagePath = imagePath + '\\' + Arguments['output'] + '.png'
                
                newImageData = []
                for i in tqdm(range(len(imageData)), desc = 'Saving Image: '): newImageData.extend(imageData[i])
                format = {3 : 'RGB', 4 : 'RGBA'}.get(len(imageData[0]))
                newImageData = Image.frombytes(format, (width, height), bytes(newImageData))
                newImageData.save(newImagePath)
            except KeyboardInterrupt: return False
            except Exception as exception: return ('Could not Save Image.', exception)
            
            pri()
            printColor('Image Successfully Saved: ', 'green', end = '')
            print(newImagePath)
        


        case 'd':
            try:
                newImageData = []
                Indexes = [{'r' : 0, 'g' : 1, 'b' : 2}.get(i) for i in Arguments['values']]
                for i in tqdm(range(len(imageData)), desc = 'Extracting Values: '):
                    pixel = imageData[i]
                    for v in Indexes: newImageData.append(list(str(pixel[v]))[-1])
            except KeyboardInterrupt: return False
            except Exception as exception: return ('Could not Extract Values.', exception)


            try:
                information = []
                length = int(''.join([str(i) for i in newImageData[:encodingLengthFill]]), encodingBase)
                for i in tqdm(range(length * encodingFill), desc = 'Collecting Necessary Values: '): information.append(newImageData[encodingLengthFill + i])
            except KeyboardInterrupt: return False
            except Exception as exception: return ('Could not Collect Necessary Values.', exception)


            if Arguments['key'] is not None:
                if Arguments['key'] < 2: return 'Argument "key" is too small of a value.'
                try:
                    key = expandKey(Arguments['key'], length * encodingFill, encodingBase)
                    for i in tqdm(range(len(key)), desc = 'Decrypting Information: '): information[i] = str(int(information[i]) ^ int(key[i]))
                except KeyboardInterrupt: return False
                except Exception as exception: return ('Could not Decrypting Information.', exception)


            try:
                decodedInformation = []
                for i in tqdm(range(0, len(information), encodingFill), desc = 'Decoding Information: '):
                    char = int(''.join(information[i:i + encodingFill]), encodingBase)
                    decodedInformation.append(chr(char))
            except KeyboardInterrupt: return False
            except Exception as exception: return ('Could not Decode Information.', exception)


            pri()
            if Arguments['output'] is not None:
                try:
                    outputPath = imagePath + '\\' + Arguments['output'] + '.txt'
                    with open(outputPath, 'w+', errors = 'ignore') as f: f.write(''.join(decodedInformation))
                    printColor('Information Output: ', 'green', end = '')
                    print(outputPath)
                except KeyboardInterrupt: return False
                except Exception as exception: return ('Could not Save Information to Output File.', exception)
            else:
                printColor('Information Found: ', 'green', end = '')
                print(''.join(decodedInformation))
        

    
    return True






#Main Function
def main():
    message = primary()
    if type(message) != bool: 
        if type(message) == tuple:
            printColor('\n\n' + message[0], 'red')
            print(message[1])
        else: printColor('\n\n' + message, 'red')

    elif not message: print('\n\nProcess Stopped')






if __name__ == '__main__': main()
