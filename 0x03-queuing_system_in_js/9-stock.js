import express from 'express';
import { promisify } from 'util';
import { createClient } from 'redis';

const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5
  },
];

const getItemById = (id) => {
  const item = listProducts.find(obj => obj.itemId === id);

  if (item) {
    return Object.fromEntries(Object.entries(item));
  }
};

const app = express();
const client = createClient();
const PORT = 1245;

/**
 * Modifies the reserved stock for a given item.
 * @param {number} itemId - The id of the item.
 * @param {number} stock - The stock of the item.
 */
const reserveStockById = async (itemId, stock) => {
  return promisify(client.SET).bind(client)(`item.${itemId}`, stock);
};

/**
 * Retrieves the reserved stock for a given item.
 * @param {number} itemId - The id of the item.
 * @returns {Promise<String>}
 */
const getCurrentReservedStockById = async (itemId) => {
  return promisify(client.GET).bind(client)(`item.${itemId}`);
};

app.get('/list_products', (_request, response) => {
  response.json(listProducts);
});

app.get('/list_products/:itemId(\\d+)', (request, response) => {
  const itemId = Number.parseInt(request.params.itemId);
  const productItem = getItemById(Number.parseInt(itemId));

  if (!productItem) {
    response.json({ status: 'Product not found' });
    return;
  }
  getCurrentReservedStockById(itemId)
    .then((result) => Number.parseInt(result || 0))
    .then((reservedStock) => {
      productItem.currentQuantity = productItem.initialAvailableQuantity - reservedStock;
      response.json(productItem);
    });
});

app.get('/reserve_product/:itemId', (request, response) => {
  const itemId = Number.parseInt(request.params.itemId);
  const productItem = getItemById(Number.parseInt(itemId));

  if (!productItem) {
    response.json({ status: 'Product not found' });
    return;
  }
  getCurrentReservedStockById(itemId)
    .then((result) => Number.parseInt(result || 0))
    .then((reservedStock) => {
      if (reservedStock >= productItem.initialAvailableQuantity) {
        response.json({ status: 'Not enough stock available', itemId });
        return;
      }
      reserveStockById(itemId, reservedStock + 1)
        .then(() => {
          response.json({ status: 'Reservation confirmed', itemId });
        });
    });
});

const resetProductsStock = () => {
  return Promise.all(
    listProducts.map(
      item => promisify(client.SET).bind(client)(`item.${item.itemId}`, 0),
    )
  );
};

app.listen(PORT, () => {
  resetProductsStock()
    .then(() => {
      console.log(`API available on localhost port ${PORT}`);
    });
});

export default app;
