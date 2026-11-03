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

void testProvisionServer() {
    DatacenterManager manager;
    std::string res = manager.provisionServer("S1", "192.168.1.10");
    if (res != "Server S1 added.") {
        printFail("TestSuite.testProvisionServer", "Expected 'Server S1 added.'");
        return;
    }
    std::vector<std::string> history = manager.getServerHistory("S1");
    if (history.size() == 1 && history[0] == "Server provisioned at 192.168.1.10") {
        printPass("TestSuite.testProvisionServer");
    } else {
        printFail("TestSuite.testProvisionServer", "Invalid deployment log");
    }
}

void testAllocateServer() {
    DatacenterManager manager;
    manager.provisionServer("S1", "192.168.1.10");
    std::string res = manager.allocateServer("S1", "AI_Training");
    
    if (res != "Server S1 allocated.") {
        printFail("TestSuite.testAllocateServer", "Invalid allocation return string");
        return;
    }
    
    std::string res2 = manager.allocateServer("S1", "Data_Mining");
    if (res2 != "Server currently in use.") {
        printFail("TestSuite.testAllocateServer", "Failed to block double allocation");
        return;
    }

    std::vector<std::string> history = manager.getServerHistory("S1");
    if (history.size() == 2 && history[1] == "Allocated to AI_Training") {
        printPass("TestSuite.testAllocateServer");
    } else {
        printFail("TestSuite.testAllocateServer", "Invalid deployment log");
    }
}

void testReleaseServer() {
    DatacenterManager manager;
    manager.provisionServer("S1", "192.168.1.10");
    
    std::string res1 = manager.releaseServer("S1", 450.5);
    if (res1 != "Server is not allocated.") {
        printFail("TestSuite.testReleaseServer", "Allowed release of free server");
        return;
    }
    
    manager.allocateServer("S1", "AI_Training");
    std::string res2 = manager.releaseServer("S1", 450.5);
    if (res2 != "Server released.") {
        printFail("TestSuite.testReleaseServer", "Failed to release allocated server");
        return;
    }
    
    std::vector<std::string> history = manager.getServerHistory("S1");
    if (history.size() == 3 && history[2] == "Released. Cycles used: 450.5") {
        printPass("TestSuite.testReleaseServer");
    } else {
        printFail("TestSuite.testReleaseServer", "Invalid deployment log");
    }
}

void testGetServerHistory() {
    DatacenterManager manager;
    std::vector<std::string> res = manager.getServerHistory("NON_EXISTENT");
    if (res.size() == 1 && res[0] == "Server not found.") {
        printPass("TestSuite.testGetServerHistory");
    } else {
        printFail("TestSuite.testGetServerHistory", "Server not found failed");
    }
}

void testTotalDatacenterUsage() {
    DatacenterManager manager;
    manager.provisionServer("S1", "192.168.1.10");
    manager.provisionServer("S2", "192.168.1.11");
    
    manager.allocateServer("S1", "A");
    manager.releaseServer("S1", 500.5);
    
    manager.allocateServer("S2", "B");
    manager.releaseServer("S2", 300.0);
    
    if (std::abs(manager.totalDatacenterUsage() - 800.5) < 0.001) {
        printPass("TestSuite.testTotalDatacenterUsage");
    } else {
        printFail("TestSuite.testTotalDatacenterUsage", "Incorrect compute cycle sum");
    }
}

void testOptimizeServers() {
    DatacenterManager manager;
    manager.provisionServer("S1", "192.168.1.10");
    manager.allocateServer("S1", "A");
    manager.releaseServer("S1", 2000.0); // Eligible > 1000.0
    
    manager.provisionServer("S2", "192.168.1.11");
    manager.allocateServer("S2", "B");
    manager.releaseServer("S2", 800.0); // Ineligible
    
    int count = manager.optimizeServers();
    if (count != 1) {
        printFail("TestSuite.testOptimizeServers", "Wrong eligible count");
        return;
    }
    
    // 2000.0 reduced by 10% = 1800.0. 1800.0 + 800.0 = 2600.0
    if (std::abs(manager.totalDatacenterUsage() - 2600.0) < 0.001) {
        std::vector<std::string> history = manager.getServerHistory("S1");
        if (history.back() == "Performance Optimized") {
            printPass("TestSuite.testOptimizeServers");
        } else {
            printFail("TestSuite.testOptimizeServers", "Log entry missing");
        }
    } else {
        printFail("TestSuite.testOptimizeServers", "Incorrect optimization calculation");
    }
}

int main() {
    std::cout << "[==========] Running 6 tests from 1 test suite.\n";
    testProvisionServer();
    testAllocateServer();
    testReleaseServer();
    testGetServerHistory();
    testTotalDatacenterUsage();
    testOptimizeServers();
    std::cout << "[==========] 6 tests from 1 test suite ran.\n";
    return 0;
}
