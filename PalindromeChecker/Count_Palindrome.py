L,R=map(int,input().split())
def is_palindrome():
    count=0
    for i in range(L,R+1):
        N=i
        ans=0
        while N>0:
            ans=(ans*10)+N%10
            N//=10
        if ans==i:
            count+=1
    print(count)
is_palindrome()
            
