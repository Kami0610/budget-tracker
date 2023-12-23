import constants as const
import utility
import tkinter as tk
from tkinter import messagebox


class BudgetTrackerApp:
    def __init__(self, root, user_dat, past_transactions):
        self.color_bg = const.COLOR_BG
        self.color_bg_sec = const.COLOR_BG_SEC
        self.color_sec = const.COLOR_SEC
        self.color_btn = const.COLOR_BTN
        self.color_txt = const.COLOR_TXT
        self.color_txt_in = const.COLOR_TXT_IN

        self.transactions = past_transactions
        self.ttl_income = 0
        self.curr_bal = 0
        self.mon_spend = 0

        for each_transaction in self.transactions:
            value_float = utility.format_to_float(each_transaction[2])
            # Add all instances of income to the total income
            if each_transaction[1] in const.INCOME_KEYWORDS:
                self.ttl_income += value_float
            # If it's this month, year and not income, then add to monthly spending
            if utility.check_this_month(each_transaction[0]) and each_transaction[1] not in const.INCOME_KEYWORDS:
                self.mon_spend -= value_float
            # Current balance is just the running value
            self.curr_bal += value_float
        print('Finished loading past transactions!')

        self.save_percent = user_dat['save']
        self.mon_budget = user_dat['aim']
        self.save_goal = user_dat['goal']

        self.root = root
        self.root.config(bg=self.color_bg)
        self.root.title(const.WINDOW_TITLE)

        # App header; balance, goal, current month spending
        self.frm_head = tk.Frame(self.root, bg=self.color_bg)
        self.frm_head.grid(row=0, pady=(5, 0))

        # Current month spending section
        # Frame
        self.frm_mon = tk.Frame(self.frm_head, width=200, height=50, bg=self.color_sec)
        self.frm_mon.pack(side=tk.LEFT, padx=5, pady=5)
        self.frm_mon.pack_propagate(False)
        # Title
        self.lbl_mon_title = tk.Label(
            self.frm_mon, text='MONTHLY SPENDING', font=('Helvetica', 10), bg=self.color_sec, fg=self.color_txt)
        # Main value
        self.color_lbl_mon_val = utility.get_colors(self.mon_budget, self.mon_spend)
        self.lbl_mon_value = tk.Label(
            self.frm_mon, text=f'${utility.format_2f(self.mon_spend)}',
            font=('Helvetica', 14), bg=self.color_sec, fg=self.color_lbl_mon_val
        )
        # Sub value
        self.lbl_mon_sub = tk.Label(
            self.frm_mon, text=f'${utility.format_2f(self.mon_budget)}',
            font=('Helvetica', 10), bg=self.color_sec, fg=self.color_txt
        )
        # Place into frame
        self.lbl_mon_title.pack(side=tk.TOP, anchor='w')
        self.lbl_mon_value.pack(side=tk.LEFT)
        self.lbl_mon_sub.pack(side=tk.RIGHT)

        # Current balance section
        # Frame
        self.frm_bal = tk.Frame(self.frm_head, width=250, height=50, bg=self.color_sec)
        self.frm_bal.pack(side=tk.LEFT, padx=5, pady=5)
        self.frm_bal.pack_propagate(False)
        # Title
        self.lbl_bal_title = tk.Label(
            self.frm_bal, text='BALANCE', font=('Helvetica', 10), bg=self.color_sec, fg=self.color_txt)
        # Main value
        self.color_lbl_bal_val = utility.get_colors(self.ttl_income, self.curr_bal, self.save_percent, True)
        self.lbl_bal_value = tk.Label(
            self.frm_bal, text=f'${utility.format_2f(self.curr_bal)}',
            font=('Helvetica', 14), bg=self.color_sec, fg=self.color_lbl_bal_val
        )
        # Sub value
        self.saving_amount = self.ttl_income * self.save_percent
        self.lbl_bal_sub = tk.Label(
            self.frm_bal, text=f'${utility.format_2f(self.saving_amount)}',
            font=('Helvetica', 10), bg=self.color_sec, fg=self.color_txt
        )
        # Place into frame
        self.lbl_bal_title.pack(side=tk.TOP, anchor='w')
        self.lbl_bal_value.pack(side=tk.LEFT)
        self.lbl_bal_sub.pack(side=tk.RIGHT)

        # Current goal section
        # Frame
        self.frm_goal = tk.Frame(self.frm_head, width=200, height=50, bg=self.color_sec)
        self.frm_goal.pack(side=tk.LEFT, padx=5, pady=5)
        self.frm_goal.pack_propagate(False)
        # Title
        self.lbl_goal_title = tk.Label(
            self.frm_goal, text='GOAL', font=('Helvetica', 10), bg=self.color_sec, fg=self.color_txt)
        # Main value
        if self.save_goal != 0:
            self.goal_percent_calc = int(((self.curr_bal - self.saving_amount) / self.save_goal) * 100)
            self.goal_percent_calc = max(self.goal_percent_calc, 0)
        else:
            self.goal_percent_calc = 0
        self.lbl_goal_value = tk.Label(
            self.frm_goal, text=f'{self.goal_percent_calc}%',
            font=('Helvetica', 14), bg=self.color_sec, fg=self.color_txt
        )
        # Sub value
        self.lbl_goal_sub = tk.Label(
            self.frm_goal, text=f'${utility.format_2f(self.save_goal)}',
            font=('Helvetica', 10), bg=self.color_sec, fg=self.color_txt
        )
        # Place into frame
        self.lbl_goal_title.pack(side=tk.TOP, anchor='w')
        self.lbl_goal_value.pack(side=tk.LEFT)
        self.lbl_goal_sub.pack(side=tk.RIGHT)

        # Main body section; user inputs, graphs, pas expenses
        self.frm_main = tk.Frame(self.root, bg=self.color_bg)
        self.frm_main.grid(row=1, pady=10)

        # Body split frames
        self.frm_left = tk.Frame(self.frm_main, bg=self.color_bg)
        self.frm_left.grid(row=0, column=0, padx=(10, 0))
        self.frm_right = tk.Frame(self.frm_main, bg=self.color_bg)
        self.frm_right.grid(row=0, column=1, padx=(0, 15))

        # Item input
        self.lbl_item = tk.Label(self.frm_left, text='Item:', bg=self.color_bg, fg=self.color_txt)
        self.lbl_item.grid(row=0, column=0, sticky='e', padx=(0, 15))
        self.ent_item = tk.Entry(self.frm_left, width=30, bg=self.color_bg_sec, fg=self.color_txt, borderwidth=0)
        self.ent_item.grid(row=0, column=1)

        # Cost input
        self.lbl_cost = tk.Label(self.frm_left, text='Cost:', bg=self.color_bg, fg=self.color_txt)
        self.lbl_cost.grid(row=1, column=0, sticky='e', padx=(0, 15))
        self.ent_cost = tk.Entry(self.frm_left, width=30, bg=self.color_bg_sec, fg=self.color_txt, borderwidth=0)
        self.ent_cost.grid(row=1, column=1)

        # Listbox
        self.listbox = tk.Listbox(
            self.frm_right, selectmode=tk.SINGLE,
            height=10, width=40, font=('Consolas', 11), bg=self.color_bg_sec, fg=self.color_txt)
        self.listbox.grid(row=0, column=0, rowspan=8, columnspan=2, padx=(25, 0))
        self.scrollbar = tk.Scrollbar(self.frm_right, command=self.listbox.yview)     # Scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=3, rowspan=8, sticky='ns')

        # Add all past transactions to the listbox
        for each_transaction in self.transactions:
            value_float = utility.format_to_float(each_transaction[2])
            self.add_to_listbox(each_transaction[1], value_float, each_transaction[0])

        # Save spending button
        self.btn_save = tk.Button(
            self.frm_left, text='SAVE EXPENSE', width=17, bg=self.color_btn, fg=self.color_txt_in,
            command=lambda: self.validate_expense())
        self.btn_save.grid(row=2, column=1, columnspan=3, pady=5)

        # Income input
        self.lbl_income = tk.Label(self.frm_left, text='Income:', bg=self.color_bg, fg=self.color_txt)
        self.lbl_income.grid(row=3, column=0, sticky='e', padx=(0, 15))
        self.ent_income = tk.Entry(self.frm_left, width=30, bg=self.color_bg_sec, fg=self.color_txt, borderwidth=0)
        self.ent_income.grid(row=3, column=1)

        # Save income button
        self.btn_add = tk.Button(
            self.frm_left, text='ADD INCOME', width=17, bg=self.color_btn, fg=self.color_txt_in,
            command=lambda: self.validate_income())
        self.btn_add.grid(row=4, column=1, columnspan=3, pady=5)

        # User preferences
        # Monthly spending budget
        self.lbl_spend = tk.Label(self.frm_left, text='Monthly Budget:', bg=self.color_bg, fg=self.color_txt)
        self.lbl_spend.grid(row=5, column=0, sticky='e')
        self.ent_spend = tk.Entry(self.frm_left, width=25, bg=self.color_bg_sec, fg=self.color_txt, borderwidth=0)
        self.ent_spend.grid(row=5, column=1)

        # Update button
        self.btn_spend = tk.Button(
            self.frm_left, text='UPDATE', bg=self.color_btn, fg=self.color_txt_in,
            command=lambda: self.validate_monthly_budget())
        self.btn_spend.grid(row=5, column=2, columnspan=2, pady=5)

        # Monthly spending budget
        self.lbl_goal = tk.Label(self.frm_left, text='Goal:', bg=self.color_bg, fg=self.color_txt)
        self.lbl_goal.grid(row=6, column=0, sticky='e')
        self.ent_goal = tk.Entry(self.frm_left, width=25, bg=self.color_bg_sec, fg=self.color_txt, borderwidth=0)
        self.ent_goal.grid(row=6, column=1)

        # Update button
        self.btn_goal = tk.Button(
            self.frm_left, text='UPDATE', bg=self.color_btn, fg=self.color_txt_in,
            command=lambda: self.validate_goal())
        self.btn_goal.grid(row=6, column=2, columnspan=2, pady=5)

        # Monthly spending budget
        self.lbl_saving = tk.Label(self.frm_left, text='Save Percentage:', bg=self.color_bg, fg=self.color_txt)
        self.lbl_saving.grid(row=7, column=0, sticky='e')
        self.ent_saving = tk.Entry(self.frm_left, width=25, bg=self.color_bg_sec, fg=self.color_txt, borderwidth=0)
        self.ent_saving.grid(row=7, column=1)

        # Update button
        self.btn_saving = tk.Button(
            self.frm_left, text='UPDATE', bg=self.color_btn, fg=self.color_txt_in,
            command=lambda: self.validate_save_percent())
        self.btn_saving.grid(row=7, column=2, columnspan=2, pady=5)

    def run(self):
        self.root.mainloop()

    def window_updater(self):
        self.color_lbl_mon_val = utility.get_colors(self.mon_budget, self.mon_spend)
        self.lbl_mon_value.config(
            text=f'${utility.format_2f(self.mon_spend)}', fg=self.color_lbl_mon_val)
        self.lbl_mon_sub.config(text=f'${utility.format_2f(self.mon_budget)}')

        self.color_lbl_bal_val = utility.get_colors(self.ttl_income, self.curr_bal, self.save_percent, True)
        self.lbl_bal_value.config(
            text=f'${utility.format_2f(self.curr_bal)}', fg=self.color_lbl_bal_val)

        self.saving_amount = self.ttl_income * self.save_percent
        self.lbl_bal_sub.config(text=f'${utility.format_2f(self.saving_amount)}')

        if self.save_goal != 0:
            self.goal_percent_calc = int(((self.curr_bal - self.saving_amount) / self.save_goal) * 100)
            self.goal_percent_calc = max(self.goal_percent_calc, 0)
        else:
            self.goal_percent_calc = 0
        self.lbl_goal_value.config(text=f'{self.goal_percent_calc}%')
        self.lbl_goal_sub.config(text=f'${utility.format_2f(self.save_goal)}')

    def add_to_listbox(self, item_name, item_cost, item_date=None):
        if item_date is None:
            item_date = utility.get_today()
        dat_format = utility.format_listbox_view(item_name, item_cost, item_date)
        self.listbox.insert(tk.END, dat_format)

    def validate_expense(self):
        item_name = self.ent_item.get()
        item_cost = self.ent_cost.get()

        # Check to see both fields are filled
        if not item_name or not item_cost:
            messagebox.showwarning('Error', 'Please input both values.')
            return 0
        # Check to see the expense cost is a valid number
        try:
            item_cost = float(item_cost)
        except ValueError:
            messagebox.showwarning('Error', 'Please enter a valid number.')
            return 0

        # If expense is not negative, make it negative
        if item_cost > 0 and item_name not in const.INCOME_KEYWORDS:
            item_cost = (item_cost * -1)

        # Save data
        utility.save_tracker(item_name, item_cost)

        # Update user GUI
        self.add_to_listbox(item_name, item_cost)

        self.ent_item.delete(0, tk.END)
        self.ent_cost.delete(0, tk.END)

        if item_name not in const.INCOME_KEYWORDS:
            self.mon_spend -= item_cost
        else:
            self.ttl_income += item_cost
        self.curr_bal += item_cost
        self.window_updater()

    def validate_income(self):
        income = self.ent_income.get()

        if not income:
            messagebox.showwarning('Error', 'Please input your income.')
            return 0
        try:
            income = float(income)
        except ValueError:
            messagebox.showwarning('Error', 'Please enter a valid number.')
            return 0

        # If income is negative, make it positive
        if income < 0:
            income = (income * -1)

        # Save data
        utility.save_tracker('INCOME', income)

        # Update user GUI
        self.add_to_listbox('INCOME', income)

        self.ent_income.delete(0, tk.END)

        self.ttl_income += income
        self.curr_bal += income
        self.window_updater()

    def validate_monthly_budget(self):
        month_budget = self.ent_spend.get()
        if not month_budget:
            messagebox.showwarning('Error', 'Please input your income.')
            return 0
        try:
            month_budget = float(month_budget)
        except ValueError:
            messagebox.showwarning('Error', 'Please enter a valid number.')
            return 0

        if month_budget < 0:
            month_budget = 0

        # Save change
        utility.update_user_data('aim', month_budget)

        # Update user GUI
        self.mon_budget = month_budget
        self.ent_spend.delete(0, tk.END)
        self.window_updater()

    def validate_goal(self):
        goal = self.ent_goal.get()
        if not goal:
            messagebox.showwarning('Error', 'Please input your income.')
            return 0
        try:
            goal = float(goal)
        except ValueError:
            messagebox.showwarning('Error', 'Please enter a valid number.')
            return 0

        if goal < 0:
            goal = 0

        # Save change
        utility.update_user_data('goal', goal)

        # Update user GUI
        self.save_goal = goal
        self.ent_goal.delete(0, tk.END)
        self.window_updater()

    def validate_save_percent(self):
        save_amount = self.ent_saving.get()
        if not save_amount:
            messagebox.showwarning('Error', 'Please input your income.')
            return 0
        try:
            save_amount = float(save_amount)
        except ValueError:
            messagebox.showwarning('Error', 'Please enter a valid number.')
            return 0

        # Clamp to between 0 and 100
        if save_amount < 0:
            save_amount = 0
        elif save_amount > 100:
            save_amount = 100

        # Convert to be between 0 and 1
        save_amount = float(save_amount / 100)

        # Save change
        utility.update_user_data('save', save_amount)

        # Update user GUI
        self.save_percent = save_amount
        self.ent_saving.delete(0, tk.END)
        self.window_updater()
