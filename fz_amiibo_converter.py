#!/usr/bin/env python3

import argparse
import os

def convert_bin_to_nfc(bin_data:bytes) -> str:
    output_data ="".join({
                "Filetype: Flipper NFC device\n"+
                "Version: 3\n"+
                "# Nfc device type can be UID, Mifare Ultralight, Mifare Classic\n"+
                "Device type: NTAG215\n"+
                "# UID, ATQA and SAK are common for all formats\n"+
                f"UID: {' '.join([bin_data[i:i+1].hex().upper() for i in range(0, 8, 1) if i != 3])}\n"+
                "ATQA: 00 44\n"+
                "SAK: 00\n"+
                "# Mifare Ultralight specific data\n"+
                "Data format version: 1\n"+
                "Signature: DF EA 07 1E DA C0 CC 4E 9E 0F D8 64 6D 57 F1 4E 63 3D D7 DA 03 C5 96 06 72 BC D8 BE 80 02 6B 7E\n"+
                "Mifare version: 00 04 04 02 01 00 11 03\n"+
                "Counter 0: 0\n"+
                "Tearing 0: 00\n"+
                "Counter 1: 0\n"+
                "Tearing 1: 00\n"+
                "Counter 2: 100\n"+
                "Tearing 2: 00\n"+
                f"Pages total: {len(bin_data)//4}\n" +
                f"Pages read: {len(bin_data)//4}\n"})

    # parse pages data
    for i in range(len(bin_data)//4):
        page_offset = i * 4
        page_data = bin_data[page_offset:page_offset+4].hex().upper()
        output_data += f"Page {i}: {page_data[0:2]} {page_data[2:4]} {page_data[4:6]} {page_data[6:8]}\n"

    output_data += "Failed authentication attempts: 0\n"
    print (output_data)
    return output_data

def process_file(input_file_path:str, output_directory:str) -> None:
    with open(input_file_path, 'rb') as bin_file:
        bin_data = bin_file.read()

    output_data = convert_bin_to_nfc(bin_data)

    # path processing
    out_p = os.path.relpath(input_file_path, args.input)
    if out_p == '.':
        filename = os.path.basename(input_file_path)
        out_p, extension = os.path.splitext(filename)
        output_file_path = os.path.join(args.output_dir_name, out_p + '.nfc')
    else:
        output_file_path = os.path.join(output_directory, out_p)
        output_file_path = os.path.splitext(output_file_path)[0] + '.nfc'

    # subdirectories creating
    output_file_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_file_dir):
        os.makedirs(output_file_dir)

    with open(output_file_path, 'w') as output_file:
        output_file.write(output_data)

    print(f"nfc file created at {output_file.name}")

def process_directory(directory_path:str, output_path_name:str) -> None:
    # check if output directory exists, create it if not
    output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_path_name)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # recursively traverse the directory and its subdirectories in search of .bin files.
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            if filename.endswith('.bin'):
                input_file_path = os.path.join(dirpath, filename)
                process_file(input_file_path, output_directory)

def main():
    parser = argparse.ArgumentParser(description="amibo .bin's to flipper zero .nfc converter")
    parser.add_argument('input', help=".bin's directory or .bin file")
    parser.add_argument('-o', '--output_dir_name', help="output directory name", default="amiibo_nfc")

    global args
    args = parser.parse_args()
    if args.input.endswith(".bin"):
        process_file(args.input, args.output_dir_name)
    else:
        process_directory(args.input, args.output_dir_name)

if __name__ == '__main__':
    main()