self.canvas = tk.Canvas(self)
        # self.canvas.grid(row=1, column=0, sticky=tk.NSEW)

        # self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        # self.scrollbar.grid(row=0, column=7, sticky=tk.NS)
        # self.canvas.config(yscrollcommand=self.scrollbar.set)

        # self.inner_frame = tk.Frame(self.canvas)
        # self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)