import sys
import time

def print_progress_bar(iteration, total, prefix='', suffix='', length=40, fill='█'):
    """
    Print a text-based progress bar to the console.

    Parameters:
    - iteration : current iteration (int)
    - total     : total iterations (int)
    - prefix    : prefix string (optional)
    - suffix    : suffix string (optional)
    - length    : character length of bar (optional)
    - fill      : bar fill character (optional)
    """
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()  # newline on complete

# -----------------------------
# Example usage
# -----------------------------
total_steps = 50
for i in range(total_steps + 1):
    print_progress_bar(i, total_steps, prefix='Progress', suffix='Complete')
    time.sleep(0.05)  # simulate work