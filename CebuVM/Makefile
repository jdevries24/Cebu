CC = gcc
CFLAGS = -g
OBJECTS =  VMInst.o CebuIO.o CebuVM.o 
LDFlags = -g

make:$(OBJECTS)
	$(CC) $(LDFlags) $(OBJECTS) -o Cebu

CebuVM.o:CebuVM.c
	$(CC) $(CFLAGS) -c CebuVM.c -o $@

VMInst.o:VMInst.c
	$(CC) $(CFLAGS) -c VMInst.c -o $@

VMMacros.o:VMMacros.c
	$(CC) $(CFLAGS) -c VMMacros.c -o $@

CebuIO.o:CebuIO.c
	$(CC) $(CFLAGS) -c CebuIO.c -o $@

clean:
	-rm -f *.o

