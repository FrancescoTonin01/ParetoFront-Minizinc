# Pareto Front Solver for MiniZinc Models

## Overview

This project provides a Python script to solve MiniZinc models and find the Pareto front for multi-objective optimization problems. It handles scenarios where MiniZinc models involve multiple objectives, either to maximize or minimize. The script also supports visualization of the Pareto front when two objectives are present.

## Features

- **Pareto Front Computation**: Automatically computes and extracts the Pareto front from a MiniZinc model with multiple objectives.
- 
- **Multi-Objective Handling**: Supports both maximization and minimization objectives, even when objectives are expressed as arrays.
- 
- **Visualization**: Generates a scatter plot for the Pareto front when dealing with two objectives, showing the trade-offs between them.
- 
- **Dynamic Model Handling**: Modifies the MiniZinc model on the fly to compute the Pareto front without altering the original model file.

## Installation

### Prerequisites

- **Python 3.7+**: Ensure you have Python installed.
- **MiniZinc**: The MiniZinc solver is required to run the models. Install it from [MiniZinc.org](https://www.minizinc.org/).
- **Required Python Packages**: You can install the necessary Python packages using:

  ```sh
  pip install matplotlib minizinc

### Clone the repository

  ```sh
  git clone https://github.com/FrancescoTonin01/ParetoFront-Minizinc/
  cd ParetoFront-Minizinc
  ```

### Or simply just download it

## Usage

To use the script, you need a MiniZinc model file (.mzn) and optionally, a data file (.dzn).

### Running the script

Use the following command to run the script:

  ```sh
  python paretoV2.py path/to/your_model.mzn --data_file path/to/your_data.dzn
  ```

- **model_file**: Path to your MiniZinc model file (.mzn)
- **data_file**(Optional): Path to your MiniZinc data file (.dzn)

### Example Command

  ```sh
  python paretoV2.py examples/example.mzn
  ```

###Output

  ```sh
  x: 8, y: 16
  x: 10, y: 15
  x: 40, y: 0
  x: 38, y: 1
  x: 36, y: 2
  x: 34, y: 3
  x: 32, y: 4
  x: 30, y: 5
  x: 28, y: 6
  x: 26, y: 7
  x: 24, y: 8
  x: 22, y: 9
  x: 20, y: 10
  x: 18, y: 11
  x: 16, y: 12
  x: 14, y: 13
  x: 12, y: 14
```

## Important Note on Writing the `solve` Statement

When using this script with MiniZinc models, it's important to correctly format the `solve` statement, especially for multi-objective optimization problems.

### Single Objective Problems

For single-objective problems, the `solve` statement can be written as usual, such as:

  ```minizinc
  solve maximize x;
  ```

### Multi-Objective Problems

For multi-objective problems, you need to include both objectives in the solve statement. The solve statement should specify the objectives in a list format, where you can either maximize or minimize each variable. The script supports various combinations, such as:

- **Minimize one objective and maximize another**(works both way):

    ```minizinc
    solve minimize var1, maximize var2;
    ```
    
- **Maximize both objectives**:

    ```minizinc
    solve maximize var1, maximize var2;
    ```
    
- **Minimize both objectives**:

    ```minizinc
    solve minimize var1, minimize var2;
    ```

## Important Note on Objective Variables (NEW)

- **Array Elements**: If you need to use array elements as objectives, you can specify a single element from an array of integers. For example, if `x` is an array, you can use `x[1]` as an objective.

## How it works

The script works by:

1-**Extracting and Removing the Solve Statement**: the script processes the MiniZinc model to extract the objectives and removes the original solve statement;

2-**Generating Pareto Front**: the script iteratively finds solutions that form the Pareto front by solving the model repeatedly and adding constraints to exclude previously found solutions that are dominated by new ones;

3-**Visualization**: finally, the script generates a scatter plot to visualize the Pareto front;

