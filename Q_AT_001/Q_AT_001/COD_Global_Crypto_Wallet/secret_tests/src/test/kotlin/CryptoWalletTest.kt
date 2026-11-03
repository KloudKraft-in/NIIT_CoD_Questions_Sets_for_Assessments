import org.junit.jupiter.api.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class CryptoWalletTest {

    @Test
    fun testInstantiation() {
        val system = CryptoExchangeSystem()
        kotlin.test.assertNotNull(system)
    }

    @Test
    fun testCreateWallet() {
        val system = CryptoExchangeSystem()
        val res = system.createWallet("W1", 1234, 100.0)
        assertEquals("Wallet W1 added.", res)
        val history = system.getTransactionLog("W1")
        assertEquals(1, history.size)
        assertEquals("Seed Deposit: $100.0", history[0])
    }

    @Test
    fun testReceiveCrypto() {
        val system = CryptoExchangeSystem()
        system.createWallet("W1", 1234, 100.0)
        val res = system.receiveCrypto("W1", 50.0)
        assertEquals("Success. Current Balance: $150.0", res)
        val history = system.getTransactionLog("W1")
        assertEquals(2, history.size)
        assertEquals("Received $50.0", history[1])
    }

    @Test
    fun testSpendCrypto() {
        val system = CryptoExchangeSystem()
        system.createWallet("W1", 1234, 100.0)
        
        // Valid spend
        val res1 = system.spendCrypto("W1", 1234, 40.0)
        assertEquals("Spent $40.0", res1)
        
        // Invalid PIN
        val res2 = system.spendCrypto("W1", 9999, 10.0)
        assertEquals("Security/Access Error.", res2)
        
        // Insufficient funds
        val res3 = system.spendCrypto("W1", 1234, 100.0)
        assertEquals("Insufficient funds.", res3)
        
        val history = system.getTransactionLog("W1")
        assertTrue(history.contains("Spent $40.0"))
    }

    @Test
    fun testGetTransactionLog() {
        val system = CryptoExchangeSystem()
        // Account not found
        val res = system.getTransactionLog("NON_EXISTENT")
        assertEquals(listOf("Wallet not found."), res)
    }

    @Test
    fun testTotalLiquidity() {
        val system = CryptoExchangeSystem()
        system.createWallet("W1", 1234, 100.0)
        system.createWallet("W2", 5678, 200.0)
        assertEquals(300.0, system.totalNetworkLiquidity())
    }

    @Test
    fun testStakingRewards() {
        val system = CryptoExchangeSystem()
        system.createWallet("W1", 1234, 2000.0) // Eligible
        system.createWallet("W2", 5678, 500.0)  // Ineligible
        
        val count = system.applyStakingRewards()
        assertEquals(1, count)
        
        assertEquals(2100.0, system.totalNetworkLiquidity() - 500.0)
        val history = system.getTransactionLog("W1")
        assertTrue(history.contains("Staking Reward"))
    }
}
