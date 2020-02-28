print("-" * 140)
print("Address" + 6*' ' + "| Value(+0)" + 5*' ' + "| Value(+4)" + 5*' ' + "| Value(+8)" + 5*' ' + "| Value(+c)" + 5*' ' + "| Value(+10)" + 4*' '+ "| Value(+14)" + 4*' ' + "| Value(+18)" + 4*' ' + "| Value(+1c)" + 2*' ' + '|' )
print("-" * 140)

m = 2000
n = []

for num in range(0, 648):
    n.append(0)
j, z, s = (0, 0, 0)

for i in range(0, 80):
    t = hex(s)
    h = str(t)
    f = h[2:]
    p = f.zfill(3)
    mem = "0x00002" + str(h) + ' ' * 3 + '|'
    print(f"{mem}            {n[j]}  |            {n[j+1]}  |            {n[j+2]}  |            {n[j+3]}  |            {n[j+4]}  |            {n[j+5]}  |            {n[j+6]}  |          {n[j+7]}  |")
    print("-" * 140)
    s = s + 32
    j = j + 8







