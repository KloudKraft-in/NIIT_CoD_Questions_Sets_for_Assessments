// import java.util.*;

// /* 
//  * Implement the 'LogProcessor' class here.
//  * The 'MalformedLogException' is already defined in the Harness.
//  * DO NOT use access modifiers (e.g.: 'public') in your class declarations.
//  */

// class LogProcessor {
//     public void processLogs(List<String> logs) {
//         // Write your code here
//     }
// }
import java.util.*;

class LogProcessor {
    public void processLogs(List<String> logs) {
        for (String log : logs) {
            try {
                if (!log.startsWith("[")) {
                    throw new MalformedLogException("Log must start with a bracketed timestamp.");
                }

                String[] parts = log.split(" ");
                if (parts.length < 2) {
                    throw new MalformedLogException("Invalid log level: " + log + ".");
                }

                String level = parts[1];
                if (!(level.equals("INFO") || level.equals("WARN") || level.equals("ERROR"))) {
                    throw new MalformedLogException("Invalid log level: " + level + ".");
                }

                System.out.println("Log Processed: " + level);

            } catch (MalformedLogException e) {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }
}
