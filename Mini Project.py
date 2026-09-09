import json
import os
import platform
import subprocess
from datetime import datetime


class Vehicle:
    def __init__(self, model, rent_price):
        self.__model = model
        self.__rent_price = rent_price
        self.__available = True
        self.__renter_name = ""
        self.__rental_cost = 0
        self.__rental_duration = ""

    def get_model(self):
        return self.__model

    def get_rent_price(self):
        return self.__rent_price

    def is_available(self):
        return self.__available

    def get_renter_name(self):
        return self.__renter_name

    def get_rental_cost(self):
        return self.__rental_cost

    def get_rental_duration(self):
        return self.__rental_duration

    def rent(self, renter_name, rental_cost, rental_duration):
        if self.__available:
            self.__available = False
            self.__renter_name = renter_name
            self.__rental_cost = rental_cost
            self.__rental_duration = rental_duration
            return True
        return False

    def return_vehicle(self):
        if not self.__available:
            self.__available = True
            self.__renter_name = ""
            self.__rental_cost = 0
            self.__rental_duration = ""
            return True
        return False

    def calculate_rent(self, duration):
        return self.__rent_price * duration

    def __str__(self):
        status = "Available" if self.__available else "Rented"

        text = (
            f"Model: {self.__model}\n"
            f"Rent Price: Rs. {self.__rent_price}\n"
            f"Status: {status}"
        )

        if not self.__available:
            text += (
                f"\nRented by: {self.__renter_name}"
                f"\nRental Duration: {self.__rental_duration}"
                f"\nRental Cost: Rs. {self.__rental_cost:.2f}"
            )

        return text

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "model": self.__model,
            "rent_price": self.__rent_price,
            "available": self.__available,
            "renter_name": self.__renter_name,
            "rental_cost": self.__rental_cost,
            "rental_duration": self.__rental_duration
        }

    @staticmethod
    def from_dict(data):
        vehicle_type = data.get("type")
        model = data.get("model")
        rent_price = data.get("rent_price")

        if vehicle_type == "Car":
            vehicle = Car(
                model,
                rent_price,
                data.get("seats", 5)
            )
        elif vehicle_type == "Bike":
            vehicle = Bike(
                model,
                rent_price,
                data.get("engine_cc", 100)
            )
        elif vehicle_type == "Truck":
            vehicle = Truck(
                model,
                rent_price,
                data.get("capacity", 1)
            )
        else:
            vehicle = Vehicle(model, rent_price)

        vehicle.__available = data.get("available", True)
        vehicle.__renter_name = data.get("renter_name", "")
        vehicle.__rental_cost = data.get("rental_cost", 0)
        vehicle.__rental_duration = data.get("rental_duration", "")

        if not vehicle.__available and not vehicle.__renter_name:
            vehicle.__renter_name = "Unknown"

        return vehicle


class Car(Vehicle):
    def __init__(self, model, rent_price, seats):
        super().__init__(model, rent_price)
        self.__seats = seats

    def get_seats(self):
        return self.__seats

    def __str__(self):
        status = "Available" if self.is_available() else "Rented"

        text = (
            f"Type: Car\n"
            f"Model: {self.get_model()}\n"
            f"Seats: {self.__seats}\n"
            f"Rent Price: Rs. {self.get_rent_price():.2f}/day\n"
            f"Status: {status}"
        )

        if not self.is_available():
            text += (
                f"\nRented by: {self.get_renter_name()}"
                f"\nRental Duration: {self.get_rental_duration()}"
                f"\nRental Cost: Rs. {self.get_rental_cost():.2f}"
            )

        return text

    def to_dict(self):
        data = super().to_dict()
        data["seats"] = self.__seats
        return data


class Bike(Vehicle):
    def __init__(self, model, rent_price, engine_cc):
        super().__init__(model, rent_price)
        self.__engine_cc = engine_cc

    def get_engine_cc(self):
        return self.__engine_cc

    def __str__(self):
        status = "Available" if self.is_available() else "Rented"

        text = (
            f"Type: Bike\n"
            f"Model: {self.get_model()}\n"
            f"Engine: {self.__engine_cc}cc\n"
            f"Rent Price: Rs. {self.get_rent_price():.2f}/hour\n"
            f"Status: {status}"
        )

        if not self.is_available():
            text += (
                f"\nRented by: {self.get_renter_name()}"
                f"\nRental Duration: {self.get_rental_duration()}"
                f"\nRental Cost: Rs. {self.get_rental_cost():.2f}"
            )

        return text

    def to_dict(self):
        data = super().to_dict()
        data["engine_cc"] = self.__engine_cc
        return data


class Truck(Vehicle):
    def __init__(self, model, rent_price, capacity):
        super().__init__(model, rent_price)
        self.__capacity = capacity

    def get_capacity(self):
        return self.__capacity

    def __str__(self):
        status = "Available" if self.is_available() else "Rented"

        text = (
            f"Type: Truck\n"
            f"Model: {self.get_model()}\n"
            f"Capacity: {self.__capacity} tons\n"
            f"Rent Price: Rs. {self.get_rent_price():.2f}/load\n"
            f"Status: {status}"
        )

        if not self.is_available():
            text += (
                f"\nRented by: {self.get_renter_name()}"
                f"\nRental Duration: {self.get_rental_duration()}"
                f"\nRental Cost: Rs. {self.get_rental_cost():.2f}"
            )

        return text

    def to_dict(self):
        data = super().to_dict()
        data["capacity"] = self.__capacity
        return data


vehicles = []


def save_data():
    data = [vehicle.to_dict() for vehicle in vehicles]

    with open("vehicles.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_data():
    global vehicles

    if not os.path.exists("vehicles.json"):
        preload_vehicles()
        save_data()
        return

    try:
        with open("vehicles.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        vehicles = [Vehicle.from_dict(item) for item in data]

        if not vehicles:
            preload_vehicles()
            save_data()

    except Exception:
        vehicles = []
        preload_vehicles()
        save_data()


def preload_vehicles():
    vehicles.clear()

    vehicles.extend([
        Car("Toyota Innova Crysta", 2500, 7),
        Car("Toyota Fortuner", 3500, 7),
        Car("Hyundai Creta", 2000, 5),
        Car("Hyundai Verna", 1800, 5),
        Car("Kia Seltos", 2000, 5),
        Car("Kia Carens", 2300, 7),
        Car("Mahindra XUV700", 2800, 7),
        Car("Mahindra Scorpio", 2700, 7),
        Car("Tata Nexon", 1700, 5),
        Car("Tata Harrier", 2500, 5),

        Bike("Royal Enfield Classic 350", 800, 349),
        Bike("Royal Enfield Hunter 350", 700, 349),
        Bike("Honda Activa 6G", 400, 109),
        Bike("Honda Shine", 450, 123),
        Bike("Yamaha R15 V4", 900, 155),
        Bike("Yamaha MT-15", 850, 155),
        Bike("TVS Apache RTR 160", 700, 159),
        Bike("Bajaj Pulsar 150", 650, 149),
        Bike("KTM Duke 200", 900, 199),
        Bike("Suzuki Gixxer", 700, 155),

        Truck("Tata 407", 5000, 2.5),
        Truck("Tata 709", 6000, 5),
        Truck("Ashok Leyland Dost", 4500, 1.5),
        Truck("Ashok Leyland 1616", 7000, 16),
        Truck("Mahindra Bolero Pickup", 4500, 1.5),
        Truck("Mahindra Furio", 7500, 10),
        Truck("Eicher Pro 2049", 6500, 5),
        Truck("Eicher Pro 3015", 8000, 10),
        Truck("BharatBenz 2823", 9000, 16),
        Truck("BharatBenz 3523", 10000, 20)
    ])


def display_vehicles():
    if not vehicles:
        print("\nNo vehicles available.")
        return

    print("\n" + "=" * 70)
    print("VEHICLE LIST")
    print("=" * 70)

    for index, vehicle in enumerate(vehicles, start=1):
        print(f"\nVehicle Number: {index}")
        print("-" * 70)
        print(vehicle)

    print("=" * 70)


def create_pdf(vehicle):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    os.makedirs("receipts", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    safe_name = vehicle.get_model()
    safe_name = "".join(
        character if character.isalnum() else "_"
        for character in safe_name
    )

    filename = os.path.abspath(
        f"receipts/rental_receipt_{safe_name}_{timestamp}.pdf"
    )

    pdf = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    pdf.setTitle("Vehicle Rental Receipt")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(
        width / 2,
        height - 70,
        "VEHICLE RENTAL RECEIPT"
    )

    pdf.setFont("Helvetica", 11)

    y = height - 120

    pdf.drawString(70, y, "Receipt Date:")
    pdf.drawString(
        220,
        y,
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

    y -= 35

    pdf.drawString(70, y, "Vehicle Type:")
    pdf.drawString(
        220,
        y,
        vehicle.__class__.__name__
    )

    y -= 35

    pdf.drawString(70, y, "Vehicle Model:")
    pdf.drawString(
        220,
        y,
        vehicle.get_model()
    )

    y -= 35

    pdf.drawString(70, y, "Rented By:")
    pdf.drawString(
        220,
        y,
        vehicle.get_renter_name()
    )

    y -= 35

    pdf.drawString(70, y, "Rental Duration:")
    pdf.drawString(
        220,
        y,
        str(vehicle.get_rental_duration())
    )

    y -= 35

    pdf.drawString(70, y, "Total Amount:")
    pdf.drawString(
        220,
        y,
        f"Rs. {vehicle.get_rental_cost():.2f}"
    )

    y -= 50

    pdf.line(70, y, width - 70, y)

    y -= 40

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        70,
        y,
        "Thank you for using our vehicle rental service."
    )

    y -= 25

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        70,
        y,
        "Please keep this receipt for your records."
    )

    pdf.save()

    return filename


def print_hard_copy(filename):
    filename = os.path.abspath(filename)

    if not os.path.exists(filename):
        print("\nPDF file not found.")
        return False

    system = platform.system()

    if system == "Windows":

        pdf_readers = [
            r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
            r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
            r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
            r"C:\Program Files\SumatraPDF\SumatraPDF.exe",
            r"C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe",
            r"C:\Program Files\Foxit Software\Foxit PDF Reader\FoxitPDFReader.exe",
            r"C:\Program Files (x86)\Foxit Software\Foxit PDF Reader\FoxitPDFReader.exe"
        ]

        for reader in pdf_readers:

            if os.path.exists(reader):

                try:

                    reader_name = os.path.basename(reader).lower()

                    if "sumatra" in reader_name:

                        subprocess.Popen([
                            reader,
                            "-print-to-default",
                            filename
                        ])

                    elif "acrobat" in reader_name or "acrobat" in reader.lower():

                        subprocess.Popen([
                            reader,
                            "/t",
                            filename
                        ])

                    elif "acro" in reader_name:

                        subprocess.Popen([
                            reader,
                            "/t",
                            filename
                        ])

                    else:

                        subprocess.Popen([
                            reader,
                            "/t",
                            filename
                        ])

                    print("\nPrinting started successfully.")
                    return True

                except Exception as error:
                    print("\nPrinting failed:", error)
                    return False

        print("\nNo supported PDF reader was found.")
        print("Please install Adobe Acrobat Reader or SumatraPDF.")
        print("\nPDF saved successfully at:")
        print(filename)

        try:
            os.startfile(filename)
            print("\nPDF opened.")
            print("Press Ctrl + P to print it manually.")
        except Exception as error:
            print("\nUnable to open PDF:", error)

        return False

    elif system == "Darwin":

        try:
            subprocess.run(
                ["lp", filename],
                check=True
            )

            print("\nPrinting started successfully.")
            return True

        except Exception as error:

            print("\nPrinting failed:", error)
            return False

    else:

        try:
            subprocess.run(
                ["lp", filename],
                check=True
            )

            print("\nPrinting started successfully.")
            return True

        except Exception as error:

            print("\nPrinting failed:", error)
            return False


def rental_receipt(vehicle):

    print("\n" + "=" * 60)
    print("RENTAL RECEIPT")
    print("=" * 60)

    print(f"Vehicle Type     : {vehicle.__class__.__name__}")
    print(f"Vehicle Model    : {vehicle.get_model()}")
    print(f"Rented By        : {vehicle.get_renter_name()}")
    print(f"Rental Duration  : {vehicle.get_rental_duration()}")
    print(f"Total Amount     : Rs. {vehicle.get_rental_cost():.2f}")
    print(
        f"Date             : "
        f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )

    print("=" * 60)

    while True:

        print("\n" + "=" * 60)
        print("RECEIPT OPTIONS")
        print("=" * 60)
        print("1. Save as PDF")
        print("2. Print Hard Copy")
        print("3. Save PDF + Print Hard Copy")
        print("4. Cancel")
        print("=" * 60)

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            try:
                filename = create_pdf(vehicle)

                print("\nPDF created successfully.")
                print("Saved at:")
                print(filename)

            except ImportError:

                print("\nReportLab is not installed.")
                print("Run:")
                print("pip install reportlab")

            except Exception as error:

                print("\nPDF creation failed:", error)

        elif choice == "2":

            try:
                filename = create_pdf(vehicle)

                print("\nPDF created successfully.")
                print("Sending to printer...")

                print_hard_copy(filename)

            except ImportError:

                print("\nReportLab is not installed.")
                print("Run:")
                print("pip install reportlab")

            except Exception as error:

                print("\nPrinting failed:", error)

        elif choice == "3":

            try:
                filename = create_pdf(vehicle)

                print("\nPDF created successfully.")
                print("Saved at:")
                print(filename)

                print("\nSending to printer...")

                print_hard_copy(filename)

            except ImportError:

                print("\nReportLab is not installed.")
                print("Run:")
                print("pip install reportlab")

            except Exception as error:

                print("\nPDF creation or printing failed:", error)

        elif choice == "4":

            print("\nReceipt operation cancelled.")
            break

        else:

            print("\nInvalid choice.")

        if choice in ["1", "2", "3"]:
            break


def add_vehicle():

    print("\n" + "=" * 60)
    print("ADD VEHICLE")
    print("=" * 60)

    print("1. Car")
    print("2. Bike")
    print("3. Truck")

    choice = input("Enter vehicle type: ").strip()

    model = input("Enter vehicle model: ").strip()

    if not model:
        print("Vehicle model cannot be empty.")
        return

    try:
        rent_price = float(
            input("Enter rental price: ").strip()
        )
    except ValueError:
        print("Invalid rental price.")
        return

    if choice == "1":

        try:
            seats = int(
                input("Enter number of seats: ").strip()
            )

            vehicles.append(
                Car(model, rent_price, seats)
            )

        except ValueError:
            print("Invalid number of seats.")
            return

    elif choice == "2":

        try:
            engine_cc = int(
                input("Enter engine CC: ").strip()
            )

            vehicles.append(
                Bike(model, rent_price, engine_cc)
            )

        except ValueError:
            print("Invalid engine CC.")
            return

    elif choice == "3":

        try:
            capacity = float(
                input("Enter capacity in tons: ").strip()
            )

            vehicles.append(
                Truck(model, rent_price, capacity)
            )

        except ValueError:
            print("Invalid capacity.")
            return

    else:

        print("Invalid vehicle type.")
        return

    save_data()

    print("\nVehicle added successfully.")


def rent_vehicle():

    if not vehicles:
        print("\nNo vehicles available.")
        return

    print("\n" + "=" * 60)
    print("AVAILABLE VEHICLES")
    print("=" * 60)

    available_vehicles = []

    for index, vehicle in enumerate(vehicles, start=1):

        if vehicle.is_available():

            available_vehicles.append((index, vehicle))

            print(
                f"{index}. "
                f"{vehicle.__class__.__name__} - "
                f"{vehicle.get_model()}"
            )

    if not available_vehicles:

        print("\nNo vehicles are currently available.")
        return

    try:

        vehicle_number = int(
            input("\nEnter vehicle number: ").strip()
        )

    except ValueError:

        print("Invalid vehicle number.")
        return

    if vehicle_number < 1 or vehicle_number > len(vehicles):

        print("Invalid vehicle number.")
        return

    vehicle = vehicles[vehicle_number - 1]

    if not vehicle.is_available():

        print("\nThis vehicle is already rented.")
        return

    renter_name = input(
        "\nEnter name of the person taking the vehicle: "
    ).strip()

    if not renter_name:

        print("Renter name cannot be empty.")
        return

    if isinstance(vehicle, Car):

        try:

            days = int(
                input("Enter number of days: ").strip()
            )

            if days <= 0:
                print("Days must be greater than zero.")
                return

        except ValueError:

            print("Invalid number of days.")
            return

        rental_cost = vehicle.calculate_rent(days)
        rental_duration = f"{days} day(s)"

    elif isinstance(vehicle, Bike):

        try:

            hours = int(
                input("Enter number of hours: ").strip()
            )

            if hours <= 0:
                print("Hours must be greater than zero.")
                return

        except ValueError:

            print("Invalid number of hours.")
            return

        rental_cost = vehicle.calculate_rent(hours)
        rental_duration = f"{hours} hour(s)"

    elif isinstance(vehicle, Truck):

        try:

            loads = int(
                input("Enter number of loads: ").strip()
            )

            if loads <= 0:
                print("Loads must be greater than zero.")
                return

        except ValueError:

            print("Invalid number of loads.")
            return

        rental_cost = vehicle.calculate_rent(loads)
        rental_duration = f"{loads} load(s)"

    else:

        try:

            duration = int(
                input("Enter rental duration: ").strip()
            )

            if duration <= 0:
                print("Duration must be greater than zero.")
                return

        except ValueError:

            print("Invalid duration.")
            return

        rental_cost = vehicle.calculate_rent(duration)
        rental_duration = str(duration)

    vehicle.rent(
        renter_name,
        rental_cost,
        rental_duration
    )

    save_data()

    print("\n" + "=" * 60)
    print("VEHICLE RENTED SUCCESSFULLY")
    print("=" * 60)

    print(f"Vehicle       : {vehicle.get_model()}")
    print(f"Rented By     : {renter_name}")
    print(f"Duration      : {rental_duration}")
    print(f"Total Cost    : Rs. {rental_cost:.2f}")

    print("=" * 60)

    rental_receipt(vehicle)


def return_vehicle():

    rented_vehicles = []

    for index, vehicle in enumerate(vehicles, start=1):

        if not vehicle.is_available():

            rented_vehicles.append((index, vehicle))

    if not rented_vehicles:

        print("\nNo vehicles are currently rented.")
        return

    print("\n" + "=" * 60)
    print("RENTED VEHICLES")
    print("=" * 60)

    for index, vehicle in rented_vehicles:

        print(
            f"{index}. "
            f"{vehicle.__class__.__name__} - "
            f"{vehicle.get_model()}"
        )

        print(
            f"   Rented By: "
            f"{vehicle.get_renter_name()}"
        )

        print(
            f"   Rental Cost: "
            f"Rs. {vehicle.get_rental_cost():.2f}"
        )

    print("=" * 60)

    try:

        vehicle_number = int(
            input("Enter vehicle number to return: ").strip()
        )

    except ValueError:

        print("Invalid vehicle number.")
        return

    if vehicle_number < 1 or vehicle_number > len(vehicles):

        print("Invalid vehicle number.")
        return

    vehicle = vehicles[vehicle_number - 1]

    if vehicle.is_available():

        print("\nThis vehicle is already available.")
        return

    renter_name = vehicle.get_renter_name()

    if vehicle.return_vehicle():

        save_data()

        print("\n" + "=" * 60)
        print("VEHICLE RETURNED SUCCESSFULLY")
        print("=" * 60)
        print(f"Vehicle   : {vehicle.get_model()}")
        print(f"Returned By: {renter_name}")
        print("=" * 60)


def print_existing_receipt():

    rented_vehicles = []

    for index, vehicle in enumerate(vehicles, start=1):

        if not vehicle.is_available():

            rented_vehicles.append((index, vehicle))

    if not rented_vehicles:

        print("\nNo rented vehicles found.")
        return

    print("\n" + "=" * 60)
    print("RENTED VEHICLES")
    print("=" * 60)

    for index, vehicle in rented_vehicles:

        print(
            f"{index}. "
            f"{vehicle.__class__.__name__} - "
            f"{vehicle.get_model()} - "
            f"{vehicle.get_renter_name()}"
        )

    print("=" * 60)

    try:

        vehicle_number = int(
            input("Enter vehicle number: ").strip()
        )

    except ValueError:

        print("Invalid vehicle number.")
        return

    if vehicle_number < 1 or vehicle_number > len(vehicles):

        print("Invalid vehicle number.")
        return

    vehicle = vehicles[vehicle_number - 1]

    if vehicle.is_available():

        print("\nThis vehicle is not currently rented.")
        return

    rental_receipt(vehicle)


def main():

    load_data()

    while True:

        print("\n")
        print("=" * 70)
        print("              VEHICLE RENTAL SYSTEM")
        print("=" * 70)
        print("1. Add Vehicle")
        print("2. View Vehicles")
        print("3. Rent Vehicle")
        print("4. Return Vehicle")
        print("5. Print Rental Receipt")
        print("6. Exit")
        print("=" * 70)

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            add_vehicle()

        elif choice == "2":

            display_vehicles()

        elif choice == "3":

            rent_vehicle()

        elif choice == "4":

            return_vehicle()

        elif choice == "5":

            print_existing_receipt()

        elif choice == "6":

            save_data()

            print("\nThank you for using Vehicle Rental System.")
            print("Program closed.")

            break

        else:

            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()