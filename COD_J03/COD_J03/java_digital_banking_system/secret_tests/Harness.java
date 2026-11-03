
// REFRESHED: Standardized Harness for J03
import java.util.*;

/* 
 * ==========================================================
 * LOCKED CODE - DO NOT MODIFY
 * ==========================================================
 */

class Harness {
    public static void main(String[] args) {
        try {
            try (Scanner sc = new Scanner(System.in)) {
                if (!sc.hasNextInt())
                    return;
                int n = Integer.parseInt(sc.nextLine());

                while (n-- > 0) {
                    if (!sc.hasNextLine())
                        break;
                    String line = sc.nextLine();
                    String[] parts = line.split(" ");
                    if (parts.length < 5)
                        continue;

                    String type = parts[0];
                    String accNo = parts[1];
                    double initialBal = Double.parseDouble(parts[2]);
                    String action = parts[3];
                    double amount = Double.parseDouble(parts[4]);

                    Object account = null;
                    Class<?> accClass = null;
                    if (type.equalsIgnoreCase("Savings")) {
                        accClass = Class.forName("SavingsAccount");
                    } else if (type.equalsIgnoreCase("Current")) {
                        accClass = Class.forName("CurrentAccount");
                    }

                    if (accClass != null) {
                        java.lang.reflect.Constructor<?> ctor = accClass.getConstructor(String.class, double.class);
                        account = ctor.newInstance(accNo, initialBal);

                        java.lang.reflect.Method getBal = accClass.getMethod("getBalance");
                        if (action.equalsIgnoreCase("Deposit")) {
                            java.lang.reflect.Method deposit = accClass.getMethod("deposit", double.class);
                            deposit.invoke(account, amount);
                            System.out.println("Deposit Successful: New Balance: " + getBal.invoke(account));
                        } else if (action.equalsIgnoreCase("Withdraw")) {
                            java.lang.reflect.Method withdraw = accClass.getMethod("withdraw", double.class);
                            if ((boolean) withdraw.invoke(account, amount)) {
                                System.out.println("Withdrawal Successful: New Balance: " + getBal.invoke(account));
                            } else {
                                System.out.println("Withdrawal Failed: Minimum balance requirement not met.");
                            }
                        }
                    }
                }
            }
        } catch (Exception e) {
            // Silently handle parsing and reflection errors
        }
    }
}
