# 012 — Wider-b sweep + atlas extension

## Setup

Family: `T_{a,b}(n) = n/2` if n even, else `a*n + b`. Scope: `a ∈ {1,3,5,7}`, `b ∈ [23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51]` (60 new variants). Per-variant: every seed `n0 ∈ [1, 100000]`. Horizons: value bound `H = 10000000000000`, step bound `T = 100000`. Same horizons as action 006. Cycle IDs start at 0 per (a, b) (independent of action 001 numbering).

## Per-variant table

| a | b | total_seeds | reached_cycle | exceeded_H | exceeded_T | n_distinct_cycles | smallest_cycle_min |
|---|---|-------------|---------------|------------|------------|-------------------|--------------------|
| 1 | 23 | 100000 | 100000 | 0 | 0 | 3 | 1 |
| 1 | 25 | 100000 | 100000 | 0 | 0 | 3 | 1 |
| 1 | 27 | 100000 | 100000 | 0 | 0 | 4 | 1 |
| 1 | 29 | 100000 | 100000 | 0 | 0 | 2 | 1 |
| 1 | 31 | 100000 | 100000 | 0 | 0 | 7 | 1 |
| 1 | 33 | 100000 | 100000 | 0 | 0 | 5 | 1 |
| 1 | 35 | 100000 | 100000 | 0 | 0 | 6 | 1 |
| 1 | 37 | 100000 | 100000 | 0 | 0 | 2 | 1 |
| 1 | 39 | 100000 | 100000 | 0 | 0 | 5 | 1 |
| 1 | 41 | 100000 | 100000 | 0 | 0 | 3 | 1 |
| 1 | 43 | 100000 | 100000 | 0 | 0 | 4 | 1 |
| 1 | 45 | 100000 | 100000 | 0 | 0 | 8 | 1 |
| 1 | 47 | 100000 | 100000 | 0 | 0 | 3 | 1 |
| 1 | 49 | 100000 | 100000 | 0 | 0 | 5 | 1 |
| 1 | 51 | 100000 | 100000 | 0 | 0 | 8 | 1 |
| 3 | 23 | 100000 | 100000 | 0 | 0 | 4 | 5 |
| 3 | 25 | 100000 | 100000 | 0 | 0 | 8 | 5 |
| 3 | 27 | 100000 | 100000 | 0 | 0 | 1 | 27 |
| 3 | 29 | 100000 | 100000 | 0 | 0 | 5 | 1 |
| 3 | 31 | 100000 | 100000 | 0 | 0 | 2 | 13 |
| 3 | 33 | 100000 | 100000 | 0 | 0 | 3 | 3 |
| 3 | 35 | 100000 | 100000 | 0 | 0 | 9 | 7 |
| 3 | 37 | 100000 | 100000 | 0 | 0 | 4 | 19 |
| 3 | 39 | 100000 | 100000 | 0 | 0 | 10 | 3 |
| 3 | 41 | 100000 | 100000 | 0 | 0 | 2 | 1 |
| 3 | 43 | 100000 | 100000 | 0 | 0 | 2 | 1 |
| 3 | 45 | 100000 | 100000 | 0 | 0 | 6 | 9 |
| 3 | 47 | 100000 | 100000 | 0 | 0 | 8 | 5 |
| 3 | 49 | 100000 | 100000 | 0 | 0 | 3 | 25 |
| 3 | 51 | 100000 | 100000 | 0 | 0 | 3 | 3 |
| 5 | 23 | 100000 | 6261 | 93739 | 0 | 11 | 1 |
| 5 | 25 | 100000 | 10097 | 89903 | 0 | 3 | 25 |
| 5 | 27 | 100000 | 6280 | 93720 | 0 | 11 | 1 |
| 5 | 29 | 100000 | 368 | 99632 | 0 | 3 | 29 |
| 5 | 31 | 100000 | 859 | 99141 | 0 | 4 | 31 |
| 5 | 33 | 100000 | 5687 | 94313 | 0 | 18 | 1 |
| 5 | 35 | 100000 | 16588 | 83412 | 0 | 6 | 5 |
| 5 | 37 | 100000 | 5963 | 94037 | 0 | 5 | 7 |
| 5 | 39 | 100000 | 8945 | 91055 | 0 | 16 | 7 |
| 5 | 41 | 100000 | 3575 | 96425 | 0 | 4 | 21 |
| 5 | 43 | 100000 | 1438 | 98562 | 0 | 5 | 9 |
| 5 | 45 | 100000 | 20540 | 79460 | 0 | 10 | 5 |
| 5 | 47 | 100000 | 265 | 99735 | 0 | 3 | 47 |
| 5 | 49 | 100000 | 5496 | 94504 | 0 | 7 | 1 |
| 5 | 51 | 100000 | 1453 | 98547 | 0 | 8 | 17 |
| 7 | 23 | 100000 | 161 | 99839 | 0 | 2 | 1 |
| 7 | 25 | 100000 | 811 | 99189 | 0 | 4 | 1 |
| 7 | 27 | 100000 | 111 | 99889 | 0 | 2 | 3 |
| 7 | 29 | 100000 | 62 | 99938 | 0 | 1 | 29 |
| 7 | 31 | 100000 | 1338 | 98662 | 0 | 5 | 31 |
| 7 | 33 | 100000 | 508 | 99492 | 0 | 2 | 33 |
| 7 | 35 | 100000 | 3539 | 96461 | 0 | 3 | 21 |
| 7 | 37 | 100000 | 60 | 99940 | 0 | 1 | 37 |
| 7 | 39 | 100000 | 55 | 99945 | 0 | 1 | 39 |
| 7 | 41 | 100000 | 54 | 99946 | 0 | 1 | 41 |
| 7 | 43 | 100000 | 52 | 99948 | 0 | 1 | 43 |
| 7 | 45 | 100000 | 914 | 99086 | 0 | 5 | 5 |
| 7 | 47 | 100000 | 51 | 99949 | 0 | 1 | 47 |
| 7 | 49 | 100000 | 2268 | 97732 | 0 | 1 | 49 |
| 7 | 51 | 100000 | 49 | 99951 | 0 | 1 | 51 |

## C-001 verdict (a ∈ {1, 3} at wider b)

**CONFIRMED at wider b.** All 3000000 trajectories (a ∈ {1, 3}, b ∈ [23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51]) reached a cycle within T = 100000 steps without exceeding H = 10000000000000.

## C-003 verdict (a = 7 at wider b — single L1 cycle?)

- Variants where the only cycle reached is the L1 cycle `{b, 2b, 4b, 8b}`: **8** out of 15 ([29, 37, 39, 41, 43, 47, 49, 51]).
- **16 additional cycle(s)** beyond the L1 cycle:
    - (a=7, b=23) cycle_id=0 | len=10 | members={1, 2, 4, 8, 15, 16, 30, 32, ... (10 total)} | seeds_reaching=97
    - (a=7, b=25) cycle_id=0 | len=6 | members={1, 2, 4, 8, 16, 32} | seeds_reaching=162
    - (a=7, b=25) cycle_id=1 | len=8 | members={15, 30, 60, 65, 120, 130, 240, 480} | seeds_reaching=94
    - (a=7, b=25) cycle_id=3 | len=42 | members={135, 270, 305, 345, 445, 485, 505, 540, ... (42 total)} | seeds_reaching=492
    - (a=7, b=27) cycle_id=0 | len=5 | members={3, 6, 12, 24, 48} | seeds_reaching=49
    - (a=7, b=31) cycle_id=0 | len=23 | members={129, 143, 159, 258, 286, 318, 467, 516, ... (23 total)} | seeds_reaching=391
    - (a=7, b=31) cycle_id=1 | len=23 | members={89, 145, 178, 290, 327, 356, 523, 580, ... (23 total)} | seeds_reaching=244
    - (a=7, b=31) cycle_id=3 | len=23 | members={101, 111, 202, 222, 369, 404, 444, 503, ... (23 total)} | seeds_reaching=390
    - (a=7, b=31) cycle_id=4 | len=23 | members={73, 146, 241, 271, 292, 482, 542, 584, ... (23 total)} | seeds_reaching=252
    - (a=7, b=33) cycle_id=0 | len=46 | members={69, 117, 129, 138, 153, 213, 234, 258, ... (46 total)} | seeds_reaching=447
    - (a=7, b=35) cycle_id=0 | len=8 | members={21, 42, 84, 91, 168, 182, 336, 672} | seeds_reaching=598
    - (a=7, b=35) cycle_id=2 | len=42 | members={189, 378, 427, 483, 623, 679, 707, 756, ... (42 total)} | seeds_reaching=2553
    - (a=7, b=45) cycle_id=0 | len=8 | members={33, 66, 69, 132, 138, 264, 276, 528} | seeds_reaching=354
    - (a=7, b=45) cycle_id=1 | len=5 | members={5, 10, 20, 40, 80} | seeds_reaching=45
    - (a=7, b=45) cycle_id=2 | len=8 | members={27, 54, 108, 117, 216, 234, 432, 864} | seeds_reaching=81
    - (a=7, b=45) cycle_id=4 | len=42 | members={243, 486, 549, 621, 801, 873, 909, 972, ... (42 total)} | seeds_reaching=383

## C-007' verdict (a = 1 at wider b)

Tag each cycle as `inherited` if gcd(members) > 1 and divides b AND the gcd-scaled image is a verified cycle of T_{a, b/gcd}; else `new`.

| b | d(b) | n_total | n_inherited | n_new | lower_holds (n_total ≥ d(b)−1) | strong_inherited (n_inh ≥ d(b)−1) |
|---|------|---------|-------------|-------|------------------------------|---------------------------------|
| 23 | 2 | 3 | 1 | 2 | True | True |
| 25 | 3 | 3 | 2 | 1 | True | True |
| 27 | 4 | 4 | 3 | 1 | True | True |
| 29 | 2 | 2 | 1 | 1 | True | True |
| 31 | 2 | 7 | 1 | 6 | True | True |
| 33 | 4 | 5 | 3 | 2 | True | True |
| 35 | 4 | 6 | 4 | 2 | True | True |
| 37 | 2 | 2 | 1 | 1 | True | True |
| 39 | 4 | 5 | 3 | 2 | True | True |
| 41 | 2 | 3 | 1 | 2 | True | True |
| 43 | 2 | 4 | 1 | 3 | True | True |
| 45 | 6 | 8 | 6 | 2 | True | True |
| 47 | 2 | 3 | 1 | 2 | True | True |
| 49 | 3 | 5 | 3 | 2 | True | True |
| 51 | 4 | 8 | 4 | 4 | True | True |

**Lower bound n_total ≥ d(b)−1 holds for all 15 wider-b variants at a=1.**

## C-009 verdict (period law t_period ≈ L · (1 + log₂ a))

For each cycle: t_period = total cycle length, L = #odd members. Per-(a, b) we report mean t_period/L. Predicted: 1 + log₂(a) (= 1 for a=1, ≈2.585 for a=3, ≈3.322 for a=5, ≈3.807 for a=7).

| a | b | n_cycles | mean t_period/L | predicted | abs deviation |
|---|---|----------|-----------------|-----------|---------------|
| 1 | 23 | 3 | 2.774 | 1.000 | 1.774 |
| 1 | 25 | 3 | 2.667 | 1.000 | 1.667 |
| 1 | 27 | 4 | 2.750 | 1.000 | 1.750 |
| 1 | 29 | 2 | 2.500 | 1.000 | 1.500 |
| 1 | 31 | 7 | 3.226 | 1.000 | 2.226 |
| 1 | 33 | 5 | 2.800 | 1.000 | 1.800 |
| 1 | 35 | 6 | 2.936 | 1.000 | 1.936 |
| 1 | 37 | 2 | 2.500 | 1.000 | 1.500 |
| 1 | 39 | 5 | 2.900 | 1.000 | 1.900 |
| 1 | 41 | 3 | 2.667 | 1.000 | 1.667 |
| 1 | 43 | 4 | 2.750 | 1.000 | 1.750 |
| 1 | 45 | 8 | 3.056 | 1.000 | 2.056 |
| 1 | 47 | 3 | 2.733 | 1.000 | 1.733 |
| 1 | 49 | 5 | 2.902 | 1.000 | 1.902 |
| 1 | 51 | 8 | 3.075 | 1.000 | 2.075 |
| 3 | 23 | 4 | 3.163 | 2.585 | 0.578 |
| 3 | 25 | 8 | 2.939 | 2.585 | 0.354 |
| 3 | 27 | 1 | 3.000 | 2.585 | 0.415 |
| 3 | 29 | 5 | 3.412 | 2.585 | 0.827 |
| 3 | 31 | 2 | 2.958 | 2.585 | 0.373 |
| 3 | 33 | 3 | 3.250 | 2.585 | 0.665 |
| 3 | 35 | 9 | 2.946 | 2.585 | 0.361 |
| 3 | 37 | 4 | 3.000 | 2.585 | 0.415 |
| 3 | 39 | 10 | 2.880 | 2.585 | 0.295 |
| 3 | 41 | 2 | 3.250 | 2.585 | 0.665 |
| 3 | 43 | 2 | 3.833 | 2.585 | 1.248 |
| 3 | 45 | 6 | 2.918 | 2.585 | 0.333 |
| 3 | 47 | 8 | 2.884 | 2.585 | 0.299 |
| 3 | 49 | 3 | 2.909 | 2.585 | 0.324 |
| 3 | 51 | 3 | 3.407 | 2.585 | 0.822 |
| 5 | 23 | 11 | 3.432 | 3.322 | 0.110 |
| 5 | 25 | 3 | 3.389 | 3.322 | 0.067 |
| 5 | 27 | 11 | 3.712 | 3.322 | 0.390 |
| 5 | 29 | 3 | 3.389 | 3.322 | 0.067 |
| 5 | 31 | 4 | 3.375 | 3.322 | 0.053 |
| 5 | 33 | 18 | 3.565 | 3.322 | 0.243 |
| 5 | 35 | 6 | 3.417 | 3.322 | 0.095 |
| 5 | 37 | 5 | 3.384 | 3.322 | 0.062 |
| 5 | 39 | 16 | 3.469 | 3.322 | 0.147 |
| 5 | 41 | 4 | 3.431 | 3.322 | 0.109 |
| 5 | 43 | 5 | 3.500 | 3.322 | 0.178 |
| 5 | 45 | 10 | 3.483 | 3.322 | 0.161 |
| 5 | 47 | 3 | 3.389 | 3.322 | 0.067 |
| 5 | 49 | 7 | 3.500 | 3.322 | 0.178 |
| 5 | 51 | 8 | 3.458 | 3.322 | 0.136 |
| 7 | 23 | 2 | 4.500 | 3.807 | 0.693 |
| 7 | 25 | 4 | 4.455 | 3.807 | 0.647 |
| 7 | 27 | 2 | 4.500 | 3.807 | 0.693 |
| 7 | 29 | 1 | 4.000 | 3.807 | 0.193 |
| 7 | 31 | 5 | 3.867 | 3.807 | 0.059 |
| 7 | 33 | 2 | 3.917 | 3.807 | 0.109 |
| 7 | 35 | 3 | 3.939 | 3.807 | 0.132 |
| 7 | 37 | 1 | 4.000 | 3.807 | 0.193 |
| 7 | 39 | 1 | 4.000 | 3.807 | 0.193 |
| 7 | 41 | 1 | 4.000 | 3.807 | 0.193 |
| 7 | 43 | 1 | 4.000 | 3.807 | 0.193 |
| 7 | 45 | 5 | 4.164 | 3.807 | 0.356 |
| 7 | 47 | 1 | 4.000 | 3.807 | 0.193 |
| 7 | 49 | 1 | 4.000 | 3.807 | 0.193 |
| 7 | 51 | 1 | 4.000 | 3.807 | 0.193 |

Max absolute deviation across all (a, b): **2.2262**.

## C-011 verdict (primitive cycle ⇒ b | (2^K − a^L))

For each `new`-tagged cycle, compute K = t_period − L and check whether b divides (2^K − a^L).

| a | b | cycle_id | cycle_min | L | K | 2^K − a^L | (2^K − a^L) mod b | matches |
|---|---|----------|-----------|---|---|-----------|-------------------|---------|
| 1 | 23 | 0 | 1 | 4 | 11 | 2047 | 0 | yes |
| 1 | 23 | 1 | 5 | 7 | 11 | 2047 | 0 | yes |
| 1 | 25 | 0 | 1 | 10 | 20 | 1048575 | 0 | yes |
| 1 | 27 | 0 | 1 | 9 | 18 | 262143 | 0 | yes |
| 1 | 29 | 0 | 1 | 14 | 28 | 268435455 | 0 | yes |
| 1 | 31 | 0 | 1 | 1 | 5 | 31 | 0 | yes |
| 1 | 31 | 1 | 3 | 2 | 5 | 31 | 0 | yes |
| 1 | 31 | 2 | 5 | 2 | 5 | 31 | 0 | yes |
| 1 | 31 | 3 | 7 | 3 | 5 | 31 | 0 | yes |
| 1 | 31 | 4 | 11 | 3 | 5 | 31 | 0 | yes |
| 1 | 31 | 5 | 15 | 4 | 5 | 31 | 0 | yes |
| 1 | 33 | 0 | 1 | 5 | 10 | 1023 | 0 | yes |
| 1 | 33 | 2 | 5 | 5 | 10 | 1023 | 0 | yes |
| 1 | 35 | 0 | 1 | 5 | 12 | 4095 | 0 | yes |
| 1 | 35 | 1 | 3 | 7 | 12 | 4095 | 0 | yes |
| 1 | 37 | 0 | 1 | 18 | 36 | 68719476735 | 0 | yes |
| 1 | 39 | 0 | 1 | 4 | 12 | 4095 | 0 | yes |
| 1 | 39 | 2 | 7 | 8 | 12 | 4095 | 0 | yes |
| 1 | 41 | 0 | 1 | 10 | 20 | 1048575 | 0 | yes |
| 1 | 41 | 1 | 3 | 10 | 20 | 1048575 | 0 | yes |
| 1 | 43 | 0 | 1 | 7 | 14 | 16383 | 0 | yes |
| 1 | 43 | 1 | 3 | 7 | 14 | 16383 | 0 | yes |
| 1 | 43 | 2 | 7 | 7 | 14 | 16383 | 0 | yes |
| 1 | 45 | 0 | 1 | 5 | 12 | 4095 | 0 | yes |
| 1 | 45 | 3 | 7 | 7 | 12 | 4095 | 0 | yes |
| 1 | 47 | 0 | 1 | 9 | 23 | 8388607 | 0 | yes |
| 1 | 47 | 1 | 5 | 14 | 23 | 8388607 | 0 | yes |
| 1 | 49 | 0 | 1 | 10 | 21 | 2097151 | 0 | yes |
| 1 | 49 | 1 | 3 | 11 | 21 | 2097151 | 0 | yes |
| 1 | 51 | 0 | 1 | 2 | 8 | 255 | 0 | yes |
| 1 | 51 | 2 | 5 | 3 | 8 | 255 | 0 | yes |
| 1 | 51 | 4 | 11 | 5 | 8 | 255 | 0 | yes |
| 1 | 51 | 6 | 19 | 6 | 8 | 255 | 0 | yes |
| 3 | 23 | 0 | 41 | 26 | 43 | 6254227193879 | 0 | yes |
| 3 | 23 | 1 | 5 | 2 | 5 | 23 | 0 | yes |
| 3 | 23 | 2 | 7 | 2 | 5 | 23 | 0 | yes |
| 3 | 25 | 0 | 7 | 8 | 16 | 58975 | 0 | yes |
| 3 | 25 | 1 | 17 | 4 | 8 | 175 | 0 | yes |
| 3 | 29 | 0 | 1 | 1 | 5 | 29 | 0 | yes |
| 3 | 29 | 1 | 11 | 9 | 17 | 111389 | 0 | yes |
| 3 | 29 | 3 | 3811 | 41 | 65 | 420491770248316829 | 0 | yes |
| 3 | 29 | 4 | 7055 | 41 | 65 | 420491770248316829 | 0 | yes |
| 3 | 31 | 0 | 13 | 12 | 23 | 7857167 | 0 | yes |
| 3 | 35 | 0 | 13 | 4 | 8 | 175 | 0 | yes |
| 3 | 35 | 1 | 17 | 4 | 8 | 175 | 0 | yes |
| 3 | 37 | 0 | 19 | 3 | 6 | 37 | 0 | yes |
| 3 | 37 | 1 | 23 | 3 | 6 | 37 | 0 | yes |
| 3 | 37 | 2 | 29 | 3 | 6 | 37 | 0 | yes |
| 3 | 41 | 0 | 1 | 8 | 20 | 1042015 | 0 | yes |
| 3 | 43 | 0 | 1 | 3 | 11 | 2021 | 0 | yes |
| 3 | 47 | 0 | 25 | 16 | 28 | 225388735 | 0 | yes |
| 3 | 47 | 1 | 5 | 7 | 18 | 259957 | 0 | yes |
| 3 | 47 | 2 | 65 | 4 | 7 | 47 | 0 | yes |
| 3 | 47 | 3 | 89 | 4 | 7 | 47 | 0 | yes |
| 3 | 47 | 4 | 73 | 4 | 7 | 47 | 0 | yes |
| 3 | 47 | 5 | 85 | 4 | 7 | 47 | 0 | yes |
| 3 | 47 | 7 | 101 | 4 | 7 | 47 | 0 | yes |
| 3 | 49 | 0 | 25 | 22 | 38 | 243496847335 | 0 | yes |
| 5 | 23 | 0 | 1 | 4 | 13 | 7567 | 0 | yes |
| 5 | 23 | 1 | 179 | 6 | 14 | 759 | 0 | yes |
| 5 | 23 | 3 | 81 | 24 | 56 | 12452949262537311 | 0 | yes |
| 5 | 23 | 5 | 187 | 6 | 14 | 759 | 0 | yes |
| 5 | 23 | 6 | 191 | 12 | 28 | 24294831 | 0 | yes |
| 5 | 23 | 7 | 231 | 6 | 14 | 759 | 0 | yes |
| 5 | 23 | 8 | 351 | 6 | 14 | 759 | 0 | yes |
| 5 | 23 | 9 | 361 | 6 | 14 | 759 | 0 | yes |
| 5 | 27 | 0 | 1 | 1 | 5 | 27 | 0 | yes |
| 5 | 31 | 1 | 91 | 15 | 35 | 3842160243 | 0 | yes |
| 5 | 33 | 0 | 1 | 2 | 8 | 231 | 0 | yes |
| 5 | 33 | 4 | 359 | 6 | 14 | 759 | 0 | yes |
| 5 | 33 | 5 | 329 | 6 | 14 | 759 | 0 | yes |
| 5 | 33 | 7 | 181 | 12 | 28 | 24294831 | 0 | yes |
| 5 | 33 | 8 | 479 | 6 | 14 | 759 | 0 | yes |
| 5 | 33 | 10 | 337 | 6 | 14 | 759 | 0 | yes |
| 5 | 33 | 11 | 293 | 6 | 14 | 759 | 0 | yes |
| 5 | 33 | 12 | 421 | 6 | 14 | 759 | 0 | yes |
| 5 | 33 | 14 | 511 | 6 | 14 | 759 | 0 | yes |
| 5 | 37 | 0 | 7 | 28 | 68 | 257895002194733685231 | 0 | yes |
| 5 | 37 | 2 | 109 | 101 | 235 | 15770925513273920028891618634076892135948550021911942202786247257191243 | 0 | yes |
| 5 | 39 | 0 | 203 | 9 | 21 | 144027 | 0 | yes |
| 5 | 39 | 2 | 7 | 2 | 6 | 39 | 0 | yes |
| 5 | 39 | 6 | 179 | 9 | 21 | 144027 | 0 | yes |
| 5 | 39 | 8 | 271 | 9 | 21 | 144027 | 0 | yes |
| 5 | 39 | 9 | 223 | 9 | 21 | 144027 | 0 | yes |
| 5 | 39 | 10 | 323 | 9 | 21 | 144027 | 0 | yes |
| 5 | 39 | 11 | 473 | 9 | 21 | 144027 | 0 | yes |
| 5 | 41 | 0 | 21 | 9 | 23 | 6435483 | 0 | yes |
| 5 | 43 | 0 | 9 | 3 | 9 | 387 | 0 | yes |
| 5 | 43 | 2 | 151 | 21 | 49 | 86112795218187 | 0 | yes |
| 5 | 49 | 0 | 1 | 12 | 36 | 68475336111 | 0 | yes |
| 7 | 23 | 0 | 1 | 2 | 8 | 207 | 0 | yes |
| 7 | 25 | 0 | 1 | 1 | 5 | 25 | 0 | yes |
| 7 | 31 | 0 | 129 | 6 | 17 | 13423 | 0 | yes |
| 7 | 31 | 1 | 89 | 6 | 17 | 13423 | 0 | yes |
| 7 | 31 | 3 | 101 | 6 | 17 | 13423 | 0 | yes |
| 7 | 31 | 4 | 73 | 6 | 17 | 13423 | 0 | yes |

**Match rate: 96/96 (100.0%).**

## New `new`-cycle inventory

- **Total `new` cycles in the wider-b sweep: 96**

- **(a=1, b=23)** — 2 new cycle(s):
    - cycle_id=0 | min=1 | L=4 | K=11 | t_period=15 | seeds=47828 | members={1, 2, 3, 4, 6, 8, 9, 12, ... (15 total)}
    - cycle_id=1 | min=5 | L=7 | K=11 | t_period=18 | seeds=47825 | members={5, 7, 10, 11, 14, 15, 17, 19, ... (18 total)}
- **(a=1, b=25)** — 1 new cycle(s):
    - cycle_id=0 | min=1 | L=10 | K=20 | t_period=30 | seeds=80000 | members={1, 2, 3, 4, 6, 7, 8, 9, ... (30 total)}
- **(a=1, b=27)** — 1 new cycle(s):
    - cycle_id=0 | min=1 | L=9 | K=18 | t_period=27 | seeds=66667 | members={1, 2, 4, 5, 7, 8, 10, 11, ... (27 total)}
- **(a=1, b=29)** — 1 new cycle(s):
    - cycle_id=0 | min=1 | L=14 | K=28 | t_period=42 | seeds=96552 | members={1, 2, 3, 4, 5, 6, 7, 8, ... (42 total)}
- **(a=1, b=31)** — 6 new cycle(s):
    - cycle_id=0 | min=1 | L=1 | K=5 | t_period=6 | seeds=16130 | members={1, 2, 4, 8, 16, 32}
    - cycle_id=1 | min=3 | L=2 | K=5 | t_period=7 | seeds=16130 | members={3, 6, 12, 17, 24, 34, 48}
    - cycle_id=2 | min=5 | L=2 | K=5 | t_period=7 | seeds=16130 | members={5, 9, 10, 18, 20, 36, 40}
    - cycle_id=3 | min=7 | L=3 | K=5 | t_period=8 | seeds=16129 | members={7, 14, 19, 25, 28, 38, 50, 56}
    - cycle_id=4 | min=11 | L=3 | K=5 | t_period=8 | seeds=16129 | members={11, 13, 21, 22, 26, 42, 44, 52}
    - cycle_id=5 | min=15 | L=4 | K=5 | t_period=9 | seeds=16127 | members={15, 23, 27, 29, 30, 46, 54, 58, ... (9 total)}
- **(a=1, b=33)** — 2 new cycle(s):
    - cycle_id=0 | min=1 | L=5 | K=10 | t_period=15 | seeds=30304 | members={1, 2, 4, 8, 16, 17, 25, 29, ... (15 total)}
    - cycle_id=2 | min=5 | L=5 | K=10 | t_period=15 | seeds=30303 | members={5, 7, 10, 13, 14, 19, 20, 23, ... (15 total)}
- **(a=1, b=35)** — 2 new cycle(s):
    - cycle_id=0 | min=1 | L=5 | K=12 | t_period=17 | seeds=34287 | members={1, 2, 4, 8, 9, 11, 16, 18, ... (17 total)}
    - cycle_id=1 | min=3 | L=7 | K=12 | t_period=19 | seeds=34285 | members={3, 6, 12, 13, 17, 19, 24, 26, ... (19 total)}
- **(a=1, b=37)** — 1 new cycle(s):
    - cycle_id=0 | min=1 | L=18 | K=36 | t_period=54 | seeds=97298 | members={1, 2, 3, 4, 5, 6, 7, 8, ... (54 total)}
- **(a=1, b=39)** — 2 new cycle(s):
    - cycle_id=0 | min=1 | L=4 | K=12 | t_period=16 | seeds=30771 | members={1, 2, 4, 5, 8, 10, 11, 16, ... (16 total)}
    - cycle_id=2 | min=7 | L=8 | K=12 | t_period=20 | seeds=30768 | members={7, 14, 17, 19, 23, 28, 29, 31, ... (20 total)}
- **(a=1, b=41)** — 2 new cycle(s):
    - cycle_id=0 | min=1 | L=10 | K=20 | t_period=30 | seeds=48781 | members={1, 2, 4, 5, 8, 9, 10, 16, ... (30 total)}
    - cycle_id=1 | min=3 | L=10 | K=20 | t_period=30 | seeds=48780 | members={3, 6, 7, 11, 12, 13, 14, 15, ... (30 total)}
- **(a=1, b=43)** — 3 new cycle(s):
    - cycle_id=0 | min=1 | L=7 | K=14 | t_period=21 | seeds=32558 | members={1, 2, 4, 8, 11, 16, 21, 22, ... (21 total)}
    - cycle_id=1 | min=3 | L=7 | K=14 | t_period=21 | seeds=32559 | members={3, 5, 6, 10, 12, 19, 20, 23, ... (21 total)}
    - cycle_id=2 | min=7 | L=7 | K=14 | t_period=21 | seeds=32558 | members={7, 9, 13, 14, 15, 17, 18, 25, ... (21 total)}
- **(a=1, b=45)** — 2 new cycle(s):
    - cycle_id=0 | min=1 | L=5 | K=12 | t_period=17 | seeds=26668 | members={1, 2, 4, 8, 16, 17, 19, 23, ... (17 total)}
    - cycle_id=3 | min=7 | L=7 | K=12 | t_period=19 | seeds=26665 | members={7, 11, 13, 14, 22, 26, 28, 29, ... (19 total)}
- **(a=1, b=47)** — 2 new cycle(s):
    - cycle_id=0 | min=1 | L=9 | K=23 | t_period=32 | seeds=48939 | members={1, 2, 3, 4, 6, 7, 8, 9, ... (32 total)}
    - cycle_id=1 | min=5 | L=14 | K=23 | t_period=37 | seeds=48934 | members={5, 10, 11, 13, 15, 19, 20, 22, ... (37 total)}
- **(a=1, b=49)** — 2 new cycle(s):
    - cycle_id=0 | min=1 | L=10 | K=21 | t_period=31 | seeds=42858 | members={1, 2, 4, 8, 9, 11, 15, 16, ... (31 total)}
    - cycle_id=1 | min=3 | L=11 | K=21 | t_period=32 | seeds=42857 | members={3, 5, 6, 10, 12, 13, 17, 19, ... (32 total)}
- **(a=1, b=51)** — 4 new cycle(s):
    - cycle_id=0 | min=1 | L=2 | K=8 | t_period=10 | seeds=15688 | members={1, 2, 4, 8, 13, 16, 26, 32, ... (10 total)}
    - cycle_id=2 | min=5 | L=3 | K=8 | t_period=11 | seeds=15688 | members={5, 7, 10, 14, 20, 28, 29, 40, ... (11 total)}
    - cycle_id=4 | min=11 | L=5 | K=8 | t_period=13 | seeds=15685 | members={11, 22, 23, 31, 37, 41, 44, 46, ... (13 total)}
    - cycle_id=6 | min=19 | L=6 | K=8 | t_period=14 | seeds=15684 | members={19, 25, 35, 38, 43, 47, 49, 50, ... (14 total)}
- **(a=3, b=23)** — 3 new cycle(s):
    - cycle_id=0 | min=41 | L=26 | K=43 | t_period=69 | seeds=47828 | members={41, 47, 49, 55, 73, 82, 85, 94, ... (69 total)}
    - cycle_id=1 | min=5 | L=2 | K=5 | t_period=7 | seeds=6370 | members={5, 10, 19, 20, 38, 40, 80}
    - cycle_id=2 | min=7 | L=2 | K=5 | t_period=7 | seeds=41455 | members={7, 11, 14, 22, 28, 44, 56}
- **(a=3, b=25)** — 2 new cycle(s):
    - cycle_id=0 | min=7 | L=8 | K=16 | t_period=24 | seeds=42532 | members={7, 11, 14, 22, 23, 28, 29, 44, ... (24 total)}
    - cycle_id=1 | min=17 | L=4 | K=8 | t_period=12 | seeds=37468 | members={17, 19, 34, 37, 38, 41, 68, 74, ... (12 total)}
- **(a=3, b=29)** — 4 new cycle(s):
    - cycle_id=0 | min=1 | L=1 | K=5 | t_period=6 | seeds=7914 | members={1, 2, 4, 8, 16, 32}
    - cycle_id=1 | min=11 | L=9 | K=17 | t_period=26 | seeds=87985 | members={11, 22, 31, 44, 47, 49, 53, 61, ... (26 total)}
    - cycle_id=3 | min=3811 | L=41 | K=65 | t_period=106 | seeds=360 | members={3811, 5731, 7622, 8611, 10153, 11462, 12931, 15244, ... (106 total)}
    - cycle_id=4 | min=7055 | L=41 | K=65 | t_period=106 | seeds=293 | members={7055, 7955, 9397, 10597, 11947, 14110, 15910, 17935, ... (106 total)}
- **(a=3, b=31)** — 1 new cycle(s):
    - cycle_id=0 | min=13 | L=12 | K=23 | t_period=35 | seeds=96775 | members={13, 17, 26, 29, 34, 35, 41, 52, ... (35 total)}
- **(a=3, b=35)** — 2 new cycle(s):
    - cycle_id=0 | min=13 | L=4 | K=8 | t_period=12 | seeds=17613 | members={13, 26, 37, 52, 73, 74, 104, 127, ... (12 total)}
    - cycle_id=1 | min=17 | L=4 | K=8 | t_period=12 | seeds=50959 | members={17, 34, 41, 43, 68, 79, 82, 86, ... (12 total)}
- **(a=3, b=37)** — 3 new cycle(s):
    - cycle_id=0 | min=19 | L=3 | K=6 | t_period=9 | seeds=47778 | members={19, 38, 47, 76, 89, 94, 152, 178, ... (9 total)}
    - cycle_id=1 | min=23 | L=3 | K=6 | t_period=9 | seeds=23664 | members={23, 46, 49, 53, 92, 98, 106, 184, ... (9 total)}
    - cycle_id=2 | min=29 | L=3 | K=6 | t_period=9 | seeds=25856 | members={29, 31, 58, 62, 65, 116, 124, 130, ... (9 total)}
- **(a=3, b=41)** — 1 new cycle(s):
    - cycle_id=0 | min=1 | L=8 | K=20 | t_period=28 | seeds=97561 | members={1, 2, 4, 8, 11, 16, 19, 22, ... (28 total)}
- **(a=3, b=43)** — 1 new cycle(s):
    - cycle_id=0 | min=1 | L=3 | K=11 | t_period=14 | seeds=97675 | members={1, 2, 4, 7, 8, 14, 16, 23, ... (14 total)}
- **(a=3, b=47)** — 7 new cycle(s):
    - cycle_id=0 | min=25 | L=16 | K=28 | t_period=44 | seeds=26038 | members={25, 49, 50, 61, 97, 98, 100, 115, ... (44 total)}
    - cycle_id=1 | min=5 | L=7 | K=18 | t_period=25 | seeds=39050 | members={5, 10, 11, 13, 19, 20, 22, 26, ... (25 total)}
    - cycle_id=2 | min=65 | L=4 | K=7 | t_period=11 | seeds=13394 | members={65, 121, 130, 205, 242, 260, 331, 410, ... (11 total)}
    - cycle_id=3 | min=89 | L=4 | K=7 | t_period=11 | seeds=6138 | members={89, 103, 157, 178, 206, 259, 314, 356, ... (11 total)}
    - cycle_id=4 | min=73 | L=4 | K=7 | t_period=11 | seeds=5973 | members={73, 133, 146, 179, 223, 266, 292, 358, ... (11 total)}
    - cycle_id=5 | min=85 | L=4 | K=7 | t_period=11 | seeds=3911 | members={85, 125, 151, 170, 211, 250, 302, 340, ... (11 total)}
    - cycle_id=7 | min=101 | L=4 | K=7 | t_period=11 | seeds=3369 | members={101, 119, 143, 175, 202, 238, 286, 350, ... (11 total)}
- **(a=3, b=49)** — 1 new cycle(s):
    - cycle_id=0 | min=25 | L=22 | K=38 | t_period=60 | seeds=85715 | members={25, 31, 50, 62, 71, 79, 89, 100, ... (60 total)}
- **(a=5, b=23)** — 8 new cycle(s):
    - cycle_id=0 | min=1 | L=4 | K=13 | t_period=17 | seeds=1837 | members={1, 2, 4, 7, 8, 14, 16, 21, ... (17 total)}
    - cycle_id=1 | min=179 | L=6 | K=14 | t_period=20 | seeds=1691 | members={179, 358, 459, 716, 918, 1141, 1159, 1432, ... (20 total)}
    - cycle_id=3 | min=81 | L=24 | K=56 | t_period=80 | seeds=995 | members={81, 107, 162, 214, 223, 279, 324, 428, ... (80 total)}
    - cycle_id=5 | min=187 | L=6 | K=14 | t_period=20 | seeds=186 | members={187, 374, 479, 748, 951, 958, 1209, 1496, ... (20 total)}
    - cycle_id=6 | min=191 | L=12 | K=28 | t_period=40 | seeds=688 | members={191, 301, 377, 382, 477, 489, 602, 617, ... (40 total)}
    - cycle_id=7 | min=231 | L=6 | K=14 | t_period=20 | seeds=131 | members={231, 371, 462, 589, 742, 924, 939, 1178, ... (20 total)}
    - cycle_id=8 | min=351 | L=6 | K=14 | t_period=20 | seeds=174 | members={351, 441, 557, 701, 702, 882, 889, 1114, ... (20 total)}
    - cycle_id=9 | min=361 | L=6 | K=14 | t_period=20 | seeds=135 | members={361, 457, 573, 577, 722, 727, 914, 1146, ... (20 total)}
- **(a=5, b=27)** — 1 new cycle(s):
    - cycle_id=0 | min=1 | L=1 | K=5 | t_period=6 | seeds=302 | members={1, 2, 4, 8, 16, 32}
- **(a=5, b=31)** — 1 new cycle(s):
    - cycle_id=1 | min=91 | L=15 | K=35 | t_period=50 | seeds=508 | members={91, 182, 243, 364, 486, 623, 728, 987, ... (50 total)}
- **(a=5, b=33)** — 9 new cycle(s):
    - cycle_id=0 | min=1 | L=2 | K=8 | t_period=10 | seeds=438 | members={1, 2, 4, 8, 16, 19, 32, 38, ... (10 total)}
    - cycle_id=4 | min=359 | L=6 | K=14 | t_period=20 | seeds=811 | members={359, 457, 718, 914, 1159, 1436, 1457, 1828, ... (20 total)}
    - cycle_id=5 | min=329 | L=6 | K=14 | t_period=20 | seeds=150 | members={329, 658, 833, 839, 1057, 1316, 1666, 1678, ... (20 total)}
    - cycle_id=7 | min=181 | L=12 | K=28 | t_period=40 | seeds=320 | members={181, 283, 362, 469, 566, 724, 899, 938, ... (40 total)}
    - cycle_id=8 | min=479 | L=6 | K=14 | t_period=20 | seeds=301 | members={479, 607, 767, 958, 967, 1214, 1217, 1534, ... (20 total)}
    - cycle_id=10 | min=337 | L=6 | K=14 | t_period=20 | seeds=179 | members={337, 541, 674, 859, 1082, 1348, 1369, 1718, ... (20 total)}
    - cycle_id=11 | min=293 | L=6 | K=14 | t_period=20 | seeds=236 | members={293, 586, 749, 931, 1172, 1483, 1498, 1862, ... (20 total)}
    - cycle_id=12 | min=421 | L=6 | K=14 | t_period=20 | seeds=85 | members={421, 527, 667, 842, 1054, 1069, 1334, 1684, ... (20 total)}
    - cycle_id=14 | min=511 | L=6 | K=14 | t_period=20 | seeds=209 | members={511, 647, 811, 817, 1022, 1291, 1294, 1622, ... (20 total)}
- **(a=5, b=37)** — 2 new cycle(s):
    - cycle_id=0 | min=7 | L=28 | K=68 | t_period=96 | seeds=4872 | members={7, 9, 14, 18, 28, 36, 41, 53, ... (96 total)}
    - cycle_id=2 | min=109 | L=101 | K=235 | t_period=336 | seeds=777 | members={109, 167, 218, 291, 309, 334, 373, 379, ... (336 total)}
- **(a=5, b=39)** — 7 new cycle(s):
    - cycle_id=0 | min=203 | L=9 | K=21 | t_period=30 | seeds=3370 | members={203, 406, 527, 812, 1054, 1337, 1624, 1681, ... (30 total)}
    - cycle_id=2 | min=7 | L=2 | K=6 | t_period=8 | seeds=354 | members={7, 14, 28, 37, 56, 74, 112, 224}
    - cycle_id=6 | min=179 | L=9 | K=21 | t_period=30 | seeds=263 | members={179, 358, 467, 716, 934, 1187, 1432, 2374, ... (30 total)}
    - cycle_id=8 | min=271 | L=9 | K=21 | t_period=30 | seeds=561 | members={271, 542, 697, 881, 1084, 1111, 1394, 1753, ... (30 total)}
    - cycle_id=9 | min=223 | L=9 | K=21 | t_period=30 | seeds=200 | members={223, 446, 577, 731, 892, 1154, 1462, 1784, ... (30 total)}
    - cycle_id=10 | min=323 | L=9 | K=21 | t_period=30 | seeds=386 | members={323, 509, 646, 827, 1018, 1289, 1292, 1621, ... (30 total)}
    - cycle_id=11 | min=473 | L=9 | K=21 | t_period=30 | seeds=207 | members={473, 601, 749, 761, 946, 961, 1202, 1211, ... (30 total)}
- **(a=5, b=41)** — 1 new cycle(s):
    - cycle_id=0 | min=21 | L=9 | K=23 | t_period=32 | seeds=3282 | members={21, 23, 33, 39, 42, 46, 59, 66, ... (32 total)}
- **(a=5, b=43)** — 2 new cycle(s):
    - cycle_id=0 | min=9 | L=3 | K=9 | t_period=12 | seeds=549 | members={9, 11, 18, 22, 36, 44, 49, 72, ... (12 total)}
    - cycle_id=2 | min=151 | L=21 | K=49 | t_period=70 | seeds=603 | members={151, 302, 317, 399, 407, 604, 634, 798, ... (70 total)}
- **(a=5, b=49)** — 1 new cycle(s):
    - cycle_id=0 | min=1 | L=12 | K=36 | t_period=48 | seeds=2817 | members={1, 2, 3, 4, 6, 8, 12, 16, ... (48 total)}
- **(a=7, b=23)** — 1 new cycle(s):
    - cycle_id=0 | min=1 | L=2 | K=8 | t_period=10 | seeds=97 | members={1, 2, 4, 8, 15, 16, 30, 32, ... (10 total)}
- **(a=7, b=25)** — 1 new cycle(s):
    - cycle_id=0 | min=1 | L=1 | K=5 | t_period=6 | seeds=162 | members={1, 2, 4, 8, 16, 32}
- **(a=7, b=31)** — 4 new cycle(s):
    - cycle_id=0 | min=129 | L=6 | K=17 | t_period=23 | seeds=391 | members={129, 143, 159, 258, 286, 318, 467, 516, ... (23 total)}
    - cycle_id=1 | min=89 | L=6 | K=17 | t_period=23 | seeds=244 | members={89, 145, 178, 290, 327, 356, 523, 580, ... (23 total)}
    - cycle_id=3 | min=101 | L=6 | K=17 | t_period=23 | seeds=390 | members={101, 111, 202, 222, 369, 404, 444, 503, ... (23 total)}
    - cycle_id=4 | min=73 | L=6 | K=17 | t_period=23 | seeds=252 | members={73, 146, 241, 271, 292, 482, 542, 584, ... (23 total)}

## Anomalies

- (a=5, b=33): 18 distinct cycles (median for a=5 across new range: 6)
- (a=7, b=31): 5 distinct cycles (median for a=7 across new range: 1)
- (a=7, b=45): 5 distinct cycles (median for a=7 across new range: 1)
- (a=5, b=23): 93739 seeds exceeded H, 0 exceeded T
- (a=5, b=25): 89903 seeds exceeded H, 0 exceeded T
- (a=5, b=27): 93720 seeds exceeded H, 0 exceeded T
- (a=5, b=29): 99632 seeds exceeded H, 0 exceeded T
- (a=5, b=31): 99141 seeds exceeded H, 0 exceeded T
- (a=5, b=33): 94313 seeds exceeded H, 0 exceeded T
- (a=5, b=35): 83412 seeds exceeded H, 0 exceeded T
- (a=5, b=37): 94037 seeds exceeded H, 0 exceeded T
- (a=5, b=39): 91055 seeds exceeded H, 0 exceeded T
- (a=5, b=41): 96425 seeds exceeded H, 0 exceeded T
- (a=5, b=43): 98562 seeds exceeded H, 0 exceeded T
- (a=5, b=45): 79460 seeds exceeded H, 0 exceeded T
- (a=5, b=47): 99735 seeds exceeded H, 0 exceeded T
- (a=5, b=49): 94504 seeds exceeded H, 0 exceeded T
- (a=5, b=51): 98547 seeds exceeded H, 0 exceeded T
- (a=7, b=23): 99839 seeds exceeded H, 0 exceeded T
- (a=7, b=25): 99189 seeds exceeded H, 0 exceeded T
- (a=7, b=27): 99889 seeds exceeded H, 0 exceeded T
- (a=7, b=29): 99938 seeds exceeded H, 0 exceeded T
- (a=7, b=31): 98662 seeds exceeded H, 0 exceeded T
- (a=7, b=33): 99492 seeds exceeded H, 0 exceeded T
- (a=7, b=35): 96461 seeds exceeded H, 0 exceeded T
- (a=7, b=37): 99940 seeds exceeded H, 0 exceeded T
- (a=7, b=39): 99945 seeds exceeded H, 0 exceeded T
- (a=7, b=41): 99946 seeds exceeded H, 0 exceeded T
- (a=7, b=43): 99948 seeds exceeded H, 0 exceeded T
- (a=7, b=45): 99086 seeds exceeded H, 0 exceeded T
- (a=7, b=47): 99949 seeds exceeded H, 0 exceeded T
- (a=7, b=49): 97732 seeds exceeded H, 0 exceeded T
- (a=7, b=51): 99951 seeds exceeded H, 0 exceeded T

## Runtime

- Total wall-clock: **22.4s**
- Sweep: **16.6s**
- Parquet + summary: 5.81s
- Per-variant timings (top 10 slowest):
    - (a=5, b=23): 0.55s
    - (a=5, b=51): 0.54s
    - (a=5, b=49): 0.54s
    - (a=5, b=37): 0.53s
    - (a=5, b=47): 0.53s
    - (a=5, b=43): 0.51s
    - (a=5, b=41): 0.51s
    - (a=5, b=39): 0.50s
    - (a=5, b=31): 0.50s
    - (a=7, b=37): 0.49s
