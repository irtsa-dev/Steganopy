#Imports
import argparse

from os import path
from PIL import Image
from tqdm import tqdm
from PyTermColor.Color import printColor






#Extra Functions
def pri(x: int = 1): print('\n' * x)


def expandKey(key: int, length: int) -> str:
    while len(bin(key)[2:]) < length: key *= key
    return bin(key)[2:][0:length]






#Parser Declarations
SteganopyParser = argparse.ArgumentParser(description="", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

SteganopyParser.add_argument('source', help = 'Picture source location.')
SteganopyParser.add_argument('action', help = 'Specifies whether to be encrypting or decrypting.')

SteganopyParser.add_argument('-v', '--values', help = 'Values used for encryption.', default = 'rgb')
SteganopyParser.add_argument('-i', '--information', help = 'Information to be added when encrypting is selected for "action" argument.')
SteganopyParser.add_argument('-o', '--output', help = 'Specifies output file name.')
SteganopyParser.add_argument('-k', '--key', type = int,  help = 'Specifies key to use for xor operation.')





#Global Variables
Arguments = vars(SteganopyParser.parse_args())
AcceptedArguments = {'action' : ['e', 'encrypt', 'd', 'decrypt'], 'values' : ['r', 'g', 'b']}
AcceptedFileExtensions = ['png', 'webp', 'jpg', 'jpeg']






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
                information = []
                for i in tqdm(range(len(Arguments['information'])), desc = 'Encoding Information: '): information.append(bin(ord(Arguments['information'][i]))[2:].zfill(8))
            except KeyboardInterrupt: return False
            except Exception as exception: return ('Could not Encode Information.', exception)


            if Arguments['key'] is not None:
                if Arguments['key'] < 2: return 'Argument "key" is too small of a value.'
                try:
                    information = list(''.join(information))
                    key = expandKey(Arguments['key'], len(information))
                    for i in tqdm(range(len(key)), desc = 'Encrypting Information: '): information[i] = str(int(information[i]) ^ int(key[i]))
                except KeyboardInterrupt: return False
                except Exception as exception: return ('Could not Encrypt Information.', exception)
            information = list(bin(int(len(information)))[2:].zfill(16) + ''.join(information))


            try:
                c, p = 0, 0
                Indexes = [{'r' : 0, 'g' : 1, 'b' : 2}.get(i) for i in Arguments['values']]
                for i in tqdm(range(len(information)), desc = 'Inserting Information: '):
                    if p > len(Indexes) - 1: 
                        p = 0
                        c += 1

                    pixel = list(str(imageData[c][Indexes[p]))
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
                length = int(''.join([str(i) for i in newImageData[:16]]), 2)
                for i in tqdm(range(length * 8), desc = 'Collecting Necessary Values: '): information.append(newImageData[16 + i])
            except KeyboardInterrupt: return False
            except Exception as exception: return ('Could not Collect Necessary Values.', exception)


            if Arguments['key'] is not None:
                if Arguments['key'] < 2: return 'Argument "key" is too small of a value.'
                try:
                    key = expandKey(Arguments['key'], length)
                    for i in tqdm(range(len(key)), desc = 'Decrypting Information: '): information[i] = str(int(information[i]) ^ int(key[i]))
                except KeyboardInterrupt: return False
                except Exception as exception: return ('Could not Decrypting Information.', exception)


            try:
                decodedInformation = []
                for i in tqdm(range(0, len(information), 8), desc = 'Decoding Information: '):
                    char = int(''.join(information[i:i + 8]), 2)
                    decodedInformation.append(chr(char))
            except KeyboardInterrupt: return False
            except Exception as exception: return ('Could not Decode Information.', exception)


            pri()
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
