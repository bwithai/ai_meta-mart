BACKEND_REQ_TEMPLATE = """
To request information about a product and its quantity, please follow these guidelines:

1. Product: Please extract the name of the product, such as "cheese," "burger," "meat," or another edible item.
2. Quantity: also extract the quantity of the product. that would be ask units like "1kg," "2 items," or simply provide the number.

From the question: {question}

For example:
- Product: "cheese"
- Quantity: "2 items"

If the product is not found, just respond with "Negative."
"""
