import org.junit.jupiter.api.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue
import kotlin.test.assertFalse

class SmartHomeTest {

    @Test
    fun testAddDevice() {
        val system = SmartHomeSystem()
        val res = system.addDevice("D1", "Light", 15.0)
        assertEquals("Device D1 added.", res)
        val history = system.getDeviceHistory("D1")
        assertEquals(1, history.size)
        assertEquals("Device Light installed.", history[0])
    }

    @Test
    fun testToggleDevice() {
        val system = SmartHomeSystem()
        system.addDevice("D1", "Light", 15.0)
        
        val resOn = system.toggleDevice("D1", true)
        assertEquals("Device D1 is now ON.", resOn)
        var history = system.getDeviceHistory("D1")
        assertEquals(2, history.size)
        assertEquals("Device turned ON", history[1])

        val resOff = system.toggleDevice("D1", false)
        assertEquals("Device D1 is now OFF.", resOff)
        history = system.getDeviceHistory("D1")
        assertEquals(3, history.size)
        assertEquals("Device turned OFF", history[2])
    }

    @Test
    fun testScheduleTimer() {
        val system = SmartHomeSystem()
        system.addDevice("D1", "Light", 15.0)
        
        // Valid schedule
        val res1 = system.scheduleTimer("D1", 30)
        assertEquals("Timer set for D1.", res1)
        
        // Invalid (Already ON)
        system.toggleDevice("D1", true)
        val res2 = system.scheduleTimer("D1", 15)
        assertEquals("Device is already ON.", res2)
        
        val history = system.getDeviceHistory("D1")
        assertTrue(history.contains("Scheduled to turn ON in 30 mins"))
    }

    @Test
    fun testGetDeviceHistory() {
        val system = SmartHomeSystem()
        // Device not found
        val res = system.getDeviceHistory("NON_EXISTENT")
        assertEquals(listOf("Device not found."), res)
    }

    @Test
    fun testTotalPowerConsumption() {
        val system = SmartHomeSystem()
        system.addDevice("D1", "Light", 15.0)
        system.addDevice("D2", "Thermostat", 1500.0)
        system.addDevice("D3", "Fan", 50.0)

        system.toggleDevice("D1", true)
        system.toggleDevice("D2", true)
        
        assertEquals(1515.0, system.totalPowerConsumption())
    }

    @Test
    fun testTurnOffAllDevices() {
        val system = SmartHomeSystem()
        system.addDevice("D1", "Light", 15.0)
        system.addDevice("D2", "Thermostat", 1500.0)
        
        system.toggleDevice("D1", true)
        system.toggleDevice("D2", true)
        
        val count = system.turnOffAllDevices()
        assertEquals(2, count)
        
        assertEquals(0.0, system.totalPowerConsumption())
        val history = system.getDeviceHistory("D1")
        assertTrue(history.contains("Turned OFF by Hub"))
    }
}
