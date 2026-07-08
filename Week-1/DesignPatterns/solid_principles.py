"""Week-1 SOLID principles examples for beginner-friendly Python training."""

from abc import ABC, abstractmethod


# =====================================================================
# Single Responsibility Principle
# =====================================================================
# Each class should have one reason to change.


class Invoice:
    def __init__(self, customer: str, amount: float) -> None:
        self.customer = customer
        self.amount = amount


class InvoiceCalculator:
    def total_with_tax(self, invoice: Invoice, tax_rate: float) -> float:
        return invoice.amount + (invoice.amount * tax_rate)


class InvoicePrinter:
    def print_invoice(self, invoice: Invoice) -> None:
        print(f"Invoice for {invoice.customer}: ${invoice.amount:.2f}")


# =====================================================================
# Open/Closed Principle
# =====================================================================
# Code should be open for extension, but closed for modification.


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


def total_area(shapes: list[Shape]) -> float:
    return sum(shape.area() for shape in shapes)


# =====================================================================
# Liskov Substitution Principle
# =====================================================================
# Any subclass should work anywhere its base class is expected.


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


class CardPayment(PaymentProcessor):
    def pay(self, amount: float) -> None:
        print(f"Paid ${amount:.2f} by card")


class CashPayment(PaymentProcessor):
    def pay(self, amount: float) -> None:
        print(f"Paid ${amount:.2f} in cash")


def checkout(processor: PaymentProcessor, amount: float) -> None:
    processor.pay(amount)


# =====================================================================
# Interface Segregation Principle
# =====================================================================
# Prefer small, focused interfaces over large, forced ones.


class Printer(ABC):
    @abstractmethod
    def print_document(self, document: str) -> None:
        pass


class Scanner(ABC):
    @abstractmethod
    def scan_document(self) -> str:
        pass


class SimplePrinter(Printer):
    def print_document(self, document: str) -> None:
        print(f"Printing: {document}")


class AllInOneMachine(Printer, Scanner):
    def print_document(self, document: str) -> None:
        print(f"Printing: {document}")

    def scan_document(self) -> str:
        return "Scanned document"


# =====================================================================
# Dependency Inversion Principle
# =====================================================================
# High-level modules should depend on abstractions, not concrete classes.


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> None:
        pass


class StripeGateway(PaymentGateway):
    def charge(self, amount: float) -> None:
        print(f"Charging ${amount:.2f} through Stripe")


class OrderService:
    def __init__(self, gateway: PaymentGateway) -> None:
        self.gateway = gateway

    def place_order(self, amount: float) -> None:
        self.gateway.charge(amount)
        print("Order placed successfully")


def demo_srp() -> None:
    print("\nSRP demo")
    invoice = Invoice("Asha", 1000)
    printer = InvoicePrinter()
    calculator = InvoiceCalculator()
    printer.print_invoice(invoice)
    print(f"Total with tax: ${calculator.total_with_tax(invoice, 0.18):.2f}")


def demo_ocp() -> None:
    print("\nOCP demo")
    shapes = [Circle(2), Rectangle(3, 4)]
    print(f"Total area: {total_area(shapes):.2f}")


def demo_lsp() -> None:
    print("\nLSP demo")
    for processor in [CardPayment(), CashPayment()]:
        checkout(processor, 250)


def demo_isp() -> None:
    print("\nISP demo")
    printer = SimplePrinter()
    printer.print_document("Week 1 notes")
    machine = AllInOneMachine()
    machine.print_document("Report")
    print(machine.scan_document())


def demo_dip() -> None:
    print("\nDIP demo")
    service = OrderService(StripeGateway())
    service.place_order(499.99)


if __name__ == "__main__":
    demo_srp()
    demo_ocp()
    demo_lsp()
    demo_isp()
    demo_dip()
