# Run

```
> python holdemup.py
```

Enter each hand on a new line, with a blank line to finish.

e.g.

```
Kc 9s Ks Kd 9d 3c 6d
9c Ah Ks Kd 9d 3c 6d
Ac Qc Ks Kd 9d 3c
9h 5s
4d 2d Ks Kd 9d 3c 6d
7s Ts Ks Kd 9d

```

After the blank line, the winning hand(s) will be calculated and the out produced. For example:

```
-------------
Kc Ks Kd 9s 9d 6d 3c Full House (winner)
Ks Kd 9c 9d Ah 6d 3c Two Pair
Ac Qc Ks Kd 9d 3c
9h 5s
Kd 9d 6d 4d 2d Ks 3c Flush
7s Ts Ks Kd 9d
```

Another set of hands can be entered after this. 

Crtl-Z to exit.


# Test

```
> python test_holdemup.py
```
