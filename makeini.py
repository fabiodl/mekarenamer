mt = "MAPPER"

mapperConv = {
    # 0 : standard sms/gg sega mapper, optional SRAM
    0: {mt: "SEGA"},
    # 1 : 32KB of RAM mapped at 0x8000-0xFFFF
    1: {mt: "RAM32K"},
    # 2 : colecovisions
    2: {mt: "COLECO"},
    # 3 : code masters mapper, registers at 0x0000, 0x4000, 0x8000
    3: {mt: "CODE"},
    # 4 : sega mapper with 93c46 eeprom
    4: {mt: "EEPROM"},
    # 5 : sg-1000 (currently incorrectly emulating 4KB of RAM instead of 2KB)
    5: {mt: "SG1000"},
    # 6 : master system action replay
    # 7 : terebi oekaki (graphic tablet)
    # 8 : sf-7000
    6: {mt: "ACTIONREPLAY"}, 7: {mt: "TVOEKAKI"}, 8: {mt: "SF7000"},
    # 9 : sms korean mapper, mapping register at 0xA000
    9: {mt: "KOR"},
    # 10 : sms display unit BIOS
    10: {mt: "DISPLAYINIT"},
    # 11 : no mapper, ROM up to 48KB (typically 32KB)
    11: {mt: "NOMAPPER"},
    # 12 : sms korean msx type 8KB banks, registers at 0x0000->0x0003
    # 13 : sms korean for Janggun-ui Adeul
    # 14 : sms 4 Pak All Action
    12: {mt: "KOR_MSX"}, 13: {mt: "KOR_JANGGUN"}, 14: {mt: "4PAK"},
    # 15 : sg-1000 II with taiwanese memory expansion adapter, 8KB RAM from 0x2000->0x3FFF + regular 2KB RAM mapped at 0xC000-0xFFFF
    15: {mt: "TW_EXP_2000"},

    # 16 : sms korean xx-in-1, register at 0xFFFF mapping 32 KB at 0x0000->0x8000 (hi-com cartridges)
    # 17 : sc-3000 survivors multicart.
    # 18 : sms korean xx-in-1, register at 0x0000 mapping 8 KB at 0x8000, register at 0x0100 mapping 8 KB at 0x4000, register at 0x0200 mapping 8 KB at 0xA000, register at 0x0300 mapping 8 KB at 0x6000
    # 19 : sms korean xx-in-1, register at 0x2000 mapping 8x4 KB 0x4000-0xBFFF using register xored with 0x1F, 0x1E, 0x1D, 0x1C. 0x0000-0x3FFF stuck on bank 0.
    # 20 : sms korean xx-in-1, register at 0xBFFC, sms+msx
    16: {mt: "KOR_HICOM"}, 17: {mt: "SURVIVORS"}, 18: {mt: "KOR_XXIN1_0000"}, 19: {mt: "KOR_XXIN1_2000"}, 20: {mt: "KOR_XXIN1_BFFC"},
    21: {mt: "TW_EXP_C000"},
}


def getIni(ma, flags):
    if not ma:
        return None
    mapper = int(ma)
    mc = mapperConv[mapper]
    for f in ["VIDEO"]:
        if f in flags:
            mc[f] = flags[f]

    r = "\n".join([f"{k}={v}" for k, v in mc.items()])
    return r
