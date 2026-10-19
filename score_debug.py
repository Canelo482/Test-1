score = 0

def local_score():
    score = 0
    score = score + 10
    print("Local score:", score)

def global_score():
    global score
    score = score + 1
    print("Global score:", score)

local_score()
local_score()
global_score()
global_score()
print("Final global score:", score)
