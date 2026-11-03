#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

class Account {
public:
    std::string accountId;
    std::string ownerName;
    double balance;
    std::vector<std::string> transactionLog;

    Account() : balance(0.0) {}

    Account(std::string id, std::string owner, double initialDeposit) 
        : accountId(id), ownerName(owner), balance(initialDeposit) {
        
        // Remove trailing zeroes from initialDeposit for the log string
        std::string amountStr = std::to_string(initialDeposit);
        amountStr.erase(amountStr.find_last_not_of('0') + 1, std::string::npos);
        if (amountStr.back() == '.') amountStr.pop_back();

        transactionLog.push_back("Account opened with deposit: $" + amountStr);
    }
};

class BankManager {
private:
    std::unordered_map<std::string, Account> accountRegistry;

    std::string formatAmount(double amount) {
        std::string amountStr = std::to_string(amount);
        amountStr.erase(amountStr.find_last_not_of('0') + 1, std::string::npos);
        if (amountStr.back() == '.') amountStr.pop_back();
        return amountStr;
    }

public:
    BankManager() {}

    std::string openAccount(std::string accountId, std::string ownerName, double initialDeposit) {
        Account newAccount(accountId, ownerName, initialDeposit);
        accountRegistry[accountId] = newAccount;
        return "Account " + accountId + " opened.";
    }

    std::string deposit(std::string accountId, double amount) {
        if (accountRegistry.find(accountId) == accountRegistry.end()) {
            return "Account not found.";
        }
        
        accountRegistry[accountId].balance += amount;
        accountRegistry[accountId].transactionLog.push_back("Deposited $" + formatAmount(amount));
        return "Success. New Balance: $" + formatAmount(accountRegistry[accountId].balance);
    }

    std::string withdraw(std::string accountId, double amount) {
        if (accountRegistry.find(accountId) == accountRegistry.end()) {
            return "Account not found.";
        }
        
        if (accountRegistry[accountId].balance < amount) {
            return "Insufficient funds.";
        }
        
        accountRegistry[accountId].balance -= amount;
        accountRegistry[accountId].transactionLog.push_back("Withdrew $" + formatAmount(amount));
        return "Withdrew $" + formatAmount(amount);
    }

    std::vector<std::string> getTransactionHistory(std::string accountId) {
        if (accountRegistry.find(accountId) == accountRegistry.end()) {
            return {"Account not found."};
        }
        return accountRegistry[accountId].transactionLog;
    }

    double totalBankLiquidity() {
        double total = 0.0;
        for (const auto& pair : accountRegistry) {
            total += pair.second.balance;
        }
        return total;
    }

    int applyInterest() {
        int count = 0;
        for (auto& pair : accountRegistry) {
            if (pair.second.balance > 1000.0) {
                pair.second.balance += pair.second.balance * 0.05;
                pair.second.transactionLog.push_back("Interest Applied");
                count++;
            }
        }
        return count;
    }
};
