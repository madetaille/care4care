care4care
=========

This is a small guide on how to install the system and run it locally.

How to run/install the system (on CentOS)
=========================================

1. $ yum groupinstall "Development tools"
2. $ git clone https://github.com/madetaille/care4care.git
3. $ yum install libjpeg libjpeg-devel libpng libpng-devel agg freetype-devel
4. $ pip3 install django Pillow numpy matplotlib django_extensions django_model_utils
5. $ cd care4care
6. Create the database: $ python3 manage.py migrate
7. Create a superuser: $ python3 manage.py createsuperuser
8. Launch the server: $ python3 manage.py runserver
9. Open web browser and go to 127.0.0.1:8000/ for the main website
10. Open web browser and go to 127.0.0.1:8000/admin for the admin website
11. Don't forget to create some branches and to set a first/last name for the administrator

Simulator and tests
===================

The source code for the simulator is available in another repository:
https://github.com/madetaille/simulator
