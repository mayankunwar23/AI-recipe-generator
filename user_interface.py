import json
import tkinter as tk
from tkinter import messagebox, ttk
import recipe_generator
import os

# Ensure the correct path for recipes.json
RECIPE_FILE = os.path.join(os.path.dirname(__file__), 'recipes.json')

class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('AI Recipe Generator')
        self.root.configure(bg='#1E1E1E')
        self.root.geometry(self.center_window(600, 600))  # Centering the window

        # Colors
        button_color, text_color = '#FFA500', '#FFFFFF'

        # UI Elements
        tk.Label(self.root, text='Generated Recipe:', font=('Arial', 16), fg=text_color, bg='#1E1E1E').pack(pady=10)

        # Frame for scrollable text
        text_frame = tk.Frame(self.root)
        text_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.generated_recipe_text = tk.Text(text_frame, width=60, height=10, font=('Arial', 12), fg='#1E1E1E', bg=button_color, bd=0, wrap=tk.WORD)
        self.recipe_scrollbar = tk.Scrollbar(text_frame, command=self.generated_recipe_text.yview)
        self.generated_recipe_text.config(yscrollcommand=self.recipe_scrollbar.set)

        self.generated_recipe_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.recipe_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for text, command in [("Generate Recipe", self.generate_recipe), 
                              ("Suggest Recipe", self.suggest_recipe), 
                              ("Return", self.return_to_main)]:
            tk.Button(self.root, text=text, command=command, font=('Arial', 12), bg=button_color, fg=text_color, width=20, height=2).pack(pady=10)

    def center_window(self, width, height):
        """Returns centered window geometry."""
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2.3
        return f"{width}x{height}+{x}+{int(y)}"

    def run(self):
        self.root.mainloop()

    def generate_recipe(self):
        try:
            generator = recipe_generator.RecipeGenerator()
            data = generator.generate_recipe()

            if not data:  # Handle empty response
                raise ValueError("No recipe generated!")

            recipe_text = f"Recipe Name: {data.get('name', 'Unknown')}\nOrigin: {data.get('origin', 'Unknown')}\n\nIngredients:\n" \
                          f"{'\n'.join(data.get('ingredients', []))}\n\nInstructions:\n{'\n'.join(data.get('instructions', []))}"

            self.generated_recipe_text.delete('1.0', tk.END)
            self.generated_recipe_text.insert(tk.END, recipe_text)

        except Exception as e:
            messagebox.showerror('Error', str(e))

    def suggest_recipe(self):
        suggest_window = tk.Toplevel(self.root)
        suggest_window.title('Suggest Recipe')
        suggest_window.geometry('400x500')
        suggest_window.configure(bg='#1E1E1E')

        fields = [("Recipe Name:", tk.Entry), ("Ingredients:", tk.Text), ("Instructions:", tk.Text)]
        entries = {}

        for label, widget in fields:
            ttk.Label(suggest_window, text=label, background='#1E1E1E', foreground='#FFFFFF').pack(pady=5)
            entry = widget(suggest_window, height=5 if widget == tk.Text else None, width=40)
            entry.pack(pady=5)
            entries[label] = entry

        # Dropdown for recipe origin
        ttk.Label(suggest_window, text="Recipe Origin:", background='#1E1E1E', foreground='#FFFFFF').pack(pady=5)
        origin_var = tk.StringVar(suggest_window)  # Attach to suggest_window
        origin_dropdown = ttk.Combobox(suggest_window, textvariable=origin_var, values=["Indian", "Italian", "Mexican", "Chinese", "French", "Other"])
        origin_dropdown.pack(pady=5)

        tk.Button(suggest_window, text='Confirm', bg="#FFA500",
                  command=lambda: self.confirm_suggested_recipe(
                      suggest_window, entries["Recipe Name:"].get(),
                      entries["Ingredients:"].get('1.0', 'end-1c'),
                      entries["Instructions:"].get('1.0', 'end-1c'),
                      origin_var.get())
                  ).pack(pady=10)

    def confirm_suggested_recipe(self, window, name, ingredients, instructions, origin):
        if not all([name, ingredients, instructions, origin]):
            return messagebox.showwarning("Warning", "All fields must be filled!")

        try:
            # Ensure recipes.json exists or create default structure
            try:
                with open(RECIPE_FILE, 'r') as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {"recipes": []}  # Default structure

            # Append new recipe
            data['recipes'].append({
                'recipe_name': name,
                'origin': origin,
                'ingredients': [line.strip() for line in ingredients.split('\n') if line.strip()],
                'instructions': [line.strip() for line in instructions.split('\n') if line.strip()]
            })

            # Write back to file
            with open(RECIPE_FILE, 'w') as file:
                json.dump(data, file, indent=4)

            messagebox.showinfo('Success', 'Recipe added!')
            window.destroy()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def return_to_main(self):
        self.generated_recipe_text.delete('1.0', tk.END)

if __name__ == '__main__':
    UserInterface().run()



