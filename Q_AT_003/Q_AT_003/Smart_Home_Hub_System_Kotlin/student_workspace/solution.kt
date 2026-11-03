class Device(val deviceId: String, val type: String, val powerUsage: Double) {
    var status: Boolean = false
    val activityLog: MutableList<String> = mutableListOf("Device $type installed.")
}

class SmartHomeSystem {
    private val deviceRegistry: MutableMap<String, Device> = mutableMapOf()

    fun addDevice(deviceId: String, type: String, powerUsage: Double): String {
        val device = Device(deviceId, type, powerUsage)
        deviceRegistry[deviceId] = device
        return "Device $deviceId added."
    }

    fun toggleDevice(deviceId: String, state: Boolean): String {
        val device = deviceRegistry[deviceId]
        return if (device != null) {
            device.status = state
            if (state) {
                device.activityLog.add("Device turned ON")
                "Device $deviceId is now ON."
            } else {
                device.activityLog.add("Device turned OFF")
                "Device $deviceId is now OFF."
            }
        } else {
            "Device not found."
        }
    }

    fun scheduleTimer(deviceId: String, timeInMinutes: Int): String {
        val device = deviceRegistry[deviceId] ?: return "Device not found."
        
        if (device.status) {
            return "Device is already ON."
        }
        
        device.activityLog.add("Scheduled to turn ON in $timeInMinutes mins")
        return "Timer set for $deviceId."
    }

    fun getDeviceHistory(deviceId: String): List<String> {
        val device = deviceRegistry[deviceId]
        return device?.activityLog ?: listOf("Device not found.")
    }

    fun totalPowerConsumption(): Double {
        return deviceRegistry.values.filter { it.status }.sumOf { it.powerUsage }
    }

    fun turnOffAllDevices(): Int {
        var count = 0
        for (device in deviceRegistry.values) {
            if (device.status) {
                device.status = false
                device.activityLog.add("Turned OFF by Hub")
                count++
            }
        }
        return count
    }
}
