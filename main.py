import json
from datetime import datetime

# TODO: dodati type hinting na sve funkcije!


OFFERS_FILE = "offers.json"
PRODUCTS_FILE = "products.json"
CUSTOMERS_FILE = "customers.json"


def load_data(filename: str) -> list:
    """Load data from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {filename}. Check file format.")
        return []


def save_data(filename: str, data: list) -> None:
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# TODO: Implementirajte funkciju za kreiranje nove ponude.
def create_new_offer(offers: list, products: list , customers: list) -> None:
    """
    Prompt user to create a new offer by selecting a customer, entering date,
    choosing products, and calculating totals.
    """
    while True:
        print("\nOdabir kupca:")
        print("--------------\n")
        
        for index in range(len(customers)):
            print(f"{index + 1}. {customers[index]["name"]} | Email: {customers[index]["email"]} | Vat broj: {customers[index]["vat_id"]})")
        
        kupac_index = int(input("\nOdaberite kupca po broju: ")) - 1
        
        if 0 <= kupac_index < len(customers):
            odabrani_kupac = customers[kupac_index]
            print(f"\nOdabrani kupac: [{odabrani_kupac["name"]} | Email : {odabrani_kupac["email"]} | Vat broj: {odabrani_kupac["vat_id"]})]")
            break
        else:
            print("\nKrivi izbor. Kupac ne postoji.")
    
    while True:

        datum = input("\nUnesite datum (YYYY-MM-DD) ili 'enter' za današnji datum: ")
        if datum == "":
            datum = datetime.now().strftime("%Y-%m-%d")
        try:
            valid_date = datetime.strptime(datum, "%Y-%m-%d")
            break
        except ValueError:
            print("\nKrivi format datuma! Molim unesite format datuma u formatu YYYY-MM-DD.")

    sub_total = 0
    ponuda = []
    while True:
        print("\nOdabir proizvoda:")
        print("-----------------")

        for index in range(len(products)):
            print(f"{index + 1}. {products[index]["name"]} | {products[index]["description"]} | Cijena : ${products[index]["price"]:.2f}")

        proizvod_index = int(input("\nOdabirite proizvod po broju ('0' za kraj): ")) -1

        if proizvod_index == -1:
            break
        
        if 0 <= proizvod_index < len(products):
            odabrani_proizvod = products[proizvod_index]
            print(f"\nOdabrani proizvod: [{odabrani_proizvod["name"]} | {odabrani_proizvod["description"]} | Cijena : ${odabrani_proizvod["price"]:2f}]")

            quantity = int(input("Unesite količinu: "))
            item_total = odabrani_proizvod['price'] * quantity
            sub_total += item_total

            ponuda.append({
                "product_id": odabrani_proizvod['id'],
                "product_name": odabrani_proizvod['name'],
                "description": odabrani_proizvod.get('description', ''),
                "quantity": quantity,
                "price": odabrani_proizvod['price'],
                "item_total": item_total 
            })

            print(ponuda)
        
        else:
            print("\nKrivi izbor. Proizvod ne postoji.")
        
        tax = sub_total * 0.25
        total = sub_total + tax

        new_offer = {
            "offer_number": len(offers) + 1,
            "customer": odabrani_kupac["name"],
            "date": datum,
            "items": ponuda,
            "sub_total": sub_total,
            "tax": tax,
            "total": total
            } 
        
        offers.append(new_offer)
        print("Ponuda uspješno kreirana!")
   
    # Omogućite unos kupca
    # Izračunajte sub_total, tax i total
    # Dodajte novu ponudu u listu offers
    pass


# TODO: Implementirajte funkciju za upravljanje proizvodima.
def manage_products(products):
    """
    Allows the user to add a new product or modify an existing product.
    """
    while True:
        print("\nUpravljanje proizvodima:")
        print("------------------------")
        print("1. Dodaj novi proizvod")
        print("2. Izmjeni postojeći proizvod")
        print("3. Prikaži listu svih proizvoda")
        print("5. Izlaz")

        izbor = input("\nOdabrana opcija: ")

        if izbor == "1":
                name = input("Unesite ime proizvoda: ")
                description = input("Unesite opis proizvoda: ")
                price = float(input("Unesite cijenu proizvoda: "))

                products_id = len(products) + 1
                products.append({'id': products_id, 'name': name, 'price': price})
        
        elif izbor == "2":
            while True:
                for index in range(len(products)):
                    print(f"{index + 1}. {products[index]["name"]} | {products[index]["description"]} | Cijena : ${products[index]["price"]:.2f}")
            
                proizvod_index = int(input("\nOdabirite proizvod po broju ('0' za kraj): ")) -1
            
                if 0 <= proizvod_index < len(products):
                    odabrani_proizvod = products[proizvod_index]
                    print(f"\nOdabrani proizvod: [{odabrani_proizvod["name"]} | {odabrani_proizvod["description"]} | Cijena : ${odabrani_proizvod["price"]:2f}]")
                    product_name = input("Unesite novi naziv proizvoda: ")
                    description = input("Unesite novi opis proizvoda: ")
                    price = float(input("Unesiti novu cijenu: "))

                    products[proizvod_index] = {'name': product_name, 'description': description, 'price': price}
                    break
                else:
                    print("\nKrivi izbor. Proizvod ne postoji.")

        elif izbor == "3":
            for product in products:
                print(f"{product["name"]} | {product["description"]} | ${product["price"]}")
        elif izbor == "5":
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")

    # Omogućite korisniku izbor između dodavanja ili izmjene proizvoda
    # Za dodavanje: unesite podatke o proizvodu i dodajte ga u listu products
    # Za izmjenu: selektirajte proizvod i ažurirajte podatke
    pass


# TODO: Implementirajte funkciju za upravljanje kupcima.
def manage_customers(customers : list) -> None:
    """
    Allows the user to add a new customer or view all customers.
    """
    while True:
        print("\nUpravljanje korisnicima")
        print("-----------------------")
        print("1. Dodaj novog korisnika")
        print("2. Prikaži listu svih kupaca")
        print("5. Izlaz")
                
        izbor = input("\nOdabrana opcija: ")

        if izbor == "1":
            name = input("Unesi ime kupca: ")
            email = input("Unesi korisnikov email: ")
            vat_id = input("Unesti korisnikov VAT broj :")
            customers.append({'name': name, 'email': email, 'vat_id': vat_id})
            
        if izbor == "2":
            print()
            for customer in customers:
                print(f"{customer["name"]} | Email:{customer["email"]} | Vat broj: {customer["vat_id"]}")
                print()                   
        elif izbor == "5":
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")
    
    # Za dodavanje: omogući unos imena kupca, emaila i unos VAT ID-a
    # Za pregled: prikaži listu svih kupaca
    pass


# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers(offers):
    """
    Display all offers, offers for a selected month, or a single offer by ID.
    """
    while True:
        print("\nPrikaz ponuda")
        print("-------------")
        print("1. Ispis svih ponuda")
        print("2. Ispis ponuda po mjesecu")
        print("3. Ispis pojedinačne ponude")
        print("5. Izlaz")

        izbor = input("\nOdabrana opcija: ")
        
        if izbor == "1":
            for offer in offers:
                print_offer(offer)
                print()
        elif izbor == "2":
            print("# TODO : Sorry!")
        elif izbor == "3":
            while True:
                broj_ponude = int(input("Broj ponude: "))
                odabrana_ponuda = None
                for offer in offers:
                    if offer["offer_number"] == broj_ponude:
                        odabrana_ponuda = offer
                        print_offer(offer)
                        break
                if odabrana_ponuda == None:
                    print("Broj ponude ne postoji!")
                else:
                    break
        elif izbor == "5":
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.") 

    # Omogućite izbor pregleda: sve ponude, po mjesecu ili pojedinačna ponuda
    # Prikaz relevantnih ponuda na temelju izbora
    pass


# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer):
    """Display details of a single offer."""
    print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']}, Datum ponude: {offer['date']}")
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']:.2f}, Ukupno: ${item['item_total']:.2f}")
    print(f"Ukupno: ${offer['sub_total']:.2f}, Porez: ${offer['tax']:.2f}, Ukupno za platiti: ${offer['total']:.2f}")


def main():
    # Učitavanje podataka iz JSON datoteka
    offers = load_data(OFFERS_FILE)
    products = load_data(PRODUCTS_FILE)
    customers = load_data(CUSTOMERS_FILE)

    while True:
        print("\nOffers Calculator izbornik:")
        print("1. Kreiraj novu ponudu")
        print("2. Upravljanje proizvodima")
        print("3. Upravljanje korisnicima")
        print("4. Prikaz ponuda")
        print("5. Izlaz")
        choice = input("Odabrana opcija: ")

        if choice == "1":
            create_new_offer(offers, products, customers)
        elif choice == "2":
            manage_products(products)
        elif choice == "3":
            manage_customers(customers)
        elif choice == "4":
            display_offers(offers)
        elif choice == "5":
            # Pohrana podataka prilikom izlaza
            save_data(OFFERS_FILE, offers)
            save_data(PRODUCTS_FILE, products)
            save_data(CUSTOMERS_FILE, customers)
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")


if __name__ == "__main__":
    main()