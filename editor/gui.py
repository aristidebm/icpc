from editor.editor  import Editor
import sys

def main():
    """
    The application entry point
    """
    # instanciate and editor
    editor = Editor()

    filename = sys.argv[1]
    with open(filename, "r") as fp:
        file = fp.readlines()
        for line in file:
            command, arguments = process_line(editor, line.strip("\n"))
            command_dispatch(editor, command)(**arguments)

def command_dispatch(editor, command):
    return {
    'I': editor.create_drawing_board,
    'C': editor.clear_drawing_board,
    'L': editor.draw_pixel,
    'K': editor.draw_rectangle,
    'F': editor.draw_pixel_region,
    'S': editor.show_image,
    'X': editor.quit_editor,
    'H': editor.draw_segment,
    'V': editor.draw_segment
    }.get(command, lambda: None)

def process_line(editor, line):

    new_arguments = {}
    command, *arguments = line.split(" ")
    arguments = [int(arg) if arg.isnumeric() else arg for arg in arguments]
    if command == 'H':
        new_arguments["orientation"] = editor.valid_orientations[0]
        new_arguments["begin"] = arguments[0]
        new_arguments["end"] = arguments[1]
        new_arguments["fixed_row"] = arguments[2]
        new_arguments["color"] = arguments[3]
    elif command == 'V':
        new_arguments["orientation"] = editor.valid_orientations[1]
        new_arguments["fixed_row"] = arguments[0]
        new_arguments["begin"] = arguments[1]
        new_arguments["end"] = arguments[2]
        new_arguments["color"] = arguments[3]
    elif command == 'I':
        new_arguments["size"] = (arguments[0], arguments[1])
    elif command == 'L':
        new_arguments["pixel"] = (arguments[0], arguments[1])
        new_arguments["color"] = arguments[2]
    elif command == 'K':
        new_arguments["upper_corner"] = (arguments[0], arguments[1])
        new_arguments["bottom_corner"] = (arguments[2], arguments[3])
        new_arguments["color"] = arguments[5]
    elif command == 'S':
        new_arguments["filename"] = arguments[0]
    elif command == "F":
        new_arguments["pixel"] = (arguments[0], arguments[1])
        new_arguments["color"] = arguments[2]

    return command, new_arguments

if __name__ == "__main__":
    main()
