def clear():
    import os
    if os.name == "nt":
        os.system("cls")
    elif os.name != "nt":
        os.system("clear")