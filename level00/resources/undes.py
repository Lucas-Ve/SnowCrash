tokens = [
    "I`fA>_88eEd:=`85h0D8HE>,D",
    "7`4Ci4=^d=J,?>i;6,7d416,7",
    "<>B16\\AD<C6,G_<1>^7ci>l4B",
    "B8b:6,3fj7:,;bh>D@>8i:6@D",
    "?4d@:,C>8C60G>8:h:Gb4?l,A",
    "G8H.6,=4k5J0<cd/D@>>B:>:4",
    "H8B8h_20B4J43><8>\\ED<;j@3",
    "78H:J4<4<9i_I4k0J^5>B1j`9",
    "bci`mC{)jxkn<\"uD~6%g7FK`7",
    "Dc6m~;}f8Cj#xFkel;#&ycfbK",
    "74H9D^3ed7k05445J0E4e;Da4",
    "70hCi,E44Df[A4B/J@3f<=:`D",
    "8_Dw\"4#?+3i]q&;p6 gtw88EC",
    "boe]!ai0FB@.:|L6l@A?>qJ}I",
    "g <t61:|4_|!@IF.-62FH&G~DCK/Ekrvvdwz?v|",
]

def ft_des(s: str) -> str:
    out = []
    pattern = "0123456"
    idx = 0
    for i, ch in enumerate(s):
        if idx == 6:
            idx = 0
        step = ord(pattern[idx])
        o = ord(ch)
        if i % 2 == 0:
            for l in range(step):
                o -= 1
                if o == 0x1F:
                    o = ord('~')
        else:
            for l in range(step):
                o += 1
                if o == 0x7F:
                    o = ord(' ')
        out.append(chr(o))
        idx += 1
    return ''.join(out)

for t in tokens:
    print(ft_des(t))