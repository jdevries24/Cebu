#include "CebuIO.h"



void PRINT_STR(JRISC_ps_t *ps){	
    uint32_t index = ps->Registers[2];
	for(;ps->Ram[index] != 0;index += 1){
		fputc(ps->Ram[index],stdout);
	}
    fflush(stdout);
}

void INPUT_STR(JRISC_ps_t *ps){
    uint32_t index = ps->Registers[2];
    uint32_t maxi = ps->Registers[3];
    uint32_t size = 0;
    while(size < maxi){
        if(!feof(stdin)){
            char input = fgetc(stdin);
            if(input == '\n'){
                ps->Ram[index] = 0;
                return;
            }
            else{
                ps->Ram[index] = input;
                index += 1;
                size += 1;
            }
        }
    }
}

void BOOT_LOAD(JRISC_ps_t *ps,FILE *disk){
	for(int i = 0;i >= 0;i += 1){
		if(feof(disk)){
			break;
		}
		ps->Ram[i+1024] = (uint8_t) getc(disk);
	}
}

void IO_INT(JRISC_ps_t *ps,FILE *disk){
    switch(ps->Registers[1]){
        case 1:
            PRINT_STR(ps);
            break;
        default:
        case 2:
            INPUT_STR(ps);
            break;
    }
}
