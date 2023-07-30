# Beam-Compressor

This is a script that compresses mods.\
`async decompresses -> async compresses png, jpg, dds -> compresses`\
Lost in file size up to 30%

# Installation and run

```bash
git clone https://github.com/SantaSpeen/Beam-Compressor.git
cd Beam-Compressor
pip install -r requirements.txt
cd src
```

Then put your mods in `mods/` directory.
Then run:
```bash
python main.py
```

# Example output

Ryzen 7 5800H, m2
```
Starting process on 68 files, 6646.55mb, cores 16...
[1 ] Started: BMW_E36_Revamp_BETA.zip
[2 ] Started: 2140SLver2.5fix.zip
....
[66] [from_start=  319.67s] [wait 2 ] | [unzip   1.28s] -> [compress  47.19s] -> [zip   18.7s] [160.28mb ->  96.25mb]: VolgaGAZ3102.31029ver.3.0.zip
[57] [from_start=  329.49s] [wait 1 ] | [unzip   1.67s] -> [compress  36.55s] -> [zip  79.45s] [145.48mb -> 114.08mb]: Toyota_AE86.zip
[67] [from_start=   366.3s] [wait 0 ] | [unzip   1.75s] -> [compress  44.12s] -> [zip  58.66s] [169.26mb ->  143.6mb]: Volkswagen_Golf_7.zip
Work: 366.312s, 6646.55mb -> 5399.82mb
```

Xeon E5-2640, HDD 7200
```
Starting process on 60 files, 8798.27mb, cores 12...
[1] Started: Honda_Civic_Type-R_EK9.zip
[2] Started: Ibishu_Kashira_gen2.zip
...
[59] [from_start=  290.06s] [wait 2 ] | [unzip   1.19s] -> [compress    3.7s] -> [zip  52.66s] [ 75.73mb ->  71.85mb]: Toyota_Supra_A70.zip
[60] [from_start=  302.17s] [wait 1 ] | [unzip   1.14s] -> [compress  18.73s] -> [zip  44.33s] [ 58.14mb ->  52.99mb]: Toyota_Supra_MKV.zip
[55] [from_start=   304.3s] [wait 0 ] | [unzip   0.88s] -> [compress  37.17s] -> [zip  15.09s] [ 90.35mb ->  67.39mb]: VolgaGAZ24ver3.0.zip
Work: 472.9341s, 8798.27mb -> 7684.17mb
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