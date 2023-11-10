#include "VMachine.h"
#include "VMMacros.c"
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
	//Todo: add Logic
	ps->Pc += 2;
}

void STH(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void STW(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void LDBI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void LDHI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void LDWI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void LDBSI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void LDHSI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void LDWSI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void STBI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void STHI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void STWI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void ADD(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void SUB(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void AND(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void ORR(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void XOR(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void NOT(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void NEG(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void LSL(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void LSR(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void MUL(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void SMUL(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void MOD(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void SMOD(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void DIV(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void SDIV(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void MOV(JRISC_ps_t *ps){
	//Todo: add Logic
	ps->Pc += 4;
}

void ADDI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void SUBI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void ANDI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void ORRI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void XORI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void ASLI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void ASRI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void LSLI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void LSRI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void MULI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void SMULI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void MODI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void SMODI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void DIVI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void SDIVI(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void JMP(JRISC_ps_t *ps){
	uint32_t imm = Load_word(ps->Pc,ps->Ram) & 0xffffff;
	//Todo: add Logic
	ps->Pc += 4;
}

void JEQ(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void JNE(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void JLT(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void JGT(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void JSEQ(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void JSNE(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void JSLT(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void JSGT(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void LEA(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_word(ps->Pc,ps->Ram) & 0xfffff;
	//Todo: add Logic
	ps->Pc += 4;
}

void MOVU(JRISC_ps_t *ps){
	LoadSrcDest()
	uint32_t imm = Load_half(ps->Pc + 2,ps->Ram);
	//Todo: add Logic
	ps->Pc += 4;
}

void ADDPC(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void CAL(JRISC_ps_t *ps){
	uint32_t imm = Load_word(ps->Pc,ps->Ram) & 0xffffff;
	//Todo: add Logic
	ps->Pc += 4;
}

void CAR(JRISC_ps_t *ps){
	LoadSrcDest()
	//Todo: add Logic
	ps->Pc += 2;
}

void RET(JRISC_ps_t *ps){
	//Todo: add Logic
	ps->Pc += 2;
}

void INT(JRISC_ps_t *ps){
	uint8_t int_number = ps->Ram[ps->Pc + 1];
	//Todo: add Logic
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

void (*JRISC_instructions[])(JRISC_ps_t*) = {
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	LDB,
	LDH,
	LDW,
	NOP,
	LDBS,
	LDHS,
	LDWS,
	NOP,
	STB,
	STH,
	STW,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	LDBI,
	LDHI,
	LDWI,
	NOP,
	LDBSI,
	LDHSI,
	LDWSI,
	NOP,
	STBI,
	STHI,
	STWI,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
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
	NOP,
	JMP,
	JEQ,
	JNE,
	JLT,
	JGT,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	JSEQ,
	JSNE,
	JSLT,
	JSGT,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	LEA,
	MOVU,
	ADDPC,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	CAL,
	CAR,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	RET,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	INT,
	RINT,
	POPIRA,
	PSHIRA,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	CSR,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP,
	NOP
};