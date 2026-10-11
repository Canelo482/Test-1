# Python Test Study Guide
Covers Unit 3 (Basic Python & Console), Unit 5 (Conditionals), Unit 7 (Looping)

---

## Unit 3: Basic Python and Console Interaction

### 3.1 Printing
```python
print("Hello")             # Hello
print("A", "B", 3)         # A B 3   (commas add a space)
print("A", "B", sep="-")   # A-B
print("Hi", end="")        # no new line after
```

### 3.2 Variables and Types
| Type | Example | Meaning |
|------|---------|---------|
| `int` | `5` | whole number |
| `float` | `5.0`, `3.14` | decimal number |
| `str` | `"5"`, `'hi'` | text |
| `bool` | `True`, `False` | true/false |

- `type(5)` → `<class 'int'>`
- Converting: `int("7")` → 7, `float("2")` → 2.0, `str(10)` → "10", `int(3.9)` → 3 (cuts off, does NOT round)
- Variable names: letters, digits, `_`; can't start with a digit; case sensitive (`age` ≠ `Age`).

### 3.3 User Input
```python
name = input("Name: ")           # ALWAYS returns a string
age = int(input("Age: "))        # convert to do math
```
Classic mistake: `input("Num: ") + 1` → TypeError (str + int).

### 3.4 Mathematical Operators
| Op | Meaning | Example | Result |
|----|---------|---------|--------|
| `+ - *` | add, sub, mult | `3 * 4` | 12 |
| `/` | division (always float) | `7 / 2` | 3.5 |
| `//` | floor division | `7 // 2` | 3 |
| `%` | remainder (modulus) | `7 % 2` | 1 |
| `**` | exponent | `2 ** 3` | 8 |

Order of operations: `()` → `**` → `* / // %` → `+ -`
Shortcuts: `x += 1` means `x = x + 1` (also `-=`, `*=`, `/=`).
Tip: `n % 2 == 0` means n is even.

### 3.5 String Operators
```python
"ab" + "cd"     # "abcd"   concatenation
"ha" * 3        # "hahaha" repetition
len("hello")    # 5
s = "Python"
s[0]   # 'P'    s[-1]  # 'n'
s[0:3] # 'Pyt'  (end not included)
s.upper() # 'PYTHON'   s.lower() # 'python'
"Age: " + str(15)   # must convert numbers to str to concatenate
f"I am {15} years old"   # f-string
```

### 3.6 Comments
```python
# single-line comment, ignored by Python
"""multi-line string often used as a comment / docstring"""
```

### 3.7 Programming Languages
- **High-level** (Python, Java): human-readable. **Low-level** (machine code, assembly): close to hardware.
- **Interpreted** (Python): runs line by line. **Compiled** (C, C++): translated all at once before running.
- **Syntax error**: breaks grammar rules, won't run. **Runtime error**: crashes while running (e.g. divide by zero). **Logic error**: runs but gives wrong answer.

---

## Unit 5: Conditionals

### 5.1 Booleans
`True` and `False` (capital T/F). Type is `bool`.

### 5.2 If Statements
```python
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C or lower")
```
- Colon `:` at end, body must be indented.
- Only the FIRST true branch runs.

### 5.3 Comparison Operators
`==` equal, `!=` not equal, `<`, `>`, `<=`, `>=`
Don't confuse `=` (assign) with `==` (compare).
Strings compare too: `"apple" < "banana"` → True.

### 5.4 Logical Operators
| | Rule |
|--|--|
| `and` | True only if both are True |
| `or` | True if at least one is True |
| `not` | flips it |

Order: `not` → `and` → `or`.
`if 13 <= age <= 19:` works in Python (chained comparison).

### 5.5 Floating Point Numbers and Rounding
```python
0.1 + 0.2            # 0.30000000000000004  (floats aren't exact!)
0.1 + 0.2 == 0.3     # False
round(3.14159, 2)    # 3.14
round(2.5)           # 2   (Python rounds .5 to the nearest EVEN number)
round(3.5)           # 4
f"{3.14159:.2f}"     # '3.14'
abs(a - b) < 0.0001  # safe way to compare floats
```

---

## Unit 7: Looping

### 7.1 While Loops
Repeats as long as the condition is True.
```python
count = 1
while count <= 3:
    print(count)
    count += 1      # forget this → infinite loop!
# prints 1 2 3
```

### 7.2 For Loops
```python
for i in range(5):        # 0 1 2 3 4
for i in range(2, 6):     # 2 3 4 5
for i in range(0, 10, 2): # 0 2 4 6 8
for i in range(5, 0, -1): # 5 4 3 2 1
for ch in "hi":           # h, i
```
`range(start, stop, step)` — stop is NOT included.

### 7.3 Break and Continue
- `break` → exit the loop immediately.
- `continue` → skip the rest of this turn, go to the next one.
```python
for i in range(10):
    if i == 5:
        break
    if i % 2 == 0:
        continue
    print(i)
# prints 1 3
```

### 7.4 Nested Control Structures
```python
for row in range(3):
    for col in range(2):
        print(row, col)
# inner loop runs fully for every outer loop → 3 * 2 = 6 lines
```
```python
for i in range(1, 4):
    print("*" * i)
# *
# **
# ***
```

---

## Practice Questions (answers at bottom)

1. What does `print(17 // 5, 17 % 5)` print?
2. What is `type(7 / 7)`?
3. `x = input("Num: ")` and the user types 4. What does `print(x * 2)` show?
4. What does `"computer"[1:4]` give?
5. What prints?
   ```python
   a = 5
   if a > 3 and a < 5:
       print("X")
   elif a >= 5 or a == 0:
       print("Y")
   else:
       print("Z")
   ```
6. What is `not (True and False)`?
7. What is `round(4.567, 1)`?
8. How many times does this print "hi"? `for i in range(3, 10, 3): print("hi")`
9. What prints?
   ```python
   n = 10
   while n > 0:
       n -= 3
   print(n)
   ```
10. What prints?
    ```python
    total = 0
    for i in range(1, 6):
        if i == 4:
            continue
        total += i
    print(total)
    ```
11. Write a program that asks for a number and prints whether it is even or odd.
12. Write a loop that prints the numbers 10 down to 1, then "Liftoff!".
13. Is `print("Hello"` a syntax, runtime, or logic error?

### Answers
1. `3 2`
2. `float` (result is 1.0)
3. `44` (input is a string, so it repeats)
4. `'omp'`
5. `Y`
6. `True`
7. `4.6`
8. 3 times (i = 3, 6, 9)
9. `-2` (10 → 7 → 4 → 1 → -2)
10. `11` (1+2+3+5)
11. ```python
    num = int(input("Number: "))
    if num % 2 == 0:
        print("Even")
    else:
        print("Odd")
    ```
12. ```python
    for i in range(10, 0, -1):
        print(i)
    print("Liftoff!")
    ```
13. Syntax error (missing `)`)
