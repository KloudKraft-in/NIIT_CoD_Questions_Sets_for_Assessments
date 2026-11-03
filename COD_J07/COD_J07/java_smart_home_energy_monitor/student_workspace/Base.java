import java.util.*;

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
