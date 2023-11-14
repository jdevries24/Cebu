#include "CebuIO.h"

void IO_INT(JRISC_ps_t *ps,FILE *disk){
    switch(ps->Registers[1]){
        case 1:
            PRINT_STR(ps);
            break;
        default:
            break;
    }
}

void PRINT_STR(JRISC_ps_t *ps){	
    uint32_t index = ps->Registers[2];
	for(;ps->Ram[index] != 0;index += 1){
		fputc(ps->Ram[index],stdout);
	}
    fflush(stdout);
}

void BOOT_LOAD(JRISC_ps_t *ps,FILE *disk){
	for(int i = 0;i < 1024;i += 1){
		if(feof(disk)){
			break;
		}
		ps->Ram[i+1024] = (uint8_t) getc(disk);
	}
}