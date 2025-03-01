# Probability Tree Visualization
![image](https://github.com/user-attachments/assets/de918a78-4c23-44cd-9a0b-4c2e1b1508b5)
![image](https://github.com/user-attachments/assets/af401f52-da35-49c6-aa9b-26716b755533)

This project is a Python application that visualizes conditional probabilities using tree diagrams. It uses the `tkinter` library for the graphical user interface and `sympy` for symbolic mathematics.

## Features

- Interactive tree diagrams for visualizing conditional probabilities.
- Shows inverted tree on the right.
- Input fields for setting probabilities and events.
- Automatic calculation of missing probabilities based on provided values.
- Reset functionality to clear all input values.
- Support of fractions and decimal probabilities.

## Requirements

- Python 3.x
- `tkinter` library
- `sympy` library

(see requirements.txt)


## Usage

1. Run the application

2. The main window will open, displaying two tree diagrams. The left frame contains input fields for setting event names. The right will show the probability tree and it's reversed tree.

3. Enter the names for events A, A', B, and B' in the respective input fields. A‘ and B’ are the complementary events.

4. Enter the probabilities in the input fields within the tree diagrams.

5. Click the "Calculate" button to calculate the missing probabilities.

6. Click the "Reset" button to clear all tree values.


## License (MIT)

This project is licensed under the MIT License. See the LICENSE file for details.
