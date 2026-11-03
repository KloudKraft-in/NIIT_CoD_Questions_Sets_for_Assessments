# Low-Level Design (LLD) – Smart Home Hub System
(Multi-Class Composition in Kotlin)

**Difficulty Level**: Intermediate | **Total Marks**: 10
**Design Format**: 2 Classes | 7 Methods | 7 Test Cases

**Summary of Design Requirements**
Implement a Smart Home automation hub featuring device state tracking and power consumption logic.

1. **Class "Device" (Data Entity)**:
   - Stores: `deviceId` (String), `type` (String), `status` (Boolean), `powerUsage` (Double), `activityLog` (MutableList of Strings).
   - Manages state for individual smart devices (e.g., Lights, Thermostats).

2. **Class "SmartHomeSystem" (Manager)**:
   - Manages a collection of "Device" objects.
   - Handles toggling devices, scheduling timers, and calculating network power consumption.

**Concepts Tested**
- Class Composition in Kotlin
- MutableList/Log management within objects
- Conditional logic with multiple constraints (Status + Constraints)
- Kotlin String templates ($)

**Problem Statement**
Design a Smart Home Hub where:
- Devices track state changes in an activity log.
- Devices can be toggled ON (true) or OFF (false).
- Devices can only be scheduled to turn ON if they are currently OFF.

Each device object has:
- `deviceId` (str)
- `type` (str)
- `status` (boolean)
- `powerUsage` (double)
- `activityLog` (MutableList<String>)

**Operations (Methods)**

1. **Initialize structures** (Class: `Device` & `SmartHomeSystem`)
Constructors for both. Device log starts with `["Device [type] installed."]`. 
`SmartHomeSystem` initializes an empty registry.

2. **Register Device** (Class: `SmartHomeSystem`)
`fun addDevice(deviceId: String, type: String, powerUsage: Double): String`
- Create Device instance with log. Status is initialized to false (OFF).
- Return `"Device [deviceId] added."`

3. **Toggle State** (Class: `SmartHomeSystem`)
`fun toggleDevice(deviceId: String, state: Boolean): String`
- Find the device. If found, update the status.
- Append `"Device turned ON"` or `"Device turned OFF"` to the device's activityLog based on the new state.
- Return `"Device [deviceId] is now [ON/OFF]."`
- If device not found, return `"Device not found."`

4. **Schedule Timer**
`fun scheduleTimer(deviceId: String, timeInMinutes: Int): String`
- Rule: Only works if the device is currently OFF (status == false).
- If valid: Log `"Scheduled to turn ON in [timeInMinutes] mins"`, return `"Timer set for [deviceId]."`
- If already ON: return `"Device is already ON."`
- Else: return `"Device not found."`

5. **Audit Trail**
`fun getDeviceHistory(deviceId: String): List<String>`
- Return the full list of strings from `device.activityLog`.
- If not found, return `["Device not found."]`.

6. **Network Power Measurement**
`fun totalPowerConsumption(): Double`
- Sum of `powerUsage` for all devices that are currently ON.
- Return Double.

7. **Bulk Turn Off Sweep**
`fun turnOffAllDevices(): Int`
- For EVERY device where status is true (ON), change status to false and log `"Turned OFF by Hub"`.
- Return the integer count of devices that were turned off.

**Test Cases & Marks Allocation:**
-----------------------------------------------------------------------------------------------------------------
| Test Case ID |                            Description                       |                 Method                     | Marks |
|-----------------|------------------------------------------------|------------------------------------|---------|
| TC1                 | Instantiate complex structures                 | init() (Both)                         |      0     |
| TC2                 | Add device with initial log                     | addDevice()                            |     1     |
| TC3                 | Toggle state with log tracking              | toggleDevice()                           |     2     |
| TC4                 | Schedule timer with state constraints      | scheduleTimer()                      |     3     |
| TC5                 | Retrieve full activity trail of device             | getDeviceHistory()          |     1     |
| TC6                 | Calculate total network power consumption           | totalPowerConsumption()           |     1     |
| TC7                 | Perform bulk turn off sweep                      | turnOffAllDevices()             |     2     |
-------------------------------------------------------------------------------------------------------------------
|                                                      Total                                   |                                    10                           |
-----------------------------------------------------------------------------------------------------------------

**Visible Test Case Descriptions**
- **TC1**: `SmartHomeSystem()` should initialize the registry.
- **TC2**: `addDevice("D_01", "Light", 15.0)` creates Device object with log `["Device Light installed."]`.
- **TC3**: `toggleDevice("D_01", true)` updates status to true and log to `["Device Light installed.", "Device turned ON"]`.
- **TC4**: `scheduleTimer("D_01", 30)` returns `"Device is already ON."`.
- **TC5**: `getDeviceHistory("D_01")` returns the full list of formatted strings.
- **TC6**: `totalPowerConsumption()` returns the Double sum of all ON devices' powerUsage.
- **TC7**: `turnOffAllDevices()` turns OFF eligible devices and returns the count of processed items.
