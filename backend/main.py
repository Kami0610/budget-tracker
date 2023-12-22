from display import BudgetTrackerApp
import tkinter as tk
import utility


if __name__ == "__main__":
    # Initialize data directory for holding tracker and user data
    utility.init_directories()

    # Load data from tracker and user data files
    load_user = utility.load_user_dat()
    load_exp = utility.load_tracker()

    # Run application
    root = tk.Tk()
    app = BudgetTrackerApp(root, load_user, load_exp)
    app.run()
