def secant_method(g, x0, x1, epsilon):
    #secant method
    # g, x0, x1, epsilon input parameters for funciton
    #return the root of g
    
    while True:
        #g of x not and x one 
        g0 = g(x0) 
        g1 = g(x1)
        #calculate using the secant method 
        x = x1 -(g1)*(x1-x0)/(g1-g0)

        #from the given stopping criteria 
        if abs(x - x1) < (abs(x1) * epsilon):
            #stop and return value
            return x

        #assign new values
        x0 = x1
        x1 = x

#function g(x)
def g(x):
    #simply return given function
    return (2*x - 1)**2 + 4*(4 - 1024*x)**4
    


x0 = 0          
x1 = 1          
epsilon = 1e-5  
sMethod = secant_method(g, x0, x1, epsilon)


print("Root g(x): ",sMethod)
print("Value of g at solution : " , g(sMethod))