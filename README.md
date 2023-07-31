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

# Tests
Config: 72 mods, 8.8Gb (from 1.66Mb to 1.47Gb per file)

AMD Ryzen 7 5800H, PCEx3 m2
```
Python 3.11.4 (Windows)
Processor: AMD Ryzen 7 5800H with Radeon Graphics x16
Starting process on 72 files, 9073.01mb, cores 16...
[1 ] Started: 2140SLver2.5fix.zip
[2 ] Started: Acura_NSX.zip
[3 ] Started: BMW_E36_Revamp_BETA.zip
....
[71] [from_start=  288.94s] [wait 2 ] | [unzip   1.49s] -> [compress  14.92s] -> [zip  60.98s] [169.26mb ->  98.47mb]: Volkswagen_Golf_7.zip
[56] [from_start=  367.51s] [wait 1 ] | [unzip   9.19s] -> [compress   63.3s] -> [zip 146.78s] [777.74mb -> 691.82mb]: RussianProvinceTownVer3.0FIXx0.28.zip
[67] [from_start=  506.11s] [wait 0 ] | [unzip  15.02s] -> [compress  87.72s] -> [zip 206.17s] [1510.97mb -> 1408.0mb]: USSRProjectMapVer3.1AutumnEditionRelease.zip
Work: 506.453s, 9073.01mb -> 6776.58mb
```

Intel Xeon E5-2640, SATA HDD 7200
```
Python 3.11.4 (Linux)
Processor: Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz x12
Starting process on 72 files, 9073.01mb, cores 12...
[1 ] Started: jato.zip
[2 ] Started: pab_v55.zip
[3 ] Started: Honda_Prelude.zip
...
[69] [from_start=   504.6s] [wait 2 ] | [unzip  25.73s] -> [compress  27.06s] -> [zip   6.52s] [ 87.12mb ->  36.27mb]: Mazda_Miata_Remastered.zip
[33] [from_start=  724.87s] [wait 1 ] | [unzip  28.56s] -> [compress 240.76s] -> [zip 294.36s] [1510.97mb -> 1411.83mb]: USSRProjectMapVer3.1AutumnEditionRelease.zip
[71] [from_start=  806.75s] [wait 0 ] | [unzip  84.52s] -> [compress  79.56s] -> [zip 185.21s] [777.74mb -> 698.99mb]: RussianProvinceTownVer3.0FIXx0.28.zip
Work: 807.3758s, 9073.01mb -> 7234.79mb
```

Intel Core i5-10600KF, PCEx3 m2
```
Python 3.10.6 (Windows)
Processor: Intel(R) Core(TM) i5-10600KF CPU @ 4.10GHz x12
Starting process on 72 files, 9073.01mb, cores 12...
[1 ] Started: 2140SLver2.5fix.zip
[3 ] Started: Bochkakvassa.zip
[2 ] Started: Acura_NSX.zip
...
[71] [from_start=  306.81s] [wait 2 ] | [unzip   1.75s] -> [compress  11.31s] -> [zip  55.34s] [169.26mb ->  98.26mb]: Volkswagen_Golf_7.zip
[56] [from_start=  375.39s] [wait 1 ] | [unzip   9.31s] -> [compress  51.64s] -> [zip 134.73s] [777.74mb -> 691.71mb]: RussianProvinceTownVer3.0FIXx0.28.zip
[67] [from_start=  496.73s] [wait 0 ] | [unzip  11.61s] -> [compress  74.72s] -> [zip 189.52s] [1510.97mb -> 1411.44mb]: USSRProjectMapVer3.1AutumnEditionRelease.zip
Work: 497.297s, 9073.01mb -> 6783.46mb
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
