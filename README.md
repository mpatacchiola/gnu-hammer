
Collection of simple tools for Unix systems which I realised for solving basic tasks.

midwife
--------

Midwife allows tracking all the new files and folders generated in a specific root directory (including all the sub-folders). It is useful to implement rudimentary sandboxes. To compile the programme it is necessary to have a recent version of g++ which implements the [filesystem library](http://en.cppreference.com/w/cpp/experimental/fs). Using g++ 7.0 it is possible to compile as follows:

```
g++-7 -std=c++1z -O3 midwife.cpp -lstdc++fs -o ./midwife
```

The executable takes the following parameters as input:

1. -d, --destination: the absolute path of the folder to track (default ./)
2. -s, sleep: define the time (in milliseconds) between calls (default 1000)

The output produced by midwife is a string which identifies the absolute path of a new file/folder which has been generated.
The output can be easily redirected in a log file:

```
midwife --destination /home/user/program --sleep 1000 >> log.txt
```
