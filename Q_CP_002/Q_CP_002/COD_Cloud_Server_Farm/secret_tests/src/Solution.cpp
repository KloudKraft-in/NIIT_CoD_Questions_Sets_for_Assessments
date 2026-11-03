#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

class ServerNode {
public:
    std::string serverId;
    std::string ipAddress;
    bool isAllocated;
    double computeCycles;
    std::vector<std::string> deploymentLog;

    ServerNode() : isAllocated(false), computeCycles(0.0) {}

    ServerNode(std::string id, std::string ip) 
        : serverId(id), ipAddress(ip), isAllocated(false), computeCycles(0.0) {
        deploymentLog.push_back("Server provisioned at " + ip);
    }
};

class DatacenterManager {
private:
    std::unordered_map<std::string, ServerNode> serverRegistry;

    std::string formatCycles(double cycles) {
        std::string cycleStr = std::to_string(cycles);
        cycleStr.erase(cycleStr.find_last_not_of('0') + 1, std::string::npos);
        if (cycleStr.back() == '.') cycleStr.pop_back();
        return cycleStr;
    }

public:
    DatacenterManager() {}

    std::string provisionServer(std::string serverId, std::string ipAddress) {
        ServerNode newNode(serverId, ipAddress);
        serverRegistry[serverId] = newNode;
        return "Server " + serverId + " added.";
    }

    std::string allocateServer(std::string serverId, std::string workloadName) {
        if (serverRegistry.find(serverId) == serverRegistry.end()) {
            return "Server not found.";
        }
        
        if (serverRegistry[serverId].isAllocated) {
            return "Server currently in use.";
        }
        
        serverRegistry[serverId].isAllocated = true;
        serverRegistry[serverId].deploymentLog.push_back("Allocated to " + workloadName);
        return "Server " + serverId + " allocated.";
    }

    std::string releaseServer(std::string serverId, double cyclesUsed) {
        if (serverRegistry.find(serverId) == serverRegistry.end()) {
            return "Server not found.";
        }
        
        if (!serverRegistry[serverId].isAllocated) {
            return "Server is not allocated.";
        }
        
        serverRegistry[serverId].isAllocated = false;
        serverRegistry[serverId].computeCycles += cyclesUsed;
        serverRegistry[serverId].deploymentLog.push_back("Released. Cycles used: " + formatCycles(cyclesUsed));
        return "Server released.";
    }

    std::vector<std::string> getServerHistory(std::string serverId) {
        if (serverRegistry.find(serverId) == serverRegistry.end()) {
            return {"Server not found."};
        }
        return serverRegistry[serverId].deploymentLog;
    }

    double totalDatacenterUsage() {
        double total = 0.0;
        for (const auto& pair : serverRegistry) {
            total += pair.second.computeCycles;
        }
        return total;
    }

    int optimizeServers() {
        int count = 0;
        for (auto& pair : serverRegistry) {
            if (pair.second.computeCycles > 1000.0) {
                pair.second.computeCycles *= 0.90; // Reduce by 10%
                pair.second.deploymentLog.push_back("Performance Optimized");
                count++;
            }
        }
        return count;
    }
};
