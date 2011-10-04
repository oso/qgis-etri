#!/usr/bin/python
import sys 
sys.path.insert(0, "..")
from mcda.types import criterion, action, profile, threshold

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
c = [ g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11 ]

# Actions
a0 = action('a0', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:2, g10:3, g11:5})
a1 = action('a1', evaluations = {g1: 1, g2:2, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
a2 = action('a2', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a3 = action('a3', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:3, g11:5})
a4 = action('a4', evaluations = {g1: 1, g2:3, g3:1, g4:2, g5:4, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
a5 = action('a5', evaluations = {g1: 1, g2:3, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:3, g11:5})
a6 = action('a6', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a7 = action('a7', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:2, g10:3, g11:5})
a8 = action('a8', evaluations = {g1: 1, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:1, g9:2, g10:3, g11:4})
a9 = action('a9', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:2, g10:1, g11:1})
a10 = action('a10', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:3, g11:5})
a11 = action('a11', evaluations = {g1: 2, g2:3, g3:3, g4:2, g5:3, g6:4, g7:2, g8:1, g9:2, g10:3, g11:5})
a12 = action('a12', evaluations = {g1: 2, g2:3, g3:3, g4:2, g5:3, g6:4, g7:2, g8:1, g9:2, g10:3, g11:5})
a13 = action('a13', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
a14 = action('a14', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a15 = action('a15', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
a16 = action('a16', evaluations = {g1: 1, g2:3, g3:3, g4:2, g5:1, g6:4, g7:3, g8:1, g9:1, g10:3, g11:1})
a17 = action('a17', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:3, g10:1, g11:1})
a18 = action('a18', evaluations = {g1: 1, g2:2, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
a19 = action('a19', evaluations = {g1: 2, g2:3, g3:1, g4:1, g5:1, g6:1, g7:2, g8:4, g9:2, g10:3, g11:1})
a20 = action('a20', evaluations = {g1: 1, g2:3, g3:1, g4:2, g5:1, g6:1, g7:3, g8:4, g9:3, g10:3, g11:4})
a21 = action('a21', evaluations = {g1: 1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:4, g9:1, g10:3, g11:1})
a22 = action('a22', evaluations = {g1: 1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:4, g9:1, g10:3, g11:1})
a23 = action('a23', evaluations = {g1: 2, g2:2, g3:1, g4:2, g5:1, g6:3, g7:2, g8:1, g9:2, g10:3, g11:5})
a24 = action('a24', evaluations = {g1: 1, g2:3, g3:1, g4:2, g5:1, g6:1, g7:2, g8:1, g9:2, g10:1, g11:1})
a25 = action('a25', evaluations = {g1: 2, g2:3, g3:1, g4:2, g5:1, g6:3, g7:3, g8:1, g9:1, g10:3, g11:1})
a26 = action('a26', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a27 = action('a27', evaluations = {g1: 1, g2:2, g3:2, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
a28 = action('a28', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
a29 = action('a29', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a30 = action('a30', evaluations = {g1: 1, g2:2, g3:1, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
a31 = action('a31', evaluations = {g1: 3, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:5, g9:1, g10:3, g11:5})
a32 = action('a32', evaluations = {g1: 1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:3, g10:1, g11:4})
a33 = action('a33', evaluations = {g1: 1, g2:2, g3:1, g4:2, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a34 = action('a34', evaluations = {g1: 1, g2:3, g3:1, g4:2, g5:3, g6:1, g7:2, g8:4, g9:2, g10:3, g11:1})
a35 = action('a35', evaluations = {g1: 1, g2:3, g3:2, g4:1, g5:3, g6:3, g7:2, g8:1, g9:2, g10:1, g11:4})
a36 = action('a36', evaluations = {g1: 2, g2:2, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:2, g10:1, g11:1})
a37 = action('a37', evaluations = {g1: 1, g2:2, g3:2, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:1})
a38 = action('a38', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:4, g6:1, g7:2, g8:5, g9:1, g10:3, g11:1})
a39 = action('a39', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
a40 = action('a40', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a41 = action('a41', evaluations = {g1: 1, g2:3, g3:1, g4:2, g5:3, g6:3, g7:1, g8:4, g9:1, g10:3, g11:1})
a42 = action('a42', evaluations = {g1: 2, g2:2, g3:2, g4:1, g5:3, g6:1, g7:1, g8:4, g9:1, g10:3, g11:1})
a43 = action('a43', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a44 = action('a44', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
a45 = action('a45', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
a46 = action('a46', evaluations = {g1: 1, g2:3, g3:1, g4:2, g5:4, g6:1, g7:2, g8:4, g9:1, g10:3, g11:1})
a47 = action('a47', evaluations = {g1: 1, g2:3, g3:1, g4:1, g5:3, g6:1, g7:1, g8:1, g9:1, g10:3, g11:4})
a48 = action('a48', evaluations = {g1: 2, g2:2, g3:1, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
a49 = action('a49', evaluations = {g1: 2, g2:3, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:2, g10:3, g11:4})
a50 = action('a50', evaluations = {g1: 1, g2:2, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a51 = action('a51', evaluations = {g1: 1, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
a52 = action('a52', evaluations = {g1: 1, g2:3, g3:1, g4:2, g5:3, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
a53 = action('a53', evaluations = {g1: 2, g2:3, g3:1, g4:1, g5:1, g6:1, g7:2, g8:4, g9:2, g10:3, g11:1})
a54 = action('a54', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:3, g7:1, g8:4, g9:2, g10:1, g11:1})
a55 = action('a55', evaluations = {g1: 1, g2:2, g3:1, g4:2, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a56 = action('a56', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
a57 = action('a57', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a58 = action('a58', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
a59 = action('a59', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
a60 = action('a60', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a61 = action('a61', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a62 = action('a62', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a63 = action('a63', evaluations = {g1: 2, g2:2, g3:1, g4:1, g5:3, g6:1, g7:1, g8:4, g9:1, g10:3, g11:1})
a64 = action('a64', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a65 = action('a65', evaluations = {g1: 1, g2:3, g3:2, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:5})
a66 = action('a66', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
a67 = action('a67', evaluations = {g1: 1, g2:2, g3:1, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
a68 = action('a68', evaluations = {g1: 1, g2:3, g3:1, g4:1, g5:3, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
a69 = action('a69', evaluations = {g1: 2, g2:2, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:2, g10:1, g11:1})
a70 = action('a70', evaluations = {g1: 2, g2:3, g3:2, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
a71 = action('a71', evaluations = {g1: 2, g2:2, g3:2, g4:2, g5:4, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
a72 = action('a72', evaluations = {g1: 1, g2:3, g3:2, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
a73 = action('a73', evaluations = {g1: 1, g2:2, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:4})
a74 = action('a74', evaluations = {g1: 1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:3, g10:3, g11:1})
a75 = action('a75', evaluations = {g1: 2, g2:1, g3:3, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
a76 = action('a76', evaluations = {g1: 2, g2:2, g3:2, g4:2, g5:3, g6:3, g7:1, g8:4, g9:2, g10:3, g11:1})
a77 = action('a77', evaluations = {g1: 2, g2:2, g3:2, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:5})
a78 = action('a78', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a79 = action('a79', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a80 = action('a80', evaluations = {g1: 1, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:4})
a81 = action('a81', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:5, g9:1, g10:3, g11:5})
a82 = action('a82', evaluations = {g1: 1, g2:2, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:5})
a83 = action('a83', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a84 = action('a84', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a85 = action('a85', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a86 = action('a86', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
a87 = action('a87', evaluations = {g1: 1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a88 = action('a88', evaluations = {g1: 1, g2:2, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
a89 = action('a89', evaluations = {g1: 2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:4, g9:1, g10:3, g11:5})
a90 = action('a90', evaluations = {g1: 1, g2:3, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
a91 = action('a91', evaluations = {g1: 1, g2:2, g3:2, g4:1, g5:3, g6:1, g7:2, g8:4, g9:1, g10:3, g11:4})
a92 = action('a92', evaluations = {g1: 3, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a93 = action('a93', evaluations = {g1: 2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
a94 = action('a94', evaluations = {g1: 2, g2:2, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:2, g10:1, g11:1})
a95 = action('a95', evaluations = {g1: 1, g2:3, g3:2, g4:2, g5:1, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
a96 = action('a96', evaluations = {g1: 1, g2:2, g3:1, g4:2, g5:3, g6:3, g7:1, g8:4, g9:1, g10:3, g11:5})
a97 = action('a97', evaluations = {g1: 2, g2:3, g3:1, g4:2, g5:4, g6:1, g7:1, g8:4, g9:1, g10:3, g11:5})
a98 = action('a98', evaluations = {g1: 1, g2:2, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a99 = action('a99', evaluations = {g1: 2, g2:2, g3:2, g4:2, g5:1, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
a100 = action('a100', evaluations = {g1:2, g2:1, g3:2, g4:2, g5:3, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
a101 = action('a101', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a102 = action('a102', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a103 = action('a103', evaluations = {g1:1, g2:2, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:3, g10:3, g11:1})
a104 = action('a104', evaluations = {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:5, g9:1, g10:3, g11:5})
a105 = action('a105', evaluations = {g1:1, g2:3, g3:2, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:3, g11:5})
a106 = action('a106', evaluations = {g1:1, g2:3, g3:2, g4:1, g5:1, g6:3, g7:1, g8:4, g9:1, g10:3, g11:1})
a107 = action('a107', evaluations = {g1:2, g2:3, g3:2, g4:2, g5:4, g6:3, g7:1, g8:4, g9:1, g10:3, g11:1})
a108 = action('a108', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a109 = action('a109', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:5, g9:1, g10:3, g11:1})
a110 = action('a110', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a111 = action('a111', evaluations = {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:3, g8:1, g9:1, g10:3, g11:4})
a112 = action('a112', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
a113 = action('a113', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:1, g11:1})
a114 = action('a114', evaluations = {g1:1, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:5, g9:1, g10:3, g11:4})
a115 = action('a115', evaluations = {g1:2, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:5, g9:1, g10:3, g11:1})
a116 = action('a116', evaluations = {g1:1, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:1, g9:3, g10:3, g11:5})
a117 = action('a117', evaluations = {g1:2, g2:3, g3:3, g4:2, g5:3, g6:4, g7:2, g8:1, g9:2, g10:3, g11:5})
a118 = action('a118', evaluations = {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:3, g8:1, g9:2, g10:3, g11:1})
a119 = action('a119', evaluations = {g1:2, g2:2, g3:1, g4:2, g5:3, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
a120 = action('a120', evaluations = {g1:2, g2:2, g3:1, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
a121 = action('a121', evaluations = {g1:2, g2:2, g3:3, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
a122 = action('a122', evaluations = {g1:2, g2:1, g3:1, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
a123 = action('a123', evaluations = {g1:2, g2:2, g3:1, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
a124 = action('a124', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a125 = action('a125', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a126 = action('a126', evaluations = {g1:1, g2:3, g3:2, g4:1, g5:4, g6:1, g7:2, g8:5, g9:1, g10:3, g11:4})
a127 = action('a127', evaluations = {g1:2, g2:3, g3:3, g4:1, g5:3, g6:3, g7:3, g8:1, g9:1, g10:3, g11:4})
a128 = action('a128', evaluations = {g1:1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:5})
a129 = action('a129', evaluations = {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:1})
a130 = action('a130', evaluations = {g1:1, g2:3, g3:2, g4:2, g5:3, g6:3, g7:2, g8:4, g9:1, g10:3, g11:1})
a131 = action('a131', evaluations = {g1:2, g2:3, g3:2, g4:1, g5:4, g6:3, g7:1, g8:4, g9:1, g10:1, g11:1})
a132 = action('a132', evaluations = {g1:2, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:3, g11:1})
a133 = action('a133', evaluations = {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
a134 = action('a134', evaluations = {g1:1, g2:2, g3:1, g4:1, g5:1, g6:3, g7:2, g8:4, g9:1, g10:3, g11:4})
a135 = action('a135', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
a136 = action('a136', evaluations = {g1:2, g2:3, g3:3, g4:2, g5:1, g6:3, g7:2, g8:4, g9:1, g10:1, g11:1})
a137 = action('a137', evaluations = {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:2, g8:1, g9:3, g10:3, g11:5})
a138 = action('a138', evaluations = {g1:2, g2:3, g3:1, g4:2, g5:4, g6:3, g7:2, g8:5, g9:1, g10:3, g11:4})
a139 = action('a139', evaluations = {g1:1, g2:3, g3:3, g4:1, g5:1, g6:3, g7:3, g8:1, g9:2, g10:3, g11:5})
a140 = action('a140', evaluations = {g1:2, g2:3, g3:2, g4:2, g5:4, g6:3, g7:1, g8:4, g9:1, g10:3, g11:5})
a141 = action('a141', evaluations = {g1:2, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:4, g9:1, g10:3, g11:1})
a142 = action('a142', evaluations = {g1:2, g2:3, g3:1, g4:1, g5:3, g6:1, g7:1, g8:4, g9:1, g10:3, g11:5})
a143 = action('a143', evaluations = {g1:1, g2:3, g3:1, g4:2, g5:4, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
a144 = action('a144', evaluations = {g1:2, g2:3, g3:2, g4:2, g5:3, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
a145 = action('a145', evaluations = {g1:2, g2:2, g3:1, g4:2, g5:1, g6:3, g7:1, g8:1, g9:2, g10:1, g11:1})
a146 = action('a146', evaluations = {g1:1, g2:2, g3:1, g4:2, g5:3, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
a147 = action('a147', evaluations = {g1:2, g2:3, g3:2, g4:1, g5:4, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
a148 = action('a148', evaluations = {g1:1, g2:2, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:5})
a149 = action('a149', evaluations = {g1:1, g2:2, g3:2, g4:2, g5:3, g6:4, g7:2, g8:4, g9:2, g10:3, g11:1})
a150 = action('a150', evaluations = {g1:1, g2:2, g3:2, g4:2, g5:1, g6:3, g7:1, g8:4, g9:1, g10:1, g11:1})
a151 = action('a151', evaluations = {g1:1, g2:2, g3:1, g4:1, g5:1, g6:3, g7:3, g8:4, g9:1, g10:3, g11:1})
a152 = action('a152', evaluations = {g1:2, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:3, g11:1})
a153 = action('a153', evaluations = {g1:2, g2:3, g3:2, g4:1, g5:4, g6:3, g7:3, g8:4, g9:2, g10:3, g11:5})
a154 = action('a154', evaluations = {g1:1, g2:3, g3:1, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
a155 = action('a155', evaluations = {g1:2, g2:3, g3:3, g4:2, g5:1, g6:3, g7:3, g8:4, g9:3, g10:1, g11:5})
a156 = action('a156', evaluations = {g1:2, g2:1, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
a157 = action('a157', evaluations = {g1:1, g2:3, g3:2, g4:2, g5:3, g6:3, g7:2, g8:5, g9:1, g10:3, g11:4})
a158 = action('a158', evaluations = {g1:2, g2:3, g3:3, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
a159 = action('a159', evaluations = {g1:2, g2:3, g3:1, g4:1, g5:3, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
a160 = action('a160', evaluations = {g1:1, g2:3, g3:3, g4:1, g5:1, g6:3, g7:3, g8:1, g9:2, g10:3, g11:5})
a161 = action('a161', evaluations = {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:2, g8:4, g9:1, g10:1, g11:1})
a162 = action('a162', evaluations = {g1:2, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:5, g9:1, g10:3, g11:5})
a163 = action('a163', evaluations = {g1:2, g2:2, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
a164 = action('a164', evaluations = {g1:2, g2:3, g3:1, g4:2, g5:4, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a165 = action('a165', evaluations = {g1:2, g2:1, g3:2, g4:2, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a166 = action('a166', evaluations = {g1:2, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a167 = action('a167', evaluations = {g1:2, g2:3, g3:1, g4:1, g5:3, g6:1, g7:2, g8:1, g9:3, g10:3, g11:1})
a168 = action('a168', evaluations = {g1:1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
a169 = action('a169', evaluations = {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:2, g8:4, g9:2, g10:3, g11:1})
a170 = action('a170', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a171 = action('a171', evaluations = {g1:1, g2:3, g3:1, g4:2, g5:4, g6:3, g7:1, g8:1, g9:1, g10:1, g11:1})
a172 = action('a172', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:3, g11:1})
a173 = action('a173', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:4})
a174 = action('a174', evaluations = {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:1, g8:5, g9:1, g10:3, g11:5})
a175 = action('a175', evaluations = {g1:1, g2:3, g3:3, g4:2, g5:1, g6:4, g7:2, g8:1, g9:3, g10:3, g11:4})
a176 = action('a176', evaluations = {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:1, g9:3, g10:3, g11:1})
a177 = action('a177', evaluations = {g1:1, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:5, g9:2, g10:3, g11:4})
a178 = action('a178', evaluations = {g1:2, g2:3, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
a179 = action('a179', evaluations = {g1:2, g2:2, g3:1, g4:1, g5:1, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
a180 = action('a180', evaluations = {g1:1, g2:3, g3:3, g4:2, g5:4, g6:3, g7:1, g8:1, g9:2, g10:3, g11:4})
a181 = action('a181', evaluations = {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:3, g8:4, g9:1, g10:3, g11:1})
a182 = action('a182', evaluations = {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:1, g8:5, g9:1, g10:3, g11:5})
a183 = action('a183', evaluations = {g1:1, g2:3, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
a184 = action('a184', evaluations = {g1:1, g2:1, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
a185 = action('a185', evaluations = {g1:1, g2:1, g3:1, g4:2, g5:1, g6:3, g7:1, g8:1, g9:2, g10:1, g11:1})
a186 = action('a186', evaluations = {g1:1, g2:2, g3:1, g4:2, g5:1, g6:1, g7:3, g8:4, g9:1, g10:3, g11:1})
a187 = action('a187', evaluations = {g1:1, g2:3, g3:2, g4:2, g5:1, g6:3, g7:3, g8:4, g9:1, g10:3, g11:1})
a188 = action('a188', evaluations = {g1:3, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
a189 = action('a189', evaluations = {g1:1, g2:3, g3:2, g4:2, g5:4, g6:3, g7:3, g8:1, g9:1, g10:3, g11:4})
a190 = action('a190', evaluations = {g1:1, g2:3, g3:1, g4:1, g5:3, g6:1, g7:1, g8:5, g9:1, g10:3, g11:1})
a191 = action('a191', evaluations = {g1:1, g2:3, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:3, g10:3, g11:4})
a192 = action('a192', evaluations = {g1:1, g2:3, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
a193 = action('a193', evaluations = {g1:1, g2:2, g3:2, g4:1, g5:3, g6:1, g7:2, g8:4, g9:2, g10:3, g11:4})
a194 = action('a194', evaluations = {g1:2, g2:2, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:5})
a195 = action('a195', evaluations = {g1:2, g2:3, g3:1, g4:2, g5:4, g6:3, g7:3, g8:4, g9:1, g10:3, g11:5})
a196 = action('a196', evaluations = {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:4, g9:1, g10:3, g11:5})
a197 = action('a197', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:1, g11:1})
a198 = action('a198', evaluations = {g1:1, g2:2, g3:1, g4:2, g5:1, g6:3, g7:1, g8:5, g9:1, g10:3, g11:5})
a199 = action('a199', evaluations = {g1:1, g2:2, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
a200 = action('a200', evaluations = {g1:3, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
a201 = action('a201', evaluations = {g1:1, g2:2, g3:1, g4:1, g5:3, g6:3, g7:3, g8:4, g9:1, g10:3, g11:4})
a202 = action('a202', evaluations = {g1:1, g2:3, g3:1, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
a203 = action('a203', evaluations = {g1:1, g2:3, g3:1, g4:2, g5:4, g6:3, g7:3, g8:1, g9:1, g10:3, g11:4})
a204 = action('a204', evaluations = {g1:1, g2:2, g3:2, g4:2, g5:4, g6:3, g7:2, g8:1, g9:2, g10:3, g11:1})
a205 = action('a205', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:4, g9:1, g10:1, g11:1})
a206 = action('a206', evaluations = {g1:2, g2:3, g3:1, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
a207 = action('a207', evaluations = {g1:2, g2:1, g3:1, g4:1, g5:1, g6:3, g7:3, g8:1, g9:1, g10:1, g11:1})
a208 = action('a208', evaluations = {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:3, g8:4, g9:1, g10:3, g11:5})
a209 = action('a209', evaluations = {g1:1, g2:3, g3:1, g4:2, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
a210 = action('a210', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:5})
a211 = action('a211', evaluations = {g1:3, g2:2, g3:1, g4:1, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:1})
a212 = action('a212', evaluations = {g1:2, g2:1, g3:1, g4:1, g5:4, g6:3, g7:3, g8:4, g9:1, g10:3, g11:5})
a213 = action('a213', evaluations = {g1:1, g2:3, g3:2, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:4})
a214 = action('a214', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:3, g8:1, g9:1, g10:1, g11:1})
a215 = action('a215', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:3, g7:2, g8:1, g9:1, g10:3, g11:1})
a216 = action('a216', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a217 = action('a217', evaluations = {g1:2, g2:3, g3:1, g4:2, g5:1, g6:3, g7:3, g8:1, g9:1, g10:3, g11:1})
a218 = action('a218', evaluations = {g1:1, g2:3, g3:1, g4:1, g5:3, g6:3, g7:2, g8:1, g9:1, g10:3, g11:4})
a219 = action('a219', evaluations = {g1:3, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:4, g9:1, g10:3, g11:5})
a220 = action('a220', evaluations = {g1:1, g2:2, g3:3, g4:2, g5:1, g6:3, g7:2, g8:1, g9:3, g10:1, g11:1})
a221 = action('a221', evaluations = {g1:1, g2:3, g3:2, g4:1, g5:3, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
a222 = action('a222', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:3, g11:1})
a223 = action('a223', evaluations = {g1:1, g2:3, g3:3, g4:1, g5:1, g6:3, g7:3, g8:1, g9:1, g10:3, g11:5})
a224 = action('a224', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:1, g11:1})
a225 = action('a225', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:1, g8:1, g9:1, g10:1, g11:1})
a226 = action('a226', evaluations = {g1:1, g2:1, g3:1, g4:1, g5:1, g6:1, g7:2, g8:1, g9:1, g10:3, g11:5})
a227 = action('a227', evaluations = {g1:2, g2:1, g3:1, g4:1, g5:1, g6:3, g7:1, g8:1, g9:1, g10:3, g11:4})
a228 = action('a228', evaluations = {g1:2, g2:3, g3:3, g4:2, g5:4, g6:3, g7:2, g8:5, g9:3, g10:3, g11:5})

a = [ a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15,
      a16, a17, a18, a19, a20, a21, a22, a23, a24, a25, a26, a27, a28, a29, a30,
      a31, a32, a33, a34, a35, a36, a37, a38, a39, a40, a41, a42, a43, a44, a45,
      a46, a47, a48, a49, a50, a51, a52, a53, a54, a55, a56, a57, a58, a59, a60,
      a61, a62, a63, a64, a65, a66, a67, a68, a69, a70, a71, a72, a73, a74, a75,
      a76, a77, a78, a79, a80, a81, a82, a83, a84, a85, a86, a87, a88, a89, a90,
      a91, a92, a93, a94, a95, a96, a97, a98, a99, a100, a101, a102, a103, a104,
      a105, a106, a107, a108, a109, a110, a111, a112, a113, a114, a115, a116, a117,
      a118, a119, a120, a121, a122, a123, a124, a125, a126, a127, a128, a129, a130,
      a131, a132, a133, a134, a135, a136, a137, a138, a139, a140, a141, a142, a143,
      a144, a145, a146, a147, a148, a149, a150, a151, a152, a153, a154, a155, a156,
      a157, a158, a159, a160, a161, a162, a163, a164, a165, a166, a167, a168, a169,
      a170, a171, a172, a173, a174, a175, a176, a177, a178, a179, a180, a181, a182,
      a183, a184, a185, a186, a187, a188, a189, a190, a191, a192, a193, a194, a195,
      a196, a197, a198, a199, a200, a201, a202, a203, a204, a205, a206, a207, a208,
      a209, a210, a211, a212, a213, a214, a215, a216, a217, a218, a219, a220, a221,
      a222, a223, a224, a225, a226, a227, a228 ]

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
