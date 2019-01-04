
# clock-sync
It provides solutions to common problems such as BIOS without battery, OS changes causing the madness of the Windows clock.
It is synchronized with NTP and is adjusted according to the indicated time zone, then with **_administrator permissions_** changes the system time.


## Run by source
You need to have installed:
- *ntplib*
>use "pip3 install *ntplib*" 

Run **main.py**
>You can give your time zone as an argument, following this format:

>- -HH:MM
>- +HH:MM

>If you don't want to see TaskEditor menu, just add '-n' as second argument

## Run by EXE

> Compiled using *[auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe)*

Download the last release [here](https://drive.google.com/open?id=1MAvog8BaVGXfvGVW1X9ASfKEGTtUB9IU)

Run **main.exe**
>You can give your time zone as an argument, following this format:

>- -HH:MM
>- +HH:MM

>If you don't want to see TaskEditor menu, just add '-n' as second argument
