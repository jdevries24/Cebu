files := VMtools.c
make: files
	ld $(wildcard *.o) -o JRISCdev

files:$(files)
	gcc -g -c $(files)

clean:
	rm -r *.o
