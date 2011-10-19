#!/usr/bin/python
import sys 
sys.path.insert(0, "..")
from mcda.types import criterion, criteria, action, actions, profile, threshold, alternative_performances, performance_table

# Weights
g1 = criterion('g1', 'g1', 0, 1, 0.02)
g2 = criterion('g2', 'g2', 0, 1, 0.05)
g3 = criterion('g3', 'g3', 0, 1, 0.06)
g4 = criterion('g4', 'g4', 0, 1, 0.06)
g5 = criterion('g5', 'g5', 0, 1, 0.07)
g6 = criterion('g6', 'g6', 0, 1, 0.09)
g7 = criterion('g7', 'g7', 0, 1, 0.09)
g8 = criterion('g8', 'g8', 0, 1, 0.11)
g9 = criterion('g9', 'g9', 0, 1, 0.13)
g10 = criterion('g10', 'g10', 0, 1, 0.15)
g11 = criterion('g11', 'g11', 0, 1, 0.17)
c = criteria([ g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11 ])

# Actions
a0 = action('a0')
a1 = action('a1')
a2 = action('a2')
a3 = action('a3')
a4 = action('a4')
a5 = action('a5')
a6 = action('a6')
a7 = action('a7')
a8 = action('a8')
a9 = action('a9')
a10 = action('a10')
a11 = action('a11')
a12 = action('a12')
a13 = action('a13')
a14 = action('a14')
a15 = action('a15')
a16 = action('a16')
a17 = action('a17')
a18 = action('a18')
a19 = action('a19')
a20 = action('a20')
a21 = action('a21')
a22 = action('a22')
a23 = action('a23')
a24 = action('a24')
a25 = action('a25')
a26 = action('a26')
a27 = action('a27')
a28 = action('a28')
a29 = action('a29')
a30 = action('a30')
a31 = action('a31')
a32 = action('a32')
a33 = action('a33')
a34 = action('a34')
a35 = action('a35')
a36 = action('a36')
a37 = action('a37')
a38 = action('a38')
a39 = action('a39')
a40 = action('a40')
a41 = action('a41')
a42 = action('a42')
a43 = action('a43')
a44 = action('a44')
a45 = action('a45')
a46 = action('a46')
a47 = action('a47')
a48 = action('a48')
a49 = action('a49')
a50 = action('a50')
a51 = action('a51')
a52 = action('a52')
a53 = action('a53')
a54 = action('a54')
a55 = action('a55')
a56 = action('a56')
a57 = action('a57')
a58 = action('a58')
a59 = action('a59')
a60 = action('a60')
a61 = action('a61')
a62 = action('a62')
a63 = action('a63')
a64 = action('a64')
a65 = action('a65')
a66 = action('a66')
a67 = action('a67')
a68 = action('a68')
a69 = action('a69')
a70 = action('a70')
a71 = action('a71')
a72 = action('a72')
a73 = action('a73')
a74 = action('a74')
a75 = action('a75')
a76 = action('a76')
a77 = action('a77')
a78 = action('a78')
a79 = action('a79')
a80 = action('a80')
a81 = action('a81')
a82 = action('a82')
a83 = action('a83')
a84 = action('a84')
a85 = action('a85')
a86 = action('a86')
a87 = action('a87')
a88 = action('a88')
a89 = action('a89')
a90 = action('a90')
a91 = action('a91')
a92 = action('a92')
a93 = action('a93')
a94 = action('a94')
a95 = action('a95')
a96 = action('a96')
a97 = action('a97')
a98 = action('a98')
a99 = action('a99')
a100 = action('a100')
a101 = action('a101')
a102 = action('a102')
a103 = action('a103')
a104 = action('a104')
a105 = action('a105')
a106 = action('a106')
a107 = action('a107')
a108 = action('a108')
a109 = action('a109')
a110 = action('a110')
a111 = action('a111')
a112 = action('a112')
a113 = action('a113')
a114 = action('a114')
a115 = action('a115')
a116 = action('a116')
a117 = action('a117')
a118 = action('a118')
a119 = action('a119')
a120 = action('a120')
a121 = action('a121')
a122 = action('a122')
a123 = action('a123')
a124 = action('a124')
a125 = action('a125')
a126 = action('a126')
a127 = action('a127')
a128 = action('a128')
a129 = action('a129')
a130 = action('a130')
a131 = action('a131')
a132 = action('a132')
a133 = action('a133')
a134 = action('a134')
a135 = action('a135')
a136 = action('a136')
a137 = action('a137')
a138 = action('a138')
a139 = action('a139')
a140 = action('a140')
a141 = action('a141')
a142 = action('a142')
a143 = action('a143')
a144 = action('a144')
a145 = action('a145')
a146 = action('a146')
a147 = action('a147')
a148 = action('a148')
a149 = action('a149')
a150 = action('a150')
a151 = action('a151')
a152 = action('a152')
a153 = action('a153')
a154 = action('a154')
a155 = action('a155')
a156 = action('a156')
a157 = action('a157')
a158 = action('a158')
a159 = action('a159')
a160 = action('a160')
a161 = action('a161')
a162 = action('a162')
a163 = action('a163')
a164 = action('a164')
a165 = action('a165')
a166 = action('a166')
a167 = action('a167')
a168 = action('a168')
a169 = action('a169')
a170 = action('a170')
a171 = action('a171')
a172 = action('a172')
a173 = action('a173')
a174 = action('a174')
a175 = action('a175')
a176 = action('a176')
a177 = action('a177')
a178 = action('a178')
a179 = action('a179')
a180 = action('a180')
a181 = action('a181')
a182 = action('a182')
a183 = action('a183')
a184 = action('a184')
a185 = action('a185')
a186 = action('a186')
a187 = action('a187')
a188 = action('a188')
a189 = action('a189')
a190 = action('a190')
a191 = action('a191')
a192 = action('a192')
a193 = action('a193')
a194 = action('a194')
a195 = action('a195')
a196 = action('a196')
a197 = action('a197')
a198 = action('a198')
a199 = action('a199')
a200 = action('a200')
a201 = action('a201')
a202 = action('a202')
a203 = action('a203')
a204 = action('a204')
a205 = action('a205')
a206 = action('a206')
a207 = action('a207')
a208 = action('a208')
a209 = action('a209')
a210 = action('a210')
a211 = action('a211')
a212 = action('a212')
a213 = action('a213')
a214 = action('a214')
a215 = action('a215')
a216 = action('a216')
a217 = action('a217')
a218 = action('a218')
a219 = action('a219')
a220 = action('a220')
a221 = action('a221')
a222 = action('a222')
a223 = action('a223')
a224 = action('a224')
a225 = action('a225')
a226 = action('a226')
a227 = action('a227')
a228 = action('a228')

a = actions([ a0, a1, a2, a3, a4, a5, a6, a7,
              a8, a9, a10, a11, a12, a13, a14, a15,
              a16, a17, a18, a19, a20, a21, a22, a23,
              a24, a25, a26, a27, a28, a29, a30, a31,
              a32, a33, a34, a35, a36, a37, a38, a39,
              a40, a41, a42, a43, a44, a45, a46, a47,
              a48, a49, a50, a51, a52, a53, a54, a55,
              a56, a57, a58, a59, a60, a61, a62, a63,
              a64, a65, a66, a67, a68, a69, a70, a71,
              a72, a73, a74, a75, a76, a77, a78, a79,
              a80, a81, a82, a83, a84, a85, a86, a87,
              a88, a89, a90, a91, a92, a93, a94, a95,
              a96, a97, a98, a99, a100, a101, a102, a103,
              a104, a105, a106, a107, a108, a109, a110, a111,
              a112, a113, a114, a115, a116, a117, a118, a119,
              a120, a121, a122, a123, a124, a125, a126, a127,
              a128, a129, a130, a131, a132, a133, a134, a135,
              a136, a137, a138, a139, a140, a141, a142, a143,
              a144, a145, a146, a147, a148, a149, a150, a151,
              a152, a153, a154, a155, a156, a157, a158, a159,
              a160, a161, a162, a163, a164, a165, a166, a167,
              a168, a169, a170, a171, a172, a173, a174, a175,
              a176, a177, a178, a179, a180, a181, a182, a183,
              a184, a185, a186, a187, a188, a189, a190, a191,
              a192, a193, a194, a195, a196, a197, a198, a199,
              a200, a201, a202, a203, a204, a205, a206, a207,
              a208, a209, a210, a211, a212, a213, a214, a215,
              a216, a217, a218, a219, a220, a221, a222, a223,
              a224, a225, a226, a227, a228 ])

# Performance table
p0 = alternative_performances(a0, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:2, g10:3, g11:5})
p1 = alternative_performances(a1, {g1: 1, g2:2, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
p2 = alternative_performances(a2, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p3 = alternative_performances(a3, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:3, g11:5})
p4 = alternative_performances(a4, {g1: 1, g2:3, g3:1, g4:2, g5:4, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
p5 = alternative_performances(a5, {g1: 1, g2:3, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:3, g11:5})
p6 = alternative_performances(a6, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p7 = alternative_performances(a7, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:2, g10:3, g11:5})
p8 = alternative_performances(a8, {g1: 1, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:1, g9:2, g10:3, g11:4})
p9 = alternative_performances(a9, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:2, g10:1, g11:1})
p10 = alternative_performances(a10, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:3, g11:5})
p11 = alternative_performances(a11, {g1: 2, g2:3, g3:3, g4:2, g5:3, g6:4, g7:2, g8:1, g9:2, g10:3, g11:5})
p12 = alternative_performances(a12, {g1: 2, g2:3, g3:3, g4:2, g5:3, g6:4, g7:2, g8:1, g9:2, g10:3, g11:5})
p13 = alternative_performances(a13, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
p14 = alternative_performances(a14, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p15 = alternative_performances(a15, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
p16 = alternative_performances(a16, {g1: 1, g2:3, g3:3, g4:2, g5:1, g6:4, g7:3, g8:1, g9:1, g10:3, g11:1})
p17 = alternative_performances(a17, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:3, g10:1, g11:1})
p18 = alternative_performances(a18, {g1: 1, g2:2, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
p19 = alternative_performances(a19, {g1: 2, g2:3, g3:1, g4:1, g5:1, g6:1, g7:2, g8:4, g9:2, g10:3, g11:1})
p20 = alternative_performances(a20, {g1: 1, g2:3, g3:1, g4:2, g5:1, g6:1, g7:3, g8:4, g9:3, g10:3, g11:4})
p21 = alternative_performances(a21, {g1: 1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:4, g9:1, g10:3, g11:1})
p22 = alternative_performances(a22, {g1: 1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:4, g9:1, g10:3, g11:1})
p23 = alternative_performances(a23, {g1: 2, g2:2, g3:1, g4:2, g5:1, g6:3, g7:2, g8:1, g9:2, g10:3, g11:5})
p24 = alternative_performances(a24, {g1: 1, g2:3, g3:1, g4:2, g5:1, g6:1, g7:2, g8:1, g9:2, g10:1, g11:1})
p25 = alternative_performances(a25, {g1: 2, g2:3, g3:1, g4:2, g5:1, g6:3, g7:3, g8:1, g9:1, g10:3, g11:1})
p26 = alternative_performances(a26, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p27 = alternative_performances(a27, {g1: 1, g2:2, g3:2, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
p28 = alternative_performances(a28, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
p29 = alternative_performances(a29, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p30 = alternative_performances(a30, {g1: 1, g2:2, g3:1, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
p31 = alternative_performances(a31, {g1: 3, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:5, g9:1, g10:3, g11:5})
p32 = alternative_performances(a32, {g1: 1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:3, g10:1, g11:4})
p33 = alternative_performances(a33, {g1: 1, g2:2, g3:1, g4:2, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p34 = alternative_performances(a34, {g1: 1, g2:3, g3:1, g4:2, g5:3, g6:1, g7:2, g8:4, g9:2, g10:3, g11:1})
p35 = alternative_performances(a35, {g1: 1, g2:3, g3:2, g4:1, g5:3, g6:3, g7:2, g8:1, g9:2, g10:1, g11:4})
p36 = alternative_performances(a36, {g1: 2, g2:2, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:2, g10:1, g11:1})
p37 = alternative_performances(a37, {g1: 1, g2:2, g3:2, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:1})
p38 = alternative_performances(a38, {g1: 1, g2:1, g3:1, g4:1, g5:4, g6:1, g7:2, g8:5, g9:1, g10:3, g11:1})
p39 = alternative_performances(a39, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
p40 = alternative_performances(a40, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p41 = alternative_performances(a41, {g1: 1, g2:3, g3:1, g4:2, g5:3, g6:3, g7:1, g8:4, g9:1, g10:3, g11:1})
p42 = alternative_performances(a42, {g1: 2, g2:2, g3:2, g4:1, g5:3, g6:1, g7:1, g8:4, g9:1, g10:3, g11:1})
p43 = alternative_performances(a43, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p44 = alternative_performances(a44, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
p45 = alternative_performances(a45, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
p46 = alternative_performances(a46, {g1: 1, g2:3, g3:1, g4:2, g5:4, g6:1, g7:2, g8:4, g9:1, g10:3, g11:1})
p47 = alternative_performances(a47, {g1: 1, g2:3, g3:1, g4:1, g5:3, g6:1, g7:1, g8:1, g9:1, g10:3, g11:4})
p48 = alternative_performances(a48, {g1: 2, g2:2, g3:1, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
p49 = alternative_performances(a49, {g1: 2, g2:3, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:2, g10:3, g11:4})
p50 = alternative_performances(a50, {g1: 1, g2:2, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p51 = alternative_performances(a51, {g1: 1, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
p52 = alternative_performances(a52, {g1: 1, g2:3, g3:1, g4:2, g5:3, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
p53 = alternative_performances(a53, {g1: 2, g2:3, g3:1, g4:1, g5:1, g6:1, g7:2, g8:4, g9:2, g10:3, g11:1})
p54 = alternative_performances(a54, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:3, g7:1, g8:4, g9:2, g10:1, g11:1})
p55 = alternative_performances(a55, {g1: 1, g2:2, g3:1, g4:2, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p56 = alternative_performances(a56, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
p57 = alternative_performances(a57, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p58 = alternative_performances(a58, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
p59 = alternative_performances(a59, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
p60 = alternative_performances(a60, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p61 = alternative_performances(a61, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p62 = alternative_performances(a62, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p63 = alternative_performances(a63, {g1: 2, g2:2, g3:1, g4:1, g5:3, g6:1, g7:1, g8:4, g9:1, g10:3, g11:1})
p64 = alternative_performances(a64, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p65 = alternative_performances(a65, {g1: 1, g2:3, g3:2, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:5})
p66 = alternative_performances(a66, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
p67 = alternative_performances(a67, {g1: 1, g2:2, g3:1, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
p68 = alternative_performances(a68, {g1: 1, g2:3, g3:1, g4:1, g5:3, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
p69 = alternative_performances(a69, {g1: 2, g2:2, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:2, g10:1, g11:1})
p70 = alternative_performances(a70, {g1: 2, g2:3, g3:2, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
p71 = alternative_performances(a71, {g1: 2, g2:2, g3:2, g4:2, g5:4, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
p72 = alternative_performances(a72, {g1: 1, g2:3, g3:2, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
p73 = alternative_performances(a73, {g1: 1, g2:2, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:4})
p74 = alternative_performances(a74, {g1: 1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:3, g10:3, g11:1})
p75 = alternative_performances(a75, {g1: 2, g2:1, g3:3, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
p76 = alternative_performances(a76, {g1: 2, g2:2, g3:2, g4:2, g5:3, g6:3, g7:1, g8:4, g9:2, g10:3, g11:1})
p77 = alternative_performances(a77, {g1: 2, g2:2, g3:2, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:5})
p78 = alternative_performances(a78, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p79 = alternative_performances(a79, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p80 = alternative_performances(a80, {g1: 1, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:4})
p81 = alternative_performances(a81, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:5, g9:1, g10:3, g11:5})
p82 = alternative_performances(a82, {g1: 1, g2:2, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:5})
p83 = alternative_performances(a83, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p84 = alternative_performances(a84, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p85 = alternative_performances(a85, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p86 = alternative_performances(a86, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
p87 = alternative_performances(a87, {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p88 = alternative_performances(a88, {g1: 1, g2:2, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
p89 = alternative_performances(a89, {g1: 2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:4, g9:1, g10:3, g11:5})
p90 = alternative_performances(a90, {g1: 1, g2:3, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
p91 = alternative_performances(a91, {g1: 1, g2:2, g3:2, g4:1, g5:3, g6:1, g7:2, g8:4, g9:1, g10:3, g11:4})
p92 = alternative_performances(a92, {g1: 3, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p93 = alternative_performances(a93, {g1: 2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
p94 = alternative_performances(a94, {g1: 2, g2:2, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:2, g10:1, g11:1})
p95 = alternative_performances(a95, {g1: 1, g2:3, g3:2, g4:2, g5:1, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
p96 = alternative_performances(a96, {g1: 1, g2:2, g3:1, g4:2, g5:3, g6:3, g7:1, g8:4, g9:1, g10:3, g11:5})
p97 = alternative_performances(a97, {g1: 2, g2:3, g3:1, g4:2, g5:4, g6:1, g7:1, g8:4, g9:1, g10:3, g11:5})
p98 = alternative_performances(a98, {g1: 1, g2:2, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p99 = alternative_performances(a99, {g1: 2, g2:2, g3:2, g4:2, g5:1, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
p100 = alternative_performances(a100, {g1:2, g2:1, g3:2, g4:2, g5:3, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
p101 = alternative_performances(a101, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p102 = alternative_performances(a102, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p103 = alternative_performances(a103, {g1:1, g2:2, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:3, g10:3, g11:1})
p104 = alternative_performances(a104, {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:5, g9:1, g10:3, g11:5})
p105 = alternative_performances(a105, {g1:1, g2:3, g3:2, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:3, g11:5})
p106 = alternative_performances(a106, {g1:1, g2:3, g3:2, g4:1, g5:1, g6:3, g7:1, g8:4, g9:1, g10:3, g11:1})
p107 = alternative_performances(a107, {g1:2, g2:3, g3:2, g4:2, g5:4, g6:3, g7:1, g8:4, g9:1, g10:3, g11:1})
p108 = alternative_performances(a108, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p109 = alternative_performances(a109, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:5, g9:1, g10:3, g11:1})
p110 = alternative_performances(a110, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p111 = alternative_performances(a111, {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:3, g8:1, g9:1, g10:3, g11:4})
p112 = alternative_performances(a112, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
p113 = alternative_performances(a113, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:1, g11:1})
p114 = alternative_performances(a114, {g1:1, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:5, g9:1, g10:3, g11:4})
p115 = alternative_performances(a115, {g1:2, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:5, g9:1, g10:3, g11:1})
p116 = alternative_performances(a116, {g1:1, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:1, g9:3, g10:3, g11:5})
p117 = alternative_performances(a117, {g1:2, g2:3, g3:3, g4:2, g5:3, g6:4, g7:2, g8:1, g9:2, g10:3, g11:5})
p118 = alternative_performances(a118, {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:3, g8:1, g9:2, g10:3, g11:1})
p119 = alternative_performances(a119, {g1:2, g2:2, g3:1, g4:2, g5:3, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
p120 = alternative_performances(a120, {g1:2, g2:2, g3:1, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
p121 = alternative_performances(a121, {g1:2, g2:2, g3:3, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
p122 = alternative_performances(a122, {g1:2, g2:1, g3:1, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
p123 = alternative_performances(a123, {g1:2, g2:2, g3:1, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
p124 = alternative_performances(a124, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p125 = alternative_performances(a125, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p126 = alternative_performances(a126, {g1:1, g2:3, g3:2, g4:1, g5:4, g6:1, g7:2, g8:5, g9:1, g10:3, g11:4})
p127 = alternative_performances(a127, {g1:2, g2:3, g3:3, g4:1, g5:3, g6:3, g7:3, g8:1, g9:1, g10:3, g11:4})
p128 = alternative_performances(a128, {g1:1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:5})
p129 = alternative_performances(a129, {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:1})
p130 = alternative_performances(a130, {g1:1, g2:3, g3:2, g4:2, g5:3, g6:3, g7:2, g8:4, g9:1, g10:3, g11:1})
p131 = alternative_performances(a131, {g1:2, g2:3, g3:2, g4:1, g5:4, g6:3, g7:1, g8:4, g9:1, g10:1, g11:1})
p132 = alternative_performances(a132, {g1:2, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:3, g11:1})
p133 = alternative_performances(a133, {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
p134 = alternative_performances(a134, {g1:1, g2:2, g3:1, g4:1, g5:1, g6:3, g7:2, g8:4, g9:1, g10:3, g11:4})
p135 = alternative_performances(a135, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
p136 = alternative_performances(a136, {g1:2, g2:3, g3:3, g4:2, g5:1, g6:3, g7:2, g8:4, g9:1, g10:1, g11:1})
p137 = alternative_performances(a137, {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:2, g8:1, g9:3, g10:3, g11:5})
p138 = alternative_performances(a138, {g1:2, g2:3, g3:1, g4:2, g5:4, g6:3, g7:2, g8:5, g9:1, g10:3, g11:4})
p139 = alternative_performances(a139, {g1:1, g2:3, g3:3, g4:1, g5:1, g6:3, g7:3, g8:1, g9:2, g10:3, g11:5})
p140 = alternative_performances(a140, {g1:2, g2:3, g3:2, g4:2, g5:4, g6:3, g7:1, g8:4, g9:1, g10:3, g11:5})
p141 = alternative_performances(a141, {g1:2, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:4, g9:1, g10:3, g11:1})
p142 = alternative_performances(a142, {g1:2, g2:3, g3:1, g4:1, g5:3, g6:1, g7:1, g8:4, g9:1, g10:3, g11:5})
p143 = alternative_performances(a143, {g1:1, g2:3, g3:1, g4:2, g5:4, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
p144 = alternative_performances(a144, {g1:2, g2:3, g3:2, g4:2, g5:3, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
p145 = alternative_performances(a145, {g1:2, g2:2, g3:1, g4:2, g5:1, g6:3, g7:1, g8:1, g9:2, g10:1, g11:1})
p146 = alternative_performances(a146, {g1:1, g2:2, g3:1, g4:2, g5:3, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
p147 = alternative_performances(a147, {g1:2, g2:3, g3:2, g4:1, g5:4, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
p148 = alternative_performances(a148, {g1:1, g2:2, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:5})
p149 = alternative_performances(a149, {g1:1, g2:2, g3:2, g4:2, g5:3, g6:4, g7:2, g8:4, g9:2, g10:3, g11:1})
p150 = alternative_performances(a150, {g1:1, g2:2, g3:2, g4:2, g5:1, g6:3, g7:1, g8:4, g9:1, g10:1, g11:1})
p151 = alternative_performances(a151, {g1:1, g2:2, g3:1, g4:1, g5:1, g6:3, g7:3, g8:4, g9:1, g10:3, g11:1})
p152 = alternative_performances(a152, {g1:2, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:3, g11:1})
p153 = alternative_performances(a153, {g1:2, g2:3, g3:2, g4:1, g5:4, g6:3, g7:3, g8:4, g9:2, g10:3, g11:5})
p154 = alternative_performances(a154, {g1:1, g2:3, g3:1, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
p155 = alternative_performances(a155, {g1:2, g2:3, g3:3, g4:2, g5:1, g6:3, g7:3, g8:4, g9:3, g10:1, g11:5})
p156 = alternative_performances(a156, {g1:2, g2:1, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
p157 = alternative_performances(a157, {g1:1, g2:3, g3:2, g4:2, g5:3, g6:3, g7:2, g8:5, g9:1, g10:3, g11:4})
p158 = alternative_performances(a158, {g1:2, g2:3, g3:3, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
p159 = alternative_performances(a159, {g1:2, g2:3, g3:1, g4:1, g5:3, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
p160 = alternative_performances(a160, {g1:1, g2:3, g3:3, g4:1, g5:1, g6:3, g7:3, g8:1, g9:2, g10:3, g11:5})
p161 = alternative_performances(a161, {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:2, g8:4, g9:1, g10:1, g11:1})
p162 = alternative_performances(a162, {g1:2, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:5, g9:1, g10:3, g11:5})
p163 = alternative_performances(a163, {g1:2, g2:2, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
p164 = alternative_performances(a164, {g1:2, g2:3, g3:1, g4:2, g5:4, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p165 = alternative_performances(a165, {g1:2, g2:1, g3:2, g4:2, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p166 = alternative_performances(a166, {g1:2, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p167 = alternative_performances(a167, {g1:2, g2:3, g3:1, g4:1, g5:3, g6:1, g7:2, g8:1, g9:3, g10:3, g11:1})
p168 = alternative_performances(a168, {g1:1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
p169 = alternative_performances(a169, {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:2, g8:4, g9:2, g10:3, g11:1})
p170 = alternative_performances(a170, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p171 = alternative_performances(a171, {g1:1, g2:3, g3:1, g4:2, g5:4, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
p172 = alternative_performances(a172, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:3, g11:1})
p173 = alternative_performances(a173, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:4})
p174 = alternative_performances(a174, {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:1, g8:5, g9:1, g10:3, g11:5})
p175 = alternative_performances(a175, {g1:1, g2:3, g3:3, g4:2, g5:1, g6:4, g7:2, g8:1, g9:3, g10:3, g11:4})
p176 = alternative_performances(a176, {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:1, g9:3, g10:3, g11:1})
p177 = alternative_performances(a177, {g1:1, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:5, g9:2, g10:3, g11:4})
p178 = alternative_performances(a178, {g1:2, g2:3, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
p179 = alternative_performances(a179, {g1:2, g2:2, g3:1, g4:1, g5:1, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
p180 = alternative_performances(a180, {g1:1, g2:3, g3:3, g4:2, g5:4, g6:3, g7:1, g8:1, g9:2, g10:3, g11:4})
p181 = alternative_performances(a181, {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:3, g8:4, g9:1, g10:3, g11:1})
p182 = alternative_performances(a182, {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:1, g8:5, g9:1, g10:3, g11:5})
p183 = alternative_performances(a183, {g1:1, g2:3, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
p184 = alternative_performances(a184, {g1:1, g2:1, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
p185 = alternative_performances(a185, {g1:1, g2:1, g3:1, g4:2, g5:1, g6:3, g7:1, g8:1, g9:2, g10:1, g11:1})
p186 = alternative_performances(a186, {g1:1, g2:2, g3:1, g4:2, g5:1, g6:1, g7:3, g8:4, g9:1, g10:3, g11:1})
p187 = alternative_performances(a187, {g1:1, g2:3, g3:2, g4:2, g5:1, g6:3, g7:3, g8:4, g9:1, g10:3, g11:1})
p188 = alternative_performances(a188, {g1:3, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
p189 = alternative_performances(a189, {g1:1, g2:3, g3:2, g4:2, g5:4, g6:3, g7:3, g8:1, g9:1, g10:3, g11:4})
p190 = alternative_performances(a190, {g1:1, g2:3, g3:1, g4:1, g5:3, g6:1, g7:1, g8:5, g9:1, g10:3, g11:1})
p191 = alternative_performances(a191, {g1:1, g2:3, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:3, g10:3, g11:4})
p192 = alternative_performances(a192, {g1:1, g2:3, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
p193 = alternative_performances(a193, {g1:1, g2:2, g3:2, g4:1, g5:3, g6:1, g7:2, g8:4, g9:2, g10:3, g11:4})
p194 = alternative_performances(a194, {g1:2, g2:2, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:5})
p195 = alternative_performances(a195, {g1:2, g2:3, g3:1, g4:2, g5:4, g6:3, g7:3, g8:4, g9:1, g10:3, g11:5})
p196 = alternative_performances(a196, {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:4, g9:1, g10:3, g11:5})
p197 = alternative_performances(a197, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
p198 = alternative_performances(a198, {g1:1, g2:2, g3:1, g4:2, g5:1, g6:3, g7:1, g8:5, g9:1, g10:3, g11:5})
p199 = alternative_performances(a199, {g1:1, g2:2, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
p200 = alternative_performances(a200, {g1:3, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
p201 = alternative_performances(a201, {g1:1, g2:2, g3:1, g4:1, g5:3, g6:3, g7:3, g8:4, g9:1, g10:3, g11:4})
p202 = alternative_performances(a202, {g1:1, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
p203 = alternative_performances(a203, {g1:1, g2:3, g3:1, g4:2, g5:4, g6:3, g7:3, g8:1, g9:1, g10:3, g11:4})
p204 = alternative_performances(a204, {g1:1, g2:2, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
p205 = alternative_performances(a205, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:1, g11:1})
p206 = alternative_performances(a206, {g1:2, g2:3, g3:1, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
p207 = alternative_performances(a207, {g1:2, g2:1, g3:1, g4:1, g5:1, g6:3, g7:3, g8:1, g9:1, g10:1, g11:1})
p208 = alternative_performances(a208, {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:4, g9:1, g10:3, g11:5})
p209 = alternative_performances(a209, {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
p210 = alternative_performances(a210, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
p211 = alternative_performances(a211, {g1:3, g2:2, g3:1, g4:1, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:1})
p212 = alternative_performances(a212, {g1:2, g2:1, g3:1, g4:1, g5:4, g6:3, g7:3, g8:4, g9:1, g10:3, g11:5})
p213 = alternative_performances(a213, {g1:1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
p214 = alternative_performances(a214, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
p215 = alternative_performances(a215, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
p216 = alternative_performances(a216, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p217 = alternative_performances(a217, {g1:2, g2:3, g3:1, g4:2, g5:1, g6:3, g7:3, g8:1, g9:1, g10:3, g11:1})
p218 = alternative_performances(a218, {g1:1, g2:3, g3:1, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
p219 = alternative_performances(a219, {g1:3, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
p220 = alternative_performances(a220, {g1:1, g2:2, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:3, g10:1, g11:1})
p221 = alternative_performances(a221, {g1:1, g2:3, g3:2, g4:1, g5:3, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
p222 = alternative_performances(a222, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
p223 = alternative_performances(a223, {g1:1, g2:3, g3:3, g4:1, g5:1, g6:3, g7:3, g8:1, g9:1, g10:3, g11:5})
p224 = alternative_performances(a224, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
p225 = alternative_performances(a225, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
p226 = alternative_performances(a226, {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:5})
p227 = alternative_performances(a227, {g1:2, g2:1, g3:1, g4:1, g5:1, g6:3, g7:1, g8:1, g9:1, g10:3, g11:4})
p228 = alternative_performances(a228, {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:5, g9:3, g10:3, g11:5})

pt = performance_table([ p0, p1, p2, p3, p4, p5, p6, p7,
              p8, p9, p10, p11, p12, p13, p14, p15,
              p16, p17, p18, p19, p20, p21, p22, p23,
              p24, p25, p26, p27, p28, p29, p30, p31,
              p32, p33, p34, p35, p36, p37, p38, p39,
              p40, p41, p42, p43, p44, p45, p46, p47,
              p48, p49, p50, p51, p52, p53, p54, p55,
              p56, p57, p58, p59, p60, p61, p62, p63,
              p64, p65, p66, p67, p68, p69, p70, p71,
              p72, p73, p74, p75, p76, p77, p78, p79,
              p80, p81, p82, p83, p84, p85, p86, p87,
              p88, p89, p90, p91, p92, p93, p94, p95,
              p96, p97, p98, p99, p100, p101, p102, p103,
              p104, p105, p106, p107, p108, p109, p110, p111,
              p112, p113, p114, p115, p116, p117, p118, p119,
              p120, p121, p122, p123, p124, p125, p126, p127,
              p128, p129, p130, p131, p132, p133, p134, p135,
              p136, p137, p138, p139, p140, p141, p142, p143,
              p144, p145, p146, p147, p148, p149, p150, p151,
              p152, p153, p154, p155, p156, p157, p158, p159,
              p160, p161, p162, p163, p164, p165, p166, p167,
              p168, p169, p170, p171, p172, p173, p174, p175,
              p176, p177, p178, p179, p180, p181, p182, p183,
              p184, p185, p186, p187, p188, p189, p190, p191,
              p192, p193, p194, p195, p196, p197, p198, p199,
              p200, p201, p202, p203, p204, p205, p206, p207,
              p208, p209, p210, p211, p212, p213, p214, p215,
              p216, p217, p218, p219, p220, p221, p222, p223,
              p224, p225, p226, p227, p228 ])

# Reference actions
b1 = {g1: 1, g2: 2, g3: 1, g4: 1, g5: 1, g6: 1, g7: 2, g8: 4, g9: 1, g10: 1, g11: 1}
b2 = {g1: 2, g2: 2, g3: 2, g4: 2, g5: 3, g6: 1, g7: 3, g8: 4, g9: 2, g10: 3, g11: 4}
b3 = {g1: 2, g2: 3, g3: 3, g4: 2, g5: 3, g6: 1, g7: 3, g8: 5, g9: 3, g10: 3, g11: 5}

# Indifference, Preference and Veto
q = threshold('q', 'indifference', {g1:0, g2:0, g3: 0, g4:0, g5:0, g6:0, g7:0, g8:0, g9:0, g10:0, g11:0})
p = threshold('p', 'preference', {g1:1, g2:1, g3: 1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:2, g11:1})
v = threshold('v', 'veto', {g11:4})

# Profiles
prof1 = profile('p1', 'profile_down', b1, q, p, v)
prof2 = profile('p2', 'profile_middle', b2, q, p, v)
prof3 = profile('p3', 'profile_up', b3, q, p, v)
profiles = [ prof1, prof2, prof3 ]

# Lambda
lbda = 0.76

# Affectation values
affect_p = {
a0: 2, a1: 2, a2: 1, a3: 2, a4: 2, a5: 2, a6: 2, a7: 2, a8: 3, a9: 1, a10: 2, a11: 3,
a12: 3, a13: 1, a14: 2, a15: 1, a16: 2, a17: 2, a18: 2, a19: 2, a20: 3, a21: 2, a22: 2,
a23: 2, a24: 2, a25: 2, a26: 1, a27: 2, a28: 2, a29: 2, a30: 2, a31: 4, a32: 2, a33: 2,
a34: 2, a35: 2, a36: 2, a37: 2, a38: 2, a39: 1, a40: 1, a41: 2, a42: 2, a43: 2, a44: 1,
a45: 2, a46: 2, a47: 2, a48: 2, a49: 2, a50: 2, a51: 2, a52: 2, a53: 2, a54: 2, a55: 2,
a56: 1, a57: 2, a58: 1, a59: 1, a60: 1, a61: 1, a62: 1, a63: 2, a64: 2, a65: 2, a66: 2,
a67: 2, a68: 2, a69: 2, a70: 3, a71: 2, a72: 2, a73: 2, a74: 2, a75: 2, a76: 2, a77: 2,
a78: 2, a79: 2, a80: 3, a81: 2, a82: 2, a83: 1, a84: 1, a85: 1, a86: 1, a87: 2, a88: 2,
a89: 4, a90: 2, a91: 2, a92: 1, a93: 3, a94: 2, a95: 2, a96: 2, a97: 2, a98: 2, a99: 2,
a100: 2, a101: 2, a102: 2, a103: 2, a104: 4, a105: 2, a106: 2, a107: 2, a108: 1, a109:2,
a110: 2, a111: 2, a112: 2, a113: 2, a114: 2, a115: 2, a116: 4, a117: 3, a118: 2, a119:2,
a120: 2, a121: 2, a122: 2, a123: 2, a124: 2, a125: 2, a126: 2, a127: 2, a128: 2, a129: 2,
a130: 2, a131: 2, a132: 2, a133: 3, a134: 2, a135: 2, a136: 2, a137: 2, a138: 2, a139: 2,
a140: 3, a141: 2, a142: 2, a143: 2, a144: 2, a145: 2, a146: 2, a147: 2, a148: 2, a149: 2,
a150: 2, a151: 2, a152: 2, a153: 3, a154: 2, a155: 3, a156: 2, a157: 3, a158: 2, a159: 2,
a160: 2, a161: 2, a162: 2, a163: 2, a164: 2, a165: 1, a166: 1, a167: 2, a168: 2, a169: 2,
a170: 1, a171: 2, a172: 2, a173: 2, a174: 2, a175: 2, a176: 2, a177: 2, a178: 2, a179: 2,
a180: 3, a181: 2, a182: 4, a183: 2, a184: 2, a185: 1, a186: 2, a187: 2, a188: 1, a189: 2,
a190: 2, a191: 2, a192: 2, a193: 3, a194: 2, a195: 3, a196: 4, a197: 2, a198: 2, a199: 2,
a200: 1, a201: 2, a202: 2, a203: 2, a204: 2, a205: 2, a206: 2, a207: 2, a208: 4, a209: 2,
a210: 1, a211: 2, a212: 2, a213: 2, a214: 2, a215: 2, a216: 1, a217: 2, a218: 2, a219: 3,
a220: 2, a221: 2, a222: 1, a223: 2, a224: 2, a225: 1, a226: 2, a227: 1, a228: 4 }

affect_o = {
a0: 2, a1: 2, a2: 1, a3: 2, a4: 2, a5: 2, a6: 2, a7: 2, a8: 3, a9: 1, a10: 2, a11: 3,
a12: 3, a13: 1, a14: 2, a15: 2, a16: 2, a17: 2, a18: 2, a19: 2, a20: 3, a21: 2, a22: 2,
a23: 3, a24: 2, a25: 2, a26: 1, a27: 2, a28: 2, a29: 2, a30: 2, a31: 4, a32: 2, a33: 2,
a34: 2, a35: 2, a36: 2, a37: 2, a38: 2, a39: 2, a40: 1, a41: 2, a42: 2, a43: 2, a44: 2,
a45: 2, a46: 2, a47: 2, a48: 2, a49: 2, a50: 2, a51: 3, a52: 2, a53: 2, a54: 2, a55: 2,
a56: 2, a57: 2, a58: 2, a59: 2, a60: 1, a61: 1, a62: 1, a63: 2, a64: 2, a65: 3, a66: 2,
a67: 2, a68: 3, a69: 2, a70: 3, a71: 2, a72: 2, a73: 2, a74: 2, a75: 2, a76: 2, a77: 3,
a78: 2, a79: 2, a80: 3, a81: 3, a82: 2, a83: 1, a84: 1, a85: 1, a86: 1, a87: 2, a88: 2,
a89: 4, a90: 2, a91: 2, a92: 1, a93: 3, a94: 2, a95: 2, a96: 3, a97: 3, a98: 2, a99: 2,
a100: 2, a101: 2, a102: 2, a103: 3, a104: 4, a105: 3, a106: 2, a107: 2, a108: 1, a109: 2,
a110: 2, a111: 2, a112: 2, a113: 2, a114: 3, a115: 3, a116: 4, a117: 3, a118: 2, a119: 3,
a120: 2, a121: 2, a122: 2, a123: 2, a124: 2, a125: 2, a126: 2, a127: 2, a128: 2, a129: 3,
a130: 2, a131: 2, a132: 2, a133: 3, a134: 2, a135: 2, a136: 2, a137: 3, a138: 3, a139: 3,
a140: 3, a141: 2, a142: 2, a143: 2, a144: 2, a145: 2, a146: 2, a147: 2, a148: 2, a149: 2,
a150: 2, a151: 2, a152: 2, a153: 3, a154: 2, a155: 3, a156: 2, a157: 3, a158: 2, a159: 3,
a160: 3, a161: 2, a162: 3, a163: 2, a164: 2, a165: 1, a166: 1, a167: 2, a168: 2, a169: 2,
a170: 1, a171: 2, a172: 2, a173: 2, a174: 3, a175: 3, a176: 3, a177: 3, a178: 2, a179: 3,
a180: 3, a181: 2, a182: 4, a183: 2, a184: 2, a185: 2, a186: 2, a187: 2, a188: 1, a189: 2,
a190: 2, a191: 2, a192: 2, a193: 3, a194: 3, a195: 3, a196: 4, a197: 2, a198: 3, a199: 2,
a200: 1, a201: 2, a202: 2, a203: 2, a204: 2, a205: 2, a206: 2, a207: 2, a208: 4, a209: 2,
a210: 2, a211: 2, a212: 3, a213: 2, a214: 2, a215: 2, a216: 1, a217: 2, a218: 2, a219: 3,
a220: 3, a221: 2, a222: 1, a223: 3, a224: 2, a225: 1, a226: 2, a227: 2, a228: 4}
