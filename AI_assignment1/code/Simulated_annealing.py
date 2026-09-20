import math
import random
import matplotlib.pyplot as plt


#core 3 functions stated in the file
def booth_function(x, y):
    return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2


def himmelblau_function(x, y):
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


def griewank_function(x, y):
    return (
        1
        + (x ** 2 + y ** 2) / 4000
        - math.cos(x) * math.cos(y / math.sqrt(2))
    )


#used to generate the values close to the current value
def generate_neighbor(
    current_x,
    current_y,
    lower_bound,
    upper_bound,
    neighborhood_size,
    random_generator
):
    """
    Generate a nearby point.

    neighborhood_size = 0.5 means x and y can each change
    by a random value between -0.5 and +0.5.
    """

    while True:
        change_in_x = random_generator.uniform(
            -neighborhood_size,
            neighborhood_size
        )

        change_in_y = random_generator.uniform(
            -neighborhood_size,
            neighborhood_size
        )

        candidate_x = current_x + change_in_x
        candidate_y = current_y + change_in_y

        #accepy the candidate only if it is inside the bounds.
        if (
            lower_bound <= candidate_x <= upper_bound
            and lower_bound <= candidate_y <= upper_bound
        ):
            return candidate_x, candidate_y

#sa implementation
def simulated_annealing(
    objective_function,
    bounds,
    mode="min",
    neighborhood_size=0.5,
    starting_temperature=1.0,
    cooling_amount=0.1,
    iterations_per_temperature=100,
    seed=None
):
    """
    Apply Simulated Annealing to a two-variable function.

    Parameters from assignment:
        neighborhood_size = 0.5
        starting_temperature = 1.0
        cooling_amount = 0.1
        iterations_per_temperature = 100

    mode:
        "min" finds a minimum
        "max" finds a maximum
    """

    if mode not in ("min", "max"):
        raise ValueError("mode must be either 'min' or 'max'")

    lower_bound, upper_bound = bounds

    #random number
    random_generator = random.Random(seed)

    #random solution geenrator

    current_x = random_generator.uniform(
        lower_bound,
        upper_bound
    )

    current_y = random_generator.uniform(
        lower_bound,
        upper_bound
    )

    current_value = objective_function(
        current_x,
        current_y
    )

    #at start, the current solution is also the best.
    best_x = current_x
    best_y = current_y
    best_value = current_value

    #lists for graphs in part 2 

    iteration_history = []
    x_history = []
    y_history = []
    objective_history = []
    best_history = []
    temperature_history = []

    temperature = starting_temperature
    iteration = 0

    #until temp 0 continue
    while temperature > 0:

        #100 iterations at this temperature.
        for _ in range(iterations_per_temperature):

            iteration += 1

            #generate nearby candidate
            candidate_x, candidate_y = generate_neighbor(
                current_x=current_x,
                current_y=current_y,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
                neighborhood_size=neighborhood_size,
                random_generator=random_generator
            )

            candidate_value = objective_function(
                candidate_x,
                candidate_y
            )

            #determine whether candidate is better
            if mode == "min":
                #negative loss means candidate is smaller/better.
                loss = candidate_value - current_value

            else:
                #maximization, larger values are better.
                loss = current_value - candidate_value

            #accept or reject candidate

            if loss <= 0:
                #better or equal candidate: always accept.
                accept_candidate = True

            else:
                #worse candidate: calculate acceptance probability by the formula
                acceptance_probability = math.exp(
                    -loss / temperature
                )

                random_number = random_generator.random()

                accept_candidate = (
                    random_number < acceptance_probability
                )

            #update current solution if accepted

            if accept_candidate:
                current_x = candidate_x
                current_y = candidate_y
                current_value = candidate_value

            #update best solution

            if mode == "min":
                current_is_better = current_value < best_value
            else:
                current_is_better = current_value > best_value

            if current_is_better:
                best_x = current_x
                best_y = current_y
                best_value = current_value

            #record information for graphs

            iteration_history.append(iteration)
            x_history.append(current_x)
            y_history.append(current_y)
            objective_history.append(current_value)
            best_history.append(best_value)
            temperature_history.append(temperature)

        #reduce temperature after K iterations

        temperature = round(
            temperature - cooling_amount,
            10
        )

    # Return the answer and all recorded graph data.
    return {
        "best_x": best_x,
        "best_y": best_y,
        "best_value": best_value,

        "iterations": iteration_history,
        "x_history": x_history,
        "y_history": y_history,
        "objective_history": objective_history,
        "best_history": best_history,
        "temperature_history": temperature_history
    }


#optional repeat because sa is random
#forpart 3 of assignment

def run_with_restarts(
    objective_function,
    bounds,
    mode="min",
    number_of_runs=1,
    base_seed=42
):
    """
    Run Simulated Annealing several times and keep the best run.

    This is helpful because Simulated Annealing is random.
    """

    best_result = None

    for run_number in range(number_of_runs):

        result = simulated_annealing(
            objective_function=objective_function,
            bounds=bounds,
            mode=mode,

                #assingment parameters
            neighborhood_size=0.5,
            starting_temperature=1.0,
            cooling_amount=0.1,
            iterations_per_temperature=100,

            # Different but reproducible seed for each run
            seed=base_seed + run_number
        )

        if best_result is None:
            best_result = result

        elif mode == "min":
            if result["best_value"] < best_result["best_value"]:
                best_result = result

        else:
            if result["best_value"] > best_result["best_value"]:
                best_result = result

    return best_result

#plot for x, y and f(x,y)
def plot_results(function_name, result):
    """
    Produce the graphs required in Question 2(b).

    Top graph:
        f(x,y) over iterations

    Bottom graph:
        x and y over iterations
    """

    iterations = result["iterations"]

    figure, axes = plt.subplots(
        2,
        1,
        figsize=(10, 7),
        sharex=True
    )

    #objective function graph

    axes[0].plot(
        iterations,
        result["objective_history"],
        color="red",
        label="Current f(x,y)"
    )

    axes[0].plot(
        iterations,
        result["best_history"],
        color="black",
        linestyle="--",
        linewidth=1.5,
        label="Best f(x,y)"
    )

    axes[0].set_title(
        f"{function_name}: Simulated Annealing"
    )

    axes[0].set_ylabel("Objective value f(x,y)")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    #x and y graph

    axes[1].plot(
        iterations,
        result["x_history"],
        color="blue",
        label="x"
    )

    axes[1].plot(
        iterations,
        result["y_history"],
        color="green",
        linestyle="--",
        label="y"
    )

    axes[1].set_xlabel("Iteration")
    axes[1].set_ylabel("Value")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.tight_layout()

    output_filename = (
        function_name.lower().replace(" ", "_")
        + "_simulated_annealing.png"
    )

    plt.savefig(
        output_filename,
        dpi=200
    )

    plt.close()

    print(f"Graph saved as: {output_filename}")


def run_normal():
    print("\n" + "#" * 50)
    print("RUNNING WITH NORMAL DEFAULTS")
    print("#" * 50)
    
    problems = [
        {
            "name": "Booth Normal",
            "function": booth_function,
            "bounds": (-10, 10),
            "params": {"neighborhood_size": 0.5, "starting_temperature": 1.0, "cooling_amount": 0.1, "iterations_per_temperature": 100}
        },
        {
            "name": "Himmelblau Normal",
            "function": himmelblau_function,
            "bounds": (-5, 5),
            "params": {"neighborhood_size": 0.5, "starting_temperature": 1.0, "cooling_amount": 0.1, "iterations_per_temperature": 100}
        },
        {
            "name": "Griewank Normal",
            "function": griewank_function,
            "bounds": (-30, 30),
            "params": {"neighborhood_size": 0.5, "starting_temperature": 1.0, "cooling_amount": 0.1, "iterations_per_temperature": 100}
        }
    ]

    for problem in problems:
        print("\n" + "=" * 50)
        print(f"Running {problem['name']}")
        print("=" * 50)

        best_result = None
        n_runs = 1

        for run_number in range(n_runs):
            result = simulated_annealing(
                objective_function=problem["function"],
                bounds=problem["bounds"],
                mode="min",
                **problem["params"],
                seed=42 + run_number
            )

            if best_result is None or result["best_value"] < best_result["best_value"]:
                best_result = result

        best_index = best_result["best_history"].index(best_result["best_value"])
        best_iteration = best_result["iterations"][best_index]
        best_temperature = best_result["temperature_history"][best_index]

        print(f"Normal Parameters Used:")
        for k, v in problem["params"].items():
            print(f"  {k}: {v}")
        print("-" * 30)
        print(f"Best x = {best_result['best_x']:.6f}")
        print(f"Best y = {best_result['best_y']:.6f}")
        print(f"Best f(x,y) = {best_result['best_value']:.10f}")
        print(f"Best found at iteration = {best_iteration}")
        print(f"Temperature at best = {best_temperature:.1f}")

        plot_results(
            function_name=problem["name"],
            result=best_result
        )


def run_fine_tuned():
    print("\n" + "#" * 50)
    print("RUNNING WITH FINE-TUNED PARAMETERS (5 Restarts)")
    print("#" * 50)
    
    problems = [
        {
            "name": "Booth Finetuned",
            "function": booth_function,
            "bounds": (-10, 10),
            "params": {"neighborhood_size": 0.25, "starting_temperature": 5.0, "cooling_amount": 0.05, "iterations_per_temperature": 100}
        },
        {
            "name": "Himmelblau Finetuned",
            "function": himmelblau_function,
            "bounds": (-5, 5),
            "params": {"neighborhood_size": 0.25, "starting_temperature": 5.0, "cooling_amount": 0.05, "iterations_per_temperature": 100}
        },
        {
            "name": "Griewank Finetuned",
            "function": griewank_function,
            "bounds": (-30, 30),
            "params": {"neighborhood_size": 1.0, "starting_temperature": 5.0, "cooling_amount": 0.05, "iterations_per_temperature": 100}
        }
    ]

    for problem in problems:
        print("\n" + "=" * 50)
        print(f"Running {problem['name']}")
        print("=" * 50)

        best_result = None
        n_runs = 5

        for run_number in range(n_runs):
            result = simulated_annealing(
                objective_function=problem["function"],
                bounds=problem["bounds"],
                mode="min",
                **problem["params"],
                seed=42 + run_number
            )

            if best_result is None or result["best_value"] < best_result["best_value"]:
                best_result = result

        best_index = best_result["best_history"].index(best_result["best_value"])
        best_iteration = best_result["iterations"][best_index]
        best_temperature = best_result["temperature_history"][best_index]

        print(f"Fine-tuned Parameters Used:")
        for k, v in problem["params"].items():
            print(f"  {k}: {v}")
        print("-" * 30)
        print(f"Best x = {best_result['best_x']:.6f}")
        print(f"Best y = {best_result['best_y']:.6f}")
        print(f"Best f(x,y) = {best_result['best_value']:.10f}")
        print(f"Best found at iteration = {best_iteration}")
        print(f"Temperature at best = {best_temperature:.1f}")

        plot_results(
            function_name=problem["name"],
            result=best_result
        )

def main():
    run_normal()
    run_fine_tuned()

if __name__ == "__main__":
    main()
