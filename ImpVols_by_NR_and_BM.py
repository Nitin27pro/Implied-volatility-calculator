import numpy as np 
import scipy.stats as si
import tkinter as tk
from tkinter import messagebox

# Black scholes model for call option
def Blackscholes_call_Option(S,K,T,r,sigma):
    d1=(-np.log(K)+np.log(S)+ (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2=(-np.log(K)+np.log(S)+ (r - 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    option_price=S*si.norm.cdf(d1) - K*np.exp(-r*T)*si.norm.cdf(d2)
    return option_price

# derivative of blackscholes model with respect to sigma as our task to find implied volatility
def derivative_blackcsholes_call_option(S,K,T,r,sigma):
    d1=(-np.log(K)+np.log(S)+ (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    derivative_option_price=S*si.norm.cdf(d1)*np.sqrt(T)
    return derivative_option_price

# Implementation of Newton-Raphsom method to find implied volatility
def Newton_Raphson_method(S,K,T,r,market_value,min_val=0.00001, n=1000):
    sigma=1.0  #         As we have to take a initial guess of value sigma in newton Raphson method
    for i in range(n):
        value=Blackscholes_call_Option(S,K,T,r,sigma) - market_value
        if( abs(value) < min_val):
            return sigma
        sigma = sigma - value / derivative_blackcsholes_call_option(S,K,T,r,sigma)
    return sigma

# Implementation of Bisection method for implied volatility
def Bisection_method(S,K,T,r,market_value, min_val=0.00001):
    low_sigma=0.00001          # f(low_sigma)< 0
    high_sigma=100         # f(high_sigma) > 0
    while (high_sigma - low_sigma) > min_val:
        sigma=(high_sigma + low_sigma) / 2
        if Blackscholes_call_Option(S,K,T,r,sigma) > market_value:
            high_sigma= sigma
        else:
            low_sigma = sigma
    return (high_sigma+low_sigma)/2

def ImpVol():
    try:
        S = float(entry_S.get())
        K = float(entry_K.get())
        T = float(entry_T.get())
        r = float(entry_r.get())
        market_price = float(entry_market_price.get())

        Impvol_by_Newton_Raphson = Newton_Raphson_method(S, K, T, r, market_price)
        Impvol_by_Bisection = Bisection_method(S, K, T, r, market_price)

        messagebox.showinfo("results",f"Implied Volatility (Newton-Raphson): { Impvol_by_Newton_Raphson:.5f}\nImplied Volatility (Bisection Method): { Impvol_by_Bisection:.5f}")
    except ValueError:
        messagebox.showerror("invalid input")

# GUI Implementation
root = tk.Tk()  
root.title("Implied Volatility")
tk.Label(root, text="Spot Price (S)").grid(row=0, column=0)
tk.Label(root, text="Strike Price (K)").grid(row=1, column=0)
tk.Label(root, text="Time to Maturity (T)").grid(row=2, column=0)
tk.Label(root, text="Risk-free Rate (r)").grid(row=3, column=0)
tk.Label(root, text="Market Price of Option").grid(row=4, column=0)
entry_S = tk.Entry(root)
entry_K = tk.Entry(root)
entry_T = tk.Entry(root)
entry_r = tk.Entry(root)
entry_market_price = tk.Entry(root)
entry_S.grid(row=0, column=1)
entry_K.grid(row=1, column=1)
entry_T.grid(row=2, column=1)
entry_r.grid(row=3, column=1)
entry_market_price.grid(row=4, column=1)

tk.Button(root, text="Compute Implied Volatility", command=ImpVol).grid(row=5, columnspan=2)
root.mainloop()