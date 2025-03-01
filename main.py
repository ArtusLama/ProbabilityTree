from __future__ import annotations
import tkinter as tk
from fractions import Fraction
from sympy import symbols, Eq, solve


# - - - -   C L A S S E S   - - - -


class Probability:
    def __init__(self, value: int | Fraction | None = None):
        self.value = value
        self.value_var = tk.StringVar(value="" if value is None else str(value))
        self.entry = tk.Entry(canvas, textvariable=self.value_var, width=8, justify="center")
        self.entry.bind("<KeyRelease>", self.on_keypress)
        self.invalid = False
        self.companion = None
    
    def set_companion(self, companion: Probability):
        self.companion = companion
        
    
    def set_value(self, value: Fraction):
        self.value = value
        self.update_entry_text()

    def on_value_update(self):
        if self.companion:
            self.companion.value_var.set(self.value_var.get())
            self.companion.read_entry()
    
    def read_entry(self):
        self.value = None
        try:
            if self.value_var.get().strip() != "":
                new_val = Fraction(self.value_var.get().strip())
                if new_val < 0 or new_val > 1:
                    raise ValueError
                self.value = new_val
            self.set_valid(True)
        except:
            self.set_valid(False)
            
        
    
    def update_entry_text(self):
        self.value_var.set(str(self.value) if self.value is not None else "")
        self.read_entry()

    def on_keypress(self, event: tk.Event):
        self.read_entry()
        self.on_value_update()
    
    def reset(self):
        self.value = None
        self.update_entry_text()
    
    def set_valid(self, valid = True):
        self.invalid = not valid
        color = "white" if valid else "red"
        self.entry.config(bg=color)





class Node:
    def __init__(
        self,
        name: tk.StringVar,
        weight: Probability,
        left: Node | None = None,
        right: Node | None = None
    ):
        self.name = name
        self.weight = weight
        self.left = left
        self.right = right
        

class RootNode(Node):
    def __init__(
        self,
        left: Node | None = None,
        right: Node | None = None
    ):
        super().__init__(tk.StringVar(value="1"), Fraction(1), left, right)


class EndNode(Node):
    def __init__(
        self,
        name: tk.StringVar,
        weight: Probability,
        end_p: Probability
    ):
        super().__init__(name, weight)
        self.end_p = end_p



# - - - -   F U N C T I O N S   - - - -
def draw_node(node: Node, x: int, y: int, size: int):
    canvas.create_oval(x - size / 2, y - size / 2, x + size / 2, y + size / 2, fill="white", outline="black")
    canvas.create_text(x, y, text=node.name.get())
    
    if isinstance(node, EndNode):
        canvas.create_window(x, y + size * 4/5, window=node.end_p.entry)
    
def draw_tree(tree: RootNode, x: int, y: int, size: int, distance: int):
        
    if tree.left:
        canvas.create_line(x, y, x - distance, y + distance)
        canvas.create_window(x - distance / 2, y + distance / 2, window=tree.left.weight.entry)
        draw_tree(tree.left, x - distance, y + distance, size, distance - size)
    
    if tree.right:
        canvas.create_line(x, y, x + distance, y + distance)
        canvas.create_window(x + distance / 2, y + distance / 2, window=tree.right.weight.entry)
        draw_tree(tree.right, x + distance, y + distance, size, distance - size)
        
    
    draw_node(tree, x, y, size)


def draw_canvas():
    canvas.delete("all")
    draw_tree(my_tree, 300, 150, 40, 125)
    draw_tree(rev_tree, 900, 150, 40, 125)


def on_update():
    draw_canvas()

def clear_values():
    tree_p_a.reset()
    tree_p_not_a.reset()
    tree_p_a_b.reset()
    tree_p_a_not_b.reset()
    tree_p_not_a_b.reset()
    tree_p_not_a_not_b.reset()
    tree_end_p_a_b.reset()
    tree_end_p_a_not_b.reset()
    tree_end_p_not_a_b.reset()
    tree_end_p_not_a_not_b.reset()
    
    tree_p_rev_a.reset()
    tree_p_rev_not_a.reset()
    tree_p_rev_a_b.reset()
    tree_p_rev_a_not_b.reset()
    tree_p_rev_not_a_b.reset()
    tree_p_rev_not_a_not_b.reset()
    tree_end_p_rev_a_b.reset()
    tree_end_p_rev_a_not_b.reset()
    tree_end_p_rev_not_a_b.reset()
    tree_end_p_rev_not_a_not_b.reset()
    
    on_update()
    
# - - - -   C A L C U L A T I O N   - - - -
def calculate():
    p_a, p_an = symbols("P(A) P(A!)")
    p_a_b, p_a_bn, p_an_b, p_an_bn = symbols("P_A(B) P_A(B!) P_A!(B) P_A!(B!)")
    p_a_union_b, p_a_union_bn, p_an_union_b, p_an_union_bn = symbols("P(AnB) P(AnB!) P(A!nB) P(A!nB!)")
    
    complement_a = Eq(p_a + p_an, 1)
    complement_a_b = Eq(p_a_b + p_a_bn, 1)
    complement_an_b = Eq(p_an_b + p_an_bn, 1)
    complement_end = Eq(p_a_union_b + p_a_union_bn + p_an_union_b + p_an_union_bn, 1)

    path_rule_a_b = Eq(p_a * p_a_b, p_a_union_b)
    path_rule_a_bn = Eq(p_a * p_a_bn, p_a_union_bn)
    path_rule_an_b = Eq(p_an * p_an_b, p_an_union_b)
    path_rule_an_bn = Eq(p_an * p_an_bn, p_an_union_bn)

    p_b, p_bn = symbols("P(B) P(B!)")
    p_b_a, p_b_an, p_bn_a, p_bn_an = symbols("P_B(A) P_B(A!) P_B!(A) P_B!(A!)")

    complement_b = Eq(p_b + p_bn, 1)
    complement_b_a = Eq(p_b_a+ p_b_an, 1)
    complement_bn_a = Eq(p_bn_a + p_bn_an, 1)

    path_rule_b_a = Eq(p_b * p_b_a, p_a_union_b)
    path_rule_b_an = Eq(p_b * p_b_an, p_an_union_b)
    path_rule_bn_a = Eq(p_bn * p_bn_a, p_a_union_bn)
    path_rule_bn_an = Eq(p_bn * p_bn_an, p_an_union_bn)

    all_equations = [complement_a, complement_a_b, complement_an_b, complement_end, 
           path_rule_a_b, path_rule_a_bn, path_rule_an_b, path_rule_an_bn,
           complement_b, complement_b_a, complement_bn_a,
           path_rule_b_a, path_rule_b_an, path_rule_bn_a, path_rule_bn_an]
    
    
    relations = {
        p_a: tree_p_a,
        p_an: tree_p_not_a,
        p_a_b: tree_p_a_b,
        p_a_bn: tree_p_a_not_b,
        p_an_b: tree_p_not_a_b,
        p_an_bn: tree_p_not_a_not_b,
        
        p_b: tree_p_rev_a,
        p_bn: tree_p_rev_not_a,
        p_b_a: tree_p_rev_a_b,
        p_b_an: tree_p_rev_a_not_b,
        p_bn_a: tree_p_rev_not_a_b,
        p_bn_an: tree_p_rev_not_a_not_b,
        
        
        p_a_union_b: tree_end_p_a_b,
        p_a_union_bn: tree_end_p_a_not_b,
        p_an_union_b: tree_end_p_not_a_b,
        p_an_union_bn: tree_end_p_not_a_not_b,
    }
    
    
    [print(f"{var} = {prop.value}") for var, prop in relations.items()]
    known_values = {var: prop.value for var, prop in relations.items() if prop.value is not None and not prop.invalid}
    
    evaluated_equations = [eq.subs(known_values) for eq in all_equations]
    
    solution = solve(evaluated_equations, dict=True)
    if len(solution) == 0:
        print("\nNo solutions found :(")
        return
    solution = solution[0]
    
    solutions_clean = {var: Fraction(value) for var, value in solution.items() if value.is_Number}
    
    
    
    for var, value in solutions_clean.items():
        relations[var].set_value(value)
        relations[var].on_value_update()
    
    print(solutions_clean)
    
    print("Provided information:\n")
    [print(f"{var} = {val}") for var, val in known_values.items()]
    print("\n\nSolutions:\n")
    [print(f"{sol[0]} = {sol[1]}") for sol in solution.items()]
    print("\n\nCleaned solutions:\n")
    [print(f"{sol[0]} = {sol[1]}") for sol in solutions_clean.items()]
    print("--------------------------------------------------")

# = = = = = = = = = =   T K - I N T E R   = = = = = = = = = =
root = tk.Tk()
root.title("Probability Tree Calculator")
root.geometry("1500x600")



# - - - -   M A I N   W I N D O W   - - - -
main_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=10)
main_window.pack(fill=tk.BOTH, expand=True)



# - - - -   L E F T   F R A M E   - - - -
left_frame = tk.Frame(main_window, width=200)
main_window.add(left_frame, minsize=200, padx=10, pady=20)	



# - - - -   R I G H T   F R A M E   - - - -
right_frame = tk.Frame(main_window)
main_window.add(right_frame, minsize=400)



# - - - -   I N T E R F A C E  - - - -
event_a_name = tk.StringVar(value="A")
event_not_a_name = tk.StringVar(value="A'")

event_b_name = tk.StringVar(value="B")
event_not_b_name = tk.StringVar(value="B'")

# - - - -   E V E N T   A   - - - -
event_a_label = tk.Label(left_frame, text="Event A:")
event_a_label.pack()

event_a_input = tk.Entry(left_frame, textvariable=event_a_name)
event_a_input.bind("<KeyRelease>", lambda e: on_update())
event_a_input.pack()

event_not_a_label = tk.Label(left_frame, text="Complement A:")
event_not_a_label.pack()

event_not_a_input = tk.Entry(left_frame, textvariable=event_not_a_name)
event_not_a_input.bind("<KeyRelease>", lambda e: on_update())
event_not_a_input.pack()

# - - - -   E V E N T   B   - - - -
event_b_label = tk.Label(left_frame, text="Event B:")
event_b_label.pack()

event_b_input = tk.Entry(left_frame, textvariable=event_b_name)
event_b_input.bind("<KeyRelease>", lambda e: on_update())
event_b_input.pack()

event_not_b_label = tk.Label(left_frame, text="Complement B:")
event_not_b_label.pack()

event_not_b_input = tk.Entry(left_frame, textvariable=event_not_b_name)
event_not_b_input.bind("<KeyRelease>", lambda e: on_update())
event_not_b_input.pack()

# - - - -   A C T I O N S   - - - -
calculate_button = tk.Button(left_frame, text="Calculate", command=calculate)
calculate_button.pack(pady=20)

reset_button = tk.Button(left_frame, text="Reset", command=clear_values)
reset_button.pack()



# - - - -   D I A G R A M   C A N V A S   - - - -
canvas = tk.Canvas(right_frame, bg="lightgray")
canvas.pack(fill=tk.BOTH, expand=True)





# = = = = = = = =    T H E   T R E E S   = = = = = = = = = =


tree_p_a = Probability()
tree_p_not_a = Probability()
tree_p_a_b = Probability()
tree_p_a_not_b = Probability()
tree_p_not_a_b = Probability()
tree_p_not_a_not_b = Probability()

tree_end_p_a_b = Probability()
tree_end_p_a_not_b = Probability()
tree_end_p_not_a_b = Probability()
tree_end_p_not_a_not_b = Probability()

my_tree = RootNode(
    left=Node(
        event_a_name,
        tree_p_a,
        left=EndNode(
            event_b_name,
            tree_p_a_b,
            tree_end_p_a_b,
        ),
        right=EndNode(
            event_not_b_name,
            tree_p_a_not_b,
            tree_end_p_a_not_b,
        ),
    ),
    right=Node(
        event_not_a_name,
        tree_p_not_a,
        left=EndNode(
            event_b_name,
            tree_p_not_a_b,
            tree_end_p_not_a_b,
        ),
        right=EndNode(
            event_not_b_name,
            tree_p_not_a_not_b,
            tree_end_p_not_a_not_b,
        ),
    )
)

tree_p_rev_a = Probability()
tree_p_rev_not_a = Probability()
tree_p_rev_a_b = Probability()
tree_p_rev_a_not_b = Probability()
tree_p_rev_not_a_b = Probability()
tree_p_rev_not_a_not_b = Probability()

tree_end_p_rev_a_b = Probability()
tree_end_p_rev_a_not_b = Probability()
tree_end_p_rev_not_a_b = Probability()
tree_end_p_rev_not_a_not_b = Probability()

tree_end_p_a_b.set_companion(tree_end_p_rev_a_b)
tree_end_p_a_not_b.set_companion(tree_end_p_rev_not_a_b)
tree_end_p_not_a_b.set_companion(tree_end_p_rev_a_not_b)
tree_end_p_not_a_not_b.set_companion(tree_end_p_rev_not_a_not_b)

tree_end_p_rev_a_b.set_companion(tree_end_p_a_b)
tree_end_p_rev_a_not_b.set_companion(tree_end_p_not_a_b)
tree_end_p_rev_not_a_b.set_companion(tree_end_p_a_not_b)
tree_end_p_rev_not_a_not_b.set_companion(tree_end_p_not_a_not_b)


rev_tree = RootNode(
    left=Node(
        event_b_name,
        tree_p_rev_a,
        left=EndNode(
            event_a_name,
            tree_p_rev_a_b,
            tree_end_p_rev_a_b,
        ),
        right=EndNode(
            event_not_a_name,
            tree_p_rev_a_not_b,
            tree_end_p_rev_a_not_b,
        ),
    ),
    right=Node(
        event_not_b_name,
        tree_p_rev_not_a,
        left=EndNode(
            event_a_name,
            tree_p_rev_not_a_b,
            tree_end_p_rev_not_a_b,
        ),
        right=EndNode(
            event_not_a_name,
            tree_p_rev_not_a_not_b,
            tree_end_p_rev_not_a_not_b,
        ),
    )
)


draw_canvas()




root.mainloop()
