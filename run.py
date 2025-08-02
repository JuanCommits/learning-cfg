import sys
from examples.ot_example import run_example as ot_example
from examples.tree_automata_example import run_example as tree_automata_example
from examples.context_example import run_example as context_example
from examples.tl_star_example import run_example as tl_star_example

def main():
    # Obtener los argumentos desde la consola
    args = sys.argv
    
    # Verificar si se pasó un parámetro
    if len(args) < 2:
        context_example()
        print("\n"+"#"*120+"\n")
        tree_automata_example()
        print("\n"+"#"*120+"\n")
        ot_example()
        print("\n"+"#"*120+"\n")
        tl_star_example()
        return

    # Evaluar el parámetro y ejecutar la función correspondiente
    if args[1] == "1":
        tl_star_example()
    if args[1] == "2":
        ot_example()
    elif args[1] == "3":
        tree_automata_example()
    elif args[1] == "4":
        context_example()
    else:
        context_example()
        print("\n"+"#"*120+"\n")
        tree_automata_example()
        print("\n"+"#"*120+"\n")
        ot_example()
        print("\n"+"#"*120+"\n")
        tl_star_example()


if __name__ == "__main__":
    main()