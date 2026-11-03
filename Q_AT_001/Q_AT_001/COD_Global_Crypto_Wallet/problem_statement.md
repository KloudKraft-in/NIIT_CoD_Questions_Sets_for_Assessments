# Low-Level Design (LLD) – Global Crypto Wallet
(Multi-Class Composition in Kotlin)

**Difficulty Level**: Intermediate | **Total Marks**: 10
**Design Format**: 2 Classes | 7 Methods | 7 Test Cases

**Summary of Design Requirements**
Implement a digital crypto wallet system featuring transaction histories and complex transaction limit logic.

1. **Class "Wallet" (Data Entity)**:
   - Stores: `walletId` (String), `pin` (Int), `balance` (Double), `transactionLog` (MutableList of Strings).
   - Manages state for individual user wallets.

2. **Class "CryptoExchangeSystem" (Manager)**:
   - Manages a collection of "Wallet" objects.
   - Handles secure transfers, staking rewards, and history retrieval.

**Concepts Tested**
- Class Composition in Kotlin
- MutableList/Log management within objects
- Conditional logic with multiple constraints (PIN + Balance + Gas Fees)
- Kotlin String templates ($)

**Problem Statement**
Design a crypto wallet hub where:
- Wallets track every spend/receive in a log.
- Transactions are blocked if the balance goes below 0 (No overdraft).
- Staking rewards are applied only to wallets with balance > 1000.

Each wallet object has:
- `walletId` (str)
- `pin` (int)
- `balance` (double)
- `transactionLog` (MutableList<String>)

**Operations (Methods)**

1. **Initialize structures** (Class: `Wallet` & `CryptoExchangeSystem`)
Constructors for both. Wallet log starts with `["Seed Deposit: $[val]"]`. 
`CryptoExchangeSystem` initializes an empty registry.

2. **Create Wallet** (Class: `CryptoExchangeSystem`)
`fun createWallet(walletId: String, pin: Int, initialDeposit: Double): String`
- Create Wallet instance with log.
- Return `"Wallet [walletId] added."`

3. **Secure Receive** (Class: `CryptoExchangeSystem`)
`fun receiveCrypto(walletId: String, amount: Double): String`
- Update balance AND append `"Received $[amount]"` to wallet.transactionLog.
- Return `"Success. Current Balance: $[new_balance]"`

4. **Gas-Fee Protected Spend**
`fun spendCrypto(walletId: String, pin: Int, amount: Double): String`
- Rule: PIN must match AND `(balance - amount) >= 0`.
- If valid: Deduct, log `"Spent $[amount]"`, return `"Spent $[amount]"`.
- If below 0: return `"Insufficient funds."`
- Else: return `"Security/Access Error."`

5. **Audit Trail**
`fun getTransactionLog(walletId: String): List<String>`
- Return the full list of strings from `wallet.transactionLog`.
- If not found, return `["Wallet not found."]`.

6. **Exchange Liquidity**
`fun totalNetworkLiquidity(): Double`
- Sum of all balances in the registry.
- Return Double.

7. **Bulk Staking Rewards**
`fun applyStakingRewards(): Int`
- For EVERY wallet where balance > 1000, add 5% reward and log `"Staking Reward"`.
- Return the integer count of wallets that received rewards.

**Test Cases & Marks Allocation:**
-----------------------------------------------------------------------------------------------------------------
| Test Case ID |                            Description                       |                 Method                     | Marks |
|-----------------|------------------------------------------------|------------------------------------|---------|
| TC1                 | Instantiate complex structures                 | init() (Both)                         |      0     |
| TC2                 | Add wallet with initial log                     | createWallet()                         |     1     |
| TC3                 | Receive with log tracking                         | receiveCrypto()                           |     2     |
| TC4                 | Spend with zero-balance logic                   | spendCrypto()                      |     3     |
| TC5                 | Retrieve full audit trail of wallet             | getTransactionLog()          |     1     |
| TC6                 | Calculate total network liquidity               | totalNetworkLiquidity()           |     1     |
| TC7                 | Perform bulk staking sweep                      | applyStakingRewards()             |     2     |
-------------------------------------------------------------------------------------------------------------------
|                                                      Total                                   |                                    10                           |
-----------------------------------------------------------------------------------------------------------------

**Visible Test Case Descriptions**
- **TC1**: `CryptoExchangeSystem()` should initialize the registry.
- **TC2**: `createWallet("W_01", 9999, 500.0)` creates Wallet object with log `["Seed Deposit: $500.0"]`.
- **TC3**: `receiveCrypto("W_01", 200.0)` updates balance to 700.0 and log to `["Seed Deposit...", "Received $200.0"]`.
- **TC4**: `spendCrypto("W_01", 9999, 800.0)` returns `"Insufficient funds."`.
- **TC5**: `getTransactionLog("W_01")` returns the full list of formatted strings.
- **TC6**: `totalNetworkLiquidity()` returns the Double sum of all balances.
- **TC7**: `applyStakingRewards()` credits 5% to eligible wallets and returns the count of processed items.
