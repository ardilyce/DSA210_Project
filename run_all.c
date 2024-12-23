#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void run_script(const char *script) {
    char command[256];
    int status;

    // Construct the system command to run the Python script
    snprintf(command, sizeof(command), "python3 %s", script);

    printf("Running %s...\n", script);

    // Execute the command
    status = system(command);

    // Check the exit status
    if (status == 0) {
        printf("%s ran successfully.\n\n", script);
    } else {
        printf("Error occurred while running %s. Stopping execution.\n", script);
        exit(EXIT_FAILURE);  // Exit the program if a script fails
    }
}

int main() {
    // List of Python scripts to run
    const char *scripts[] = {
        "scripts/analyze_openings.py",
        "scripts/analyze_outcomes.py",
        "scripts/analyze_time_management.py",
        "scripts/visualize.py"
    };

    int num_scripts = sizeof(scripts) / sizeof(scripts[0]);

    // Run each script sequentially
    for (int i = 0; i < num_scripts; i++) {
        run_script(scripts[i]);
    }

    printf("All analyses completed successfully!\n");

    return 0;
}
