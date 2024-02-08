import { createClient, print } from 'redis';

const client = createClient();

client.on('error', (error) => {
  console.log('Redis client not connected to the server:', error.toString());
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const setNewSchool = (schoolName, value) => {
  client.SET(schoolName, value, print);
};

const displaySchoolValue = (schoolName) => {
  client.GET(schoolName, (_error, response) => {
    console.log(response);
  });
};

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
