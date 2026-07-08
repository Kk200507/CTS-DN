"""Week-1 structural pattern examples for beginner-friendly Python training."""

# =====================================================================
# Adapter Pattern
# =====================================================================
# Convert one interface into another interface the client expects.


class EuropeanPlug:
    def connect_european_socket(self) -> str:
        return "Connected to European socket"


class USSocket:
    def plug_in(self) -> str:
        return "Connected to US socket"


class PlugAdapter:
    def __init__(self, european_plug: EuropeanPlug) -> None:
        self.european_plug = european_plug

    def plug_in(self) -> str:
        return self.european_plug.connect_european_socket()


# =====================================================================
# Decorator Pattern
# =====================================================================
# Add new behavior without changing the original object.


class Coffee:
    def cost(self) -> float:
        return 50

    def description(self) -> str:
        return "Plain coffee"


class CoffeeDecorator:
    def __init__(self, coffee: Coffee) -> None:
        self.coffee = coffee


class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self.coffee.cost() + 10

    def description(self) -> str:
        return self.coffee.description() + ", milk"


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self.coffee.cost() + 5

    def description(self) -> str:
        return self.coffee.description() + ", sugar"


# =====================================================================
# Proxy Pattern
# =====================================================================
# Control access to another object.


class RealImage:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        print(f"Loading {filename} from disk")

    def display(self) -> None:
        print(f"Displaying {self.filename}")


class ImageProxy:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._real_image = None

    def display(self) -> None:
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()


def demo_adapter() -> None:
    print("\nAdapter demo")
    adapter = PlugAdapter(EuropeanPlug())
    print(adapter.plug_in())


def demo_decorator() -> None:
    print("\nDecorator demo")
    coffee = Coffee()
    coffee = MilkDecorator(coffee)
    coffee = SugarDecorator(coffee)
    print(coffee.description())
    print(f"Cost: {coffee.cost()}")


def demo_proxy() -> None:
    print("\nProxy demo")
    image = ImageProxy("profile.png")
    image.display()
    image.display()


if __name__ == "__main__":
    demo_adapter()
    demo_decorator()
    demo_proxy()
