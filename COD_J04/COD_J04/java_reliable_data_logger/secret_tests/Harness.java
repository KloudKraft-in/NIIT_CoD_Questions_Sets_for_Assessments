import java.util.*;


class Harness {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            if (!sc.hasNextInt()) return;
            int n = Integer.parseInt(sc.nextLine());
            List<String> logs = new ArrayList<>();
            
            while (n-- > 0) {
                if (sc.hasNextLine()) logs.add(sc.nextLine());
            }

            try {
                Class<?> processorClass = Class.forName("LogProcessor");
                java.lang.reflect.Constructor<?> ctor = processorClass.getDeclaredConstructor();
                ctor.setAccessible(true);
                Object processor = ctor.newInstance();

                java.lang.reflect.Method processMethod = processorClass.getDeclaredMethod("processLogs", List.class);
                processMethod.setAccessible(true);
                processMethod.invoke(processor, logs);
            } catch (Exception e) {
                // Silently skip if not implemented yet
            }
        }
    }
}
