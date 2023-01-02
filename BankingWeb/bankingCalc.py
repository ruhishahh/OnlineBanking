#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 20:30:33 2021

@author: ruhishah
"""

'''
This is the base class representing a bank account.  It contains the  basic data 
for an account (ID, owner, balance) and methods to access those attributes, as well 
as methods for adding and removing money and checking a balance.
'''
class Account:
    def __init__(self, sOwner, iID, fBalance):
        self.__sOwner = sOwner
        self.__iID = iID
        self.__fBalance = fBalance
        
    def getOwner(self):
        #Returns the owner of the account.
        return self.__sOwner
    
    def getID(self):
        #Returns the ID number of the account.
        return self.__iID
    
    def getBalance(self):
        #Returns the current balance in the account
        return self.__fBalance
    
    
    def setOwner(self, sOwner):
        #Updates the owner of the account from the method argument
        self.__sOwner = sOwner
             
    def setID(self, iID):
        #Updates the ID number of the account from the method argument.
        self.__iID = iID
        
    def setBalance(self, fBalance):
        #Updates the balance in the account from the method argument.
        self.__fBalance = fBalance
        
                
    def deposit(self, amount):
        #Takes the method argument and adds it to current account balance.
        self.__fBalance += amount
    
    def withdraw(self, amount): 
        '''
        Takes the method argument and subtracts it from the account balance. 
        If the balance falls below 0, a warning message is printed and an extra $5 penalty
        is deducted from the account.
        '''
        self.__fBalance -= amount
            
    def printAccountInfo(self):
        # Prints the owner, ID, and balance of the account.
        print("Owner: " + self.__sOwner + "\n")
        print("ID: " + self.__iID + "\n")
        print("Balance: " + self.__fBalance + "\n")

'''
This bank permits customers to sign up for checking accounts.  But banks need to make 
money too, so this account comes with a few twists.  In addition to inheriting all of the
attributes of the Account class, this checking account class also stores a count of 
operations and an accompanying operation fee.  The function descriptions below explain these 
in more detail.  Additionally, the constructor for this class should initialize
 self.__transactionCount to 0.
'''                  
class CheckingAccount(Account):
    def __init__(self, sOwner, iID, fBalance, iTF):
        self.__iTF = iTF
        self.__iTC = 0
        super().__init__(sOwner, iID, fBalance)
        
    def getTransactionCount(self):
        #Returns the number of transactions since the last fee.
        return self.__iTC
    
    def getTransactionFee(self):
        # Return the amount charged for transaction fees.
        return self.__iTF
    
    def setTransactionCount(self, iTC):
        #Updates the number of transactions since the last fee.
        self.__iTC = iTC
        
    def setTransactionFee(self, iTF):
        #Updates the transaction fee amount.
        self.__iTF = iTF 
    
    def deposit(self, amount):
        '''
        Takes the method argument and adds it to the current account balance.  
        Also adds 1 to the number of transactions since the last fee, and calls 
        the deductFees() function.
        '''

        self.setBalance(self.getBalance() + amount)
        self.setTransactionCount(self.getTransactionCount() + 1)
        self.deductFees()
    
    def withdraw(self, amount):
        '''
        Takes the method argument and subtracts it from the account balance.  
        If the balance falls below 0, a warning message is printed and an extra $5
        penalty is deducted from the account.  Also adds 1 to the number of transactions
        since the last fee, and calls the deductFees() function.
        '''
        
        if self.getBalance() < amount:
            print("Warning: Insufficient Funds" + "\n" + "$5 Deduction")
            self.setBalance(int(self.getBalance()) - 5)
            #self.setBalance(self.getBalance() - 5)
            #self.setBalance(self.getBalance().__add__(-5))
        self.setBalance(self.getBalance() - amount)
        self.setTransactionCount(self.getTransactionCount() + 1)
        self.deductFees()
    
    def deductFees(self):
        #If there have been 5 transactions since the last fee, deduct the TransactionFee from the account balance and reset the counter to 0.
        if self.__iTC >= 5:
            self.setBalance(self.getBalance()-self.__iTF)
            self.setTransactionCount(0)
        
    
    
'''
This bank also permits customers to sign up for savings accounts.  In addition to inheriting 
all of the attributes of the Account class, this savings account class also stores an interest
rate which gives customers some additional cash, just for being a customer.
'''   
class SavingsAccount(Account):
    def __init__(self, sOwner, iID, fBalance, fIR):
        self.__fIR = fIR
        super().__init__(sOwner, iID, fBalance)       

    def getInterestRate(self):
        # Returns the interest rate associated with the account.
        return self.__fIR
    
    def setInterestRate(self, fIR):
        #Updates the interest rate associated with the account.
        self.__fIR = fIR
    
    def withdraw(self, amount):
        '''
        Takes the method argument and subtracts it from the account balance.  
        If the balance falls below 0, a warning message is printed and an extra $5 penalty 
        is deducted from the account, and the interest rate is also reduced to 0.
        '''
        if self.getBalance() < amount:
            print("Warning: Insufficient Funds" + "\n" + "$5 Deduction")
            self.setBalance(int(self.getBalance()) - 5)
            self.__fIR = self.setInterestRate(0)
        self.setBalance(self.getBalance() - amount)

    def applyInterest(self):
        #When this function is called, the interest rate is applied to update the balance
        self.setBalance((1 + self.__fIR) * self.getBalance())
            
          
            