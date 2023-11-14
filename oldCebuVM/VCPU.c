#include "VM.h"
#define loadsd() \
u8 src = JR->ram[JR->pc + 1] >> 4;\
u8 dest = JR->ram[JR->pc + 1] & 0xf;

#define loadim() \
u32 im = u16load(JR->ram,JR->pc + 2);

void INVALID(JRISCdev *JR){
    //Todo Logic
}


void NOP(JRISCdev *JR){
    JR->pc += 2;
}

void RET(JRISCdev *JR){
    JR->pc = JR->registers[15];
}

void CAR(JRISCdev *JR){
    loadsd()
    JR->registers[15] = JR->pc + 2;
    JR->pc = JR->registers[src];
}

void CAL(JRISCdev *JR){
    u32 pc = JR->pc;
    u32 offset = (u32)JR->ram[pc + 1];
    offset <<= 8;
    offset |= (u32)JR->ram[pc + 2];
    offset <<= 8;
    offset |= (u32)JR->ram[pc + 3];
    JR->registers[15] = pc + 4;
    JR->pc = s24add(JR->pc,offset);
}

void LEA(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = s16add(JR->pc,im);
    JR->pc += 4;
}

void INT(JRISCdev *JR){
    //Todo Write Logic
    JR->pc += 2;
}

void RINT(JRISCdev *JR){
    //Todo Write Logic
    JR->pc += 2;
}

void POPINT(JRISCdev *JR){
    loadsd()
    //Todo Write Logic
    JR->pc += 2;
}

void PSHINT(JRISCdev *JR){
    loadsd()
    //Todo Write Logic
    JR->pc += 2;
}

void CSR(JRISCdev *JR){
    //Todo Write Logic
    JR->pc += 2;
}

void LDB(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = u8load(JR->ram,JR->registers[src]);
    JR->pc += 2;
}

void LDH(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = u16load(JR->ram,JR->registers[src]);
    JR->pc += 2;
}

void LDW(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = u32load(JR->ram,JR->registers[src]);
    JR->pc += 2;
}

void LSB(JRISCdev *JR){
    loadsd()
    u32 val = u8load(JR->ram,JR->registers[src]);
    if(val & 0x70){
        val |= 0xffffff00;
    }
    JR->registers[dest] = val;
    JR->pc += 2;
}

void LSH(JRISCdev *JR){
    loadsd()
    u32 val = u16load(JR->ram,JR->registers[src]);
    if(val & 0x7000){
        val |= 0xffff0000;
    }
    JR->registers[dest] = val;
    JR->pc += 2;
}

void LSW(JRISCdev *JR){
    LDW(JR);
}

void STB(JRISCdev *JR){
    loadsd()
    u8store(JR->registers[src],JR->ram,JR->registers[dest]);
    JR->pc += 2;
}

void STH(JRISCdev *JR){
    loadsd()
    u16store(JR->registers[src],JR->ram,JR->registers[dest]);
    JR->pc += 2;
}

void STW(JRISCdev *JR){
    loadsd()
    u32store(JR->registers[src],JR->ram,JR->registers[dest]);
    JR->pc += 2;
}

void ADD(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = JR->registers[src] + JR->registers[dest];
    JR->pc += 2;
}

void SUB(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = JR->registers[src] - JR->registers[dest];
    JR->pc += 2;
}

void AND(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = JR->registers[src] & JR->registers[dest];
    JR->pc += 2;
}

void ORR(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = JR->registers[src] | JR->registers[dest];
    JR->pc += 2;
}

void XOR(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = JR->registers[src] ^ JR->registers[dest];
    JR->pc += 2;
}

void NEG(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = (!JR->registers[src]) + 1;
    JR->pc += 2;
}

void NOT(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = !JR->registers[src];
    JR->pc += 2;
}

void LSL(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = JR->registers[src] >> JR->registers[dest];
    JR->pc += 2;
}

void LSR(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = JR->registers[src] >> JR->registers[dest];
    JR->pc += 2;
}

void MUL(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = JR->registers[src] * JR->registers[dest];
    JR->pc += 2;
}

void SMUL(JRISCdev *JR){
    loadsd()
    //Todo Write Logic
    JR->pc += 2;
}

void MOD(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = JR->registers[src] % JR->registers[dest];
    JR->pc += 2;
}

void SMOD(JRISCdev *JR){
    loadsd()
    //Todo Write Logic
    JR->pc += 2;
}

void DIV(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = JR->registers[src] / JR->registers[dest];
    JR->pc += 2;
}

void SDIV(JRISCdev *JR){
    loadsd()
    //Todo Write Logic
    JR->pc += 2;
}

void JMP(JRISCdev *JR){
    loadim()
    JR->pc = s16add(JR->pc,im);
}

void JME(JRISCdev *JR){
    loadsd()
    loadim()
    if(JR->registers[src] == JR->registers[dest]){
        JR->pc = s16add(JR->pc,im);
    }
    else{
        JR->pc += 4;
    }
}


void JNE(JRISCdev *JR){
    loadsd()
    loadim()
    if(JR->registers[src] != JR->registers[dest]){
        JR->pc = s16add(JR->pc,im);
    }
    else{
        JR->pc += 4;
    }
}

void JLT(JRISCdev *JR){
    loadsd()
    loadim()
    if(JR->registers[src] < JR->registers[dest]){
        JR->pc = s16add(JR->pc,im);
    }
    else{
        JR->pc += 4;
    }
}

void JGT(JRISCdev *JR){
    loadsd()
    loadim()
    if(JR->registers[src] > JR->registers[dest]){
        JR->pc = s16add(JR->pc,im);
    }
    else{
        JR->pc += 4;
    }
}

void JSME(JRISCdev *JR){
    loadsd()
    loadim()
    //Todo Write Logic
    JR->pc += 4;
}

void JSNE(JRISCdev *JR){
    loadsd()
    loadim()
    //Todo Write Logic
    JR->pc += 4;
}

void JSLT(JRISCdev *JR){
    loadsd()
    loadim()
    //Todo Write Logic
    JR->pc += 4;
}

void JSGT(JRISCdev *JR){
    loadsd()
    loadim()
    //Todo Write Logic
    JR->pc += 4;
}

void LDBI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = u8load(JR->ram,s16add(JR->registers[src],im));
    JR->pc += 4;
}

void LDHI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = u16load(JR->ram,s16add(JR->registers[src],im));
    JR->pc += 4;
}

void LDWI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = u32load(JR->ram,s16add(JR->registers[src],im));
    JR->pc += 4;
}

void LSBI(JRISCdev *JR){
    loadsd()
    loadim()
    u32 value = u8load(JR->ram,s16add(JR->registers[src],im));
    if(value & 0x70){
        value |= 0xffffff00;
    }
    JR->registers[dest] = value;
    JR->pc += 4;
}

void LSHI(JRISCdev *JR){
    loadsd()
    loadim()
    u32 value = u16load(JR->ram,s16add(JR->registers[src],im));
    if(value & 0x7000){
        value |= 0xffff0000;
    }
    JR->registers[dest] = value;
    JR->pc += 4;
}

void LSWI(JRISCdev *JR){
    loadsd()
    loadim()
    LDWI(JR);
}

void STBI(JRISCdev *JR){
    loadsd()
    loadim()
    u8store(JR->registers[src],JR->ram,s16add(JR->registers[dest],im));
    JR->pc += 4;
}

void STHI(JRISCdev *JR){
    loadsd()
    loadim()
    u32store(JR->registers[src],JR->ram,s16add(JR->registers[dest],im));
    JR->pc += 4;
}

void STWI(JRISCdev *JR){
    loadsd()
    loadim()
    u32store(JR->registers[src],JR->ram,s16add(JR->registers[dest],im));
    JR->pc += 4;
}

void ADDI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = JR->registers[src] + im;
    JR->pc += 4;
}

void SUBI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = JR->registers[src] - im;
    JR->pc += 4;
}

void ANDI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = JR->registers[src] & im;
    JR->pc += 4;
}

void ORRI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = JR->registers[src] | im;
    JR->pc += 4;
}

void XORI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = JR->registers[src] ^ im;
    JR->pc += 4;
}

void LSLI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = JR->registers[src] << im;
    JR->pc += 4;
}

void LSRI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = JR->registers[src] >> im;
    JR->pc += 4;
}

void MULI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = JR->registers[src] * im;
    JR->pc += 4;
}

void SMULI(JRISCdev *JR){
    loadsd()
    loadim()
    //Todo Write Logic
    JR->pc += 4;
}

void MODI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = JR->registers[src] % im;
    JR->pc += 4;
}

void SMODI(JRISCdev *JR){
    loadsd()
    loadim()
    //Todo Write Logic
    JR->pc += 4;
}

void DIVI(JRISCdev *JR){
    loadsd()
    loadim()
    JR->registers[dest] = JR->registers[src] / im;
    JR->pc += 4;
}

void SDIVI(JRISCdev *JR){
    loadsd()
    loadim()
    //Todo Write Logic
    JR->pc += 4;
}

void MOV(JRISCdev *JR){
    loadsd()
    JR->registers[dest] = JR->registers[src];
    JR->pc += 2;
}

void (*INSTRUCTIONS[255])(JRISCdev *JR) = {NOP,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,LDB,LDH,LDW,INVALID,LSB,LSH,LSW,INVALID,STB,STH,STW,INVALID,INVALID,INVALID,INVALID,INVALID,LDBI,LDHI,LDWI,INVALID,LSBI,LSHI,LSWI,INVALID,STBI,STHI,STWI,INVALID,INVALID,INVALID,INVALID,INVALID,ADD,SUB,AND,ORR,XOR,NOT,NEG,LSL,LSR,MUL,SMUL,MOD,SMOD,DIV,SDIV,INVALID,ADDI,SUBI,ANDI,ORRI,XORI,INVALID,INVALID,LSLI,LSRI,MULI,SMULI,MODI,SMODI,DIVI,SDIVI,INVALID,JMP,JME,JNE,JLT,JGT,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,JSME,JSNE,JSLT,JSGT,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,MOV,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,CAL,CAR,LEA,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,RET,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INT,RINT,POPINT,PSHINT,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,CSR,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID,INVALID};