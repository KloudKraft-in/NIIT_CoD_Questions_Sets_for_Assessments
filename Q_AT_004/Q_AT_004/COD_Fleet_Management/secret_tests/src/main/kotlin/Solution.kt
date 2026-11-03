class Vehicle(val vehicleId: String, val driverName: String) {
    var isAvailable: Boolean = true
    var totalEarnings: Double = 0.0
    val tripLog: MutableList<String> = mutableListOf("Vehicle registered to $driverName")
}

class FleetManager {
    private val fleetRegistry: MutableMap<String, Vehicle> = mutableMapOf()

    fun registerVehicle(vehicleId: String, driverName: String): String {
        val vehicle = Vehicle(vehicleId, driverName)
        fleetRegistry[vehicleId] = vehicle
        return "Vehicle $vehicleId added."
    }

    fun dispatchVehicle(vehicleId: String, destination: String): String {
        val vehicle = fleetRegistry[vehicleId] ?: return "Vehicle not found."
        
        if (!vehicle.isAvailable) {
            return "Vehicle unavailable."
        }
        
        vehicle.isAvailable = false
        vehicle.tripLog.add("Dispatched to $destination")
        return "Vehicle $vehicleId dispatched."
    }

    fun completeTrip(vehicleId: String, fare: Double): String {
        val vehicle = fleetRegistry[vehicleId] ?: return "Vehicle not found."
        
        if (vehicle.isAvailable) {
            return "Vehicle is not on a trip."
        }
        
        vehicle.isAvailable = true
        vehicle.totalEarnings += fare
        vehicle.tripLog.add("Trip completed. Earned $$fare")
        return "Trip completed."
    }

    fun getVehicleHistory(vehicleId: String): List<String> {
        val vehicle = fleetRegistry[vehicleId]
        return vehicle?.tripLog ?: listOf("Vehicle not found.")
    }

    fun totalFleetEarnings(): Double {
        return fleetRegistry.values.sumOf { it.totalEarnings }
    }

    fun applySurgeBonus(): Int {
        var count = 0
        for (vehicle in fleetRegistry.values) {
            if (vehicle.totalEarnings > 500.0) {
                vehicle.totalEarnings += vehicle.totalEarnings * 0.10
                vehicle.tripLog.add("Surge Bonus Applied")
                count++
            }
        }
        return count
    }
}
