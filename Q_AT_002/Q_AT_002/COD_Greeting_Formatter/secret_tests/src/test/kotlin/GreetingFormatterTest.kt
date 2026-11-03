import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class GreetingFormatterTest {

    @Test
    fun testAliceGreeting() {
        val result = formatGreeting("Alice")
        assertEquals("Hello, Alice! Welcome to Kotlin.", result)
    }

    @Test
    fun testBobGreeting() {
        val result = formatGreeting("Bob")
        assertEquals("Hello, Bob! Welcome to Kotlin.", result)
    }

    @Test
    fun testCharlieGreeting() {
        val result = formatGreeting("Charlie")
        assertEquals("Hello, Charlie! Welcome to Kotlin.", result)
    }
}
