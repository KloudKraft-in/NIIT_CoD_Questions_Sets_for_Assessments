#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include "../src/Solution.cpp"

void printPass(const std::string& testName) {
    std::cout << "[  PASSED  ] " << testName << "\n";
}

void printFail(const std::string& testName, const std::string& msg) {
    std::cout << "[  FAILED  ] " << testName << " - " << msg << "\n";
}

void testOpenAccount() {
    BankManager system;
    std::string res = system.openAccount("A1", "Alice", 100.0);
    if (res != "Account A1 opened.") {
        printFail("TestSuite.testOpenAccount", "Expected 'Account A1 opened.'");
        return;
    }
    std::vector<std::string> history = system.getTransactionHistory("A1");
    if (history.size() == 1 && history[0] == "Account opened with deposit: $100") {
        printPass("TestSuite.testOpenAccount");
    } else {
        printFail("TestSuite.testOpenAccount", "Invalid transaction log");
    }
}

void testDeposit() {
    BankManager system;
    system.openAccount("A1", "Alice", 100.0);
    std::string res = system.deposit("A1", 50.0);
    if (res != "Success. New Balance: $150") {
        printFail("TestSuite.testDeposit", "Invalid deposit return string");
        return;
    }
    std::vector<std::string> history = system.getTransactionHistory("A1");
    if (history.size() == 2 && history[1] == "Deposited $50") {
        printPass("TestSuite.testDeposit");
    } else {
        printFail("TestSuite.testDeposit", "Invalid transaction log");
    }
}

void testWithdraw() {
    BankManager system;
    system.openAccount("A1", "Alice", 100.0);
    
    std::string res1 = system.withdraw("A1", 40.0);
    if (res1 != "Withdrew $40") {
        printFail("TestSuite.testWithdraw", "Invalid withdraw return");
        return;
    }
    
    std::string res2 = system.withdraw("A1", 100.0);
    if (res2 != "Insufficient funds.") {
        printFail("TestSuite.testWithdraw", "Overdraft allowed");
        return;
    }
    
    std::vector<std::string> history = system.getTransactionHistory("A1");
    if (history.size() == 2 && history[1] == "Withdrew $40") {
        printPass("TestSuite.testWithdraw");
    } else {
        printFail("TestSuite.testWithdraw", "Invalid transaction log");
    }
}

void testGetTransactionHistory() {
    BankManager system;
    std::vector<std::string> res = system.getTransactionHistory("NON_EXISTENT");
    if (res.size() == 1 && res[0] == "Account not found.") {
        printPass("TestSuite.testGetTransactionHistory");
    } else {
        printFail("TestSuite.testGetTransactionHistory", "Account not found failed");
    }
}

void testTotalBankLiquidity() {
    BankManager system;
    system.openAccount("A1", "Alice", 100.0);
    system.openAccount("A2", "Bob", 200.0);
    system.deposit("A1", 50.0);
    
    if (std::abs(system.totalBankLiquidity() - 350.0) < 0.001) {
        printPass("TestSuite.testTotalBankLiquidity");
    } else {
        printFail("TestSuite.testTotalBankLiquidity", "Incorrect liquidity sum");
    }
}

void testApplyInterest() {
    BankManager system;
    system.openAccount("A1", "Alice", 2000.0);
    system.openAccount("A2", "Bob", 500.0);
    
    int count = system.applyInterest();
    if (count != 1) {
        printFail("TestSuite.testApplyInterest", "Wrong eligible count");
        return;
    }
    
    if (std::abs(system.totalBankLiquidity() - 2600.0) < 0.001) {
        std::vector<std::string> history = system.getTransactionHistory("A1");
        if (history.back() == "Interest Applied") {
            printPass("TestSuite.testApplyInterest");
        } else {
            printFail("TestSuite.testApplyInterest", "Log entry missing");
        }
    } else {
        printFail("TestSuite.testApplyInterest", "Incorrect interest applied");
    }
}

int main() {
    std::cout << "[==========] Running 6 tests from 1 test suite.\n";
    testOpenAccount();
    testDeposit();
    testWithdraw();
    testGetTransactionHistory();
    testTotalBankLiquidity();
    testApplyInterest();
    std::cout << "[==========] 6 tests from 1 test suite ran.\n";
    return 0;
}
