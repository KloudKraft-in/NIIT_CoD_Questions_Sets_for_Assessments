import org.junit.jupiter.api.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue
import kotlin.test.assertFalse

class FleetManagerTest {

    @Test
    fun testInstantiation() {
        val manager = FleetManager()
        assertTrue(manager != null)
    }

    @Test
    fun testRegisterVehicle() {
        val manager = FleetManager()
        val res = manager.registerVehicle("V1", "Alice")
        assertEquals("Vehicle V1 added.", res)
        val history = manager.getVehicleHistory("V1")
        assertEquals(1, history.size)
        assertEquals("Vehicle registered to Alice", history[0])
    }

    @Test
    fun testDispatchVehicle() {
        val manager = FleetManager()
        manager.registerVehicle("V1", "Alice")
        
        val res1 = manager.dispatchVehicle("V1", "Downtown")
        assertEquals("Vehicle V1 dispatched.", res1)
        
        // Try dispatching again
        val res2 = manager.dispatchVehicle("V1", "Airport")
        assertEquals("Vehicle unavailable.", res2)
        
        val history = manager.getVehicleHistory("V1")
        assertEquals(2, history.size)
        assertEquals("Dispatched to Downtown", history[1])
    }

    @Test
    fun testCompleteTrip() {
        val manager = FleetManager()
        manager.registerVehicle("V1", "Alice")
        
        // Complete trip without dispatching
        val res1 = manager.completeTrip("V1", 50.0)
        assertEquals("Vehicle is not on a trip.", res1)
        
        // Dispatch then complete
        manager.dispatchVehicle("V1", "Downtown")
        val res2 = manager.completeTrip("V1", 45.5)
        assertEquals("Trip completed.", res2)
        
        val history = manager.getVehicleHistory("V1")
        assertTrue(history.contains("Trip completed. Earned $45.5"))
    }

    @Test
    fun testGetVehicleHistory() {
        val manager = FleetManager()
        val res = manager.getVehicleHistory("NON_EXISTENT")
        assertEquals(listOf("Vehicle not found."), res)
    }

    @Test
    fun testTotalFleetEarnings() {
        val manager = FleetManager()
        manager.registerVehicle("V1", "Alice")
        manager.registerVehicle("V2", "Bob")
        
        manager.dispatchVehicle("V1", "A")
        manager.completeTrip("V1", 100.0)
        
        manager.dispatchVehicle("V2", "B")
        manager.completeTrip("V2", 250.5)
        
        assertEquals(350.5, manager.totalFleetEarnings())
    }

    @Test
    fun testApplySurgeBonus() {
        val manager = FleetManager()
        manager.registerVehicle("V1", "Alice")
        manager.dispatchVehicle("V1", "A")
        manager.completeTrip("V1", 1000.0) // Eligible
        
        manager.registerVehicle("V2", "Bob")
        manager.dispatchVehicle("V2", "B")
        manager.completeTrip("V2", 400.0) // Ineligible
        
        val count = manager.applySurgeBonus()
        assertEquals(1, count)
        
        assertEquals(1500.0, manager.totalFleetEarnings()) // 1000 + 100 bonus + 400
        val history = manager.getVehicleHistory("V1")
        assertTrue(history.contains("Surge Bonus Applied"))
    }
}
