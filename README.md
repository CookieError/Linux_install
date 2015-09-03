Linux_install.py
=================

>This script helps you set up a new new linux install. After install linux to your system if you run this script it will upgread all your packages and then installs any packages. 

How to use
==========

>If you pass a ````-a```` flag and then a path to a text file with all the packages you want to install.

>````-a```` flag is for debian systems
>````-r```` flag is for red hat systems

Example
=======

This is for a debian system
````python Linux_install.py -a /home/username/list_of_packages.txt````

This is for a redhat system
````python Linux_install.py -r /home/username/list_of_packages.txt````
