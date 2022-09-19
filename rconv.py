MAXBASE=36

import sys
r1=0
dmax=0
r2=0
n=0
zLen=0
fracLim=10

# converts the string in radix-r1 to its value
def r1ToValue(digits):
    exp=zLen-1
    value=0

    # multiply each digit by r^(digit position)
    # digit positions are as follows for n integer digits and m fractional digits
    # n-1 n-2 ... 3 2 1 0 . -1 -2 -3 ... -(m-1) -m
    # the sum of all converted digits is the value
    for d in digits:
        # make sure all digits are inside the specified radix
        if(d > dmax):
            print("error, the entered number has a digit > radix-r")
            sys.exit()
        v = d * (r1**(exp))
        value += v
        exp-=1
    return value

# recursively calculate the integer digits, then add them 
# calculated in big endian, appended in little endian so digits are appended backwards on return
def intToR2(z, digs):
    if(z < 1):
        return
    intToR2(int(z / r2), digs)
    digs.append(z % r2)


# recursively calculate the fractional digits, then add them 
def fracToR2(f,digs):
    if f == 0:
        return
    if len(digs) > fracLim:
        print("more floating point digits exist")
        return
    digs.append(int(f * r2))
    fracToR2((f * r2) % 1, digs)

# converts number value to string in radix-r2 
def valueToR2(value):
    nz=[]
    nf=["."]
    # separate integer and fractions
    z=int(value)
    f=value % 1
    # calculate them separately (different functions)
    intToR2(z,nz)
    fracToR2(f,nf)
    # append to each other
    num=nz
    num += nf
    return num

# changes number string to a list of digits
def chrToDigs(str):
    l = list(str)
    i=0
    for e in l:
        # converts ascii numbers to decimal numbers
        l[i]=ord(e)-48
        # converts uppercase letters to decimal
        if(l[i] > 10):
            l[i] -= 7
        # if lowercase letter, 
        if(l[i]>40):
            l[i]-=32
        i+=1
    return l

# changes list of digits to number string
def digsToChr(l):
    i=0
    str = ""
    for e in l:
        if e == '.':
            str+=e
            continue
        # converts to ascii digit
        if e < 10:
            str+=chr(e+48)
            continue
        # converts to uppercase letter
        str+=chr(e+55)
    return str

# check 
def helpFlag():
    try:
        if sys.argv[0] == "--h": return True
    except:
        return False

# check for enough args or help flag
def preChecks(argsl):
    if (argsl != 4 and argsl != 5 or helpFlag()):
        print("\nenter 'rconv.py r1 r2 N [f]'")
        print("converts the number N from base r1 to base r2, with f floating points (default 10)")
        print("\nreccommended maximum radix of 36 (10 digits + 26 letters)")
        print("larger bases can be acheived by changing MAXBASE in line 1")
        print("if increased, format is printed as a list of DECIMAL digits")
        print("eg. 2FA in R-16 is [2, 15, 10]")
        print("ex. 1011.0100 in R-2 to R-16 is printed as B.4 or [11, \".\", 4] if MAXBASE > 36")
        sys.exit()

if __name__=="__main__" :
    argsl = len(sys.argv)
    preChecks(argsl)

    # assign params
    r1=int(sys.argv[1])
    dmax=r1-1
    r2=int(sys.argv[2])
    n=sys.argv[3]

    # change max fractions length, and check for maximum base allowed
    if argsl > 4:
        fracLim = int(sys.argv[4])
    if(r1 > MAXBASE or r2 > MAXBASE):
        print("36 is the maximum radix allowed")
        print("larger bases can be acheived by changing MAXBASE in line 1")
        sys.exit()

    # convert string to list
    n=list(n)

    # remove the radix point; note the number of digits for the integers
    try:
        zLen = n.index('.')
        n.remove('.')
    except:
        zLen=len(n)

    # converts the individual digits into decimal representations for calculation
    n = chrToDigs(n)
    # convert from string in radix-r1 to value
    n = r1ToValue(n)
    # convert from value to radix-r2
    res = valueToR2(n)
    if MAXBASE > 36:
        print(res)
        sys.exit()
    print(digsToChr(res))
    
