#include <stdint.h>
typedef struct{
	uint32_t address;
	uint8_t level;
}Inturupt_RA_t;

typedef struct{
	uint8_t *Ram;
	uint32_t Registers[16];
	uint32_t Pc;
	uint32_t CSR;
	uint8_t Inturupt_level;
	uint8_t Inturupt;
	Inturupt_RA_t INT_RAs[5];
}JRISC_ps_t;
