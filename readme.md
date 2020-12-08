from project import db, create_app

You will make some changes to your models in your Python source code.
You will then run flask db migrate to generate a new database migration for these changes.
You will finally apply the changes to the database by running flask db upgrade.


>>> import os
>>> base=os.path.basename('/root/dir/sub/file.ext')
>>> base
'file.ext'
>>> os.path.splitext(base)
('file', '.ext')
>>> os.path.splitext(base)[0]
'file'

new=Methods(methodname="Soil Structure Auto Detection", body= "Based on article A Geometric Equation for Representing Morphological Field Information in Horizons with Compound Structure (2017) Hirmas and Gimenez",folder="method4")


You can't merge with local modifications. Git protects you from losing potentially important changes.

You have three options:

Commit the change using
git commit -m "My message"
Stash it.
Stashing acts as a stack, where you can push changes, and you pop them in reverse order.

To stash, type

git stash
Do the merge, and then pull the stash:

git stash pop
Discard the local changes
using git reset --hard
or git checkout -t -f remote/branch

Or: Discard local changes for a specific file
using git checkout filename
-------------------

skbuild is for Scikit-build.

Install it using pip:

As for windows: pip install scikit-build

After the succesfull installation:

pip install cmake
pip install --ugrade setuptools wheel
-----------
ps -ef |grep redis
redis-cli ping #should return 'PONG'
And this solved my issue:

$ ps -ef |grep redis

root      6622  4836  0 11:07 pts/0    00:00:00 grep redis
redis     6632     1  0 Jun23 ?        04:21:50 /usr/bin/redis-server *:6379
Locate redis process, and stop it!

$ kill -9 6632
$ service redis restart


Stopping redis-server: [  OK  ]
Starting redis-server: [  OK  ]


$ service redis status
------------
Для установки cv2 на сервер !!!

RUN apt-get update ##[edited]
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y
