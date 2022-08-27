#!/usr/bin/env python3
import glob
import zlib
import os
import io
import re
from pathlib import Path
import shutil
from makeini import getIni
import sys

meka = {}

for l in open("meka.nam").readlines():
    tok = l.split()

    if "OLD DATA" in l:
        break
    if l[0] == ";" or len(tok) < 2:
        continue
    meka[tok[1]] = l


def compFileset(loc):
    crc = {}
    for zn in glob.glob(loc+"**/*", recursive=True):
        if os.path.isfile(zn):
            c = zlib.crc32(open(zn, "rb").read())
            cs = f"{c:08x}"
            crc.setdefault(cs, []).append(zn)
    print(f"Found {len(crc)} unique roms")
    return crc


def getField(m, field):
    flags = re.search(f"{field}=([^/]*)", meka[m].strip())
    if flags is not None:
        flags = flags.group(1)
    return flags


def getFlags(m):
    return getField(m, "FLAGS")


def isOfficial(m):
    flags = getFlags(m)
    return flags is None or all([x not in flags for x in ["BAD", "HOMEBREW", "HACK", "PROTO"]])


def printSet(s):
    for m in s:
        print(meka[m])


extMap = {"GG": "gg",
          "OMV": "omv",
          "SC3": "sc",
          "SF7": "sf7",
          "SG1": "sg",
          "SMS": "sms"
          }


def getNames(mekaSet):
    shortnames = {}
    variants = {}
    for m in mekaSet:
        tok = meka[m].split()
        ext = tok[0]
        crc = tok[1]
        content = " ".join(tok[3:])
        name = content.split("/")[0]
        country = getField(m, "COUNTRY")
        if country is None:
            country = ""
        else:
            country = f"[{country.split()[0]}]"

        if (flags := getFlags(m)) is not None and "TRANS" in flags:
            tt = getField(m, "TRANS")
            ta = getField(m, "AUTHORS")
            fields = ",".join(
                ["_" if f == "?" else f for f in [tt, ta] if f is not None])
            if fields != "":
                country += f"[{fields}]"
        sname = name+country+"."+extMap[ext]

        shortnames[crc] = sname
        variants.setdefault(sname, []).append(meka[m])
        if len(variants[sname]) > 1:
            print(variants[sname])
            return None
    return shortnames


membackup = ["35fa3f68",
             "e2791cc1", "c674eccc", "09f9ed60",
             "04302bbd",
             "4cf97801",
             "c7ded988",
             "48651325",
             "5dabfdc3",
             "7f7b568d",
             "a12a28a0",
             "abddf0eb",
             "4af7f2aa", "808a71c3",
             "58459edd",
             "7ec95282",
             "00c34d94",
             "12eb2287",
             "0a634d79",
             "568f4825",
             "8f82a6b9",
             "1c2c2b04",
             "36ebcd6d",
             "2e4ec17b",
             "4ec30806",
             "b9fdf6d9", "0e333b6e", "301a59aa",
             "4d5d15fb",
             "026d94a4", "69538469", "7e9d87fc",
             "73939de4",
             "3679be80",
             "4ed45bda",
             "2bcdb8fa", "fb163003", "56bd2455", "f97e9875",
             "6605d36a", "07301f83", "00bef1d7", "75971bef", "747e83b5", "e4a65e79",
             "a942514a",
             "445d7cd2",
             "5e2b39b8",
             "4d1f4699",
             "6019fe5e", "30374681", "a6ca6fa9",
             "45ef2062",
             "7b7717b8",
             "b52d60c8",
             "de9f8517",
             "32759751", "b33e2827", "e8b82066"
             ]


def getNames(mekaSet):
    shortnames = {}
    variants = {}
    for m in mekaSet:
        tok = meka[m].split()
        ext = tok[0]
        crc = tok[1]
        content = " ".join(tok[3:])
        name = content.split("/")[0]
        country = getField(m, "COUNTRY")
        if country is None:
            country = ""
        else:
            country = f"[{country.split()[0]}]"

        if (flags := getFlags(m)) is not None and "TRANS" in flags:
            tt = getField(m, "TRANS")
            ta = getField(m, "AUTHORS")
            fields = ",".join(
                ["_" if f == "?" else f for f in [tt, ta] if f is not None])
            if fields != "":
                country += f"[{fields}]"
        sname = name+country+"."+extMap[ext]

        shortnames[crc] = sname
        variants.setdefault(sname, []).append(meka[m])
        if len(variants[sname]) > 1:
            raise Exception("Multiple roms have the same name",
                            variants[sname])
    return shortnames


extToFolder = {"GG": "Game Gear",
               "OMV": "SG 1000",
               "SC3": "SG 1000",
               "SF7": "SF 7000",
               "SG1": "SG 1000",
               "SMS": "Master System"
               }


def makeTree(dst, mekaSet, byletter):
    shortnames = getNames(mekaSet)
    for m in mekaSet:
        if m in have:
            name = shortnames[m]
            let = name[0].upper()
            leadLetter = let if 'A' <= let <= 'Z' else '0'
            tok = meka[m].split()
            sys = extToFolder[tok[0]]
            folder = [dst, sys]
            if byletter(sys):
                folder.append(leadLetter)
            # print("folder", folder)
            Path(os.path.join(*folder)).mkdir(
                parents=True, exist_ok=True)
            fname = os.path.join(*(folder+[name]))
            shutil.copyfile(have[m][0], fname)
            ini = getIni(getField(m, "MAPPER"), [])
            if ini:
                inifname = os.path.splitext(fname)[0]+".ini"
                with open(inifname, "w") as f:
                    f.write(ini)
                    print("created", inifname)
            if m in membackup:
                ramfname = os.path.splitext(fname)[0]+".ram"
                with open(ramfname, "wb") as f:
                    f.write(bytes([0x00] * 32*1024))
                    print("created", ramfname)
        else:
            print("missing", meka[m])


def getFields(m):
    fields = {}
    for f in meka[m].split("/")[1:]:
        t = [t.strip() for t in f.split("=")]
        if len(t) > 1:
            fields[t[0]] = t[1]
        else:
            fields[t[0]] = ""
    return fields


mekafields = {m: getFields(m) for m in meka}
allfields = set()
for m, d in mekafields.items():
    allfields = allfields.union(d.keys())


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage {sys.argv[0]} sourceFolder destionationFolder")
    else:
        homebrew = [m for m in meka if (flags := getFlags(
            m)) is not None and "HOMEBREW" in flags and "BAD" not in flags]

        have = compFileset(sys.argv[1])
        missing = set(meka.keys()).difference(have.keys())
        mekaOff = set([m for m in meka if isOfficial(m)])
        missingOff = mekaOff.difference(have.keys())
        print("==OFFICIAL==")
        out = Path(sys.argv[2])
        makeTree(out/"rom", mekaOff,
                 byletter=lambda sys: sys != "SF 7000")
        print("==HOMEBREW==")
        makeTree(out/"rom"/"Homebrew",
                 homebrew, byletter=lambda _: False)
