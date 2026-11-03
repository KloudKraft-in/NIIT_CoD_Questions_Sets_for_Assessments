# Low-Level Design (LLD) – Cloud Server Farm Management
(Multi-Class Composition in C++)

**Difficulty Level**: Intermediate | **Total Marks**: 10
**Design Format**: 2 Classes | 7 Methods | 7 Test Cases

**Summary of Design Requirements**
Implement a Cloud Server Farm tracking compute resource allocation and cycle usage.

1. **Class "ServerNode" (Data Entity)**:
   - Stores: `serverId` (string), `ipAddress` (string), `isAllocated` (bool), `computeCycles` (double), `deploymentLog` (vector of strings).
   - Manages state for bare-metal servers.

2. **Class "DatacenterManager" (Manager)**:
   - Manages a collection of "ServerNode" objects.
   - Handles provisioning, workload allocation, resource releasing, and fleet optimization.

**Concepts Tested**
- Class Composition in C++
- `std::vector` and `std::unordered_map` usage
- State tracking and accumulation
- Conditional constraints

**Problem Statement**
Design a Cloud Server Farm where:
- Servers log their allocations and releases.
- A server cannot be allocated if it's currently in use (`isAllocated` is true).
- Servers with heavily accumulated compute cycles get optimized.

Each server object has:
- `serverId` (string)
- `ipAddress` (string)
- `isAllocated` (boolean)
- `computeCycles` (double)
- `deploymentLog` (std::vector<std::string>)

**Operations (Methods)**

1. **Initialize structures** (Class: `ServerNode` & `DatacenterManager`)
Constructors for both. Server log starts with `["Server provisioned at [ipAddress]"]`. `isAllocated` defaults to false. `computeCycles` is 0.0.
`DatacenterManager` initializes an empty registry.

2. **Provision Server** (Class: `DatacenterManager`)
`std::string provisionServer(std::string serverId, std::string ipAddress)`
- Create ServerNode instance with initial log.
- Return `"Server [serverId] added."`

3. **Allocate Server** (Class: `DatacenterManager`)
`std::string allocateServer(std::string serverId, std::string workloadName)`
- Find the server. If `isAllocated` is false, set it to true.
- Append `"Allocated to [workloadName]"` to the server's deploymentLog.
- Return `"Server [serverId] allocated."`
- If already allocated, return `"Server currently in use."`
- If server not found, return `"Server not found."`

4. **Release Server** (Class: `DatacenterManager`)
`std::string releaseServer(std::string serverId, double cyclesUsed)`
- Rule: Only works if the server is currently allocated (`isAllocated` == true).
- If valid: Set `isAllocated` to false, add `cyclesUsed` to `computeCycles`.
- Log `"Released. Cycles used: [cyclesUsed]"`.
- Return `"Server released."`
- If already released (free): return `"Server is not allocated."`
- Else if server not found: return `"Server not found."`

5. **Audit Trail** (Class: `DatacenterManager`)
`std::vector<std::string> getServerHistory(std::string serverId)`
- Return the full list of strings from `server.deploymentLog`.
- If not found, return `["Server not found."]`.

6. **Network Computation** (Class: `DatacenterManager`)
`double totalDatacenterUsage()`
- Sum of `computeCycles` for all registered servers.
- Return double.

7. **Bulk Fleet Optimization** (Class: `DatacenterManager`)
`int optimizeServers()`
- For EVERY server where `computeCycles` is greater than 1000.0, reduce their `computeCycles` by 10% (multiply by 0.90) and log `"Performance Optimized"`.
- Return the integer count of servers that were optimized.

**Test Cases & Marks Allocation:**
-----------------------------------------------------------------------------------------------------------------
| Test Case ID |                            Description                       |                 Method                     | Marks |
|-----------------|------------------------------------------------|------------------------------------|---------|
| TC1                 | Instantiate complex structures                 | init() (Both)                         |      0     |
| TC2                 | Provision server with initial log              | provisionServer()                   |     1     |
| TC3                 | Allocate server with state check               | allocateServer()                    |     2     |
| TC4                 | Release server and accumulate usage            | releaseServer()                     |     3     |
| TC5                 | Retrieve full deployment trail                 | getServerHistory()                  |     1     |
| TC6                 | Calculate total datacenter usage               | totalDatacenterUsage()              |     1     |
| TC7                 | Perform bulk compute optimization              | optimizeServers()                   |     2     |
-------------------------------------------------------------------------------------------------------------------
|                                                      Total                                   |                                    10                           |
-----------------------------------------------------------------------------------------------------------------

**Visible Test Case Descriptions**
- **TC1**: `DatacenterManager()` should initialize the registry.
- **TC2**: `provisionServer("S1", "192.168.1.10")` creates ServerNode object with log `["Server provisioned at 192.168.1.10"]`.
- **TC3**: `allocateServer("S1", "AI_Training")` updates status to true and log to `["Server provisioned at 192.168.1.10", "Allocated to AI_Training"]`.
- **TC4**: `releaseServer("S1", 450.5)` updates status to false, adds 450.5 to computeCycles, and returns `"Server released."`.
- **TC5**: `getServerHistory("S1")` returns the full vector of formatted strings.
- **TC6**: `totalDatacenterUsage()` returns the double sum of all compute cycles.
- **TC7**: `optimizeServers()` reduces compute cycles by 10% for eligible servers and returns the count.
