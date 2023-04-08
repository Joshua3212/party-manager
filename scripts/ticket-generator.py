### @noahcfie (GitHub) ###

import qrcode

# Mock-Data:
# namen = ["Michael Brown", "Emily Davis", "David Kim", "Jessica Taylor", "Jacob Perez", "Ashley Rodriguez", "Matthew Wilson", "Samantha Martinez", "Joshua Garcia", "Amanda Thompson"]
# geburtstage = ["12.03.1988", "23.07.1991", "06.11.1989", "13.05.1993", "01.01.1995", "21.09.1992", "10.02.1986", "11.08.1994", "25.12.1990", "18.06.1987"]

# Data-Arrays
namen = []
geburtstage = []

# Input + List-append
while True:
    print(" ")
    name = input("Name (weiter zur Ticketerstellung mit 'skip'): ")
    namen.append(name)

    if name.lower() in ["skip"]:
        print("Ticketerstellung läuft...")
        break
    else:
        geburtstag = input("Zugehöriges Geburtsdatum (dd/mm/yyyy): ")
        geburtstage.append(geburtstag)


namen.remove("skip")

# Data-Review
print(" ")
print(namen)
print(geburtstage)

# Count
ticket_anzahl = len(namen)
print("Anzahl: " + str(len(namen)))

# iteration-vars
i = 1
y = 0

# ticket-gen
while i <= ticket_anzahl:

    ticket_data = {"Name": namen[y], "Geburtstdatum": geburtstage[y]}
    ticket_data = {"Name": namen[y], "Geburtstdatum": geburtstage[y]}
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(ticket_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("QRCodes/{}.png".format(namen[y]))

    y = y + 1
    i = i + 1
