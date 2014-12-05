care4care
=========

This is a small guide on how to install the system and run it locally.

How to run/install the system
=============================

1. Make sure python3 is installed
2. Install the decoders for png and jpeg images that pillow uses (don't remember the names)
3. Install the following python3 modules: django, django-extensions, django-model-utils, django-admin-bootstrapped,
    pillow, numpy, matplotlib
4. Obtain access permission to the repository on github
5. git clone https://github.com/madetaille/care4care.git
6. cd care4care/
7. python3 manage.py runserver
8. Open web browser and go to 127.0.0.1:8000/ for the main website
9. Open web browser and go to 127.0.0.1:8000/admin for the admin website

Simulator and tests
===================

The source code for the simulator is available in another repository:
https://github.com/madetaille/simulator
