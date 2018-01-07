def checkbal(exp):
    stack = []
    for i in exp:
        if i == "(":
            stack.append(i)
        elif i=="{":
            stack.append(i)
        elif i=="}":
            if len(stack) == 0:
                return False
            else:
                temp = stack.pop()
                if temp != "{":
                    return False
        elif i==")":
            if len(stack) == 0:
                return False
            else:
                temp = stack.pop()
                if temp != "(":
                    return False
    if len(stack) !=0:
        return False
    return True
