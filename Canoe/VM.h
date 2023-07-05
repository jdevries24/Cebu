#include "VMtools.h"
typedef struct{
    u32 registers[16];
    u32 irqstack[5];
    u8 irqpointer;
    u32 pc;
    u8 *ram;
    u8 CSR_Call;
}JRISCdev;