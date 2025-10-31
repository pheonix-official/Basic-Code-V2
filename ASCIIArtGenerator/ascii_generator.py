import sys
# checks for pyfiglet existence before attempting import in a real project
try:
    import pyfiglet
except ImportError:
    print("\nFATAL ERROR: 'pyfiglet' library is not installed.")
    print("Please run: pip install pyfiglet\n")
    sys.exit(1)


def generate_ascii_art(text, font="slant"):
    """
    generates the  ASCII art from text using a specified font.
    """
    try:
        # uses pyfiglet.figlet_format to generate the ASCII art string
        ascii_art = pyfiglet.figlet_format(text, font=font)
        
        print("\n" + "="*50)
        print(f" ASCII Art (Font: {font}) ")
        print(ascii_art)
        print("="*50 + "\n")
        
    except pyfiglet.FigletError:
        print(f"\n Error: Font '{font}' not found or invalid.")
        print("Falling back to standard font...")
        # Fallback
        ascii_art = pyfiglet.figlet_format(text)
        print(ascii_art)
        
    except Exception as e:
        print(f"\n An unexpected error occurred: {e}")

if __name__ == "__main__":
    print(" Text to ASCII Art Generator ")
    
    # gets text input from user
    text_input = input("Enter the text you want to convert: ").strip()
    if not text_input:
        print("Text cannot be empty. Exiting.")
        sys.exit()

    # gets font input (optional, 'slant' is a good default)
    font_input = input("Enter font name (e.g., slant, doh, epic) or press Enter for default: ").strip()
    
    font_to_use = font_input if font_input else "slant"
    
    generate_ascii_art(text_input, font_to_use)