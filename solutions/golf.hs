x=zipWith
y=isSpace
t=True
f a=not.((||)$y a).y
i a b
 |y a=b
 |t=a
s a=a++repeat ' '
d[a,b]=x i(s a)b
h l@[a,b]
 |or$x f a b=h[" "++a,b]
 |t=d$m l
m=sortBy(comparing length)
g=h.m

-- very sad... the above code is a valid solution...
-- if and only if the input to g is length 2
-- lol
-- should have read the question better
