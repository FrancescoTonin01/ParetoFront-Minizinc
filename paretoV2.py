import argparse
import asyncio
from enum import Enum
from typing import AsyncIterator, List, Tuple
from minizinc import Instance, Result, Model, Solver
import matplotlib.pyplot as plt
import re
import tempfile
import os


class OptDirection(Enum):
    MAXIMIZE = 1
    MINIMIZE = 2

    def cmp_op(self) -> str:
        if self == OptDirection.MAXIMIZE:
            return ">"
        elif self == OptDirection.MINIMIZE:
            return "<"
        else:
            raise ValueError("Invalid optimization direction")

    def better(self, a, b) -> bool:
        if self == OptDirection.MAXIMIZE:
            return a > b
        elif self == OptDirection.MINIMIZE:
            return a < b
        else:
            raise ValueError("Invalid optimization direction")


async def pareto_solutions(
    inst: Instance, objectives: List[Tuple[str, OptDirection]], *args, **kwargs
) -> AsyncIterator[Result]:
    with inst.branch() as branch:
        result = await branch.solve_async(*args, **kwargs)
        while result.status.has_solution():
            yield result
            branch.add_string(
                "constraint "
                + "\\/".join(
                    [
                        f"({name} {o.cmp_op()} {result[name]})"
                        for (name, o) in objectives
                    ]
                )
                + ";"
            )
            result = await branch.solve_async(*args, **kwargs)


async def pareto_front(
    inst: Instance, objectives: List[Tuple[str, OptDirection]], *args, **kwargs
) -> List[Result]:
    solns = []
    async for res in pareto_solutions(inst, objectives, *args, **kwargs):
        is_dominated = False
        solns_to_remove = []
        for existing_sol in solns:
            if all(o.better(res[name], existing_sol[name]) or res[name] == existing_sol[name] for name, o in objectives) and \
               any(o.better(res[name], existing_sol[name]) for name, o in objectives):
                solns_to_remove.append(existing_sol)
            elif all(o.better(existing_sol[name], res[name]) or existing_sol[name] == res[name] for name, o in objectives) and \
                 any(o.better(existing_sol[name], res[name]) for name, o in objectives):
                is_dominated = True
                break
        if not is_dominated:
            solns = [sol for sol in solns if sol not in solns_to_remove]
            solns.append(res)
    return solns


    # Extract x_values and y_values based on the variables
    x_var, y_var = variables[0][0], variables[1][0] if len(variables) > 1 else None
    x_values = [res[x_var] for res in solns]
    y_values = [res[y_var] for res in solns] if y_var else [0] * len(x_values)

    # Check if all corresponding pairs of x_values and y_values are equal
    if y_var:
        all_equal = all(x == y for x, y in zip(x_values, y_values))
        if all_equal:
            # If all pairs are equal, create a new array with only x_values
            res = x_values
            x_values = [pair[0] for pair in res] 
            y_values = [pair[1] for pair in res]
            new_res = [{"x": x, "y": y} for x, y in zip(x_values, y_values)]
            print("All corresponding pairs of x_values and y_values are equal.")
            print("Recalculating Pareto front with new array.")

            # Recalculate Pareto front with the new array
            solns = []
            for res in new_res:
                is_dominated = False
                solns_to_remove = []
                for existing_sol in solns:
                    if all(res[name] <= existing_sol[name] for name in ["x", "y"]) and \
                       any(res[name] < existing_sol[name] for name in ["x", "y"]):
                        solns_to_remove.append(existing_sol)
                    elif all(existing_sol[name] <= res[name] for name in ["x", "y"]) and \
                         any(existing_sol[name] < res[name] for name in ["x", "y"]):
                        is_dominated = True
                        break
                if not is_dominated:
                    solns = [sol for sol in solns if sol not in solns_to_remove]
                    solns.append(res)
    else:
        print("y_var does not exist; cannot perform comparison.")

    return solns


def extract_and_remove_solve_statement(file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    objectives = []
    onearray = False
    twoarrays = False

    for line in lines:
        if line.startswith("solve"):
            # Controllo il numero di parentesi quadre
            if line.count('[') == 2:
                onearray = True
            elif line.count('[') == 4:
                twoarrays = True

            # Modifica l'espressione regolare
            matches = re.findall(r'(maximize|minimize)\s+(\w+(?:\[\d+\])?)', line)

            if matches:
                objectives = [
                    (var, OptDirection.MAXIMIZE if direction == 'maximize' else OptDirection.MINIMIZE)
                    for direction, var in matches
                ]
        else:
            new_lines.append(line)

    # Controllo se ci sono variabili con "[]" negli obiettivi
    array_vars = [var for var, _ in objectives if '[' in var]
    helper =["bbb","ccc"]
    if array_vars:
        # Aggiungo linee nel file temporaneo se trovo variabili con "[]"
        print(array_vars)
        for var in array_vars:
            new_lines.append(f'var int: {helper};\n')
            new_lines.append(f'constraint {helper} = {var};\n')

    # Creazione del file temporaneo
    temp_model_file = file_path.replace(".mzn", "_temp.mzn")
    with open(temp_model_file, 'w') as temp_file:
        temp_file.writelines(new_lines)

    return objectives, temp_model_file, onearray, twoarrays


def main(model_file: str, data_file: str = None):
    onearray= False
    twoarrays=False
    # Extract and remove the solve statement before loading the model
    variables, temp_model_file, onearray, twoarrays = extract_and_remove_solve_statement(model_file)

    if not variables:
        print("No variables specified for optimization. Exiting.")
        return

    print("Finding solutions...")

    # Load the MiniZinc model after modifying the file
    model = Model(temp_model_file)
    if data_file:
        model.add_file(data_file)

    gecode = Solver.lookup("gecode")
    instance = Instance(gecode, model)
    
    results = asyncio.run(pareto_front(instance, variables))
    x_var, y_var = variables[0][0], variables[1][0] if len(variables) > 1 else None
    x_values = [res[x_var] for res in results]
    y_values = [res[y_var] for res in results] if y_var else [0] * len(x_values)
    # Check if all corresponding pairs of x_values and y_values are equal
    if y_var:  # Ensure y_values exists
    	all_equal = all(x == y for x, y in zip(x_values, y_values))
    	if all_equal:
      	  # Create an array with only the x_values if all pairs (x, y) are equal
          res = x_values
          x_values = [pair[0] for pair in res] 
          y_values = [pair[1] for pair in res]
          print("All corresponding pairs of x_values and y_values are equal.")
          print("New array with only x_values:", res)
    	else:
        # Handle the case where not all pairs are equal (optional)
       	  print("Not all corresponding pairs of x_values and y_values are equal.")
    else:
    # Handle the case where y_var does not exist (optional)
    	print("y_var does not exist; cannot perform comparison.")

    for res in results:
        print(", ".join(f"{var}: {res[var]}" for var, _ in variables))
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x_values, y_values, color='blue', s=100)
    
    for x, y in zip(x_values, y_values):
        plt.annotate(f'({x}, {y})', (x, y), xytext=(5, 5), textcoords='offset points')
    
    plt.xlabel(x_var)
    plt.ylabel(y_var if y_var else "")
    plt.title(f'Pareto Front: {x_var} vs {y_var}' if y_var else f'Pareto Front: {x_var}')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    os.remove(temp_model_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a MiniZinc model and find the Pareto front.")
    parser.add_argument("model_file", type=str, help="Path to the MiniZinc model file (.mzn)")
    parser.add_argument("--data_file", type=str, default=None, help="Optional path to the MiniZinc data file (.dzn)")

    args = parser.parse_args()

    main(args.model_file, args.data_file)
