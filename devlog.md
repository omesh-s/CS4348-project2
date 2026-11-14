\# Project 2 Development Log



\## 11/13/2026 11:14 PM CST | Project start



Project 2 is a bank simulation with three tellers and 50 customers.

I have a Python draft to review and test. I plan to start by tracing

how a customer gives the teller a transaction and waits for it to finish.

Then I will run the program and check how the bank closes.





\## 11/13/2026 11:20 PM CST | Session 1 start



I plan to bring in the Python draft and trace one deposit and one

withdrawal. I want to see how the teller gets the customer's request

and how the customer knows the transaction is done.





\## 11/13/2026 11:36 PM CST | Session 1 end



I ran the one-customer prototype in PowerShell. The customer waited

for the teller to ask, then sent a deposit request. The teller

signaled when the deposit was done. The customer left, the teller

exited, and the bank closed.



I saw how the semaphores keep these steps in order. In the next

session, I plan to test the full bank with three tellers and 50

customers and check how they share the door, manager, and safe.







\## 11/14/2026 12:46 AM CST | Session 2 start



The one-customer prototype ran and closed the bank after the customer

left. I plan to bring in the version with three tellers and 50 customers.

I will check that all three tellers are ready before customers enter

and that a teller visits the manager before taking a withdrawal to the safe.







\## 11/14/2026 12:54 AM CST | Session 2 end



I ran the full-bank version in PowerShell. The log showed 50

customers leaving the bank and three tellers leaving for the day.

The bank closed on the last line.



In the next session, I plan to run more tests and check that the

submission ZIP includes the Git history.

