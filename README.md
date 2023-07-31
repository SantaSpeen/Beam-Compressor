# Beam-Compressor

This is a script that compresses mods.\
`async decompresses -> async compresses png, jpg, dds -> async compresses`\
Lost in file size up to 30%

# Installation and run

```bash
git clone https://github.com/SantaSpeen/Beam-Compressor.git
cd Beam-Compressor
pip install -r requirements.txt
cd src
```

Then put your mods in `mods/` directory.\
Then run:
```bash
python main.py
```

# Example output

Ryzen 7 5800H, m2
```
Starting process on 68 files, 6646.55mb, cores 16...
[1 ] Started: 2140SLver2.5fix.zip
[2 ] Started: BMW_E36_Revamp_BETA.zip
[3 ] Started: Bochkakvassa.zip
....
[66] [from_start=  302.89s] [wait 2 ] | [unzip   1.19s] -> [compress  48.72s] -> [zip  18.31s] [160.28mb ->   96.5mb]: VolgaGAZ3102.31029ver.3.0.zip
[57] [from_start=  313.19s] [wait 1 ] | [unzip   1.62s] -> [compress  34.94s] -> [zip  77.92s] [145.48mb -> 114.09mb]: Toyota_AE86.zip
[67] [from_start=  348.47s] [wait 0 ] | [unzip    1.8s] -> [compress  45.05s] -> [zip  57.67s] [169.26mb -> 143.41mb]: Volkswagen_Golf_7.zip
Work: 349.531s, 6646.55mb -> 5404.37mb
```

Xeon E5-2640, HDD 7200
```
Starting process on 60 files, 8798.27mb, cores 12...
[1 ] Started: jato.zip
[2 ] Started: pab_v55.zip
[3 ] Started: Honda_Prelude.zip
...
[58] [from_start=  427.44s] [wait 2 ] | [unzip    0.5s] -> [compress  51.95s] -> [zip   7.18s] [ 87.12mb ->  54.63mb]: Mazda_Miata_Remastered.zip
[49] [from_start=  430.46s] [wait 1 ] | [unzip   2.56s] -> [compress  24.36s] -> [zip 106.72s] [ 128.3mb -> 126.95mb]: Honda_Civic_Ferio.zip
[50] [from_start=  430.82s] [wait 0 ] | [unzip   1.06s] -> [compress  46.75s] -> [zip   79.8s] [145.48mb -> 114.19mb]: Toyota_AE86.zip
Work: 431.8857s, 8798.27mb -> 7688.41mb
```

# License
```
MIT License

Copyright (c) 2023 SantaSpeen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```