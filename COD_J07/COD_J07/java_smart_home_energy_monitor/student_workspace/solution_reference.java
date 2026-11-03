import java.util.*;

class ConstantLoadDevice extends Device {
    public ConstantLoadDevice(String name, double basePower) {
        super(name, basePower);
    }

    @Override
    public double calculateEnergyConsumption(int hours) {
        return basePower * hours;
    }
}

class VariableLoadDevice extends Device {
    private double dutyCycle;

    public VariableLoadDevice(String name, double basePower, double dutyCycle) {
        super(name, basePower);
        this.dutyCycle = dutyCycle;
    }

    public double getDutyCycle() {
        return dutyCycle;
    }

    @Override
    public double calculateEnergyConsumption(int hours) {
        return basePower * hours * dutyCycle;
    }
}

class SmartHomeService {
    public double calculateTotalConsumption(List<Device> devices, int hours) {
        if (devices == null) {
            return 0.0;
        }
        double total = 0.0;
        for (Device dev : devices) {
            total += dev.calculateEnergyConsumption(hours);
        }
        return total;
    }

    public Device getPeakConsumingDevice(List<Device> devices, int hours) {
        if (devices == null || devices.isEmpty()) {
            return null;
        }
        Device peak = null;
        double maxConsumption = -1.0;
        for (Device dev : devices) {
            double cons = dev.calculateEnergyConsumption(hours);
            if (cons > maxConsumption) {
                maxConsumption = cons;
                peak = dev;
            }
        }
        return peak;
    }

    public void monitorLoad(List<Device> devices, double maxLimit) throws PowerOverloadException {
        if (devices == null) {
            return;
        }
        double totalLoad = 0.0;
        for (Device dev : devices) {
            totalLoad += dev.getBasePower();
        }
        if (totalLoad > maxLimit) {
            throw new PowerOverloadException("Overload detected: Current load is " + totalLoad + "W, which exceeds limit of " + maxLimit + "W.");
        }
    }
}
