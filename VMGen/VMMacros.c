#define LoadSrcDest() \
uint8_t Dest_num = (ps->Ram[ps->Pc + 1] >> 4) & 0xf;\
uint8_t Src_num = ps->Ram[ps->Pc + 1] & 0xf;\
uint32_t Dest_val = ps->Registers[Dest_num];\
uint32_t Src_val = ps->Registers[Src_num];


inline uint32_t Add_signed_24(uint32_t base,uint32_t value){
	if(value & 0x800000){
		return base - (value & 0x7fffff);
	}
	else{
		return base + (value & 0x7fffff);
	}
}

inline uint32_t Add_signed_20(uint32_t base,uint32_t value){
	if(value & 0x80000){
		return base - (value & 0x7ffff);
	}
	else{
		return base + (value & 0x7ffff);
	}
}

inline uint32_t Add_signed_16(uint32_t base,uint32_t value){
	if(value & 0x8000){
		return base - (value & 0x7fff);
	}
	else{
		return base + (value & 0x7fff);
	}
}


inline uint32_t Load_half(uint32_t addr,uint8_t *ram){
	uint8_t high = ram[addr];
	uint8_t low = ram[addr + 1];
	return (((uint32_t)high) << 8) | ((uint32_t)low);
}

inline uint32_t Load_word(uint32_t addr,uint8_t *ram){
	uint8_t o1 = ram[addr];
	uint8_t o2 = ram[addr + 1];
	uint8_t o3 = ram[addr + 2];
	uint8_t o4 = ram[addr + 3];
	return (((uint32_t)o1) << 24) | (((uint32_t)o2) << 16) | (((uint32_t)o3) << 8) | ((uint32_t)o4);
}
