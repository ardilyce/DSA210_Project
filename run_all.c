/*******************************************************
 * Program Overview:
 * This program is designed to execute a series of 
 * Python scripts sequentially. The scripts are stored 
 * in the 'scripts/' directory and are executed in the 
 * order specified in the 'scripts' array.
 *
 * Functionality:
 * - Reads preprocessed chess game data from a JSON file.
 * - Engineers features like 'Rating Differential.'
 * - Trains a Random Forest Classifier to predict 
 *   game outcomes ('Win', 'Draw', 'Loss').
 * - Evaluates the model's performance using accuracy 
 *   and classification metrics.
 * - Analyzes the effectiveness of chess openings by 
 *   calculating win rates and visualizes them in a bar chart.
 *
 * Usage:
 * - Run this program from the command line.
 * - Ensure the scripts are correctly placed in the 
 *   'scripts/' and 'ml/ml_models' directories before execution.
 *
 ******************************************************/

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
        "scripts/visualize.py",
        "ml/ml_models/game_outcome_prediction.py",
        "ml/ml_models/opening_effectiveness.py",
    };

    int num_scripts = sizeof(scripts) / sizeof(scripts[0]);

    // Run each script sequentially
    for (int i = 0; i < num_scripts; i++) {
        run_script(scripts[i]);
    }

    printf("All analyses completed successfully!\n");

    return 0;
}
