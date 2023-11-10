#include "VM.h"

inline u32 s16add(u32 base,u32 value){
    if(value && 0x8000){
        return base - (value & 0x7fff);
    }
    else{
        return base + value;
    }
}

inline u32 s24add(u32 base,u32 value){
    if(value & 0x800000){
        return base - (value & 0x7fffff);
    }
    else{
        return base + value;
    }
}

inline u32 u8load(u8 *ram,u32 loc){
    return (u8) ram[loc];
}

inline u32 u16load(u8 *ram,u32 loc){
    u32 value = (u32) ram[loc];
    value <<= 8;
    value |= (u32) ram[loc+1];
    return value;
}

inline u32 u32load(u8 *ram,u32 loc){
    u32 value = (u32) ram[loc];
    value <<= 8;
    value |= (u32) ram[loc + 1];
    value <<= 8;
    value |= (u32) ram[loc + 2];
    value <<= 8;
    value |= (u32) ram[loc + 3];
    return value;
}

inline void u8store(u32 value,u8 *ram,u32 loc){
    ram[loc] = (u8) value & 0xff;
}

inline void u16store(u32 value,u8 *ram,u32 loc){
    u8 little = (u8) value & 0xff;
    u8 big = (u8) (value >> 8) & 0xff; 
    ram[loc] = big;
    ram[loc + 1] = little;
}

inline void u32store(u32 value,u8 *ram,u32 loc){
    u8 D = (u8) value & 0xff;
    u8 C = (u8) (value >> 8) & 0xff;
    u8 B = (u8) (value >> 16) & 0xff;
    u8 A = (u8) (value >> 24) & 0xff;
    ram[loc] = A;
    ram[loc + 1] = B;
    ram[loc + 2] = C;
    ram[loc + 3] = D;
}

inline s32 u32tos32(u32 value){
    union{u32 uvalue;
    s32 svalue;} c;
    c.uvalue = value;
    return c.svalue;
}

inline s32 s32tou32(s32 value){
    union{u32 uvalue;
    s32 svalue} c;
    c.svalue = value;
    return c.uvalue;
}
