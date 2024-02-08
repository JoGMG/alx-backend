import { createClient } from 'redis';

const client = createClient();
const EXIT_MESSAGE = 'KILL_SERVER';

client.on('error', (error) => {
  console.log('Redis client not connected to the server:', error.toString());
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.subscribe('holberton school channel');

client.on('message', (_error, message) => {
  console.log(message);
  if (message === EXIT_MESSAGE) {
    client.unsubscribe();
    client.quit();
  }
});
