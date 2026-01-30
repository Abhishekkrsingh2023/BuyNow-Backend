from pydantic import BaseModel


class AddressSchema(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

class OrderSchema(BaseModel):
    product_id: str
    quantity: int
    address: AddressSchema



order = OrderSchema(
    product_id="64b8f0f2e1b1c8a12345678",
    quantity=2,
    address=AddressSchema(
        street="123 Main St",
        city="Metropolis",
        state="NY",
        zip_code="12345",
        country="USA"
    )
)

print(order.model_dump())
print(order.address.model_dump())
