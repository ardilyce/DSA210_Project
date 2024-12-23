/* This program is written to run a series of Python scripts sequentially. The scripts are stored in the scripts/ directory. The program will run each script in the order they are listed in the scripts array. If a script fails, the program will stop execution and print an error message. Otherwise, it will print a success message after all scripts have been run. This program is written in C and uses the system function to execute the Python scripts. The program is intended to be run from the command line. */

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
