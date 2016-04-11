from __future__ import division

def str_dist(s1, s2):
    if len(s1) > 100 or len(s2) > 100:
        if s1 != s2:
            return 2.0
        else:
            return 0

    d = dist1(s1, s2)
    ret = (1.0-d)*2
    return ret


# the main dynamic programming part
# similar to the structure of diff_list
def dist1(s1, s2):
    if s1 == s2:
        return 1.0
    if s1 == "" or s2 == "":
        return 0
    s = set()
    for i in range(len(s1)-1):
        s.add(s1[i:i+2])
    count = 0
    for j in range(len(s2)-1):
        if s2[j:j+2] in s:
            count += 1

    return (2 * count) / (len(s1)+len(s2)-2)


a = "verticalDrawAction"
b = "drawVerticalAction"
print str_dist(a, b)
