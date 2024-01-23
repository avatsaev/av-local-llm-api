def get_system_prompt():
    # Open the file in read mode ('r')
    file = open('./system_prompt.txt', 'r')

    # Read the entire content of the file
    content = file.read()

    # Close the file
    file.close()
    return content
