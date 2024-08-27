# Pareto Front Solver for MiniZinc Models

## Overview

This project provides a Python script to solve MiniZinc models and find the Pareto front for multi-objective optimization problems. It handles scenarios where MiniZinc models involve multiple objectives, either to maximize or minimize. The script also supports visualization of the Pareto front when two objectives are present.

## Features

- **Pareto Front Computation**: Automatically computes and extracts the Pareto front from a MiniZinc model with multiple objectives.
- **Multi-Objective Handling**: Supports both maximization and minimization objectives, even when objectives are expressed as arrays.
- **Visualization**: Generates a scatter plot for the Pareto front when dealing with two objectives, showing the trade-offs between them.
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

