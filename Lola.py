import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import re

name = 'lola'
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Función para hablar y registrar en consola lo que Lola dice
def talk(text):
    print(f"Lola: {text}")  # Mostrar lo que dice Lola
    engine.say(text)
    engine.runAndWait()

# Función para escuchar y registrar en consola lo que tú dices
def listen():
    rec = ""
    try:
        with sr.Microphone() as source:
            print("Lola: Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice).lower()
            print(f"Tú: {rec}")  # Mostrar lo que tú dices
            if name in rec:
                rec = rec.replace(name, '').strip()
    except Exception as e:
        print(f"Error: {e}")
    return rec

# Lógica principal
def run():
    rec = listen()
    if not rec:
        talk("No escuché nada, intenta de nuevo.")
        return

    if 'reproduce' in rec:
        music = rec.replace('reproduce', '').strip()
        talk('Reproduciendo ' + music)
        pywhatkit.playonyt(music)
    
    elif 'saludame' in rec:
        talk('Hola, buen día.')

    elif 'hora' in rec:
        hora = datetime.datetime.now().strftime('%H:%M %p')
        talk("Son las " + hora)

    elif 'busca' in rec:
        order = rec.replace('busca', '').strip()
        talk(f"Buscando {order} en Google.")
        pywhatkit.search(order)

    elif 'calcula' in rec:
        try:
            # Mapeo de números en español
            spanish_numbers = {
                "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
                "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
            }

            # Extraer números en dígitos y palabras
            numbers = re.findall(r'\d+', rec)
            words = re.findall(r'\b\w+\b', rec)
            for word in words:
                if word in spanish_numbers:
                    numbers.append(spanish_numbers[word])

            if len(numbers) < 2:
                talk("No entendí los números, intenta de nuevo.")
            else:
                num1, num2 = map(int, numbers[:2])  # Tomar los primeros dos números

                if 'mas' in rec or 'suma' in rec:
                    result = num1 + num2
                    talk(f"El resultado es {result}")
                elif 'menos' in rec or 'resta' in rec:
                    result = num1 - num2
                    talk(f"El resultado es {result}")
                elif 'por' in rec:
                    result = num1 * num2
                    talk(f"El resultado es {result}")
                elif 'entre' in rec:
                    if num2 != 0:
                        result = num1 / num2
                        talk(f"El resultado es {result}")
                    else:
                        talk("No se puede dividir entre cero.")
                else:
                    talk("No entendí la operación, intenta de nuevo.")
        except Exception as e:
            print(f"Error: {e}")
            talk("Ocurrió un error, intenta de nuevo.")
    
    elif 'adios' in rec:
        talk("Hasta luego.")
        exit()
    
    else:
        talk("No entendí eso, intenta de nuevo.")

def main():
    while True:
        run()

if __name__ == '__main__':
    main()
 
