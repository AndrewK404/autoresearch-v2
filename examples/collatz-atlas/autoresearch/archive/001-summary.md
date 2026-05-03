# 001 — Opening sweep summary

## Setup
Family: `T_{a,b}(n) = n/2` if n even, else `a*n + b`. Scope: `a ∈ {1,3,5,7}`, `b ∈ {1,3,5,7,9,11,13,15,17,19,21}` (44 variants). Per-variant: every seed `n0 ∈ [1, 10^4]`. Horizons: value bound `H = 10^12`, step bound `T = 10^4`. Outcomes: `cycle` (revisit), `exceeded-H`, `exceeded-T`.

## Per-variant table

| a | b | total_seeds | reached_cycle | exceeded_H | exceeded_T | n_distinct_cycles | smallest_cycle_min | largest_cycle_len | max_value_seen |
|---|---|-------------|---------------|------------|------------|-------------------|--------------------|-------------------|----------------|
| 1 | 1 | 10000 | 10000 | 0 | 0 | 1 | 1 | 2 | 10000 |
| 1 | 3 | 10000 | 10000 | 0 | 0 | 2 | 1 | 3 | 10002 |
| 1 | 5 | 10000 | 10000 | 0 | 0 | 2 | 1 | 6 | 10004 |
| 1 | 7 | 10000 | 10000 | 0 | 0 | 3 | 1 | 5 | 10006 |
| 1 | 9 | 10000 | 10000 | 0 | 0 | 3 | 1 | 9 | 10008 |
| 1 | 11 | 10000 | 10000 | 0 | 0 | 2 | 1 | 15 | 10010 |
| 1 | 13 | 10000 | 10000 | 0 | 0 | 2 | 1 | 18 | 10012 |
| 1 | 15 | 10000 | 10000 | 0 | 0 | 5 | 1 | 7 | 10014 |
| 1 | 17 | 10000 | 10000 | 0 | 0 | 3 | 1 | 12 | 10016 |
| 1 | 19 | 10000 | 10000 | 0 | 0 | 2 | 1 | 27 | 10018 |
| 1 | 21 | 10000 | 10000 | 0 | 0 | 6 | 1 | 10 | 10020 |
| 3 | 1 | 10000 | 10000 | 0 | 0 | 1 | 1 | 3 | 27114424 |
| 3 | 3 | 10000 | 10000 | 0 | 0 | 1 | 3 | 3 | 24460860 |
| 3 | 5 | 10000 | 10000 | 0 | 0 | 6 | 1 | 44 | 62129744 |
| 3 | 7 | 10000 | 10000 | 0 | 0 | 2 | 5 | 6 | 29723800 |
| 3 | 9 | 10000 | 10000 | 0 | 0 | 1 | 9 | 3 | 11492424 |
| 3 | 11 | 10000 | 10000 | 0 | 0 | 3 | 1 | 22 | 3503552 |
| 3 | 13 | 10000 | 10000 | 0 | 0 | 10 | 1 | 39 | 13153168 |
| 3 | 15 | 10000 | 10000 | 0 | 0 | 6 | 3 | 44 | 186389232 |
| 3 | 17 | 10000 | 10000 | 0 | 0 | 3 | 1 | 49 | 12439136 |
| 3 | 19 | 10000 | 10000 | 0 | 0 | 2 | 5 | 16 | 15090748 |
| 3 | 21 | 10000 | 10000 | 0 | 0 | 2 | 15 | 6 | 89171400 |
| 5 | 1 | 10000 | 726 | 9274 | 0 | 3 | 1 | 10 | 2495450717166 |
| 5 | 3 | 10000 | 641 | 9359 | 0 | 7 | 1 | 10 | 2499734983598 |
| 5 | 5 | 10000 | 1305 | 8695 | 0 | 3 | 5 | 10 | 2491044501830 |
| 5 | 7 | 10000 | 2118 | 7882 | 0 | 6 | 1 | 60 | 2482496582662 |
| 5 | 9 | 10000 | 2644 | 7356 | 0 | 10 | 1 | 90 | 2483973570744 |
| 5 | 11 | 10000 | 1194 | 8806 | 0 | 5 | 1 | 20 | 2497001134576 |
| 5 | 13 | 10000 | 1510 | 8490 | 0 | 5 | 3 | 60 | 2496653855658 |
| 5 | 15 | 10000 | 1165 | 8835 | 0 | 7 | 5 | 10 | 2497013176240 |
| 5 | 17 | 10000 | 568 | 9432 | 0 | 4 | 9 | 28 | 2498884815472 |
| 5 | 19 | 10000 | 292 | 9708 | 0 | 4 | 11 | 14 | 2491275469904 |
| 5 | 21 | 10000 | 1433 | 8567 | 0 | 12 | 3 | 60 | 2499723206236 |
| 7 | 1 | 10000 | 82 | 9918 | 0 | 1 | 1 | 4 | 3496642466346 |
| 7 | 3 | 10000 | 61 | 9939 | 0 | 1 | 3 | 4 | 3496307106190 |
| 7 | 5 | 10000 | 498 | 9502 | 0 | 3 | 3 | 42 | 3499307619974 |
| 7 | 7 | 10000 | 306 | 9694 | 0 | 1 | 7 | 4 | 3473214715978 |
| 7 | 9 | 10000 | 79 | 9921 | 0 | 2 | 1 | 5 | 3496807620980 |
| 7 | 11 | 10000 | 303 | 9697 | 0 | 2 | 11 | 46 | 3494770618616 |
| 7 | 13 | 10000 | 40 | 9960 | 0 | 1 | 13 | 4 | 3494181834968 |
| 7 | 15 | 10000 | 544 | 9456 | 0 | 4 | 9 | 42 | 3497193930784 |
| 7 | 17 | 10000 | 36 | 9964 | 0 | 1 | 17 | 4 | 3498234292080 |
| 7 | 19 | 10000 | 299 | 9701 | 0 | 2 | 5 | 24 | 3487909104748 |
| 7 | 21 | 10000 | 205 | 9795 | 0 | 1 | 21 | 4 | 3478448304366 |

## Cycle inventory

- **(a=1, b=1)** — 1 distinct cycle(s):
    - cycle_id=0 | min=1 | len=2 | members={1, 2} | seeds_reaching=10000
- **(a=1, b=3)** — 2 distinct cycle(s):
    - cycle_id=0 | min=1 | len=3 | members={1, 2, 4} | seeds_reaching=6667
    - cycle_id=1 | min=3 | len=2 | members={3, 6} | seeds_reaching=3333
- **(a=1, b=5)** — 2 distinct cycle(s):
    - cycle_id=0 | min=1 | len=6 | members={1, 2, 3, 4, 6, 8} | seeds_reaching=8000
    - cycle_id=1 | min=5 | len=2 | members={5, 10} | seeds_reaching=2000
- **(a=1, b=7)** — 3 distinct cycle(s):
    - cycle_id=0 | min=1 | len=4 | members={1, 2, 4, 8} | seeds_reaching=4287
    - cycle_id=1 | min=3 | len=5 | members={3, 5, 6, 10, 12} | seeds_reaching=4285
    - cycle_id=2 | min=7 | len=2 | members={7, 14} | seeds_reaching=1428
- **(a=1, b=9)** — 3 distinct cycle(s):
    - cycle_id=0 | min=1 | len=9 | members={1, 2, 4, 5, 7, 8, ... (9 total)} | seeds_reaching=6667
    - cycle_id=1 | min=3 | len=3 | members={3, 6, 12} | seeds_reaching=2222
    - cycle_id=2 | min=9 | len=2 | members={9, 18} | seeds_reaching=1111
- **(a=1, b=11)** — 2 distinct cycle(s):
    - cycle_id=0 | min=1 | len=15 | members={1, 2, 3, 4, 5, 6, ... (15 total)} | seeds_reaching=9091
    - cycle_id=1 | min=11 | len=2 | members={11, 22} | seeds_reaching=909
- **(a=1, b=13)** — 2 distinct cycle(s):
    - cycle_id=0 | min=1 | len=18 | members={1, 2, 3, 4, 5, 6, ... (18 total)} | seeds_reaching=9231
    - cycle_id=1 | min=13 | len=2 | members={13, 26} | seeds_reaching=769
- **(a=1, b=15)** — 5 distinct cycle(s):
    - cycle_id=0 | min=1 | len=5 | members={1, 2, 4, 8, 16} | seeds_reaching=2668
    - cycle_id=1 | min=3 | len=6 | members={3, 6, 9, 12, 18, 24} | seeds_reaching=2667
    - cycle_id=2 | min=5 | len=3 | members={5, 10, 20} | seeds_reaching=1334
    - cycle_id=3 | min=7 | len=7 | members={7, 11, 13, 14, 22, 26, ... (7 total)} | seeds_reaching=2665
    - cycle_id=4 | min=15 | len=2 | members={15, 30} | seeds_reaching=666
- **(a=1, b=17)** — 3 distinct cycle(s):
    - cycle_id=0 | min=1 | len=12 | members={1, 2, 4, 8, 9, 13, ... (12 total)} | seeds_reaching=4707
    - cycle_id=1 | min=3 | len=12 | members={3, 5, 6, 7, 10, 11, ... (12 total)} | seeds_reaching=4705
    - cycle_id=2 | min=17 | len=2 | members={17, 34} | seeds_reaching=588
- **(a=1, b=19)** — 2 distinct cycle(s):
    - cycle_id=0 | min=1 | len=27 | members={1, 2, 3, 4, 5, 6, ... (27 total)} | seeds_reaching=9474
    - cycle_id=1 | min=19 | len=2 | members={19, 38} | seeds_reaching=526
- **(a=1, b=21)** — 6 distinct cycle(s):
    - cycle_id=0 | min=1 | len=8 | members={1, 2, 4, 8, 11, 16, ... (8 total)} | seeds_reaching=2859
    - cycle_id=1 | min=3 | len=4 | members={3, 6, 12, 24} | seeds_reaching=1429
    - cycle_id=2 | min=5 | len=10 | members={5, 10, 13, 17, 19, 20, ... (10 total)} | seeds_reaching=2856
    - cycle_id=3 | min=7 | len=3 | members={7, 14, 28} | seeds_reaching=952
    - cycle_id=4 | min=9 | len=5 | members={9, 15, 18, 30, 36} | seeds_reaching=1428
    - cycle_id=5 | min=21 | len=2 | members={21, 42} | seeds_reaching=476
- **(a=3, b=1)** — 1 distinct cycle(s):
    - cycle_id=0 | min=1 | len=3 | members={1, 2, 4} | seeds_reaching=10000
- **(a=3, b=3)** — 1 distinct cycle(s):
    - cycle_id=0 | min=3 | len=3 | members={3, 6, 12} | seeds_reaching=10000
- **(a=3, b=5)** — 6 distinct cycle(s):
    - cycle_id=0 | min=1 | len=4 | members={1, 2, 4, 8} | seeds_reaching=1436
    - cycle_id=2 | min=5 | len=3 | members={5, 10, 20} | seeds_reaching=2000
    - cycle_id=1 | min=19 | len=8 | members={19, 31, 38, 49, 62, 76, ... (8 total)} | seeds_reaching=4817
    - cycle_id=3 | min=23 | len=8 | members={23, 29, 37, 46, 58, 74, ... (8 total)} | seeds_reaching=953
    - cycle_id=4 | min=187 | len=44 | members={187, 283, 374, 427, 566, 587, ... (44 total)} | seeds_reaching=371
    - cycle_id=5 | min=347 | len=44 | members={347, 359, 407, 461, 523, 541, ... (44 total)} | seeds_reaching=423
- **(a=3, b=7)** — 2 distinct cycle(s):
    - cycle_id=0 | min=5 | len=6 | members={5, 10, 11, 20, 22, 40} | seeds_reaching=8572
    - cycle_id=1 | min=7 | len=3 | members={7, 14, 28} | seeds_reaching=1428
- **(a=3, b=9)** — 1 distinct cycle(s):
    - cycle_id=0 | min=9 | len=3 | members={9, 18, 36} | seeds_reaching=10000
- **(a=3, b=11)** — 3 distinct cycle(s):
    - cycle_id=0 | min=1 | len=8 | members={1, 2, 4, 7, 8, 14, ... (8 total)} | seeds_reaching=1957
    - cycle_id=2 | min=11 | len=3 | members={11, 22, 44} | seeds_reaching=909
    - cycle_id=1 | min=13 | len=22 | members={13, 25, 26, 29, 31, 35, ... (22 total)} | seeds_reaching=7134
- **(a=3, b=13)** — 10 distinct cycle(s):
    - cycle_id=0 | min=1 | len=5 | members={1, 2, 4, 8, 16} | seeds_reaching=4803
    - cycle_id=1 | min=13 | len=3 | members={13, 26, 52} | seeds_reaching=769
    - cycle_id=2 | min=131 | len=39 | members={131, 179, 203, 262, 275, 311, ... (39 total)} | seeds_reaching=2552
    - cycle_id=3 | min=211 | len=13 | members={211, 323, 422, 491, 646, 743, ... (13 total)} | seeds_reaching=311
    - cycle_id=5 | min=227 | len=13 | members={227, 347, 454, 527, 601, 694, ... (13 total)} | seeds_reaching=186
    - cycle_id=7 | min=251 | len=13 | members={251, 383, 439, 502, 581, 665, ... (13 total)} | seeds_reaching=209
    - cycle_id=4 | min=259 | len=13 | members={259, 341, 395, 518, 599, 682, ... (13 total)} | seeds_reaching=376
    - cycle_id=8 | min=283 | len=13 | members={283, 373, 431, 493, 566, 653, ... (13 total)} | seeds_reaching=236
    - cycle_id=6 | min=287 | len=13 | members={287, 331, 437, 503, 574, 662, ... (13 total)} | seeds_reaching=431
    - cycle_id=9 | min=319 | len=13 | members={319, 367, 421, 485, 557, 638, ... (13 total)} | seeds_reaching=127
- **(a=3, b=15)** — 6 distinct cycle(s):
    - cycle_id=1 | min=3 | len=4 | members={3, 6, 12, 24} | seeds_reaching=1446
    - cycle_id=2 | min=15 | len=3 | members={15, 30, 60} | seeds_reaching=2000
    - cycle_id=0 | min=57 | len=8 | members={57, 93, 114, 147, 186, 228, ... (8 total)} | seeds_reaching=4848
    - cycle_id=3 | min=69 | len=8 | members={69, 87, 111, 138, 174, 222, ... (8 total)} | seeds_reaching=957
    - cycle_id=4 | min=561 | len=44 | members={561, 849, 1122, 1281, 1698, 1761, ... (44 total)} | seeds_reaching=382
    - cycle_id=5 | min=1041 | len=44 | members={1041, 1077, 1221, 1383, 1569, 1623, ... (44 total)} | seeds_reaching=367
- **(a=3, b=17)** — 3 distinct cycle(s):
    - cycle_id=0 | min=1 | len=9 | members={1, 2, 4, 5, 8, 10, ... (9 total)} | seeds_reaching=3363
    - cycle_id=2 | min=17 | len=3 | members={17, 34, 68} | seeds_reaching=588
    - cycle_id=1 | min=23 | len=49 | members={23, 25, 31, 35, 43, 46, ... (49 total)} | seeds_reaching=6049
- **(a=3, b=19)** — 2 distinct cycle(s):
    - cycle_id=0 | min=5 | len=16 | members={5, 7, 10, 14, 17, 20, ... (16 total)} | seeds_reaching=9474
    - cycle_id=1 | min=19 | len=3 | members={19, 38, 76} | seeds_reaching=526
- **(a=3, b=21)** — 2 distinct cycle(s):
    - cycle_id=0 | min=15 | len=6 | members={15, 30, 33, 60, 66, 120} | seeds_reaching=8572
    - cycle_id=1 | min=21 | len=3 | members={21, 42, 84} | seeds_reaching=1428
- **(a=5, b=1)** — 3 distinct cycle(s):
    - cycle_id=0 | min=1 | len=7 | members={1, 2, 3, 4, 6, 8, ... (7 total)} | seeds_reaching=256
    - cycle_id=1 | min=13 | len=10 | members={13, 26, 33, 52, 66, 83, ... (10 total)} | seeds_reaching=383
    - cycle_id=2 | min=17 | len=10 | members={17, 27, 34, 43, 54, 68, ... (10 total)} | seeds_reaching=87
- **(a=5, b=3)** — 7 distinct cycle(s):
    - cycle_id=0 | min=1 | len=4 | members={1, 2, 4, 8} | seeds_reaching=73
    - cycle_id=1 | min=3 | len=7 | members={3, 6, 9, 12, 18, 24, ... (7 total)} | seeds_reaching=146
    - cycle_id=2 | min=39 | len=10 | members={39, 78, 99, 156, 198, 249, ... (10 total)} | seeds_reaching=167
    - cycle_id=3 | min=43 | len=10 | members={43, 86, 109, 137, 172, 218, ... (10 total)} | seeds_reaching=75
    - cycle_id=4 | min=51 | len=10 | members={51, 81, 102, 129, 162, 204, ... (10 total)} | seeds_reaching=43
    - cycle_id=5 | min=53 | len=10 | members={53, 67, 106, 134, 169, 212, ... (10 total)} | seeds_reaching=64
    - cycle_id=6 | min=61 | len=10 | members={61, 77, 97, 122, 154, 194, ... (10 total)} | seeds_reaching=73
- **(a=5, b=5)** — 3 distinct cycle(s):
    - cycle_id=0 | min=5 | len=7 | members={5, 10, 15, 20, 30, 40, ... (7 total)} | seeds_reaching=588
    - cycle_id=1 | min=65 | len=10 | members={65, 130, 165, 260, 330, 415, ... (10 total)} | seeds_reaching=549
    - cycle_id=2 | min=85 | len=10 | members={85, 135, 170, 215, 270, 340, ... (10 total)} | seeds_reaching=168
- **(a=5, b=7)** — 6 distinct cycle(s):
    - cycle_id=0 | min=1 | len=49 | members={1, 2, 3, 4, 6, 8, ... (49 total)} | seeds_reaching=1394
    - cycle_id=1 | min=7 | len=7 | members={7, 14, 21, 28, 42, 56, ... (7 total)} | seeds_reaching=97
    - cycle_id=2 | min=9 | len=7 | members={9, 13, 18, 26, 36, 52, ... (7 total)} | seeds_reaching=104
    - cycle_id=3 | min=57 | len=60 | members={57, 59, 71, 73, 93, 114, ... (60 total)} | seeds_reaching=409
    - cycle_id=4 | min=91 | len=10 | members={91, 182, 231, 364, 462, 581, ... (10 total)} | seeds_reaching=87
    - cycle_id=5 | min=119 | len=10 | members={119, 189, 238, 301, 378, 476, ... (10 total)} | seeds_reaching=27
- **(a=5, b=9)** — 10 distinct cycle(s):
    - cycle_id=0 | min=1 | len=12 | members={1, 2, 4, 7, 8, 11, ... (12 total)} | seeds_reaching=850
    - cycle_id=1 | min=3 | len=4 | members={3, 6, 12, 24} | seeds_reaching=40
    - cycle_id=2 | min=9 | len=7 | members={9, 18, 27, 36, 54, 72, ... (7 total)} | seeds_reaching=87
    - cycle_id=3 | min=29 | len=90 | members={29, 58, 71, 77, 91, 113, ... (90 total)} | seeds_reaching=832
    - cycle_id=5 | min=89 | len=30 | members={89, 143, 178, 181, 227, 283, ... (30 total)} | seeds_reaching=636
    - cycle_id=4 | min=117 | len=10 | members={117, 234, 297, 468, 594, 747, ... (10 total)} | seeds_reaching=71
    - cycle_id=6 | min=129 | len=10 | members={129, 258, 327, 411, 516, 654, ... (10 total)} | seeds_reaching=33
    - cycle_id=7 | min=153 | len=10 | members={153, 243, 306, 387, 486, 612, ... (10 total)} | seeds_reaching=25
    - cycle_id=8 | min=159 | len=10 | members={159, 201, 318, 402, 507, 636, ... (10 total)} | seeds_reaching=34
    - cycle_id=9 | min=183 | len=10 | members={183, 231, 291, 366, 462, 582, ... (10 total)} | seeds_reaching=36
- **(a=5, b=11)** — 5 distinct cycle(s):
    - cycle_id=0 | min=1 | len=5 | members={1, 2, 4, 8, 16} | seeds_reaching=520
    - cycle_id=1 | min=11 | len=7 | members={11, 22, 33, 44, 66, 88, ... (7 total)} | seeds_reaching=76
    - cycle_id=3 | min=141 | len=20 | members={141, 179, 282, 357, 358, 449, ... (20 total)} | seeds_reaching=516
    - cycle_id=2 | min=143 | len=10 | members={143, 286, 363, 572, 726, 913, ... (10 total)} | seeds_reaching=60
    - cycle_id=4 | min=187 | len=10 | members={187, 297, 374, 473, 594, 748, ... (10 total)} | seeds_reaching=22
- **(a=5, b=13)** — 5 distinct cycle(s):
    - cycle_id=0 | min=3 | len=8 | members={3, 6, 7, 12, 14, 24, ... (8 total)} | seeds_reaching=604
    - cycle_id=2 | min=13 | len=7 | members={13, 26, 39, 52, 78, 104, ... (7 total)} | seeds_reaching=69
    - cycle_id=1 | min=53 | len=60 | members={53, 106, 131, 139, 167, 177, ... (60 total)} | seeds_reaching=764
    - cycle_id=3 | min=169 | len=10 | members={169, 338, 429, 676, 858, 1079, ... (10 total)} | seeds_reaching=53
    - cycle_id=4 | min=221 | len=10 | members={221, 351, 442, 559, 702, 884, ... (10 total)} | seeds_reaching=20
- **(a=5, b=15)** — 7 distinct cycle(s):
    - cycle_id=0 | min=5 | len=4 | members={5, 10, 20, 40} | seeds_reaching=167
    - cycle_id=1 | min=15 | len=7 | members={15, 30, 45, 60, 90, 120, ... (7 total)} | seeds_reaching=330
    - cycle_id=2 | min=195 | len=10 | members={195, 390, 495, 780, 990, 1245, ... (10 total)} | seeds_reaching=231
    - cycle_id=3 | min=215 | len=10 | members={215, 430, 545, 685, 860, 1090, ... (10 total)} | seeds_reaching=117
    - cycle_id=4 | min=255 | len=10 | members={255, 405, 510, 645, 810, 1020, ... (10 total)} | seeds_reaching=84
    - cycle_id=5 | min=265 | len=10 | members={265, 335, 530, 670, 845, 1060, ... (10 total)} | seeds_reaching=115
    - cycle_id=6 | min=305 | len=10 | members={305, 385, 485, 610, 770, 970, ... (10 total)} | seeds_reaching=121
- **(a=5, b=17)** — 4 distinct cycle(s):
    - cycle_id=0 | min=9 | len=28 | members={9, 11, 18, 22, 29, 31, ... (28 total)} | seeds_reaching=447
    - cycle_id=1 | min=17 | len=7 | members={17, 34, 51, 68, 102, 136, ... (7 total)} | seeds_reaching=59
    - cycle_id=2 | min=221 | len=10 | members={221, 442, 561, 884, 1122, 1411, ... (10 total)} | seeds_reaching=44
    - cycle_id=3 | min=289 | len=10 | members={289, 459, 578, 731, 918, 1156, ... (10 total)} | seeds_reaching=18
- **(a=5, b=19)** — 4 distinct cycle(s):
    - cycle_id=0 | min=11 | len=14 | members={11, 22, 37, 44, 51, 74, ... (14 total)} | seeds_reaching=178
    - cycle_id=1 | min=19 | len=7 | members={19, 38, 57, 76, 114, 152, ... (7 total)} | seeds_reaching=58
    - cycle_id=2 | min=247 | len=10 | members={247, 494, 627, 988, 1254, 1577, ... (10 total)} | seeds_reaching=40
    - cycle_id=3 | min=323 | len=10 | members={323, 513, 646, 817, 1026, 1292, ... (10 total)} | seeds_reaching=16
- **(a=5, b=21)** — 12 distinct cycle(s):
    - cycle_id=1 | min=3 | len=49 | members={3, 6, 9, 12, 18, 24, ... (49 total)} | seeds_reaching=672
    - cycle_id=3 | min=7 | len=4 | members={7, 14, 28, 56} | seeds_reaching=26
    - cycle_id=0 | min=13 | len=14 | members={13, 26, 43, 52, 59, 79, ... (14 total)} | seeds_reaching=205
    - cycle_id=2 | min=17 | len=14 | members={17, 23, 34, 46, 53, 68, ... (14 total)} | seeds_reaching=105
    - cycle_id=4 | min=21 | len=7 | members={21, 42, 63, 84, 126, 168, ... (7 total)} | seeds_reaching=53
    - cycle_id=5 | min=27 | len=7 | members={27, 39, 54, 78, 108, 156, ... (7 total)} | seeds_reaching=49
    - cycle_id=6 | min=171 | len=60 | members={171, 177, 213, 219, 279, 342, ... (60 total)} | seeds_reaching=209
    - cycle_id=7 | min=273 | len=10 | members={273, 546, 693, 1092, 1386, 1743, ... (10 total)} | seeds_reaching=38
    - cycle_id=8 | min=301 | len=10 | members={301, 602, 763, 959, 1204, 1526, ... (10 total)} | seeds_reaching=20
    - cycle_id=9 | min=357 | len=10 | members={357, 567, 714, 903, 1134, 1428, ... (10 total)} | seeds_reaching=16
    - cycle_id=10 | min=371 | len=10 | members={371, 469, 742, 938, 1183, 1484, ... (10 total)} | seeds_reaching=22
    - cycle_id=11 | min=427 | len=10 | members={427, 539, 679, 854, 1078, 1358, ... (10 total)} | seeds_reaching=18
- **(a=7, b=1)** — 1 distinct cycle(s):
    - cycle_id=0 | min=1 | len=4 | members={1, 2, 4, 8} | seeds_reaching=82
- **(a=7, b=3)** — 1 distinct cycle(s):
    - cycle_id=0 | min=3 | len=4 | members={3, 6, 12, 24} | seeds_reaching=61
- **(a=7, b=5)** — 3 distinct cycle(s):
    - cycle_id=0 | min=3 | len=8 | members={3, 6, 12, 13, 24, 26, ... (8 total)} | seeds_reaching=81
    - cycle_id=1 | min=5 | len=4 | members={5, 10, 20, 40} | seeds_reaching=50
    - cycle_id=2 | min=27 | len=42 | members={27, 54, 61, 69, 89, 97, ... (42 total)} | seeds_reaching=367
- **(a=7, b=7)** — 1 distinct cycle(s):
    - cycle_id=0 | min=7 | len=4 | members={7, 14, 28, 56} | seeds_reaching=306
- **(a=7, b=9)** — 2 distinct cycle(s):
    - cycle_id=0 | min=1 | len=5 | members={1, 2, 4, 8, 16} | seeds_reaching=38
    - cycle_id=1 | min=9 | len=4 | members={9, 18, 36, 72} | seeds_reaching=41
- **(a=7, b=11)** — 2 distinct cycle(s):
    - cycle_id=1 | min=11 | len=4 | members={11, 22, 44, 88} | seeds_reaching=40
    - cycle_id=0 | min=23 | len=46 | members={23, 39, 43, 46, 51, 71, ... (46 total)} | seeds_reaching=263
- **(a=7, b=13)** — 1 distinct cycle(s):
    - cycle_id=0 | min=13 | len=4 | members={13, 26, 52, 104} | seeds_reaching=40
- **(a=7, b=15)** — 4 distinct cycle(s):
    - cycle_id=1 | min=9 | len=8 | members={9, 18, 36, 39, 72, 78, ... (8 total)} | seeds_reaching=60
    - cycle_id=0 | min=11 | len=8 | members={11, 22, 23, 44, 46, 88, ... (8 total)} | seeds_reaching=217
    - cycle_id=2 | min=15 | len=4 | members={15, 30, 60, 120} | seeds_reaching=39
    - cycle_id=3 | min=81 | len=42 | members={81, 162, 183, 207, 267, 291, ... (42 total)} | seeds_reaching=228
- **(a=7, b=17)** — 1 distinct cycle(s):
    - cycle_id=0 | min=17 | len=4 | members={17, 34, 68, 136} | seeds_reaching=36
- **(a=7, b=19)** — 2 distinct cycle(s):
    - cycle_id=0 | min=5 | len=24 | members={5, 10, 13, 20, 26, 27, ... (24 total)} | seeds_reaching=266
    - cycle_id=1 | min=19 | len=4 | members={19, 38, 76, 152} | seeds_reaching=33
- **(a=7, b=21)** — 1 distinct cycle(s):
    - cycle_id=0 | min=21 | len=4 | members={21, 42, 84, 168} | seeds_reaching=205

## Surprises against the predictions

Predictions from `autoresearch/log/000-research-kickoff.md`:

1. **a=1: trivial. All seeds reach the b-fixed-cycle quickly. No surprises.**
2. **a=3, b=1 (classical Collatz): all seeds in [1, 10^4] reach 1.**
3. **a=3, b=3: equivalent to classical via n→n/3 substitution if 3|n; otherwise diverges from {n: 3∤n}. (Possibly conjugate — flag.)**
4. **a=3, b=5: classical literature suggests at least one extra cycle. Expect: not all seeds reach the trivial cycle.**
5. **a=5, b=1: known empirically to have orbits unbounded up to large N for some seeds. Expect: at least one seed hits the H bound or T bound.**
6. **a=5,b=3 / ... / a=7,b=*: less tabulated. Expect ≥ 2 (a,b) pairs to show "additional cycle" classification.**

### Verdicts

- **P1 (a=1 trivial): MIXED/CONTRADICTED.**
    - a=1, b=1: distinct_cycles=1, reached=10000, exceeded_H=0, exceeded_T=0.
    - a=1, b=3: distinct_cycles=2, reached=10000, exceeded_H=0, exceeded_T=0.
    - a=1, b=5: distinct_cycles=2, reached=10000, exceeded_H=0, exceeded_T=0.
    - a=1, b=7: distinct_cycles=3, reached=10000, exceeded_H=0, exceeded_T=0.
    - a=1, b=9: distinct_cycles=3, reached=10000, exceeded_H=0, exceeded_T=0.
    - a=1, b=11: distinct_cycles=2, reached=10000, exceeded_H=0, exceeded_T=0.
    - a=1, b=13: distinct_cycles=2, reached=10000, exceeded_H=0, exceeded_T=0.
    - a=1, b=15: distinct_cycles=5, reached=10000, exceeded_H=0, exceeded_T=0.
    - a=1, b=17: distinct_cycles=3, reached=10000, exceeded_H=0, exceeded_T=0.
    - a=1, b=19: distinct_cycles=2, reached=10000, exceeded_H=0, exceeded_T=0.
    - a=1, b=21: distinct_cycles=6, reached=10000, exceeded_H=0, exceeded_T=0.
- **P2 (a=3, b=1 classical Collatz → {1,2,4}): CONFIRMED.** All 10000 seeds reach the cycle {1,2,4}. (Sanity check passed.)
- **P3 (a=3, b=3 conjugacy):** distinct_cycles=1, reached=10000, H=0, T=0. Among 3∤n0: cycle=6667, H=0. Among 3|n0: cycle=3333, H=0. Note: the iteration `n→3n+3` always produces multiples of 3, and division by 2 preserves the 3-divisibility class once we reach an odd multiple of 3 (n is odd, 3|n → 3n+3=3(n+1) and division by 2 doesn't disturb the 3-factor since 3∤2). So the long-run dynamics partition by `n0 mod 3` exactly as the prediction suggests; verdict here depends on whether non-multiples-of-3 escape or join a separate cycle.
- **P4 (a=3, b=5 extra cycle):** distinct_cycles=6, reached=10000/10000, H=0, T=0. **CONFIRMED** — multiple cycles found.
- **P5 (a=5, b=1 horizon escape):** reached=726, H=9274, T=0, distinct_cycles=3. **CONFIRMED** — at least one seed hits horizon.
- **P6 (a∈{5,7}, ≥2 variants with additional cycle):** 16 variant(s) with ≥2 distinct cycles. Variants: (a=5,b=1,nc=3), (a=5,b=3,nc=7), (a=5,b=5,nc=3), (a=5,b=7,nc=6), (a=5,b=9,nc=10), (a=5,b=11,nc=5), (a=5,b=13,nc=5), (a=5,b=15,nc=7), (a=5,b=17,nc=4), (a=5,b=19,nc=4), (a=5,b=21,nc=12), (a=7,b=5,nc=3), (a=7,b=9,nc=2), (a=7,b=11,nc=2), (a=7,b=15,nc=4), (a=7,b=19,nc=2). **CONFIRMED**.

## Anomalies and standouts

- **Single-cycle, all-seeds-reach** (4 variants): (a=1,b=1), (a=3,b=1), (a=3,b=3), (a=3,b=9)
- **Multiple distinct cycles**: (a=1,b=3,nc=2), (a=1,b=5,nc=2), (a=1,b=7,nc=3), (a=1,b=9,nc=3), (a=1,b=11,nc=2), (a=1,b=13,nc=2), (a=1,b=15,nc=5), (a=1,b=17,nc=3), (a=1,b=19,nc=2), (a=1,b=21,nc=6), (a=3,b=5,nc=6), (a=3,b=7,nc=2), (a=3,b=11,nc=3), (a=3,b=13,nc=10), (a=3,b=15,nc=6), (a=3,b=17,nc=3), (a=3,b=19,nc=2), (a=3,b=21,nc=2), (a=5,b=1,nc=3), (a=5,b=3,nc=7), (a=5,b=5,nc=3), (a=5,b=7,nc=6), (a=5,b=9,nc=10), (a=5,b=11,nc=5), (a=5,b=13,nc=5), (a=5,b=15,nc=7), (a=5,b=17,nc=4), (a=5,b=19,nc=4), (a=5,b=21,nc=12), (a=7,b=5,nc=3), (a=7,b=9,nc=2), (a=7,b=11,nc=2), (a=7,b=15,nc=4), (a=7,b=19,nc=2)
- **Variants with ≥1 horizon escape**: (a=5,b=1,H=9274,T=0), (a=5,b=3,H=9359,T=0), (a=5,b=5,H=8695,T=0), (a=5,b=7,H=7882,T=0), (a=5,b=9,H=7356,T=0), (a=5,b=11,H=8806,T=0), (a=5,b=13,H=8490,T=0), (a=5,b=15,H=8835,T=0), (a=5,b=17,H=9432,T=0), (a=5,b=19,H=9708,T=0), (a=5,b=21,H=8567,T=0), (a=7,b=1,H=9918,T=0), (a=7,b=3,H=9939,T=0), (a=7,b=5,H=9502,T=0), (a=7,b=7,H=9694,T=0), (a=7,b=9,H=9921,T=0), (a=7,b=11,H=9697,T=0), (a=7,b=13,H=9960,T=0), (a=7,b=15,H=9456,T=0), (a=7,b=17,H=9964,T=0), (a=7,b=19,H=9701,T=0), (a=7,b=21,H=9795,T=0)
- **Top 10 variants by max value reached**:
    - (a=7, b=5): max_value = 3499307619974
    - (a=7, b=17): max_value = 3498234292080
    - (a=7, b=15): max_value = 3497193930784
    - (a=7, b=9): max_value = 3496807620980
    - (a=7, b=1): max_value = 3496642466346
    - (a=7, b=3): max_value = 3496307106190
    - (a=7, b=11): max_value = 3494770618616
    - (a=7, b=13): max_value = 3494181834968
    - (a=7, b=19): max_value = 3487909104748
    - (a=7, b=21): max_value = 3478448304366

## Runtime

- Total wall-clock: **2.5s**
- Sweep loop (44 variants): **1.0s**
- Parquet write: 1.53s
- Per-variant timings (top 10 slowest):
    - (a=5, b=21): 0.06s
    - (a=5, b=1): 0.04s
    - (a=5, b=9): 0.04s
    - (a=5, b=7): 0.04s
    - (a=5, b=11): 0.04s
    - (a=5, b=13): 0.04s
    - (a=5, b=3): 0.04s
    - (a=5, b=17): 0.04s
    - (a=5, b=19): 0.04s
    - (a=7, b=11): 0.04s
