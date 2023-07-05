files := VMtools.c
make: $(files)
	ld -o JRISCdev *.o

$(files):
	gcc -g -c %@

clean:
	rm -r *.o