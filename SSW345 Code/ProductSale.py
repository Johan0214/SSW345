# needed for forward reference of Sale in Product,
# since Sale is not yet defined.
from __future__ import annotations
from typing import List

# forward reference used for class Sale
class Product:
    __lastSale: Sale = None
    __productInventory: int = 0

    def __init__(self, sale: Sale = None, inventory: int = 0):  
        self.__lastSale = sale
        self.__productInventory = inventory

    def setLastSale(self, lastSale: Sale):
        self.__lastSale = lastSale

    @property
    def getLastSale(self) -> Sale:
        return self.__lastSale

    def __getitem__(self, item):
        return self

    @property
    def getInventory(self) -> int:
        return self.__productInventory

    def removeInventory(self, quantity: int):
        if self.__productInventory >= quantity:
            self.__productInventory -= quantity
        else:
            print("Not enough inventory for this sale")


# no forward reference needed since Product is defined
class Sale:
    __saleTimes = 0
    __productSold: List[Product] = None
    __saleNumber: int = 0

    def __init__(self, products: List[Product], amounts: List[int]): 
        Sale.__saleTimes += 1
        self.__product = products
        self.__saleNumber = Sale.__saleTimes
        for prod, amount in zip(products, amounts):  
            prod.setLastSale(self)
            prod.removeInventory(amount)

    def setProductsSold(self, productSold: List[Product]):
        self.__productSold = productSold

    @property
    def getSaleNumber(self) -> int:
        return self.__saleNumber


productOne = Product(sale=None, inventory=10)
productTwo = Product(sale=None, inventory=15)

saleOne = Sale([productOne, productTwo], [2, 1])
saleTwo = Sale([productOne], [2])
saleThree = Sale([productTwo], [3])


print(f"{productOne.getLastSale.getSaleNumber}, {productTwo.getLastSale.getSaleNumber}, Inventory of Product 1: {productOne.getInventory}, Inventory of Product 2: {productTwo.getInventory}")
