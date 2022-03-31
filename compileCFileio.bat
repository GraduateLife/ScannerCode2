gcc -c -o fileobject.o fileiotesting.c
gcc -o fileio.dll -s -shared fileobject.o 
