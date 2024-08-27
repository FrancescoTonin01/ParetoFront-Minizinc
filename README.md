Pareto Front Solver for MiniZinc Models
Overview
This project provides a Python script to solve MiniZinc models and find the Pareto front for multi-objective optimization problems. It handles scenarios where MiniZinc models involve multiple objectives, either to maximize or minimize. The script also supports visualization of the Pareto front when two objectives are present.

Features
Pareto Front Computation: Automatically computes and extracts the Pareto front from a MiniZinc model with multiple objectives.
Multi-Objective Handling: Supports both maximization and minimization objectives, even when objectives are expressed as arrays.
Visualization: Generates a scatter plot for the Pareto front when dealing with two objectives, showing the trade-offs between them.
Dynamic Model Handling: Modifies the MiniZinc model on the fly to compute the Pareto front without altering the original model file.
Installation
Prerequisites
Python 3.7+: Ensure you have Python installed.

MiniZinc: The MiniZinc solver is required to run the models. Install it from MiniZinc.org.

Required Python Packages: You can install the necessary Python packages using:

sh
Copia codice
pip install matplotlib minizinc
Clone the Repository
sh
Copia codice
git clone https://github.com/your-username/pareto-front-solver.git
cd pareto-front-solver
Usage
Command-Line Interface
The script can be run directly from the command line.

Basic Command
sh
Copia codice
python pareto_front_solver.py <model_file.mzn> [--data_file <data_file.dzn>]
<model_file.mzn>: Path to your MiniZinc model file.
--data_file <data_file.dzn> (optional): Path to a MiniZinc data file if required by the model.
Example
If you have a MiniZinc model example.mzn with optional data file example.dzn, run:

sh
Copia codice
python pareto_front_solver.py example.mzn --data_file example.dzn
Output
Solutions: The script outputs the non-dominated solutions of the objectives specified in the MiniZinc model.
Visualization: If there are two objectives, the script generates a scatter plot showing the Pareto front.
Handling Arrays in Objectives
The script can automatically manage models where objectives are specified using array indices (e.g., maximize x[1] + x[2];). It does this by creating auxiliary variables internally to process and plot the objectives.

Code Structure
pareto_front_solver.py: Main script containing all the logic for extracting objectives, computing the Pareto front, and visualizing the results.
extract_and_remove_solve_statement(): Function that extracts objectives from the solve statement in the MiniZinc model and prepares the model for optimization.
pareto_solutions(): Coroutine that yields solutions along the Pareto front.
pareto_front(): Coroutine that computes and returns the list of non-dominated solutions.
main(): The main entry point for the script, handling user inputs and invoking the optimization process.
Visualization
If your model includes two objectives, the script automatically generates a scatter plot of the Pareto front, with options to annotate the points for better readability.

Limitations
Multi-objective Limit: Currently, the visualization is only supported for two objectives. If your model has more than two objectives, it will still compute the Pareto front, but without visualization.
Array Indexing: The script assumes objectives are either scalar variables or indexed arrays. Complex indexing or nested arrays might require manual adjustments.
Contributing
Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

