from utils.generate_response import generate_response

if __name__ == "__main__":
    query = "Como cierro mi cuenta"
    # query = input("Ingrese su pregunta\n")
    print(generate_response(query))