import json
from datetime import datetime


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
def create_new_offer(offers: list, products: list, customers: list) -> None:
    """
    Prompt user to create a new offer by selecting a customer, entering date,
    choosing products, and calculating totals.
    """
    while True:
        print("\nOdabir kupca:")
        print("--------------\n")
        
        for index in range(len(customers)):
            print(f"{index + 1}. {customers[index]['name']} | Email: {customers[index]['email']} | Vat broj: {customers[index]['vat_id']}")
            # python index počinje sa 0, pa podižemo index u console ispisu za 1
        
        try:
            kupac_index = int(input("\nOdaberite kupca po broju: ")) - 1
            # korisnikov index spustamo za -1 da budemo u python indexu
        
            if 0 <= kupac_index < len(customers): # # provjera da li je rasponu
                odabrani_kupac = customers[kupac_index]
                print(f"\nOdabrani kupac: [{odabrani_kupac["name"]} | Email : {odabrani_kupac["email"]} | Vat broj: {odabrani_kupac["vat_id"]})]")
                break
            else:
                print("\nKrivi izbor. Kupac ne postoji.")
        except ValueError:
            print("\nPogrešan unos. Molimo unesite broj.")
    
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
            # python index počinje sa 0, pa podižemo index u console ispisu za 1

        proizvod_index = int(input("\nOdabirite proizvod po broju ('0' za kraj): ")) -1
        # korisnikov index spustamo za -1 da budemo u python indexu

        if proizvod_index == -1: # ako je 0, izlazimo iz petlje
            break
        
        if 0 <= proizvod_index < len(products): # provjera da li je rasponu
            odabrani_proizvod = products[proizvod_index]
            print(f"\nOdabrani proizvod: [{odabrani_proizvod["name"]} | {odabrani_proizvod["description"]} | Cijena : ${odabrani_proizvod["price"]:.2f}]")

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
def manage_products(products: list) -> None:
    """
    Allows the user to add a new product or modify an existing product.
    """
    while True:
        print("\nUpravljanje proizvodima izbornik:")
        print("1. Dodaj novi proizvod")
        print("2. Izmjeni postojeći proizvod")
        print("0. Izlaz")

        choice = input("Odabrana opcija: ")
        
        if choice == "0": # 0 izlazimo iz petlje
            break
        elif choice == "1":
            zadnji_id = 0
            for product in products:
                if product["id"] > zadnji_id:
                    zadnji_id = product["id"]
            novi_id = zadnji_id + 1
            #{'id': 1, 'name': 'Asus', 'description': 'Laptop', 'price': 2.0}
            name = input("Unesite ime proizvoda: ")
            description = input("Unesite opis proizvoda: ")
            
            while True:
                try:
                    price = float(input("Unesite cijenu proizvoda: "))
                    break
                except ValueError:
                    print("Neispravan unos cijene, pokušajte ponovno!")

            novi_proizvod = {
            "id" : novi_id,
            "name": name,
            "description" : description,
            "price" : price
            }

            products.append(novi_proizvod)

            try:
                # Pokušajmo spremiti promjene u products.json
                save_data(PRODUCTS_FILE, products)
                print(f"\nNovi proizvod {name} je uspješno dodan. ID: {novi_id}")
            except Exception as e:
                print(f"Dogodila se greška tijekom spremanja podataka - {e}")
                # Rollback promjena u memoriji
                products.remove(novi_proizvod)
                print("Promjena nije spremljena. Pokušajte ponovno.")
        elif choice == "2":
            while True:
                print("\nDostupni proizvodi:")
                for product in products:
                    print(f"{product['id']}. {product['name']} | {product['description']} | ${product['price']:.2f}")
                    #{'id': 1, 'name': 'Asus', 'description': 'Laptop', 'price': 2.0}
                try:
                    izbor = int(input("\nUnesite ID proizvoda koji želite izmijeniti ('0' za izlaz): "))
                    
                    if izbor == 0:
                        break
                    
                    proizvod_pronadjen = False 

                    for product in products:
                        if product["id"] == izbor:
                            proizvod_pronadjen = True
                            print(f"\nIzabrali ste proizvod:\n[{product['id']}. {product['name']} | {product['description']} | ${product['price']:.2f}]")

                            # Spremljena originalna vrijednost za rollback
                            original_product = product.copy()
                            
                            product['name'] = input("Unesite novo ime proizvoda: ")
                            product['description'] = input("Unesite novi opis proizvoda: ")
                            
                            while True:
                                try:
                                    product['price'] = float(input("Unesite novu cijenu proizvoda: "))
                                    break
                                except ValueError:
                                    print("Neispravan unos cijene, pokušajte ponovno!")
                            try:
                                save_data(PRODUCTS_FILE, products)
                                print(f"\nProizvod je uspješno izmjenjen!\n[{product['id']}. {product['name']} | {product['description']} | ${product['price']:.2f}]")
                            except Exception as e:
                                print(f"Dogodila se greška tijekom spremanja izmjena - {e}")
                                # Vraćanje originalnih vrijednosti u slučaju greške
                                product.update(original_product)
                                print("Izmjene nisu spremljene i proizvod je vraćen na originalne vrijednosti.")
                                break                    
                    if not proizvod_pronadjen:
                        print("Proizvod sa izabranim ID-om ne postoji, pokušajte ponovo!")
                
                except ValueError:
                    print("Neispravan unos. Unesite broj za ID ili '0' za izlaz.")
        elif choice == "0":
            break

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
        print("\nUpravljanje korisnicima izbornik:")
        print("1. Unesi novog kupca")
        print("2. Prikaži list svih kupaca")
        print("0. Izlaz")

        choice = input("Odabrana opcija: ")

        if choice == "0": # 0 izlazimo iz petlje
            break
        if choice == "1":
            print("\nUnos novog kupca")
            print("-----------------\n")
            try:
                name = input("Unesi ime novog kupca: ")
                email = input("Unesi Email novog kupca: ")
                vat_id = input("Unesi Vat_ID novog kupca: ")
                new_customer = {'name': name, 'email': email, 'vat_id': vat_id}
                customers.append(new_customer)
            # Pokušajmo spremiti promjene u customers.json
                save_data(CUSTOMERS_FILE, customers)
                print("Kupac uspješno dodan!")
            except Exception as e:
                print(f"Dogodila se greška tijekom spremanja podataka - {e}")
            # Rollback promjena u memoriji
                customers.remove(new_customer)
                print("Molim pokušajte ponovno.")

        if choice == "2":
            for customer in customers:
                print(f"Kupac: {customer['name']} | Email: {customer['email']} | Vat_ID: {customer['vat_id']}")
                #{'name': 'Tech Solutions', 'email': 'info@techsolutions.com', 'vat_id': '01234567890'}

    # Za dodavanje: omogući unos imena kupca, emaila i unos VAT ID-a
    # Za pregled: prikaži listu svih kupaca
    pass


# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers(offers: list) -> None:
    """
    Display all offers, offers for a selected month, or a single offer by ID.
    """
    while True:
        print("Prikaz ponuda izbornik:")
        print("1. Prikaz svih ponuda")
        print("2. Prikaz ponuda za određeni mjesec")
        print("3. Prikaz pojedinačne ponude po ID-u")
        print("0. Izlaz")

        choice = input("Odabrana opcija: ")

        if choice == "0":
            break

        elif choice == '1':
            # Prikaz svih ponuda
            for offer in offers:
                print_offer(offer)

        elif choice == '2':
            while True:
                # Prikaz ponuda za određeni mjesec
                month = input("Unesite mjesec ('0' za kraj): ")
                if month == "0":
                    break
                else:
                    for offer in offers:
                        if offer['date'].startswith(f"2024-{month}"):
                            print_offer(offer)
                            break

        elif choice == '3':
            # Prikaz pojedinačne ponude po ID-u
            while True:
                dostupne_ponude = []
                for offer in offers:
                    dostupne_ponude.append(offer['offer_number'])

                print(f"Dostupne ponude: {dostupne_ponude}")

                try:
                    offer_id = int(input("Unesite ID ponude ('0' za kraj): "))
                    if offer_id == 0:
                        break
                    elif offer_id not in dostupne_ponude:
                        print("Ponuda s tim ID-om nije pronađena.")
                    else:
                        # Tražena ponuda je pronađena
                        for offer in offers:
                            if offer['offer_number'] == offer_id:
                                print_offer(offer)
                                break  # Prekidamo petlju jer smo već našli traženu ponudu
                            
                except ValueError:
                    print("Krivi izbor, unesite broj.")

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