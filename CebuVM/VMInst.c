#include "VMachine.h"
#include "VMMacros.c"
#include <stdint.h>

void INVALID(JRISC_ps_t *ps){
	ps->Inturupt = 254;
}

void NOP(JRISC_ps_t *ps){
	ps->Pc += 2;
}

void LDB(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = (uint32_t) ps->Ram[Src_val];
	ps->Pc += 2;
}

void LDH(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Load_half(Src_val,ps->Ram);
	ps->Pc += 2;
}

void LDW(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Load_word(Src_val,ps->Ram);
	ps->Pc += 2;
}

void LDBS(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t value = (uint32_t) ps->Ram[Src_val];
	if(value & 0x80){
		value |= 0xffffff00;
	}
	ps->Registers[Dest_num] = value;
	ps->Pc += 2;
}

void LDHS(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t value = Load_half(Src_val,ps->Ram);
	if(value & 0x8000){
		value |= 0xffff0000;
	}
	ps->Registers[Dest_num] = value;
	ps->Pc += 2;
}

void LDWS(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Load_word(Src_val,ps->Ram);
	ps->Pc += 2;
}

void STB(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Ram[Src_val] = (uint8_t)Dest_val & 0xff;
	ps->Pc += 2;
}

void STH(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Ram[Src_val] =(uint8_t) (Dest_val >> 8) & 0xff;
	ps->Ram[Src_val + 1] = (uint8_t) (Dest_val) & 0xff;
	ps->Pc += 2;
}

void STW(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Ram[Src_val] = (uint8_t)(Dest_val >> 24) & 0xff;
	ps->Ram[Src_val + 1] = (uint8_t)(Dest_val >> 16) & 0xff;
	ps->Ram[Src_val + 2] = (uint8_t)(Dest_val >> 8) & 0xff;
	ps->Ram[Src_val + 3] = (uint8_t)(Dest_val & 0xff);
	ps->Pc += 2;
}

void LDBI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	uint32_t addr = Add_signed_16(Src_val,imm);
	ps->Registers[Dest_num] = (uint32_t) ps->Ram[addr];
	ps->Pc += 4;
}

void LDHI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	uint32_t addr = Add_signed_16(Src_val,imm);
	ps->Registers[Dest_num] = Load_half(addr,ps->Ram);
	ps->Pc += 4;
}

void LDWI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	uint32_t addr = Add_signed_16(Src_val,imm);
	ps->Registers[Dest_num] = Load_word(addr,ps->Ram);
	ps->Pc += 4;
}

void LDBSI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	uint32_t addr = Add_signed_16(Src_val,imm);
	uint32_t value = (uint32_t) ps->Ram[addr];
	if(value & 0x80){
		value |= 0xffffff00;
	}
	ps->Registers[Dest_num] = value;
	ps->Pc += 4;
}

void LDHSI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	uint32_t addr = Add_signed_16(Src_val,imm);
	uint32_t value = Load_half(addr,ps->Ram);
	if(value & 0x8000){
		value |= 0xffff0000;
	}
	ps->Registers[Dest_num] = value;
	ps->Pc += 4;
}

void LDWSI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	uint32_t addr = Add_signed_16(Src_val,imm);
	ps->Registers[Dest_num] = Load_word(addr,ps->Ram);
	ps->Pc += 4;
}

void STBI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	uint32_t addr = Add_signed_16(Src_val,imm);
	ps->Ram[addr] = (uint8_t)Dest_val & 0xff;
	ps->Pc += 4;
}

void STHI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	uint32_t addr = Add_signed_16(Src_val,imm);
	ps->Ram[addr] = (uint8_t)(Dest_val >> 8) & 0xff;
	ps->Ram[addr + 1] = (uint8_t) Dest_val & 0xff;
	ps->Pc += 4;
}

void STWI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	uint32_t addr = Add_signed_16(Src_val,imm);
	ps->Ram[addr] = (uint8_t)(Dest_val >> 24) & 0xff;
	ps->Ram[addr + 1] = (uint8_t)(Dest_val >> 16) & 0xff;
	ps->Ram[addr + 2] = (uint8_t)(Dest_val >> 8) & 0xff;
	ps->Ram[addr + 3] = (uint8_t)(Dest_val & 0xff);
	ps->Pc += 4;
}

void ADD(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Dest_val + Src_val;
	ps->Pc += 2;
}

void SUB(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Dest_val - Src_val;
	ps->Pc += 2;
}

void AND(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Dest_val & Src_val;
	ps->Pc += 2;
}

void ORR(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Dest_val | Src_val;
	ps->Pc += 2;
}

void XOR(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Dest_val ^ Src_val;
	ps->Pc += 2;
}

void NOT(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = !Src_val;
	ps->Pc += 2;
}

void NEG(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = (uint32_t)((int32_t)Src_val * -1);
	ps->Pc += 2;
}

void LSL(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Dest_val << Src_val;
	ps->Pc += 2;
}

void LSR(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Dest_val >> Src_val;
	ps->Pc += 2;
}

void MUL(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Dest_val & Src_val;
	ps->Pc += 2;
}

void SMUL(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = (uint32_t)((int32_t)Dest_val * (int32_t)Src_val);
	ps->Pc += 2;
}

void MOD(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Dest_val % Src_val;
	ps->Pc += 2;
}

void SMOD(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] =(uint32_t)((int32_t) Dest_val % (int32_t)Src_val);
	ps->Pc += 2;
}

void DIV(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Dest_val / Src_val;
	ps->Pc += 2;
}

void SDIV(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = (uint32_t)((int32_t)Dest_val / (int32_t)Src_val);
	ps->Pc += 2;
}

void MOV(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = Src_val;
	ps->Pc += 2;
}

void ADDI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = Src_val + imm;
	ps->Pc += 4;
}

void SUBI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = Src_val - imm;
	ps->Pc += 4;
}

void ANDI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = Src_val & imm;
	ps->Pc += 4;
}

void ORRI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = Src_val | imm;
	ps->Pc += 4;
}

void XORI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = Src_val ^ imm;
	ps->Pc += 4;
}

void ASLI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	uint32_t bit = Src_val & 0x1;
	for(uint32_t i = 0;i < (imm && 0xff);i += 1){
		Src_val <<= 1;
		Src_val |= bit;
	}
	ps->Registers[Dest_num] = Src_val;
	ps->Pc += 4;
}

void ASRI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	uint32_t bit = Src_val = 0x80000000;
	for(uint32_t i = 0;i < (imm && 0x3f);i += 1){
		Src_val >>= 1;
		Src_val |= bit;
	}
	ps->Registers[Dest_num] = Src_val;
	ps->Pc += 4;
}

void LSLI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = Src_val << imm;
	ps->Pc += 4;
}

void LSRI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = Src_val >> imm;
	ps->Pc += 4;
}

void MULI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = Src_val * imm;
	ps->Pc += 4;
}

void SMULI(JRISC_ps_t *ps){
	LoadSrcDest()
	int32_t imm = (int32_t)Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] =(uint32_t)((int32_t) Src_val * imm);
	ps->Pc += 4;
}

void MODI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = Src_val % imm;
	ps->Pc += 4;
}

void SMODI(JRISC_ps_t *ps){
	LoadSrcDest()
	int32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = Src_val % imm;
	ps->Pc += 4;
}

void DIVI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = Src_val / imm;
	ps->Pc += 4;
}

void SDIVI(JRISC_ps_t *ps){
	LoadSrcDest()
	int32_t imm = (int32_t)Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = ((int32_t)Src_val) / imm;
	ps->Pc += 4;
}

void JMP(JRISC_ps_t *ps){
	uint32_t imm = Load_word(ps->Pc,ps->Ram) & 0xffffff;
	ps->Pc = Add_signed_24(ps->Pc,imm);
}

void JEQ(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	if(Src_val == Dest_val){
		ps->Pc = Add_signed_16(ps->Pc,imm);
	}
	else{
		ps->Pc += 4;
	}
}

void JNE(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	if(Src_val != Dest_val){
		ps->Pc = Add_signed_16(ps->Pc,imm);
	}
	else{
		ps->Pc += 4;
	}
}

void JLT(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	if(Dest_val < Src_val){
		ps->Pc = Add_signed_16(ps->Pc,imm);
	}
	else{
		ps->Pc += 4;
	}
}

void JGT(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	if(Dest_val > Src_val){
		ps->Pc = Add_signed_16(ps->Pc,imm);
	}
	else{
		ps->Pc += 4;
	}
}

void JLE(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	if(Dest_val <= Src_val){
		ps->Pc = Add_signed_16(ps->Pc,imm);
	}
	else{
		ps->Pc += 4;
	}
}

void JGE(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	if(Dest_val >= Src_val){
		ps->Pc = Add_signed_16(ps->Pc,imm);
	}
	else{
		ps->Pc += 4;
	}
}

void JSEQ(JRISC_ps_t *ps){
	JEQ(ps);
}

void JSNE(JRISC_ps_t *ps){
	JNE(ps);
}

void JSLT(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	if(((int32_t)Dest_val)  < ((int32_t)Src_val)){
		ps->Pc = Add_signed_16(ps->Pc,imm);
	}
	else{
		ps->Pc += 4;
	}
}

void JSGT(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	if(((int32_t)Dest_val)  > ((int32_t)Src_val)){
		ps->Pc = Add_signed_16(ps->Pc,imm);
	}
	else{
		ps->Pc += 4;
	}
}

void JSLE(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	if(((int32_t)Dest_val)  <= ((int32_t)Src_val)){
		ps->Pc = Add_signed_16(ps->Pc,imm);
	}
	else{
		ps->Pc += 4;
	}
}

void JSGE(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	if(((int32_t)Dest_val)  >= ((int32_t)Src_val)){
		ps->Pc = Add_signed_16(ps->Pc,imm);
	}
	else{
		ps->Pc += 4;
	}
}

void LEA(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_word(ps->Pc,ps->Ram) & 0xffff;
	ps->Registers[Dest_num] = Add_signed_16(ps->Pc,imm);
	ps->Pc += 4;
}

void MOVU(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	ps->Registers[Dest_num] = imm << 16;
	ps->Pc += 4;
}

void ADDPC(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[Dest_num] = ps->Pc + Src_val;
	ps->Pc += 2;
}

void CAL(JRISC_ps_t *ps){
	uint32_t imm = Load_word(ps->Pc,ps->Ram) & 0xffffff;
	ps->Registers[0xf] = ps->Pc + 4;
	ps->Pc = Add_signed_24(ps->Pc,imm);
}

void CAR(JRISC_ps_t *ps){
	LoadSrcDest()
	ps->Registers[0xf] = ps->Pc + 2;
	ps->Pc = Dest_val;
}

void RET(JRISC_ps_t *ps){
	ps->Pc = ps->Registers[0xf];
}

void INT_INS(JRISC_ps_t *ps){
	uint8_t int_number = ps->Ram[ps->Pc + 1];
	ps->Inturupt = int_number;
	ps->Pc += 2;
}

void RINT(JRISC_ps_t *ps){
	//Todo: add Logic
	ps->Pc += 2;
}

void POPIRA(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void PSHIRA(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void CSR(JRISC_ps_t *ps){
	//Todo: add Logic
	ps->Pc += 4;
}

void (*JRISC_instructions[256])(JRISC_ps_t*) = {
	NOP,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	LDB,
	LDH,
	LDW,
	INVALID,
	LDBS,
	LDHS,
	LDWS,
	INVALID,
	STB,
	STH,
	STW,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	LDBI,
	LDHI,
	LDWI,
	INVALID,
	LDBSI,
	LDHSI,
	LDWSI,
	INVALID,
	STBI,
	STHI,
	STWI,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	ADD,
	SUB,
	AND,
	ORR,
	XOR,
	NOT,
	NEG,
	LSL,
	LSR,
	MUL,
	SMUL,
	MOD,
	SMOD,
	DIV,
	SDIV,
	MOV,
	ADDI,
	SUBI,
	ANDI,
	ORRI,
	XORI,
	ASLI,
	ASRI,
	LSLI,
	LSRI,
	MULI,
	SMULI,
	MODI,
	SMODI,
	DIVI,
	SDIVI,
	INVALID,
	JMP,
	JEQ,
	JNE,
	JLT,
	JGT,
	JLE,
	JGE,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	JSEQ,
	JSNE,
	JSLT,
	JSGT,
	JSLE,
	JSGE,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	LEA,
	MOVU,
	ADDPC,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	CAL,
	CAR,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	RET,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INT_INS,
	RINT,
	POPIRA,
	PSHIRA,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	CSR,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID,
	INVALID
};
