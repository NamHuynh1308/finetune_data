import os
import json

# Define the folder containing the files
folder_path = 'complex_sequences'
# Define the prefix to prepend to the image paths
prefix_path = '/ourdisk/hpc/disc/nam/auto_archive_notyet/tape_2copies/InternVL/internvl_chat/shell/data/finetune_data/'

# Get the list of all files in the folder
files = os.listdir(folder_path)

# Filter the images and text files
images = [f for f in files if f.endswith('.png')]
text_files = [f for f in files if f.endswith('.txt')]

# Function to read the content of a text file
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Path for the output JSONL file
output_file_path = os.path.join(folder_path, 'complex_sequences.jsonl') # Change jsonl file name to create

# Open the output file in write mode
with open(output_file_path, 'w') as jsonl_file:
    # Process each image and its corresponding text file
    for image in images:
        base_name = os.path.splitext(image)[0]
        text_file = base_name + '.txt'
        
        if text_file in text_files:
            text_content = read_text_file(os.path.join(folder_path, text_file))
            
            # Create the JSON structure
            image_full_path = os.path.join(folder_path, image).replace('\\', '/')
            data = {
                "id": base_name,
                "image": prefix_path + image_full_path,
                "conversations": [
                    {
                        "from": "human",
                        "value": "Generate plant UML code to create this UML graph?\n<image>"
                    },
                    {
                        "from": "gpt",
                        "value": text_content
                    }
                ]
            }
            
            # Write to the .jsonl file
            jsonl_file.write(json.dumps(data) + '\n')

print("Processing completed.")
