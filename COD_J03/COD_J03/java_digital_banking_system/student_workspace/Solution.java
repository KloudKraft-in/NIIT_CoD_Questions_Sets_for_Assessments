
// /* 
//  * Implement the 'SavingsAccount' and 'CurrentAccount' classes here.
//  * Both should extend 'BankAccount' and implement 'AccountOperations'.
//  * The 'BankAccount' and 'AccountOperations' are already defined in the Harness.
//  * DO NOT use access modifiers (e.g.: 'public') in your class declarations.
//  */

// class SavingsAccount extends BankAccount {
//     public SavingsAccount(String accNo, double bal) {
//         super(accNo, bal);
//     }

//     @Override
//     public void deposit(double amount) {
//         // Write your code here
//     }

//     @Override
//     public boolean withdraw(double amount) {
//         // Write your code here
//         return false;
//     }
// }

// class CurrentAccount extends BankAccount {
//     public CurrentAccount(String accNo, double bal) {
//         super(accNo, bal);
//     }

//     @Override
//     public void deposit(double amount) {
//         // Write your code here
//     }

//     @Override
//     public boolean withdraw(double amount) {
//         // Write your code here
//         return false;
//     }
// }

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
