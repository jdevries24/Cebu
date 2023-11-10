typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;

inline u32 s16add(u32 base,u32 value);

inline u32 s24add(u32 base,u32 value);

inline u32 u8load(u8 *ram,u32 loc);

inline u32 u16load(u8 *ram,u32 loc);

inline u32 u32load(u8 *ram,u32 loc);

inline void u8store(u32 value,u8 *ram,u32 loc);

inline void u16store(u32 value,u8 *ram,u32 loc);

inline void u32store(u32 value,u8 *ram,u32 loc);

inline u32 s32tou32(s32 value);

inline s32 u32tos32(u32 value);