
## How to determine the line of code that causes a segmentation fault by GDB? 
https://stackoverflow.com/questions/2876357/determine-the-line-of-code-that-causes-a-segmentation-fault

Compile you program using the -g switch, like this:

gcc program.c -g
Then use gdb:

$ gdb ./a.out
(gdb) run
<segfault happens here>
(gdb) backtrace
<offending code is shown here>
Here is a nice tutorial to get you started with GDB.

## How to check the line of code which causes segmentation fault in core file?
  
Identify what's causing segmentation faults (segfaults)
https://kb.iu.edu/d/aqsj
  
You could use GNU's well-known debugger GDB to view the backtrace of a core file dumped by your program; 
whenever programs segfault, they usually dump the content of (their section of the) memory at the time of the crash into a core file. 
Start your debugger with the command gdb core, and then use the backtrace command to see where the program was when it crashed. 
```
  gdb core
```
  
## How to debug C program run by java jni?
  
Debug a running Java process in Linux

Start your java application
Look up the pid using top, ps, jps, ... 
Start gdb with this pid
Attach your program code
Debug as usual using gdb

```bash
 # start java app
# find application PID
jps
# start gdb with application PID
gdb -p 1234
# gdb will pause our application
```

## How to debug jni code on MacOS?

  https://www.owsiak.org/lldb-and-jni/
  
[ GDB debug native part of a Java application](https://medium.com/@pirogov.alexey/gdb-debug-native-part-of-java-application-c-c-libraries-and-jdk-6593af3b4f3f)

  https://lldb.llvm.org/use/map.html

  https://opensource.apple.com/source/lldb/lldb-159/www/tutorial.html
  
  
