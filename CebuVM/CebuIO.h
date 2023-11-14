#include "VMachine.h"
#include <stdio.h>
#include <stdlib.h>
void IO_INT(JRISC_ps_t *ps,FILE *disk);
void BOOT_LOAD(JRISC_ps_t *ps,FILE *disk);
void PRINT_STR(JRISC_ps_t *ps);