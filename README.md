# clock-sync
It provides solutions to common problems such as BIOS without battery, OS changes causing the madness of the Windows clock.
It is synchronized with NTP and is adjusted according to the indicated time zone, then with **_administrator permissions_** changes the system time.


## Run
You will need *ntplib* and *win32api*, install it with pip3
**pip3 install** *name*
Run __main.py__, at first time the program ask you the time zone, if you want to change it just run __TimeZone.py__
