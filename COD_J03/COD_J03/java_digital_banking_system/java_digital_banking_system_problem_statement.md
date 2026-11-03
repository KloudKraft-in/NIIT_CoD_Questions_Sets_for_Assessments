# Java: Digital Banking System

Implement a Java program using inheritance and interfaces to manage different types of bank accounts. The program should:

* Calculate interest based on the specific account type
* Enforce withdrawal limits and minimum balance requirements
* Track the total number of active accounts using static members

**Class Description**
Complete the classes `SavingsAccount` and `CurrentAccount` which extend the abstract class `BankAccount`. You must also implement the `AccountOperations` interface.

1. **BankAccount (Abstract Class)**:

   * `double balance`: Stores the current balance.
   * `String accountNumber`: Stores the account ID.
   * `abstract void deposit(double amount)`: Adds money to the balance.
   * `abstract boolean withdraw(double amount)`: Removes money if constraints are met.
2. **SavingsAccount**:

   * Minimum Balance: $500.
   * Withdrawal must keep the balance $\ge 500$.
   * Interest Rate: 4% per year.
3. **CurrentAccount**:

   * Overdraft Limit: $2000$ (balance can go down to $-2000$).
   * Interest Rate: 0%.

**Returns**

* `double`: The updated balance after operations.
* `boolean`: `true` if the withdrawal was successful, `false` otherwise.

**Constraints**

* $1 \le NumberOfAccounts \le 50$.
* $0 \le InitialBalance \le 1,000,000$.

**Input Format For Custom Testing**
The first line contains an integer $N$ denoting the number of operations.
Each operation consists of: `{AccountType} {AccountNumber} {InitialBalance} {OperationType} {Amount}`.

**Sample Case 0**
**Sample Input For Custom Testing**

```text
2
Savings ACC01 1000 Withdraw 600
Current ACC02 100 Withdraw 1500
```

**Sample Output**

```text
Withdrawal Failed: Minimum balance requirement not met.
Withdrawal Successful: New Balance: -1400.0
```

**Explanation**
Case 1: Withdrawing 600 from 1000 leaves 400, which is below the 500 minimum for Savings.
Case 2: Current accounts allow overdrafts up to 2000, so a 1500 withdrawal from 100 is valid.


**Boilerplate:**

```
// student_workspace/soluiton.java
 
 * Implement the 'SavingsAccount' and 'CurrentAccount' classes here.
 * Both should extend 'BankAccount' and implement 'AccountOperations'.
 * The 'BankAccount' and 'AccountOperations' are already defined in the Harness.
 * DO NOT use access modifiers (e.g.: 'public') in your class declarations.
 */

class SavingsAccount extends BankAccount {
    public SavingsAccount(String accNo, double bal) {
        super(accNo, bal);
    }

    @Override
    public void deposit(double amount) {
        // Write your code here
    }

    @Override
    public boolean withdraw(double amount) {
        // Write your code here
        return false;
    }
}

class CurrentAccount extends BankAccount {
    public CurrentAccount(String accNo, double bal) {
        super(accNo, bal);
    }

    @Override
    public void deposit(double amount) {
        // Write your code here
    }

    @Override
    public boolean withdraw(double amount) {
        // Write your code here
        return false;
    }
}

```

Solution.java:

```
// student_workspace/soluiton.java

class SavingsAccount extends BankAccount {
    public SavingsAccount(String accNo, double bal) {
        super(accNo, bal);
    }

    @Override
    public void deposit(double amount) {
        this.balance += amount;
    }

    @Override
    public boolean withdraw(double amount) {
        if (this.balance - amount >= 500) {
        this.balance -= amount;
        return true;
        }
        return false;
    }
}

class CurrentAccount extends BankAccount {
    public CurrentAccount(String accNo, double bal) {
        super(accNo, bal);
    }

    @Override
    public void deposit(double amount) {
        this.balance += amount;
    }

    @Override
    public boolean withdraw(double amount) {
        if (this.balance - amount >= -2000) {
        this.balance -= amount;
        return true;
        }
        return false;
    }
}
```
