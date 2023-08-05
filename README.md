# flipper-zero-amiibo-converter
Amiibo .bin to .nfc flipper zero converter scipt

usage:
```bash
chmod +x fz_amiibo_converter.py
./fz_amiibo_converter.py <input> <output>
```
or
```bash
python3 fz_amiibo_converter.py <input> -o <output>
```

input - directory path (processed recursively) or .bin file

output - the name of the output directory. optional parameter, default is amiibo nfc. will be created in the script call directory

also you can use flag ```--norename``` to specify that files and subdirectories of the output folder do not need to be renamed to a format compatible with the flipper zero file system (NOT RECOMMENDED)

f.e:
```bash
./fz_amiibo_converter.py Amiibo_Bins
./fz_amiibo_converter.py Amiibo_Bins -o my_custom_dir
```
# where to get .bin files
i used this: https://amiibodoctor.com/2021/06/01/all-amiibo-bin-files-download-for-tagmo-powersaves-placiibo-etc/

you only need the Amiibo .bin itself, you don't need key_retail.bin and so on
