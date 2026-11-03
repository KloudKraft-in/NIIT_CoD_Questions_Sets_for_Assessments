class Wallet(val walletId: String, val pin: Int, var balance: Double) {
    val transactionLog: MutableList<String> = mutableListOf("Seed Deposit: $$balance")
}

class CryptoExchangeSystem {
    private val walletRegistry: MutableMap<String, Wallet> = mutableMapOf()

    fun createWallet(walletId: String, pin: Int, initialDeposit: Double): String {
        val wallet = Wallet(walletId, pin, initialDeposit)
        walletRegistry[walletId] = wallet
        return "Wallet $walletId added."
    }

    fun receiveCrypto(walletId: String, amount: Double): String {
        val wallet = walletRegistry[walletId]
        return if (wallet != null) {
            wallet.balance += amount
            wallet.transactionLog.add("Received $$amount")
            "Success. Current Balance: $${wallet.balance}"
        } else {
            "Wallet not found."
        }
    }

    fun spendCrypto(walletId: String, pin: Int, amount: Double): String {
        val wallet = walletRegistry[walletId] ?: return "Security/Access Error."
        
        if (wallet.pin != pin) {
            return "Security/Access Error."
        }
        
        if (wallet.balance < amount) {
            return "Insufficient funds."
        }
        
        wallet.balance -= amount
        wallet.transactionLog.add("Spent $$amount")
        return "Spent $$amount"
    }

    fun getTransactionLog(walletId: String): List<String> {
        val wallet = walletRegistry[walletId]
        return wallet?.transactionLog ?: listOf("Wallet not found.")
    }

    fun totalNetworkLiquidity(): Double {
        return walletRegistry.values.sumOf { it.balance }
    }

    fun applyStakingRewards(): Int {
        var count = 0
        for (wallet in walletRegistry.values) {
            if (wallet.balance > 1000.0) {
                wallet.balance += wallet.balance * 0.05
                wallet.transactionLog.add("Staking Reward")
                count++
            }
        }
        return count
    }
}
