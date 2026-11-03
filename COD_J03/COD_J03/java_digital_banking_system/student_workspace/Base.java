
interface AccountOperations {
    void deposit(double amount);
    boolean withdraw(double amount);
}

abstract class BankAccount implements AccountOperations {
    protected String accountNumber;
    protected double balance;

    public BankAccount(String accountNumber, double balance) {
        this.accountNumber = accountNumber;
        this.balance = balance;
    }

    public double getBalance() {
        return balance;
    }
}
