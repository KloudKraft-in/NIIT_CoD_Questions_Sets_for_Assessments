import java.util.*;
import java.lang.reflect.*;

/* 
 * ==========================================================
 * LOCKED CODE - DO NOT MODIFY
 * ==========================================================
 */

abstract class Device {
    protected String name;
    protected double basePower;

    public Device(String name, double basePower) {
        this.name = name;
        this.basePower = basePower;
    }

    public String getName() {
        return name;
    }

    public double getBasePower() {
        return basePower;
    }

    public abstract double calculateEnergyConsumption(int hours);
}

class PowerOverloadException extends Exception {
    public PowerOverloadException(String message) {
        super(message);
    }
}

class HarnessJ07 {
    public static void main(String[] args) {
        try {
            try (Scanner sc = new Scanner(System.in)) {
                if (!sc.hasNextInt()) return;
                int n = Integer.parseInt(sc.nextLine());

                List<Device> devices = new ArrayList<>();
                for (int i = 0; i < n; i++) {
                    if (!sc.hasNextLine()) break;
                    String line = sc.nextLine();
                    String[] parts = line.split(" ");
                    if (parts.length < 3) continue;

                    String type = parts[0];
                    String name = parts[1];
                    double basePower = Double.parseDouble(parts[2]);

                    if (type.equalsIgnoreCase("Constant")) {
                        Class<?> clazz = Class.forName("ConstantLoadDevice");
                        Constructor<?> ctor = clazz.getConstructor(String.class, double.class);
                        devices.add((Device) ctor.newInstance(name, basePower));
                    } else if (type.equalsIgnoreCase("Variable")) {
                        double dutyCycle = parts.length > 3 ? Double.parseDouble(parts[3]) : 1.0;
                        Class<?> clazz = Class.forName("VariableLoadDevice");
                        Constructor<?> ctor = clazz.getConstructor(String.class, double.class, double.class);
                        devices.add((Device) ctor.newInstance(name, basePower, dutyCycle));
                    }
                }

                if (!sc.hasNextLine()) return;
                String finalLine = sc.nextLine();
                String[] fParts = finalLine.split(" ");
                if (fParts.length < 2) return;

                int hours = Integer.parseInt(fParts[0]);
                double maxLimit = Double.parseDouble(fParts[1]);

                // Create SmartHomeService via reflection
                Class<?> serviceClass = Class.forName("SmartHomeService");
                Object service = serviceClass.getDeclaredConstructor().newInstance();
                
                // Invoke calculateTotalConsumption
                Method calcMethod = serviceClass.getMethod("calculateTotalConsumption", List.class, int.class);
                double totalConsumption = (double) calcMethod.invoke(service, devices, hours);
                System.out.printf(Locale.US, "Total Consumption: %.2f Wh\n", totalConsumption);

                // Invoke getPeakConsumingDevice
                Method peakMethod = serviceClass.getMethod("getPeakConsumingDevice", List.class, int.class);
                Device peak = (Device) peakMethod.invoke(service, devices, hours);
                if (peak != null) {
                    System.out.println("Peak Device: " + peak.getName());
                } else {
                    System.out.println("Peak Device: None");
                }

                // Invoke monitorLoad
                Method monitorMethod = serviceClass.getMethod("monitorLoad", List.class, double.class);
                try {
                    monitorMethod.invoke(service, devices, maxLimit);
                } catch (InvocationTargetException e) {
                    Throwable cause = e.getCause();
                    if (cause instanceof PowerOverloadException) {
                        System.out.println("Error: " + cause.getMessage());
                    } else {
                        System.out.println("Execution Error: " + cause.getMessage());
                    }
                }
            }
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
