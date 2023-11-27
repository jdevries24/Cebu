#include <stdio.h>
#include <stdlib.h>
#include "VMachine.h"

FILE *disk;

extern void (*JRISC_instructions[256])(JRISC_ps_t*);

void Run(JRISC_ps_t *ps){
	while(ps->Inturupt != 255){
		if(ps->Inturupt == 0){
			//printf("Opcode %x\n",ps->Ram[ps->Pc]);
			JRISC_instructions[ps->Ram[ps->Pc]](ps);
			ps->Registers[0] = 0;
		}
		else if(ps->Inturupt == 13){
			IO_INT(ps,disk);
			ps->Inturupt = 0;
		}
		else if(ps->Inturupt == 254){
			printf("Invalid Instruction");
			printf("Opcode %x\n",ps->Ram[ps->Pc]);
			break;
		}
		else if(ps->Inturupt == 10){
			printf("Debug Ping\n");
			ps->Inturupt = 0;
			fflush(stdout);
		}
	}
}


JRISC_ps_t *init_ps(){
	JRISC_ps_t *ps = calloc(1,sizeof(JRISC_ps_t));
	ps->Ram = calloc(0x10000,sizeof(uint8_t));
	ps->Registers[14] = 0xffff;
	ps->Pc = 1024;
	return ps;
}

int main(int len_args,char **args){
	if(len_args < 2){
		printf("Missing input disk!\n");
		return 0;
	}
	else{
		disk = fopen(args[1],"r+");
		if(disk == 0){
			printf("Non existent disk\n");
			return 0;
		}
		JRISC_ps_t *ps = init_ps();
		BOOT_LOAD(ps,disk);
		Run(ps);
		free((void*)ps->Ram);
		free((void*)ps);
		return 1;
	}
}
