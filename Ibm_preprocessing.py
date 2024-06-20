import os

def transform_file(input_path, output_path):
    with open(input_path, 'r') as file:
        lines = file.readlines()

    processed_lines = []
    for line in lines:
        # Dividir la línea por espacios y filtrar los elementos vacíos
        split_line = [element for element in line.strip().split() if element]
        # Tomar solo los dos últimos elementos y formatearlos
        if len(split_line) >= 2:
            processed_line = f"{split_line[-2]},{split_line[-1]}"
            processed_lines.append(processed_line)

    with open(output_path, 'w') as file:
        for line in processed_lines:
            file.write(line + '\n')


input_file_name='ibm-5000.txt'
output_file_name='processed_ibm-5000.txt'
input_path = os.path.join('./Input/',input_file_name)
output_path =os.path.join('./Input/',output_file_name)

# Llamar a la función
transform_file(input_path, output_path)

